"""
Approval workflow commands for sprint review.
"""

import typer
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn

from stride.core.approval_manager import (
    approve_sprint,
    revoke_approval,
    get_approval_status,
    get_pending_approvals,
    can_approve
)
from stride.core.team_file_manager import read_team_config

app = typer.Typer()
console = Console()


@app.command()
def approve(
    sprint_id: str = typer.Argument(..., help="Sprint ID to approve"),
    approver: Optional[str] = typer.Option(
        None,
        "--by",
        "-b",
        help="Email of approver (uses git identity if omitted)"
    ),
    comment: Optional[str] = typer.Option(
        None,
        "--comment",
        "-c",
        help="Approval comment"
    ),
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help="Skip confirmation prompt"
    )
):
    """
    Approve a sprint for completion.
    
    Adds your approval to the sprint's approval workflow. The sprint can
    be completed once it reaches the required approval threshold.
    
    Examples:
        stride approve sprint-feature-x
        stride approve sprint-feature-x --by alice@example.com --comment "LGTM"
    """
    try:
        # TODO: Get approver from git identity if not specified
        if not approver:
            console.print(
                "[yellow]--by required (git identity detection not yet implemented)[/yellow]"
            )
            raise typer.Exit(1)
        
        # Check approval status before approving
        status = get_approval_status(sprint_id)
        
        if not status["workflow_enabled"]:
            console.print("[yellow]Approval workflow is disabled for this project.[/yellow]")
            raise typer.Exit(1)
        
        # Show current status
        console.print(f"\n[bold]Sprint:[/bold] [cyan]{sprint_id}[/cyan]")
        console.print(
            f"[bold]Current Approvals:[/bold] "
            f"[cyan]{status['current_approvals']}/{status['required_approvals']}[/cyan]"
        )
        
        if status["approved"]:
            console.print("[green]✓ Already has required approvals[/green]")
        
        # Confirm approval
        if not force:
            if comment:
                console.print(f"[dim]Comment: {comment}[/dim]\n")
            
            confirmed = Confirm.ask(
                f"Approve this sprint?",
                default=True
            )
            if not confirmed:
                console.print("[dim]Cancelled[/dim]")
                raise typer.Exit(0)
        
        # Perform approval
        metadata = approve_sprint(
            sprint_id=sprint_id,
            approver_email=approver,
            comment=comment
        )
        
        # Get team config for names
        team_config = read_team_config()
        member = team_config.get_member(approver)
        approver_name = member.name if member else approver
        
        console.print(
            f"\n[bold green]✓[/bold green] Approved by [cyan]{approver_name}[/cyan]"
        )
        
        if comment:
            console.print(f"[dim]Comment: {comment}[/dim]")
        
        # Show updated status
        new_status = get_approval_status(sprint_id, team_config)
        console.print(
            f"\n[bold]Approval Progress:[/bold] "
            f"[cyan]{new_status['current_approvals']}/{new_status['required_approvals']}[/cyan]"
        )
        
        if new_status["approved"]:
            console.print(
                "[bold green]✓ Sprint has reached approval threshold and can be completed![/bold green]"
            )
        else:
            console.print(
                f"[yellow]{new_status['missing_approvals']} more approval(s) needed[/yellow]"
            )
        
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
def revoke(
    sprint_id: str = typer.Argument(..., help="Sprint ID"),
    approver: str = typer.Argument(..., help="Email of approver to revoke"),
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help="Skip confirmation prompt"
    )
):
    """
    Revoke an approval from a sprint.
    
    Example:
        stride approve revoke sprint-feature-x alice@example.com
    """
    try:
        # Confirm revocation
        if not force:
            confirmed = Confirm.ask(
                f"Revoke approval from [cyan]{approver}[/cyan]?",
                default=False
            )
            if not confirmed:
                console.print("[dim]Cancelled[/dim]")
                raise typer.Exit(0)
        
        # Perform revocation
        metadata = revoke_approval(sprint_id=sprint_id, approver_email=approver)
        
        console.print(
            f"[bold green]✓[/bold green] Revoked approval from [cyan]{approver}[/cyan]"
        )
        
        # Show updated status
        status = get_approval_status(sprint_id)
        console.print(
            f"[bold]Current Approvals:[/bold] "
            f"[cyan]{status['current_approvals']}/{status['required_approvals']}[/cyan]"
        )
        
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
def status(
    sprint_id: str = typer.Argument(..., help="Sprint ID to check")
):
    """
    Show detailed approval status for a sprint.
    
    Example:
        stride approve status sprint-feature-x
    """
    try:
        status = get_approval_status(sprint_id)
        
        if not status["workflow_enabled"]:
            console.print("\n[yellow]Approval workflow is disabled[/yellow]\n")
            return
        
        # Header
        console.print()
        console.print(Panel.fit(
            f"[bold cyan]{sprint_id}[/bold cyan]\n\n"
            f"Approvals: [cyan]{status['current_approvals']}/{status['required_approvals']}[/cyan]\n"
            f"Status: {'[green]✓ Approved[/green]' if status['approved'] else '[yellow]Pending[/yellow]'}",
            title="Approval Status",
            border_style="cyan"
        ))
        
        # Progress bar
        if status["required_approvals"] > 0:
            console.print()
            with Progress(
                TextColumn("[bold blue]{task.description}"),
                BarColumn(complete_style="green", finished_style="bold green"),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                console=console
            ) as progress:
                task = progress.add_task(
                    "Approval Progress",
                    total=status["required_approvals"],
                    completed=status["current_approvals"]
                )
            console.print()
        
        # Approvers table
        if status["approvers"]:
            table = Table(
                title="Approvers",
                show_header=True,
                header_style="bold cyan"
            )
            table.add_column("Name", style="cyan")
            table.add_column("Email", style="dim")
            table.add_column("Approved At", style="green")
            table.add_column("Comment", style="dim")
            
            for approver in status["approvers"]:
                approved_at_str = approver["approved_at"].strftime("%Y-%m-%d %H:%M")
                comment_str = approver["comment"] or "[dim]—[/dim]"
                table.add_row(
                    approver["name"],
                    approver["email"],
                    approved_at_str,
                    comment_str
                )
            
            console.print(table)
            console.print()
        
        # Summary
        if status["approved"]:
            console.print("[bold green]✓ This sprint can be completed[/bold green]")
        else:
            console.print(
                f"[yellow]{status['missing_approvals']} more approval(s) needed[/yellow]"
            )
        
        console.print()
        
    except FileNotFoundError as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(1)


@app.command()
def pending(
    approver: Optional[str] = typer.Option(
        None,
        "--by",
        "-b",
        help="Filter to sprints where this person can approve"
    )
):
    """
    List sprints pending approval.
    
    Examples:
        stride approve pending  # All pending
        stride approve pending --by alice@example.com  # Pending for Alice
    """
    try:
        pending_list = get_pending_approvals(approver_email=approver)
        
        if not pending_list:
            if approver:
                console.print(
                    f"\n[green]No sprints pending approval by {approver}[/green]\n"
                )
            else:
                console.print("\n[green]No sprints pending approval[/green]\n")
            return
        
        # Create table
        table = Table(
            title=f"Pending Approvals{f' for {approver}' if approver else ''}",
            show_header=True,
            header_style="bold cyan"
        )
        table.add_column("Sprint ID", style="cyan", no_wrap=True)
        table.add_column("Assignee", style="green")
        table.add_column("Current", justify="center", style="yellow")
        table.add_column("Required", justify="center", style="cyan")
        table.add_column("Missing", justify="center", style="red")
        
        for item in pending_list:
            assignee_str = item["assignee"] or "[dim]Unassigned[/dim]"
            if item["assignee"]:
                # Show just username part
                assignee_str = item["assignee"].split('@')[0]
            
            table.add_row(
                item["sprint_id"],
                assignee_str,
                str(item["current_approvals"]),
                str(item["required_approvals"]),
                str(item["missing_approvals"])
            )
        
        console.print()
        console.print(table)
        console.print()
        console.print(f"[dim]Total: {len(pending_list)} sprint(s) pending approval[/dim]")
        console.print()
        
    except FileNotFoundError as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(1)
