"""
Authentication module for Stride.
Handles GitHub OAuth via Supabase for user tracking and identification.
Credentials are stored globally using keyring for all Stride projects.
"""

import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from typing import Optional, Dict
from supabase import create_client, Client
import keyring
import questionary
from rich.console import Console

from stride.config import SUPABASE_URL, SUPABASE_PUBLISHABLE_KEY, REDIRECT_URI

console = Console()

# Global keyring service name
KEYRING_SERVICE = "stride_global"


class OAuthCallbackHandler(BaseHTTPRequestHandler):
    """HTTP handler for capturing OAuth callback with authorization code."""
    
    def do_GET(self):
        """Handle GET request from OAuth redirect."""
        query = urlparse(self.path).query
        params = parse_qs(query)
        
        # Store authorization code in server instance
        self.server.auth_code = params.get("code", [None])[0]
        self.server.error = params.get("error", [None])[0]
        
        # Send response to browser
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        
        if self.server.auth_code:
            html = """
            <html>
                <body style="font-family: Arial; text-align: center; padding: 50px;">
                    <h1 style="color: #22c55e;">✓ Authentication Successful!</h1>
                    <p>You can close this tab and return to your terminal.</p>
                </body>
            </html>
            """
        else:
            html = """
            <html>
                <body style="font-family: Arial; text-align: center; padding: 50px;">
                    <h1 style="color: #ef4444;">✗ Authentication Failed</h1>
                    <p>Please try again in your terminal.</p>
                </body>
            </html>
            """
        
        self.wfile.write(html.encode())
    
    def log_message(self, format, *args):
        """Suppress server logs."""
        pass


class SupabaseAuth:
    """
    Manages authentication with Supabase using GitHub OAuth.
    Provides methods for login, logout, and credential management.
    """
    
    def __init__(self):
        """Initialize Supabase authentication manager."""
        self.supabase_url = SUPABASE_URL
        self.api_key = SUPABASE_PUBLISHABLE_KEY
        self.redirect_uri = REDIRECT_URI
        
        # Validate configuration
        if not self.supabase_url or not self.api_key:
            console.print("[red]✗ Missing Supabase configuration[/red]")
            raise ValueError("Missing Supabase credentials")
        
        # Initialize Supabase client
        try:
            self.supabase: Client = create_client(
                self.supabase_url,
                self.api_key
            )
            console.print("[dim]✓ Supabase client initialized[/dim]")
        except Exception as e:
            console.print(f"[red]✗ Failed to initialize Supabase client: {str(e)}[/red]")
            raise
    
    def start_oauth_flow(self) -> Optional[str]:
        """
        Start OAuth flow by opening browser and capturing authorization code.
        
        Returns:
            Authorization code if successful, None otherwise
        """
        # Get OAuth URL from Supabase client
        try:
            response = self.supabase.auth.sign_in_with_oauth({
                "provider": "github",
                "options": {
                    "redirect_to": self.redirect_uri
                }
            })
            
            auth_url = response.url
            
        except Exception as e:
            console.print(f"[red]✗ Failed to get OAuth URL: {str(e)}[/red]")
            return None
        
        # Try to start local server on multiple ports
        ports = [37777, 37778, 37779, 37780]
        server = None
        actual_port = None
        
        for port in ports:
            try:
                server = HTTPServer(("localhost", port), OAuthCallbackHandler)
                actual_port = port
                console.print(f"[dim]Starting server on port {port}...[/dim]")
                break
            except OSError:
                continue
        
        if not server:
            console.print("[red]✗ Could not start local server. Ports 37777-37780 are in use.[/red]")
            console.print(f"[yellow]Please open this URL manually:[/yellow]\n{auth_url}")
            return None
        
        # Open browser
        console.print("🔐 [cyan]Opening browser for GitHub authentication...[/cyan]")
        webbrowser.open(auth_url)
        
        # Wait for callback
        console.print("⏳ [yellow]Waiting for login...[/yellow]")
        server.handle_request()
        
        # Get authorization code
        code = getattr(server, "auth_code", None)
        error = getattr(server, "error", None)
        
        if error:
            console.print(f"[red]✗ OAuth error: {error}[/red]")
            return None
        
        if not code:
            console.print("[red]✗ No authorization code received[/red]")
            return None
        
        return code
    
    def exchange_code_for_token(self, code: str) -> Optional[Dict]:
        """
        Exchange authorization code for access and refresh tokens.
        
        Args:
            code: Authorization code from OAuth callback
            
        Returns:
            Dict with access_token, refresh_token, and user info if successful
        """
        try:
            # Use Supabase's built-in method to exchange code for session
            # Pass as dict with 'auth_code' key
            response = self.supabase.auth.exchange_code_for_session({"auth_code": code})
            
            # Handle different response types (dict vs object)
            if isinstance(response, dict):
                session = response.get("session")
                user = response.get("user")
                
                if not session:
                    console.print("[red]✗ No session received from Supabase[/red]")
                    return None
                
                return {
                    "access_token": session.get("access_token"),
                    "refresh_token": session.get("refresh_token"),
                    "user": {
                        "id": user.get("id"),
                        "email": user.get("email"),
                        "user_metadata": user.get("user_metadata", {})
                    }
                }
            else:
                # Response is an object with attributes
                if not response or not hasattr(response, "session"):
                    console.print("[red]✗ No session received from Supabase[/red]")
                    return None
                
                session = response.session
                user = response.user
                
                return {
                    "access_token": session.access_token,
                    "refresh_token": session.refresh_token,
                    "user": {
                        "id": user.id,
                        "email": user.email,
                        "user_metadata": user.user_metadata
                    }
                }
            
        except Exception as e:
            console.print(f"[red]✗ Token exchange failed: {str(e)}[/red]")
            import traceback
            console.print(f"[dim]{traceback.format_exc()}[/dim]")
            return None
    
    def prompt_for_username(self) -> str:
        """
        Prompt user for their preferred username.
        
        Returns:
            Username string
        """
        console.print("\n👤 [cyan]What should we call you?[/cyan] [dim](This will be used throughout Stride)[/dim]")
        
        username = questionary.text(
            "",
            validate=lambda text: len(text) > 0 or "Username cannot be empty"
        ).ask()
        
        return username or "User"
    
    def store_credentials(self, access_token: str, refresh_token: str, 
                         github_email: str, username: str) -> None:
        """
        Store credentials globally using keyring.
        
        Args:
            access_token: Supabase access token
            refresh_token: Supabase refresh token
            github_email: User's GitHub email
            username: User's chosen display name
        """
        try:
            keyring.set_password(KEYRING_SERVICE, "access_token", access_token)
            keyring.set_password(KEYRING_SERVICE, "refresh_token", refresh_token)
            keyring.set_password(KEYRING_SERVICE, "github_email", github_email)
            keyring.set_password(KEYRING_SERVICE, "username", username)
        except Exception as e:
            console.print(f"[red]✗ Failed to store credentials: {str(e)}[/red]")
            console.print("[yellow]⚠ Credentials may not persist across sessions[/yellow]")
    
    def get_current_user(self) -> Optional[Dict[str, str]]:
        """
        Get currently authenticated user information.
        
        Returns:
            Dict with 'email', 'username', 'token' if authenticated, None otherwise
        """
        try:
            access_token = keyring.get_password(KEYRING_SERVICE, "access_token")
            github_email = keyring.get_password(KEYRING_SERVICE, "github_email")
            username = keyring.get_password(KEYRING_SERVICE, "username")
            
            if not access_token or not github_email:
                return None
            
            return {
                "email": github_email,
                "username": username or "User",
                "token": access_token,
            }
        except Exception:
            return None
    
    def clear_credentials(self) -> None:
        """Clear all stored credentials from keyring."""
        keys = ["access_token", "refresh_token", "github_email", "username"]
        
        for key in keys:
            try:
                keyring.delete_password(KEYRING_SERVICE, key)
            except keyring.errors.PasswordDeleteError:
                pass  # Password doesn't exist, that's fine
            except Exception as e:
                console.print(f"[yellow]⚠ Warning: Could not clear {key}: {str(e)}[/yellow]")
    
    def is_authenticated(self) -> bool:
        """
        Check if user is currently authenticated.
        
        Returns:
            True if authenticated, False otherwise
        """
        return self.get_current_user() is not None
    
    def refresh_access_token(self) -> Optional[str]:
        """
        Refresh expired access token using refresh token.
        
        Returns:
            New access token if successful, None otherwise
        """
        try:
            refresh_token = keyring.get_password(KEYRING_SERVICE, "refresh_token")
            if not refresh_token:
                return None
            
            # Use Supabase client to refresh session
            response = self.supabase.auth.refresh_session(refresh_token)
            
            if not response or not response.session:
                return None
            
            session = response.session
            new_access_token = session.access_token
            new_refresh_token = session.refresh_token
            
            if new_access_token:
                keyring.set_password(KEYRING_SERVICE, "access_token", new_access_token)
                if new_refresh_token:
                    keyring.set_password(KEYRING_SERVICE, "refresh_token", new_refresh_token)
            
            return new_access_token
            
        except Exception:
            return None
