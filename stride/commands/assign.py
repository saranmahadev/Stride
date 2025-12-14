"""
Sprint assignment command for team collaboration.
"""

import typer
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.panel import Panel

from stride.core.assignment_manager import (
    assign_sprint,
    unassign_sprint,
    get_member_assignments,
    recommend_assignee
)
from stride.core.team_file_manager import read_team_config
from stride.core.workload_analyzer import (
    calculate_team_workload,
    analyze_workload_distribution,
    get_workload_recommendations
)

app = typer.Typer()
console = Console()


@app.command()
def assign(
    sprint_id: str = typer.Argument(..., help="Sprint ID to assign"),
    to: Optional[str] = typer.Option(
        None,
        "--to",
        "-t",
        help="Email of team member to assign to"
    ),
    assigner: Optional[str] = typer.Option(
        None,
        "--by",
        "-b",
        help="Email of person making the assignment"
    ),
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help="Skip recommendations and confirmation"
    )
):
    """
    Assign a sprint to a team member.
    
    If --to is not provided, shows AI-powered recommendations based on
    workload, roles, and assignment history.
    
    Examples:
        stride assign sprint-feature-x --to alice@example.com
        stride assign sprint-feature-x  # Interactive mode with recommendations
    """
    try:
        assignee_email = to
        
        # Interactive mode: show recommendations
        if not assignee_email and not force:
            console.print("\n[bold cyan]Finding best assignee...[/bold cyan]\n")
            
            recommendations = recommend_assignee(sprint_id)
            
            if not recommendations:
                console.print("[yellow]No team members available.[/yellow]")
                console.print("[dim]Run 'stride team init' to set up team.[/dim]")
                raise typer.Exit(1)
            
            # Display recommendations
            table = Table(
                title="Recommended Assignees",
                show_header=True,
                header_style="bold cyan"
            )
            table.add_column("#", style="dim", width=3)
            table.add_column("Name", style="cyan")
            table.add_column("Email", style="dim")
            table.add_column("Workload", justify="center", style="yellow")
            table.add_column("Score", justify="center", style="green")
            table.add_column("Reasons", style="dim")
            
            for idx, rec in enumerate(recommendations[:5], 1):  # Top 5
                member = rec["member"]
                reasons_str = ", ".join(rec["reasons"])
                table.add_row(
                    str(idx),
                    member.name,
                    member.email,
                    str(rec["current_workload"]),
                    str(rec["score"]),
                    reasons_str
                )
            
            console.print(table)
            console.print()
            
            # Prompt for selection
            choice = Prompt.ask(
                "Select assignee by number (or enter email)",
                default="1"
            )
            
            # Parse choice
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(recommendations):
                    assignee_email = recommendations[idx]["member"].email
                else:
                    console.print("[red]Invalid selection[/red]")
                    raise typer.Exit(1)
            else:
                assignee_email = choice
        
        # Require assignee email
        if not assignee_email:
            console.print("[red]Error: --to required when using --force[/red]")
            raise typer.Exit(1)
        
        # Perform assignment
        metadata = assign_sprint(
            sprint_id=sprint_id,
            assignee_email=assignee_email,
            assigner_email=assigner
        )
        
        # Get member name
        team_config = read_team_config()
        member = team_config.get_member(assignee_email)
        
        console.print(
            f"\n[bold green]✓[/bold green] Assigned [cyan]{sprint_id}[/cyan] "
            f"to [cyan]{member.name}[/cyan] ({assignee_email})"
        )
        
        if metadata.assigned_by:
            console.print(f"[dim]Assigned by: {metadata.assigned_by}[/dim]")
        
        console.print()
        
    except FileNotFoundError as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(1)
    except ValueError as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(1)


@app.command()
def unassign(
    sprint_id: str = typer.Argument(..., help="Sprint ID to unassign"),
    actor: Optional[str] = typer.Option(
        None,
        "--by",
        "-b",
        help="Email of person removing the assignment"
    ),
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help="Skip confirmation prompt"
    )
):
    """
    Remove assignment from a sprint.
    
    Example:
        stride unassign sprint-feature-x
    """
    try:
        # Confirm unassignment
        if not force:
            confirmed = Confirm.ask(
                f"Remove assignment from [cyan]{sprint_id}[/cyan]?",
                default=False
            )
            if not confirmed:
                console.print("[dim]Cancelled[/dim]")
                raise typer.Exit(0)
        
        # Perform unassignment
        metadata = unassign_sprint(sprint_id=sprint_id, actor_email=actor)
        
        if metadata is None:
            console.print(f"[yellow]Sprint [cyan]{sprint_id}[/cyan] was not assigned[/yellow]")
        else:
            console.print(
                f"[bold green]✓[/bold green] Removed assignment from [cyan]{sprint_id}[/cyan]"
            )
        
    except FileNotFoundError as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(1)


@app.command()
def workload(
    email: Optional[str] = typer.Argument(
        None,
        help="Email of team member (shows all if omitted)"
    ),
    export: bool = typer.Option(
        False,
        "--export",
        help="Export workload data as JSON"
    )
):
    """
    Show workload summary for team member(s) with complexity analysis.
    
    Examples:
        stride assign workload alice@example.com  # Single member
        stride assign workload  # All members with distribution stats
        stride assign workload --export  # JSON output
    """
    try:
        from stride.core.workload_analyzer import calculate_member_workload
        import json
        
        team_config = read_team_config()
        
        if email:
            # Single member view with complexity
            workload = calculate_member_workload(email)
            member = team_config.get_member(email)
            
            if export:
                console.print(json.dumps(workload, indent=2, default=str))
                return
            
            console.print()
            console.print(Panel.fit(
                f"[bold cyan]{member.name}[/bold cyan]\n\n"
                f"Email: [dim]{member.email}[/dim]\n"
                f"Total Sprints: [cyan]{workload['active_count']}[/cyan]\n"
                f"Pending: [yellow]{workload['pending_count']}[/yellow]\n"
                f"In Review: [green]{workload['in_review_count']}[/green]\n"
                f"Complexity Score: [magenta]{workload['complexity_score']}[/magenta]\n"
                f"Weighted Load: [bold magenta]{workload['weighted_load']}[/bold magenta]",
                title="Workload Summary",
                border_style="cyan"
            ))
            
            if workload["assigned_sprints"]:
                table = Table(
                    title="Assigned Sprints",
                    show_header=True,
                    header_style="bold cyan"
                )
                table.add_column("Sprint ID", style="cyan")
                table.add_column("Assigned At", style="dim")
                table.add_column("Status", style="yellow")
                table.add_column("Approvals", justify="center", style="green")
                
                for assignment in workload["assigned_sprints"]:
                    assigned_at_str = (
                        assignment["assigned_at"].strftime("%Y-%m-%d %H:%M")
                        if assignment["assigned_at"]
                        else "Unknown"
                    )
                    table.add_row(
                        assignment["sprint_id"],
                        assigned_at_str,
                        assignment["status"],
                        str(assignment["approval_count"])
                    )
                
                console.print()
                console.print(table)
            
            console.print()
        
        else:
            # All members view with distribution stats
            workloads = calculate_team_workload()
            distribution = analyze_workload_distribution()
            
            if export:
                export_data = {
                    "distribution": distribution,
                    "workloads": workloads
                }
                console.print(json.dumps(export_data, indent=2, default=str))
                return
            
            # Distribution summary
            console.print()
            console.print(Panel.fit(
                f"[bold]Team Size:[/bold] [cyan]{distribution['total_members']}[/cyan] members\n"
                f"[bold]Total Sprints:[/bold] [cyan]{distribution['total_sprints']}[/cyan]\n"
                f"[bold]Average Load:[/bold] [yellow]{distribution['avg_load']}[/yellow]\n"
                f"[bold]Load Range:[/bold] [{distribution['min_load']}-{distribution['max_load']}]\n"
                f"[bold]Std Deviation:[/bold] [dim]{distribution['std_dev']}[/dim]\n"
                f"[bold]Balance Score:[/bold] [{'green' if distribution['balance_score'] >= 70 else 'yellow'}]{distribution['balance_score']}/100[/{'green' if distribution['balance_score'] >= 70 else 'yellow'}]",
                title="Workload Distribution",
                border_style="cyan"
            ))
            
            # Workload table with progress bars
            table = Table(
                title="Team Workload Details",
                show_header=True,
                header_style="bold cyan"
            )
            table.add_column("Name", style="cyan")
            table.add_column("Sprints", justify="center", style="white")
            table.add_column("Load", justify="center", style="magenta")
            table.add_column("Distribution", style="yellow")
            
            max_load = distribution['max_load'] if distribution['max_load'] > 0 else 1
            
            for workload in workloads:
                # Create progress bar
                bar_width = 20
                filled = int((workload['weighted_load'] / max_load) * bar_width)
                bar = "█" * filled + "░" * (bar_width - filled)
                
                table.add_row(
                    workload['member_name'],
                    f"{workload['active_count']} ({workload['pending_count']}P, {workload['in_review_count']}R)",
                    str(workload['weighted_load']),
                    bar
                )
            
            console.print()
            console.print(table)
            
            # Recommendations
            recommendations = get_workload_recommendations()
            if recommendations:
                console.print()
                console.print("[bold]Recommendations:[/bold]")
                for rec in recommendations:
                    console.print(f"  {rec}")
            
            console.print()
    
    except FileNotFoundError as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        console.print("[yellow]Run 'stride team init' to set up team.[/yellow]")
        raise typer.Exit(1)
    except ValueError as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(1)
