"""
Team management commands for Stride.

This module provides CLI commands for managing team members, roles, and
approval policies in a Git-based collaborative environment.
"""

import typer
from pathlib import Path
from typing import Optional, List
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.panel import Panel

from stride.models import TeamConfig, TeamMember
from stride.core.team_file_manager import read_team_config, write_team_config
from stride.utils import get_stride_dir

app = typer.Typer(help="Manage team members and collaboration settings")
console = Console()


@app.command()
def init(
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help="Overwrite existing team.yaml if present"
    )
):
    """
    Initialize team collaboration by creating team.yaml.
    
    Creates a new team configuration file with interactive prompts for
    team members, roles, and approval policies.
    """
    try:
        stride_dir = get_stride_dir()
        team_file = stride_dir / "team.yaml"
        
        # Check if team.yaml already exists
        if team_file.exists() and not force:
            console.print(
                "[yellow]team.yaml already exists. Use --force to overwrite.[/yellow]"
            )
            raise typer.Exit(1)
        
        console.print(Panel.fit(
            "[bold cyan]Team Collaboration Setup[/bold cyan]\n\n"
            "Let's configure your team for collaborative sprint management.",
            border_style="cyan"
        ))
        
        # Collect team members
        members = []
        console.print("\n[bold]Add Team Members[/bold]")
        console.print("(Press Enter with empty name to finish)\n")
        
        while True:
            name = Prompt.ask("Member name", default="")
            if not name:
                break
            
            email = Prompt.ask(f"Email for {name}")
            
            # Collect roles
            console.print("\n[dim]Available roles: lead, developer, reviewer, designer, qa, docs[/dim]")
            roles_input = Prompt.ask(
                "Roles (comma-separated)",
                default="developer"
            )
            roles = {role.strip(): True for role in roles_input.split(",")}
            
            members.append(TeamMember(
                name=name,
                email=email,
                roles=roles
            ))
            console.print(f"[green]✓[/green] Added {name}\n")
        
        if not members:
            console.print("[yellow]No team members added. Aborting.[/yellow]")
            raise typer.Exit(1)
        
        # Configure approval policy
        console.print("\n[bold]Approval Policy[/bold]")
        enabled = Confirm.ask("Enable approval workflow?", default=True)
        
        required_approvals = 1
        roles_can_approve = ["lead", "reviewer"]
        
        if enabled:
            required_approvals = int(Prompt.ask(
                "Required approvals",
                default="1"
            ))
            
            roles_input = Prompt.ask(
                "Roles that can approve (comma-separated)",
                default="lead,reviewer"
            )
            roles_can_approve = [role.strip() for role in roles_input.split(",")]
        
        # Create team config
        team_config = TeamConfig(
            members=members,
            approval_policy={
                "enabled": enabled,
                "required_approvals": required_approvals,
                "roles_can_approve": roles_can_approve
            }
        )
        
        # Write to file
        write_team_config(team_config)
        
        console.print("\n[bold green]✓ Team configuration created![/bold green]")
        console.print(f"[dim]File: {team_file}[/dim]")
        console.print(f"\n[cyan]{len(members)}[/cyan] team members configured")
        console.print(f"Approval workflow: [cyan]{'enabled' if enabled else 'disabled'}[/cyan]")
        
    except FileNotFoundError as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        console.print("[yellow]Run 'stride init' first to initialize the project.[/yellow]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(1)


@app.command()
def add(
    name: str = typer.Argument(..., help="Member name"),
    email: str = typer.Argument(..., help="Member email"),
    roles: str = typer.Option(
        "developer",
        "--roles",
        "-r",
        help="Comma-separated roles (e.g., 'lead,reviewer')"
    )
):
    """
    Add a new team member to team.yaml.
    
    Example:
        stride team add "John Doe" john@example.com --roles lead,developer
    """
    try:
        team_config = read_team_config()
        
        # Check if member already exists
        if team_config.has_member(email):
            console.print(f"[yellow]Member with email {email} already exists.[/yellow]")
            raise typer.Exit(1)
        
        # Parse roles
        roles_dict = {role.strip(): True for role in roles.split(",")}
        
        # Create new member
        new_member = TeamMember(
            name=name,
            email=email,
            roles=roles_dict
        )
        
        # Add to team
        team_config.members.append(new_member)
        write_team_config(team_config)
        
        console.print(f"[bold green]✓[/bold green] Added {name} ({email})")
        console.print(f"[dim]Roles: {', '.join(roles_dict.keys())}[/dim]")
        
    except FileNotFoundError:
        console.print("[bold red]Error:[/bold red] team.yaml not found")
        console.print("[yellow]Run 'stride team init' first.[/yellow]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(1)


@app.command()
def remove(
    email: str = typer.Argument(..., help="Email of member to remove"),
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help="Skip confirmation prompt"
    )
):
    """
    Remove a team member from team.yaml.
    
    Example:
        stride team remove john@example.com
    """
    try:
        team_config = read_team_config()
        
        # Find member
        member = team_config.get_member(email)
        if not member:
            console.print(f"[yellow]No member found with email {email}[/yellow]")
            raise typer.Exit(1)
        
        # Confirm removal
        if not force:
            confirmed = Confirm.ask(
                f"Remove {member.name} ({email})?",
                default=False
            )
            if not confirmed:
                console.print("[dim]Cancelled[/dim]")
                raise typer.Exit(0)
        
        # Remove member
        team_config.members = [
            m for m in team_config.members if m.email != email
        ]
        write_team_config(team_config)
        
        console.print(f"[bold green]✓[/bold green] Removed {member.name}")
        
    except FileNotFoundError:
        console.print("[bold red]Error:[/bold red] team.yaml not found")
        console.print("[yellow]Run 'stride team init' first.[/yellow]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(1)


@app.command()
def edit(
    email: str = typer.Argument(..., help="Email of member to edit"),
    name: Optional[str] = typer.Option(None, "--name", "-n", help="New name"),
    roles: Optional[str] = typer.Option(
        None,
        "--roles",
        "-r",
        help="New roles (comma-separated)"
    )
):
    """
    Edit an existing team member's information.
    
    Example:
        stride team edit john@example.com --name "John Smith" --roles lead,developer
    """
    try:
        team_config = read_team_config()
        
        # Find member
        member = team_config.get_member(email)
        if not member:
            console.print(f"[yellow]No member found with email {email}[/yellow]")
            raise typer.Exit(1)
        
        # Update fields
        if name:
            member.name = name
        
        if roles:
            member.roles = {role.strip(): True for role in roles.split(",")}
        
        # Save changes
        write_team_config(team_config)
        
        console.print(f"[bold green]✓[/bold green] Updated {member.name}")
        console.print(f"[dim]Roles: {', '.join(member.roles.keys())}[/dim]")
        
    except FileNotFoundError:
        console.print("[bold red]Error:[/bold red] team.yaml not found")
        console.print("[yellow]Run 'stride team init' first.[/yellow]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(1)


@app.command()
def list():
    """
    List all team members with their roles.
    
    Displays a formatted table of team members, their emails, and assigned roles.
    """
    try:
        team_config = read_team_config()
        
        if not team_config.members:
            console.print("[yellow]No team members configured.[/yellow]")
            console.print("[dim]Run 'stride team add' to add members.[/dim]")
            raise typer.Exit(0)
        
        # Create table
        table = Table(title="Team Members", show_header=True, header_style="bold cyan")
        table.add_column("Name", style="cyan", no_wrap=True)
        table.add_column("Email", style="dim")
        table.add_column("Roles", style="green")
        
        for member in team_config.members:
            roles_str = ", ".join(member.roles.keys())
            table.add_row(member.name, member.email, roles_str)
        
        console.print()
        console.print(table)
        console.print()
        
        # Show approval policy
        policy = team_config.approval_policy
        if policy.get("enabled"):
            console.print("[bold]Approval Policy[/bold]")
            console.print(f"  Required approvals: [cyan]{policy.get('required_approvals', 1)}[/cyan]")
            console.print(f"  Can approve: [green]{', '.join(policy.get('roles_can_approve', []))}[/green]")
        else:
            console.print("[dim]Approval workflow: disabled[/dim]")
        
        console.print()
        
    except FileNotFoundError:
        console.print("[bold red]Error:[/bold red] team.yaml not found")
        console.print("[yellow]Run 'stride team init' first.[/yellow]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(1)


@app.command()
def show(
    email: str = typer.Argument(..., help="Email of member to show")
):
    """
    Show detailed information about a specific team member.
    
    Example:
        stride team show john@example.com
    """
    try:
        team_config = read_team_config()
        
        # Find member
        member = team_config.get_member(email)
        if not member:
            console.print(f"[yellow]No member found with email {email}[/yellow]")
            raise typer.Exit(1)
        
        # Display member details
        console.print()
        console.print(Panel.fit(
            f"[bold cyan]{member.name}[/bold cyan]\n\n"
            f"Email: [dim]{member.email}[/dim]\n"
            f"Roles: [green]{', '.join(member.roles.keys())}[/green]",
            title="Team Member",
            border_style="cyan"
        ))
        console.print()
        
    except FileNotFoundError:
        console.print("[bold red]Error:[/bold red] team.yaml not found")
        console.print("[yellow]Run 'stride team init' first.[/yellow]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(1)
