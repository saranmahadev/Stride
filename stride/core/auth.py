"""
Authentication module for Stride.
Handles Magic Link (email) and GitHub OAuth authentication via Supabase.
Credentials are stored globally using keyring for all Stride projects.
"""

import time
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from typing import Optional, Dict
from supabase import create_client, Client
import keyring
from rich.console import Console
from rich.prompt import Prompt
from rich.progress import Progress, SpinnerColumn, TextColumn

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
            html = self._get_success_page()
        else:
            html = self._get_error_page()
        
        self.wfile.write(html.encode())
    
    def _get_success_page(self):
        """Return unified success page HTML."""
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Stride Authentication - Success</title>
            <style>
                * {
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }
                body {
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    min-height: 100vh;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                }
                .container {
                    background: rgba(255, 255, 255, 0.1);
                    border-radius: 24px;
                    padding: 60px 40px;
                    backdrop-filter: blur(10px);
                    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
                    border: 1px solid rgba(255, 255, 255, 0.18);
                    max-width: 500px;
                    text-align: center;
                    animation: slideIn 0.5s ease-out;
                }
                @keyframes slideIn {
                    from {
                        opacity: 0;
                        transform: translateY(-20px);
                    }
                    to {
                        opacity: 1;
                        transform: translateY(0);
                    }
                }
                .icon {
                    font-size: 80px;
                    margin-bottom: 20px;
                    animation: checkmark 0.6s ease-in-out;
                }
                @keyframes checkmark {
                    0% { transform: scale(0); }
                    50% { transform: scale(1.2); }
                    100% { transform: scale(1); }
                }
                h1 {
                    font-size: 32px;
                    font-weight: 600;
                    margin-bottom: 16px;
                    color: #4ade80;
                }
                p {
                    font-size: 18px;
                    line-height: 1.6;
                    opacity: 0.9;
                }
                .brand {
                    margin-top: 30px;
                    padding-top: 20px;
                    border-top: 1px solid rgba(255, 255, 255, 0.2);
                    font-size: 14px;
                    opacity: 0.7;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="icon">✓</div>
                <h1>Authentication Successful!</h1>
                <p>You can close this window and return to your terminal.</p>
                <div class="brand">Stride CLI</div>
            </div>
        </body>
        </html>
        """
    
    def _get_error_page(self):
        """Return unified error page HTML."""
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Stride Authentication - Error</title>
            <style>
                * {
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }
                body {
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    min-height: 100vh;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                }
                .container {
                    background: rgba(255, 255, 255, 0.1);
                    border-radius: 24px;
                    padding: 60px 40px;
                    backdrop-filter: blur(10px);
                    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
                    border: 1px solid rgba(255, 255, 255, 0.18);
                    max-width: 500px;
                    text-align: center;
                    animation: slideIn 0.5s ease-out;
                }
                @keyframes slideIn {
                    from {
                        opacity: 0;
                        transform: translateY(-20px);
                    }
                    to {
                        opacity: 1;
                        transform: translateY(0);
                    }
                }
                .icon {
                    font-size: 80px;
                    margin-bottom: 20px;
                    animation: shake 0.5s ease-in-out;
                }
                @keyframes shake {
                    0%, 100% { transform: translateX(0); }
                    25% { transform: translateX(-10px); }
                    75% { transform: translateX(10px); }
                }
                h1 {
                    font-size: 32px;
                    font-weight: 600;
                    margin-bottom: 16px;
                    color: #f87171;
                }
                p {
                    font-size: 18px;
                    line-height: 1.6;
                    opacity: 0.9;
                }
                .brand {
                    margin-top: 30px;
                    padding-top: 20px;
                    border-top: 1px solid rgba(255, 255, 255, 0.2);
                    font-size: 14px;
                    opacity: 0.7;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="icon">✗</div>
                <h1>Authentication Failed</h1>
                <p>Please try again in your terminal.</p>
                <div class="brand">Stride CLI</div>
            </div>
        </body>
        </html>
        """
    
    def log_message(self, format, *args):
        """Suppress server logs."""
        pass


class MagicLinkHandler(BaseHTTPRequestHandler):
    """HTTP handler for magic link callback."""
    
    auth_data = None
    auth_complete = False
    
    def do_GET(self):
        """Handle GET request from magic link redirect."""
        parsed_url = urlparse(self.path)
        
        # Magic link callback page
        if parsed_url.path == "/auth/callback":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            # HTML that extracts tokens from hash and sends to server
            html = """
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Stride Authentication</title>
                <style>
                    * {
                        margin: 0;
                        padding: 0;
                        box-sizing: border-box;
                    }
                    body {
                        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        min-height: 100vh;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: white;
                    }
                    .container {
                        background: rgba(255, 255, 255, 0.1);
                        border-radius: 24px;
                        padding: 60px 40px;
                        backdrop-filter: blur(10px);
                        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
                        border: 1px solid rgba(255, 255, 255, 0.18);
                        max-width: 500px;
                        text-align: center;
                    }
                    .spinner {
                        border: 4px solid rgba(255, 255, 255, 0.3);
                        border-radius: 50%;
                        border-top: 4px solid white;
                        width: 50px;
                        height: 50px;
                        animation: spin 1s linear infinite;
                        margin: 0 auto 30px;
                    }
                    @keyframes spin {
                        0% { transform: rotate(0deg); }
                        100% { transform: rotate(360deg); }
                    }
                    .icon {
                        font-size: 80px;
                        margin-bottom: 20px;
                    }
                    .success-icon {
                        animation: checkmark 0.6s ease-in-out;
                    }
                    @keyframes checkmark {
                        0% { transform: scale(0); }
                        50% { transform: scale(1.2); }
                        100% { transform: scale(1); }
                    }
                    .error-icon {
                        animation: shake 0.5s ease-in-out;
                    }
                    @keyframes shake {
                        0%, 100% { transform: translateX(0); }
                        25% { transform: translateX(-10px); }
                        75% { transform: translateX(10px); }
                    }
                    h1 {
                        font-size: 32px;
                        font-weight: 600;
                        margin-bottom: 16px;
                    }
                    p {
                        font-size: 18px;
                        line-height: 1.6;
                        opacity: 0.9;
                    }
                    .brand {
                        margin-top: 30px;
                        padding-top: 20px;
                        border-top: 1px solid rgba(255, 255, 255, 0.2);
                        font-size: 14px;
                        opacity: 0.7;
                    }
                    .success-color { color: #4ade80; }
                    .error-color { color: #f87171; }
                </style>
            </head>
            <body>
                <div class="container">
                    <div id="loading">
                        <div class="spinner"></div>
                        <h1>Authenticating...</h1>
                        <p>Please wait while we complete your login.</p>
                        <div class="brand">Stride CLI</div>
                    </div>
                    <div id="success" style="display:none;">
                        <div class="icon success-icon">✓</div>
                        <h1 class="success-color">Authentication Successful!</h1>
                        <p>You can close this window and return to the terminal.</p>
                        <div class="brand">Stride CLI</div>
                    </div>
                    <div id="error" style="display:none;">
                        <div class="icon error-icon">✗</div>
                        <h1 class="error-color">Authentication Failed</h1>
                        <p>Please try again or check your email link.</p>
                        <div class="brand">Stride CLI</div>
                    </div>
                </div>
                <script>
                    function extractTokens() {
                        const hash = window.location.hash.substring(1);
                        const params = new URLSearchParams(hash);
                        
                        const accessToken = params.get('access_token');
                        const refreshToken = params.get('refresh_token');
                        
                        if (accessToken) {
                            fetch('/auth/complete?' + new URLSearchParams({
                                access_token: accessToken,
                                refresh_token: refreshToken || ''
                            }))
                            .then(response => {
                                document.getElementById('loading').style.display = 'none';
                                if (response.ok) {
                                    document.getElementById('success').style.display = 'block';
                                } else {
                                    document.getElementById('error').style.display = 'block';
                                }
                            })
                            .catch(() => {
                                document.getElementById('loading').style.display = 'none';
                                document.getElementById('error').style.display = 'block';
                            });
                        } else {
                            document.getElementById('loading').style.display = 'none';
                            document.getElementById('error').style.display = 'block';
                        }
                    }
                    window.onload = extractTokens;
                </script>
            </body>
            </html>
            """
            
            self.wfile.write(html.encode())
        
        elif parsed_url.path == "/auth/complete":
            # Receive tokens from JavaScript
            query = parse_qs(parsed_url.query)
            
            if 'access_token' in query:
                MagicLinkHandler.auth_data = {
                    'access_token': query['access_token'][0],
                    'refresh_token': query.get('refresh_token', [''])[0]
                }
                MagicLinkHandler.auth_complete = True
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(b'{"status":"success"}')
            else:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(b'{"status":"error"}')
    
    def log_message(self, format, *args):
        """Suppress server logs."""
        pass


class SupabaseAuth:
    """
    Manages authentication with Supabase using Magic Link or GitHub OAuth.
    Provides methods for login, logout, and credential management.
    """
    
    def __init__(self):
        """Initialize Supabase authentication manager."""
        self.supabase_url = SUPABASE_URL
        self.api_key = SUPABASE_PUBLISHABLE_KEY
        self.redirect_uri = REDIRECT_URI
        
        # Initialize Supabase client
        try:
            self.supabase: Client = create_client(
                self.supabase_url,
                self.api_key
            )
        except Exception as e:
            console.print(f"[red]✗ Failed to initialize Supabase: {str(e)}[/red]")
            raise
    
    # ==================== MAGIC LINK AUTHENTICATION ====================
    
    def login_with_magic_link(self, email: str = None) -> Optional[Dict]:
        """
        Authenticate using Magic Link (passwordless email).
        
        Args:
            email: User's email address (will prompt if None)
        
        Returns:
            Dict with access_token, refresh_token, and user info if successful
        """
        try:
            # Prompt for email if not provided
            if not email:
                console.print()
                email = Prompt.ask("📧 [cyan]Email address[/cyan]")
            
            # Basic email validation
            if "@" not in email or "." not in email.split("@")[1]:
                console.print("[red]✗ Invalid email format[/red]")
                return None
            
            console.print(f"\n🔄 [cyan]Sending magic link to {email}...[/cyan]")
            
            # Send magic link
            response = self.supabase.auth.sign_in_with_otp({
                "email": email,
                "options": {
                    "email_redirect_to": "http://localhost:37777/auth/callback"
                }
            })
            
            if not response:
                console.print("[red]✗ Failed to send magic link[/red]")
                return None
            
            console.print(f"[green]✓ Magic link sent to {email}[/green]")
            console.print("\n[bold cyan]📬 Check your email inbox![/bold cyan]")
            console.print("[dim]Click the link in the email to complete authentication.[/dim]\n")
            
            # Wait for callback
            token_data = self._wait_for_magic_link_callback()
            
            if not token_data:
                return None
            
            # Get user info
            access_token = token_data['access_token']
            user_response = self.supabase.auth.get_user(access_token)
            
            if user_response and user_response.user:
                user = user_response.user
                return {
                    "access_token": access_token,
                    "refresh_token": token_data.get('refresh_token'),
                    "user": {
                        "id": user.id,
                        "email": user.email,
                        "user_metadata": user.user_metadata or {}
                    }
                }
            
            return None
            
        except Exception as e:
            error_str = str(e).lower()
            if "rate limit" in error_str or "too many" in error_str:
                console.print("[red]✗ Too many requests. Please wait a few minutes.[/red]")
            else:
                console.print(f"[red]✗ Authentication failed: {str(e)}[/red]")
            return None
    
    def _wait_for_magic_link_callback(self, timeout: int = 300) -> Optional[Dict]:
        """
        Wait for magic link callback.
        
        Args:
            timeout: Timeout in seconds (default: 5 minutes)
        
        Returns:
            Dict with tokens if successful
        """
        # Start local server
        server = HTTPServer(('localhost', 37777), MagicLinkHandler)
        server.timeout = 1
        
        start_time = time.time()
        
        # Wait with progress indicator
        with Progress(
            SpinnerColumn(),
            TextColumn("[cyan]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Waiting for magic link click...", total=None)
            
            while time.time() - start_time < timeout:
                server.handle_request()
                
                if MagicLinkHandler.auth_complete:
                    progress.update(task, description="[green]✓ Authentication received![/green]")
                    time.sleep(0.5)  # Brief pause to show success
                    break
                
                elapsed = int(time.time() - start_time)
                progress.update(task, description=f"Waiting for magic link click... ({elapsed}s)")
            else:
                console.print("\n[yellow]⏱ Timeout: No magic link clicked within 5 minutes[/yellow]")
                console.print("[dim]Please try again or check your email spam folder.[/dim]")
                return None
        
        return MagicLinkHandler.auth_data
    
    # ==================== GITHUB OAUTH AUTHENTICATION ====================
    
    def login_with_github(self) -> Optional[Dict]:
        """
        Authenticate using GitHub OAuth.
        
        Returns:
            Dict with access_token, refresh_token, and user info if successful
        """
        try:
            # Get OAuth URL from Supabase
            response = self.supabase.auth.sign_in_with_oauth({
                "provider": "github",
                "options": {
                    "redirect_to": self.redirect_uri
                }
            })
            
            auth_url = response.url
            
            # Open browser
            console.print("\n🔐 [cyan]Opening browser for GitHub authentication...[/cyan]")
            webbrowser.open(auth_url)
            
            # Start local server and wait for callback
            code = self._wait_for_oauth_callback()
            
            if not code:
                return None
            
            # Exchange code for tokens
            token_data = self._exchange_code_for_session(code)
            
            return token_data
            
        except Exception as e:
            console.print(f"[red]✗ GitHub authentication failed: {str(e)}[/red]")
            return None
    
    def _wait_for_oauth_callback(self) -> Optional[str]:
        """
        Wait for OAuth callback and return authorization code.
        
        Returns:
            Authorization code if successful
        """
        # Try multiple ports
        ports = [37777, 37778, 37779, 37780]
        server = None
        
        for port in ports:
            try:
                server = HTTPServer(("localhost", port), OAuthCallbackHandler)
                break
            except OSError:
                continue
        
        if not server:
            console.print("[red]✗ Could not start local server on ports 37777-37780[/red]")
            return None
        
        # Wait for callback with progress
        with Progress(
            SpinnerColumn(),
            TextColumn("[cyan]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Waiting for GitHub authorization...", total=None)
            
            server.handle_request()
            
            code = getattr(server, "auth_code", None)
            error = getattr(server, "error", None)
            
            if error:
                progress.update(task, description=f"[red]✗ OAuth error: {error}[/red]")
                time.sleep(1)
                return None
            
            if code:
                progress.update(task, description="[green]✓ Authorization received![/green]")
                time.sleep(0.5)
            
            return code
    
    def _exchange_code_for_session(self, code: str) -> Optional[Dict]:
        """
        Exchange authorization code for access tokens.
        
        Args:
            code: Authorization code from OAuth callback
            
        Returns:
            Dict with tokens and user info if successful
        """
        try:
            response = self.supabase.auth.exchange_code_for_session({"auth_code": code})
            
            # Handle different response types
            if isinstance(response, dict):
                session = response.get("session")
                user = response.get("user")
                
                if not session:
                    console.print("[red]✗ No session received[/red]")
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
                # Response is an object
                if not response or not hasattr(response, "session"):
                    console.print("[red]✗ No session received[/red]")
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
            return None
    
    # ==================== CREDENTIAL MANAGEMENT ====================
    
    def prompt_for_username(self, default: str = None) -> str:
        """
        Prompt user for username with validation.
        
        Args:
            default: Default username to suggest
            
        Returns:
            Validated username string
        """
        console.print()
        
        while True:
            username = Prompt.ask(
                "👤 [cyan]Choose a username[/cyan]",
                default=default or "developer"
            )
            
            if len(username) < 3:
                console.print("[yellow]⚠ Username must be at least 3 characters[/yellow]")
                continue
            
            if not username.replace("-", "").replace("_", "").isalnum():
                console.print("[yellow]⚠ Username can only contain letters, numbers, - and _[/yellow]")
                continue
            
            return username
    
    def store_credentials(self, access_token: str, refresh_token: str, 
                         email: str, username: str) -> None:
        """
        Store credentials globally using keyring.
        
        Args:
            access_token: Supabase access token
            refresh_token: Supabase refresh token
            email: User's email address
            username: User's chosen display name
        """
        try:
            keyring.set_password(KEYRING_SERVICE, "access_token", access_token)
            keyring.set_password(KEYRING_SERVICE, "refresh_token", refresh_token or "")
            keyring.set_password(KEYRING_SERVICE, "email", email)
            keyring.set_password(KEYRING_SERVICE, "username", username)
        except Exception as e:
            console.print(f"[yellow]⚠ Warning: Could not store credentials: {str(e)}[/yellow]")
    
    def get_current_user(self) -> Optional[Dict[str, str]]:
        """
        Get currently authenticated user information.
        
        Returns:
            Dict with 'email', 'username', 'token' if authenticated, None otherwise
        """
        try:
            access_token = keyring.get_password(KEYRING_SERVICE, "access_token")
            email = keyring.get_password(KEYRING_SERVICE, "email")
            username = keyring.get_password(KEYRING_SERVICE, "username")
            
            if not access_token or not email:
                return None
            
            return {
                "email": email,
                "username": username or "User",
                "token": access_token,
            }
        except Exception:
            return None
    
    def clear_credentials(self) -> None:
        """Clear all stored credentials from keyring."""
        keys = ["access_token", "refresh_token", "email", "username"]
        
        for key in keys:
            try:
                keyring.delete_password(KEYRING_SERVICE, key)
            except keyring.errors.PasswordDeleteError:
                pass
            except Exception:
                pass
    
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
