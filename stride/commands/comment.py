"""
Comment and communication commands for sprints.
"""

import typer
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.panel import Panel
from rich.tree import Tree
from rich.markdown import Markdown

from stride.core.comment_manager import (
    add_comment,
    get_comments,
    resolve_comment,
    unresolve_comment,
    reply_to_comment,
    get_comment_stats
)
from stride.core.team_file_manager import read_team_config

app = typer.Typer()
console = Console()


@app.command()
def add(
    sprint_id: str = typer.Argument(..., help="Sprint ID"),
    content: str = typer.Argument(..., help="Comment text"),
    author: Optional[str] = typer.Option(
        None,
        "--by",
        "-b",
        help="Email of author (uses git identity if omitted)"
    ),
    file: Optional[str] = typer.Option(
        None,
        "--file",
        "-f",
        help="File path being commented on"
    ),
    line: Optional[int] = typer.Option(
        None,
        "--line",
        "-l",
        help="Line number in file"
    ),
    reply_to: Optional[str] = typer.Option(
        None,
        "--reply-to",
        "-r",
        help="Parent comment ID for replies"
    )
):
    """
    Add a comment to a sprint.
    
    Comments support markdown formatting. Use --file and --line to anchor
    comments to specific code locations.
    
    Examples:
        stride comment add sprint-x "Great work!"
        stride comment add sprint-x "Fix this" --file src/main.py --line 42
        stride comment add sprint-x "Done" --reply-to c1234567890
    """
    try:
        # TODO: Get author from git identity if not specified
        if not author:
            console.print(
                "[yellow]--by required (git identity detection not yet implemented)[/yellow]"
            )
            raise typer.Exit(1)
        
        # Add comment or reply
        if reply_to:
            comment = reply_to_comment(
                sprint_id=sprint_id,
                parent_id=reply_to,
                author_email=author,
                content=content
            )
        else:
            comment = add_comment(
                sprint_id=sprint_id,
                author_email=author,
                content=content,
                file_path=file,
                line_number=line
            )
        
        # Get author name
        try:
            team_config = read_team_config()
            member = team_config.get_member(author)
            author_name = member.name if member else author
        except:
            author_name = author
        
        console.print(f"\n[bold green]✓[/bold green] Comment added by [cyan]{author_name}[/cyan]")
        console.print(f"[dim]ID: {comment.id}[/dim]")
        
        if file:
            console.print(f"[dim]File: {file}" + (f":{line}" if line else "") + "[/dim]")
        
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
def list(
    sprint_id: str = typer.Argument(..., help="Sprint ID"),
    file: Optional[str] = typer.Option(
        None,
        "--file",
        "-f",
        help="Filter by file path"
    ),
    unresolved: bool = typer.Option(
        False,
        "--unresolved",
        "-u",
        help="Show only unresolved comments"
    ),
    flat: bool = typer.Option(
        False,
        "--flat",
        help="Show flat list instead of threaded view"
    )
):
    """
    List comments for a sprint.
    
    By default, shows threaded comment view. Use --flat for linear list.
    
    Examples:
        stride comment list sprint-x
        stride comment list sprint-x --unresolved
        stride comment list sprint-x --file src/main.py
    """
    try:
        comments = get_comments(
            sprint_id=sprint_id,
            file_path=file,
            unresolved_only=unresolved,
            flat=flat
        )
        
        if not comments:
            console.print(f"\n[yellow]No comments found for {sprint_id}[/yellow]\n")
            return
        
        # Load team config for names
        team_config = None
        try:
            team_config = read_team_config()
        except:
            pass
        
        console.print()
        
        if flat:
            # Flat table view
            table = Table(
                title=f"Comments for {sprint_id}",
                show_header=True,
                header_style="bold cyan"
            )
            table.add_column("ID", style="dim", no_wrap=True, width=15)
            table.add_column("Author", style="cyan", no_wrap=True)
            table.add_column("Content", style="white")
            table.add_column("File", style="dim", no_wrap=True)
            table.add_column("Status", justify="center", no_wrap=True)
            
            for comment in comments:
                author_name = comment.author
                if team_config:
                    member = team_config.get_member(comment.author)
                    author_name = member.name if member else comment.author
                
                file_str = ""
                if comment.file_path:
                    file_str = comment.file_path
                    if comment.line_number:
                        file_str += f":{comment.line_number}"
                
                status = "[green]✓[/green]" if comment.is_resolved else "[yellow]○[/yellow]"
                
                table.add_row(
                    comment.id[-12:],  # Last 12 chars
                    author_name,
                    comment.content[:60] + "..." if len(comment.content) > 60 else comment.content,
                    file_str,
                    status
                )
            
            console.print(table)
        else:
            # Threaded tree view
            tree = Tree(f"[bold cyan]{sprint_id}[/bold cyan] - Comments")
            
            for comment in comments:
                _add_comment_to_tree(tree, comment, team_config)
            
            console.print(tree)
        
        # Show stats
        stats = get_comment_stats(sprint_id)
        console.print()
        console.print(
            f"[dim]Total: {stats['total']} | "
            f"Unresolved: [yellow]{stats['unresolved']}[/yellow] | "
            f"Resolved: [green]{stats['resolved']}[/green][/dim]"
        )
        console.print()
        
    except FileNotFoundError as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(1)


def _add_comment_to_tree(tree, comment, team_config):
    """Recursively add comment and replies to tree."""
    # Get author name
    author_name = comment.author
    if team_config:
        member = team_config.get_member(comment.author)
        author_name = member.name if member else comment.author
    
    # Format header
    status_icon = "[green]✓[/green]" if comment.is_resolved else "[yellow]○[/yellow]"
    file_info = ""
    if comment.file_path:
        file_info = f" [dim]({comment.file_path}"
        if comment.line_number:
            file_info += f":{comment.line_number}"
        file_info += ")[/dim]"
    
    header = f"{status_icon} [cyan]{author_name}[/cyan]{file_info} [dim]{comment.id[-8:]}[/dim]"
    
    # Add to tree
    branch = tree.add(header)
    branch.add(f"[white]{comment.content}[/white]")
    
    # Add replies
    if comment.replies:
        replies_branch = branch.add("[dim]Replies[/dim]")
        for reply in comment.replies:
            _add_comment_to_tree(replies_branch, reply, team_config)


@app.command()
def resolve(
    sprint_id: str = typer.Argument(..., help="Sprint ID"),
    comment_id: str = typer.Argument(..., help="Comment ID to resolve"),
    resolver: Optional[str] = typer.Option(
        None,
        "--by",
        "-b",
        help="Email of resolver (uses git identity if omitted)"
    )
):
    """
    Mark a comment as resolved.
    
    Example:
        stride comment resolve sprint-x c1234567890
    """
    try:
        # TODO: Get resolver from git identity if not specified
        if not resolver:
            console.print(
                "[yellow]--by required (git identity detection not yet implemented)[/yellow]"
            )
            raise typer.Exit(1)
        
        comment = resolve_comment(
            sprint_id=sprint_id,
            comment_id=comment_id,
            resolver_email=resolver
        )
        
        console.print(f"\n[bold green]✓[/bold green] Comment {comment_id} marked as resolved\n")
        
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
def unresolve(
    sprint_id: str = typer.Argument(..., help="Sprint ID"),
    comment_id: str = typer.Argument(..., help="Comment ID to unresolve")
):
    """
    Mark a resolved comment as unresolved.
    
    Example:
        stride comment unresolve sprint-x c1234567890
    """
    try:
        comment = unresolve_comment(sprint_id=sprint_id, comment_id=comment_id)
        
        console.print(f"\n[bold green]✓[/bold green] Comment {comment_id} marked as unresolved\n")
        
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
def stats(
    sprint_id: str = typer.Argument(..., help="Sprint ID")
):
    """
    Show comment statistics for a sprint.
    
    Example:
        stride comment stats sprint-x
    """
    try:
        stats = get_comment_stats(sprint_id)
        
        console.print()
        console.print(Panel.fit(
            f"[bold]Total Comments:[/bold] [cyan]{stats['total']}[/cyan]\n"
            f"[bold]Unresolved:[/bold] [yellow]{stats['unresolved']}[/yellow]\n"
            f"[bold]Resolved:[/bold] [green]{stats['resolved']}[/green]\n"
            f"[bold]Files with Comments:[/bold] [cyan]{len(stats['files_with_comments'])}[/cyan]",
            title=f"Comment Stats: {sprint_id}",
            border_style="cyan"
        ))
        
        if stats['files_with_comments']:
            console.print("\n[bold]Files with Comments:[/bold]")
            for file_path in stats['files_with_comments']:
                console.print(f"  [dim]•[/dim] {file_path}")
        
        console.print()
        
    except FileNotFoundError as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(1)
