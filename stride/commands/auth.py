"""
Authentication commands for Stride CLI.
Provides login, logout, and whoami functionality using GitHub OAuth via Supabase.
"""

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from stride.core.auth import SupabaseAuth

console = Console()


def login():
    """
    Authenticate with GitHub via Supabase.
    
    Opens browser for OAuth flow, prompts for username, and stores
    credentials globally for all Stride projects.
    """
    auth = SupabaseAuth()
    
    # Check if already logged in
    current_user = auth.get_current_user()
    if current_user:
        console.print(f"\n[yellow]⚠ Already logged in as:[/yellow] [bold]{current_user['username']}[/bold] ({current_user['email']})")
        
        if not typer.confirm("Login with a different account?", default=False):
            console.print("[dim]Login cancelled.[/dim]")
            return
        
        # Logout first
        auth.clear_credentials()
        console.print("[green]✓ Previous session cleared[/green]\n")
    
    # Start OAuth flow
    code = auth.start_oauth_flow()
    
    if not code:
        console.print("\n[red]✗ Authentication failed[/red]")
        console.print("[yellow]Please try again or check your internet connection.[/yellow]")
        return
    
    # Exchange code for tokens
    console.print("🔄 [cyan]Exchanging authorization code...[/cyan]")
    token_data = auth.exchange_code_for_token(code)
    
    if not token_data:
        console.print("\n[red]✗ Failed to obtain access token[/red]")
        console.print("[yellow]Please try again later.[/yellow]")
        return
    
    # Extract user info
    access_token = token_data.get("access_token")
    refresh_token = token_data.get("refresh_token")
    user_info = token_data.get("user", {})
    github_email = user_info.get("email") or user_info.get("user_metadata", {}).get("email", "unknown@github.com")
    
    if not access_token:
        console.print("\n[red]✗ No access token received[/red]")
        return
    
    console.print(f"[green]✓ Authenticated as:[/green] [bold]{github_email}[/bold]\n")
    
    # Prompt for username
    username = auth.prompt_for_username()
    
    # Store credentials globally
    auth.store_credentials(access_token, refresh_token, github_email, username)
    
    # Success message
    console.print()
    success_panel = Panel(
        f"[green]✓ Welcome, [bold]{username}[/bold]! You're all set.[/green]\n"
        f"[dim]Your credentials are saved globally for all Stride projects.[/dim]",
        title="[bold]Login Successful[/bold]",
        border_style="green",
        padding=(1, 2),
    )
    console.print(success_panel)


def logout():
    """
    Clear stored authentication credentials.
    
    Removes all credentials from global keyring storage.
    """
    auth = SupabaseAuth()
    
    # Check if logged in
    current_user = auth.get_current_user()
    
    if not current_user:
        console.print("\n[yellow]⚠ Not currently logged in[/yellow]")
        console.print("[dim]Run 'stride login' to authenticate.[/dim]\n")
        return
    
    # Show current user
    console.print(f"\n👤 [cyan]Currently logged in as:[/cyan] [bold]{current_user['username']}[/bold] ({current_user['email']})")
    
    # Confirm logout
    if not typer.confirm("\nAre you sure you want to logout?", default=True):
        console.print("[dim]Logout cancelled.[/dim]")
        return
    
    # Clear credentials
    auth.clear_credentials()
    
    # Success message
    console.print("\n[green]✓ Logged out successfully[/green]")
    console.print(f"[dim]Goodbye, {current_user['username']}![/dim]\n")


def whoami():
    """
    Display currently authenticated user information.
    
    Shows username, email, and authentication status.
    """
    auth = SupabaseAuth()
    
    # Get current user
    current_user = auth.get_current_user()
    
    if not current_user:
        console.print()
        not_logged_in_panel = Panel(
            "[yellow]❌ Not logged in[/yellow]\n"
            "[dim]Run 'stride login' to authenticate with GitHub.[/dim]",
            title="[bold]Authentication Status[/bold]",
            border_style="yellow",
            padding=(1, 2),
        )
        console.print(not_logged_in_panel)
        console.print()
        return
    
    # Create info table
    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column("Field", style="cyan")
    table.add_column("Value", style="white")
    
    table.add_row("👤 Username", f"[bold]{current_user['username']}[/bold]")
    table.add_row("📧 GitHub", current_user['email'])
    table.add_row("🔑 Token", "[green]Active[/green]")
    
    # Display panel with table
    console.print()
    user_panel = Panel(
        table,
        title="[bold]Authenticated User[/bold]",
        border_style="green",
        padding=(1, 0),
    )
    console.print(user_panel)
    console.print()
