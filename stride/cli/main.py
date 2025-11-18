"""
Main CLI entry point for Stride.
"""
import builtins
import click
import sys
import json
from pathlib import Path
from typing import Optional

from stride import __version__
from stride.core.folder_manager import FolderManager, SprintStatus
from stride.core.sprint_manager import SprintManager
from stride.core.config_manager import ConfigManager, ConfigError, ConfigValidationError
from stride.utils.id_generator import generate_sprint_id, validate_sprint_id

try:
    from rich.console import Console
    from rich.table import Table
    from rich import print as rprint
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    Console = None
    Table = None
    rprint = print


# Global console for rich output
console = Console() if RICH_AVAILABLE else None


@click.group()
@click.version_option(version=__version__, prog_name="stride")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
@click.option("--quiet", "-q", is_flag=True, help="Suppress non-essential output")
@click.pass_context
def cli(ctx: click.Context, verbose: bool, quiet: bool) -> None:
    """
    Stride - Sprint-Powered, Spec-Driven Development for AI Agents
    
    A framework that combines spec-first development with agile sprint methodology,
    designed to work seamlessly with AI coding agents.

    \b
    Common commands:
      stride init          Initialize Stride in current directory
      stride create        Create a new sprint
      stride list          List all sprints
      stride status        Show sprint status
      stride move          Move sprint to different status
    
    Use 'stride COMMAND --help' for more information on a command.
    """
    ctx.ensure_object(dict)
    
    # Set project_root if not already set (for testing)
    if "project_root" not in ctx.obj:
        ctx.obj["project_root"] = Path.cwd()
    
    ctx.obj["verbose"] = verbose
    ctx.obj["quiet"] = quiet
    
    # Initialize managers if not already initialized (for testing)
    if "folder_manager" not in ctx.obj:
        ctx.obj["folder_manager"] = FolderManager(ctx.obj["project_root"])
    if "sprint_manager" not in ctx.obj:
        ctx.obj["sprint_manager"] = SprintManager(ctx.obj["folder_manager"])


@cli.command()
@click.pass_context
def version(ctx: click.Context) -> None:
    """Display Stride version information."""
    if not ctx.obj.get("quiet"):
        if RICH_AVAILABLE:
            rprint(f"[bold cyan]Stride[/bold cyan] version [bold]{__version__}[/bold]")
            rprint("[dim]Sprint-Powered, Spec-Driven Development for AI Agents[/dim]")
        else:
            click.echo(f"Stride version {__version__}")
            click.echo("Sprint-Powered, Spec-Driven Development for AI Agents")


@cli.command()
@click.option("--name", "-n", help="Project name")
@click.option("--force", "-f", is_flag=True, help="Force initialization even if Stride already exists")
@click.pass_context
def init(ctx: click.Context, name: Optional[str], force: bool) -> None:
    """
    Initialize Stride in the current directory.
    
    Creates the necessary folder structure:
      - stride/sprints/proposed/
      - stride/sprints/active/
      - stride/sprints/blocked/
      - stride/sprints/review/
      - stride/sprints/completed/
      - stride/specs/
      - stride/introspection/
    
    Example:
      stride init --name "My Project"
    """
    fm: FolderManager = ctx.obj["folder_manager"]
    quiet = ctx.obj.get("quiet", False)
    
    # Check if already initialized
    if fm.stride_root.exists() and not force:
        click.echo("❌ Stride is already initialized in this directory.", err=True)
        click.echo("   Use --force to reinitialize.", err=True)
        sys.exit(1)
    
    # Create structure
    try:
        fm.ensure_structure()
        
        if not quiet:
            if RICH_AVAILABLE:
                rprint(f"[bold green]✓[/bold green] Stride initialized in {fm.project_root}")
                rprint("\n[bold]Created directories:[/bold]")
                rprint("  📁 stride/sprints/proposed/")
                rprint("  📁 stride/sprints/active/")
                rprint("  📁 stride/sprints/blocked/")
                rprint("  📁 stride/sprints/review/")
                rprint("  📁 stride/sprints/completed/")
                rprint("  📁 stride/specs/")
                rprint("  📁 stride/introspection/")
                rprint("\n[dim]Ready to create your first sprint with:[/dim]")
                rprint("  stride create")
            else:
                click.echo(f"✓ Stride initialized in {fm.project_root}")
                click.echo("\nCreated directories:")
                click.echo("  📁 stride/sprints/proposed/")
                click.echo("  📁 stride/sprints/active/")
                click.echo("  📁 stride/sprints/blocked/")
                click.echo("  📁 stride/sprints/review/")
                click.echo("  📁 stride/sprints/completed/")
                click.echo("  📁 stride/specs/")
                click.echo("  📁 stride/introspection/")
                click.echo("\nReady to create your first sprint with:")
                click.echo("  stride create")
                
    except Exception as e:
        click.echo(f"❌ Failed to initialize Stride: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option("--id", "sprint_id", help="Sprint ID (auto-generated if not provided)")
@click.option("--title", "-t", required=True, help="Sprint title")
@click.option("--description", "-d", default="", help="Sprint description")
@click.option("--author", "-a", help="Author email")
@click.option("--priority", "-p", type=click.Choice(["low", "medium", "high", "critical"]), default="medium", help="Priority level")
@click.option("--tags", help="Comma-separated tags")
@click.pass_context
def create(ctx: click.Context, sprint_id: Optional[str], title: str, description: str, 
          author: Optional[str], priority: str, tags: Optional[str]) -> None:
    """
    Create a new sprint in the PROPOSED status.
    
    The sprint will be created with a unique ID (auto-generated or provided),
    and a proposal.md file will be generated with metadata.
    
    Examples:
      stride create --title "Add user authentication"
      stride create --id SPRINT-AUTH --title "Auth System" --priority high
      stride create -t "Bug fixes" -d "Fix critical bugs" --tags "bugfix,urgent"
    """
    sm: SprintManager = ctx.obj["sprint_manager"]
    quiet = ctx.obj.get("quiet", False)
    
    # Validate or generate sprint ID
    if sprint_id:
        if not validate_sprint_id(sprint_id):
            click.echo(f"❌ Invalid sprint ID format: {sprint_id}", err=True)
            click.echo("   Sprint IDs must match: SPRINT-XXXX (uppercase letters/numbers)", err=True)
            sys.exit(1)
    else:
        sprint_id = generate_sprint_id()
    
    # Parse tags
    tag_list = [t.strip() for t in tags.split(",")] if tags else []
    
    # Get author from git config if not provided
    if not author:
        try:
            import subprocess
            result = subprocess.run(
                ["git", "config", "user.email"],
                capture_output=True,
                text=True,
                check=False
            )
            if result.returncode == 0:
                author = result.stdout.strip()
        except Exception:
            pass
    
    if not author:
        author = "unknown@example.com"
    
    # Create sprint
    try:
        sprint_path = sm.create_sprint(
            sprint_id=sprint_id,
            title=title,
            description=description,
            author=author,
            status=SprintStatus.PROPOSED,
            tags=tag_list,
            priority=priority
        )
        
        if not quiet:
            if RICH_AVAILABLE:
                rprint(f"[bold green]✓[/bold green] Created sprint [bold cyan]{sprint_id}[/bold cyan]")
                rprint(f"  📝 Title: {title}")
                rprint(f"  👤 Author: {author}")
                rprint(f"  🏷️  Priority: {priority}")
                if tag_list:
                    rprint(f"  🔖 Tags: {', '.join(tag_list)}")
                rprint(f"\n  📁 Location: {sprint_path}")
                rprint(f"\n[dim]Next steps:[/dim]")
                rprint(f"  stride move {sprint_id} active")
            else:
                click.echo(f"✓ Created sprint {sprint_id}")
                click.echo(f"  📝 Title: {title}")
                click.echo(f"  👤 Author: {author}")
                click.echo(f"  🏷️  Priority: {priority}")
                if tag_list:
                    click.echo(f"  🔖 Tags: {', '.join(tag_list)}")
                click.echo(f"\n  📁 Location: {sprint_path}")
                click.echo(f"\nNext steps:")
                click.echo(f"  stride move {sprint_id} active")
        else:
            click.echo(sprint_id)
            
    except Exception as e:
        click.echo(f"❌ Failed to create sprint: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option("--status", "-s", type=click.Choice(["proposed", "active", "blocked", "review", "completed"]), help="Filter by status")
@click.option("--format", "-f", type=click.Choice(["table", "list", "json"]), default="table", help="Output format")
@click.pass_context
def list(ctx: click.Context, status: Optional[str], format: str) -> None:
    """
    List all sprints or sprints in a specific status.
    
    By default, shows all sprints across all statuses in a table format.
    
    Examples:
      stride list
      stride list --status active
      stride list --status proposed --format list
      stride list --format json
    """
    sm: SprintManager = ctx.obj["sprint_manager"]
    fm: FolderManager = ctx.obj["folder_manager"]
    quiet = ctx.obj.get("quiet", False)
    
    # Get sprints
    if status:
        try:
            sprint_status = SprintStatus(status)
            sprint_ids = fm.list_sprints_by_status(sprint_status)
            sprints = []
            for sid in sprint_ids:
                sprint_info = sm.get_sprint(sid)
                if sprint_info:
                    sprints.append(sprint_info)
        except ValueError:
            click.echo(f"❌ Invalid status: {status}", err=True)
            sys.exit(1)
    else:
        sprints = sm.list_all_sprints()
    
    if not sprints:
        if not quiet:
            click.echo("No sprints found.")
        return
    
    # Output based on format
    if format == "json":
        import json
        output = []
        for sprint in sprints:
            output.append({
                "id": sprint["id"],
                "status": sprint["status"].value if hasattr(sprint["status"], "value") else sprint["status"],
                "title": sprint["metadata"].get("title", "N/A") if sprint["metadata"] else "N/A",
                "author": sprint["metadata"].get("author", "N/A") if sprint["metadata"] else "N/A",
                "priority": sprint["metadata"].get("priority", "N/A") if sprint["metadata"] else "N/A",
            })
        click.echo(json.dumps(output, indent=2))
        
    elif format == "list":
        for sprint in sprints:
            status_str = sprint["status"].value if hasattr(sprint["status"], "value") else sprint["status"]
            title = sprint["metadata"].get("title", "N/A") if sprint["metadata"] else "N/A"
            click.echo(f"{sprint['id']} [{status_str}] - {title}")
            
    else:  # table format
        if RICH_AVAILABLE and console:
            table = Table(title=f"Sprints ({len(sprints)} total)")
            table.add_column("ID", style="cyan", no_wrap=True)
            table.add_column("Status", style="magenta")
            table.add_column("Title", style="white")
            table.add_column("Author", style="dim")
            table.add_column("Priority", style="yellow")
            
            for sprint in sprints:
                status_str = sprint["status"].value if hasattr(sprint["status"], "value") else sprint["status"]
                meta = sprint["metadata"] or {}
                table.add_row(
                    sprint["id"],
                    status_str,
                    meta.get("title", "N/A"),
                    meta.get("author", "N/A"),
                    meta.get("priority", "N/A")
                )
            
            console.print(table)
        else:
            # Fallback ASCII table
            click.echo(f"{'ID':<15} {'Status':<12} {'Title':<30} {'Author':<25} {'Priority':<10}")
            click.echo("-" * 95)
            for sprint in sprints:
                status_str = sprint["status"].value if hasattr(sprint["status"], "value") else sprint["status"]
                meta = sprint["metadata"] or {}
                click.echo(
                    f"{sprint['id']:<15} {status_str:<12} "
                    f"{meta.get('title', 'N/A')[:30]:<30} "
                    f"{meta.get('author', 'N/A')[:25]:<25} "
                    f"{meta.get('priority', 'N/A'):<10}"
                )


@cli.command()
@click.argument("sprint_id")
@click.pass_context
def status(ctx: click.Context, sprint_id: str) -> None:
    """
    Show detailed status of a sprint.
    
    Displays complete information including metadata, location, and validation status.
    
    Example:
      stride status SPRINT-A1B2
    """
    sm: SprintManager = ctx.obj["sprint_manager"]
    quiet = ctx.obj.get("quiet", False)
    
    # Get sprint info
    sprint_info = sm.get_sprint(sprint_id)
    
    if not sprint_info:
        click.echo(f"❌ Sprint not found: {sprint_id}", err=True)
        sys.exit(1)
    
    meta = sprint_info["metadata"] or {}
    status_val = sprint_info["status"].value if hasattr(sprint_info["status"], "value") else sprint_info["status"]
    
    # Validate sprint
    is_valid, errors = sm.validate_sprint(sprint_id)
    
    if not quiet:
        if RICH_AVAILABLE:
            rprint(f"\n[bold cyan]{sprint_id}[/bold cyan]")
            rprint(f"[bold]Title:[/bold] {meta.get('title', 'N/A')}")
            rprint(f"[bold]Status:[/bold] {status_val}")
            rprint(f"[bold]Author:[/bold] {meta.get('author', 'N/A')}")
            rprint(f"[bold]Priority:[/bold] {meta.get('priority', 'N/A')}")
            
            if meta.get('tags'):
                rprint(f"[bold]Tags:[/bold] {', '.join(meta['tags'])}")
            
            rprint(f"\n[bold]Created:[/bold] {meta.get('created', 'N/A')}")
            rprint(f"[bold]Updated:[/bold] {meta.get('updated', 'N/A')}")
            rprint(f"\n[bold]Location:[/bold] {sprint_info['path']}")
            
            if is_valid:
                rprint(f"\n[bold green]✓ Valid[/bold green]")
            else:
                rprint(f"\n[bold red]✗ Invalid[/bold red]")
                for error in errors:
                    rprint(f"  [red]• {error}[/red]")
        else:
            click.echo(f"\n{sprint_id}")
            click.echo(f"Title: {meta.get('title', 'N/A')}")
            click.echo(f"Status: {status_val}")
            click.echo(f"Author: {meta.get('author', 'N/A')}")
            click.echo(f"Priority: {meta.get('priority', 'N/A')}")
            
            if meta.get('tags'):
                click.echo(f"Tags: {', '.join(meta['tags'])}")
            
            click.echo(f"\nCreated: {meta.get('created', 'N/A')}")
            click.echo(f"Updated: {meta.get('updated', 'N/A')}")
            click.echo(f"\nLocation: {sprint_info['path']}")
            
            if is_valid:
                click.echo(f"\n✓ Valid")
            else:
                click.echo(f"\n✗ Invalid")
                for error in errors:
                    click.echo(f"  • {error}")


@cli.command()
@click.argument("sprint_id")
@click.argument("to_status", type=click.Choice(["proposed", "active", "blocked", "review", "completed"]))
@click.option("--reason", "-r", help="Reason for move (especially for blocked status)")
@click.pass_context
def move(ctx: click.Context, sprint_id: str, to_status: str, reason: Optional[str]) -> None:
    """
    Move a sprint to a different status.
    
    Updates both the folder location and metadata.
    
    Examples:
      stride move SPRINT-A1B2 active
      stride move SPRINT-A1B2 blocked --reason "Waiting for API approval"
      stride move SPRINT-A1B2 completed
    """
    sm: SprintManager = ctx.obj["sprint_manager"]
    quiet = ctx.obj.get("quiet", False)
    
    try:
        status_enum = SprintStatus(to_status)
    except ValueError:
        click.echo(f"❌ Invalid status: {to_status}", err=True)
        sys.exit(1)
    
    # Move sprint
    success = sm.move_sprint_status(sprint_id, status_enum, reason)
    
    if not success:
        click.echo(f"❌ Failed to move sprint {sprint_id}", err=True)
        click.echo("   Sprint may not exist or move operation failed.", err=True)
        sys.exit(1)
    
    if not quiet:
        if RICH_AVAILABLE:
            rprint(f"[bold green]✓[/bold green] Moved [bold cyan]{sprint_id}[/bold cyan] to [bold magenta]{to_status}[/bold magenta]")
            if reason:
                rprint(f"  💬 Reason: {reason}")
        else:
            click.echo(f"✓ Moved {sprint_id} to {to_status}")
            if reason:
                click.echo(f"  💬 Reason: {reason}")


@cli.command()
@click.argument("sprint_id", required=False)
@click.option("--all", "validate_all", is_flag=True, help="Validate all sprints")
@click.option("--status", "-s", type=click.Choice(["proposed", "active", "blocked", "review", "completed"]), help="Validate sprints in specific status")
@click.option("--strict", is_flag=True, help="Enable strict validation")
@click.pass_context
def validate(ctx: click.Context, sprint_id: Optional[str], validate_all: bool, status: Optional[str], strict: bool) -> None:
    """
    Validate sprint structure and metadata.
    
    Can validate a single sprint, all sprints, or sprints in a specific status.
    
    Examples:
      stride validate SPRINT-A1B2
      stride validate --all
      stride validate --status active
      stride validate --all --strict
    """
    sm: SprintManager = ctx.obj["sprint_manager"]
    fm: FolderManager = ctx.obj["folder_manager"]
    quiet = ctx.obj.get("quiet", False)
    
    sprints_to_validate = []
    
    if sprint_id:
        sprints_to_validate = [sprint_id]
    elif validate_all:
        all_sprints = sm.list_all_sprints()
        sprints_to_validate = [s["id"] for s in all_sprints]
    elif status:
        try:
            status_enum = SprintStatus(status)
            sprints_to_validate = fm.list_sprints_by_status(status_enum)
        except ValueError:
            click.echo(f"❌ Invalid status: {status}", err=True)
            sys.exit(1)
    else:
        click.echo("❌ Please specify a sprint ID, --all, or --status", err=True)
        click.echo("   Use 'stride validate --help' for more information", err=True)
        sys.exit(1)
    
    if not sprints_to_validate:
        if not quiet:
            click.echo("No sprints to validate.")
        return
    
    # Validate sprints
    results = []
    for sid in sprints_to_validate:
        is_valid, errors = sm.validate_sprint(sid, strict=strict)
        results.append((sid, is_valid, errors))
    
    # Report results
    valid_count = sum(1 for _, is_valid, _ in results if is_valid)
    invalid_count = len(results) - valid_count
    
    if not quiet:
        if RICH_AVAILABLE:
            for sid, is_valid, errors in results:
                if is_valid:
                    rprint(f"[green]✓[/green] {sid}")
                else:
                    rprint(f"[red]✗[/red] {sid}")
                    for error in errors:
                        rprint(f"    [dim red]• {error}[/dim red]")
            
            rprint(f"\n[bold]Summary:[/bold] {valid_count} valid, {invalid_count} invalid")
        else:
            for sid, is_valid, errors in results:
                if is_valid:
                    click.echo(f"✓ {sid}")
                else:
                    click.echo(f"✗ {sid}")
                    for error in errors:
                        click.echo(f"    • {error}")
            
            click.echo(f"\nSummary: {valid_count} valid, {invalid_count} invalid")
    
    # Exit with error if any invalid
    if invalid_count > 0:
        sys.exit(1)


@cli.command()
@click.argument("sprint_id", required=False)
@click.option("--all", "archive_all", is_flag=True, help="Archive all sprints in a status")
@click.option("--status", "-s", type=click.Choice(["proposed", "active", "blocked", "review", "completed"]), help="Archive all sprints in this status")
@click.option("--yes", "-y", is_flag=True, help="Skip confirmation prompt")
@click.pass_context
def archive(ctx: click.Context, sprint_id: Optional[str], archive_all: bool, status: Optional[str], yes: bool) -> None:
    """
    Archive (soft-delete) a sprint or multiple sprints.
    
    Archived sprints are moved to .archive/ folder and can be restored later.
    
    Examples:
      stride archive SPRINT-A1B2
      stride archive --status completed --yes
      stride archive --all --status proposed
    """
    fm: FolderManager = ctx.obj["folder_manager"]
    sm: SprintManager = ctx.obj["sprint_manager"]
    quiet = ctx.obj.get("quiet", False)
    
    sprints_to_archive = []
    
    if sprint_id:
        # Find sprint's current status
        result = fm.find_sprint(sprint_id)
        if not result:
            click.echo(f"❌ Sprint not found: {sprint_id}", err=True)
            sys.exit(1)
        _, sprint_status = result
        sprints_to_archive = [(sprint_id, sprint_status)]
    elif archive_all and status:
        try:
            status_enum = SprintStatus(status)
            sprint_ids = fm.list_sprints_by_status(status_enum)
            sprints_to_archive = [(sid, status_enum) for sid in sprint_ids]
        except ValueError:
            click.echo(f"❌ Invalid status: {status}", err=True)
            sys.exit(1)
    else:
        click.echo("❌ Please specify a sprint ID or --all with --status", err=True)
        click.echo("   Use 'stride archive --help' for more information", err=True)
        sys.exit(1)
    
    if not sprints_to_archive:
        if not quiet:
            click.echo("No sprints to archive.")
        return
    
    # Confirmation prompt
    if not yes:
        count = len(sprints_to_archive)
        if count == 1:
            message = f"Archive sprint {sprints_to_archive[0][0]}?"
        else:
            message = f"Archive {count} sprints?"
        
        if not click.confirm(message):
            click.echo("Cancelled.")
            return
    
    # Archive sprints
    archived_count = 0
    for sid, sprint_status in sprints_to_archive:
        try:
            fm.archive_sprint(sid, sprint_status)
            archived_count += 1
            if not quiet:
                if RICH_AVAILABLE:
                    rprint(f"[green]✓[/green] Archived {sid}")
                else:
                    click.echo(f"✓ Archived {sid}")
        except Exception as e:
            click.echo(f"❌ Failed to archive {sid}: {e}", err=True)
    
    if not quiet:
        click.echo(f"\nArchived {archived_count} sprint(s)")


@cli.command()
@click.argument("sprint_id")
@click.argument("to_status", type=click.Choice(["proposed", "active", "blocked", "review", "completed"]))
@click.pass_context
def restore(ctx: click.Context, sprint_id: str, to_status: str) -> None:
    """
    Restore an archived sprint to a status folder.
    
    The sprint must exist in the .archive/ folder.
    
    Examples:
      stride restore SPRINT-A1B2 proposed
      stride restore SPRINT-A1B2 active
    """
    fm: FolderManager = ctx.obj["folder_manager"]
    quiet = ctx.obj.get("quiet", False)
    
    try:
        status_enum = SprintStatus(to_status)
    except ValueError:
        click.echo(f"❌ Invalid status: {to_status}", err=True)
        sys.exit(1)
    
    # Restore sprint
    try:
        restored_path = fm.restore_sprint(sprint_id, status_enum)
        
        if not quiet:
            if RICH_AVAILABLE:
                rprint(f"[bold green]✓[/bold green] Restored [bold cyan]{sprint_id}[/bold cyan] to [bold magenta]{to_status}[/bold magenta]")
                rprint(f"  📁 Location: {restored_path}")
            else:
                click.echo(f"✓ Restored {sprint_id} to {to_status}")
                click.echo(f"  📁 Location: {restored_path}")
    except FileNotFoundError as e:
        click.echo(f"❌ {e}", err=True)
        sys.exit(1)
    except FileExistsError as e:
        click.echo(f"❌ {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"❌ Failed to restore sprint: {e}", err=True)
        sys.exit(1)


@cli.group()
@click.pass_context
def config(ctx: click.Context) -> None:
    """
    Manage Stride configuration settings.
    
    Configure user preferences, project settings, and AI agent configurations.
    Supports both user-level (~/.stride/config.yaml) and project-level (stride.config.yaml) settings.
    
    \b
    Examples:
      stride config get user.name
      stride config set user.email "dev@example.com"
      stride config list --user
      stride config init --project
      stride config validate
      stride config reset --user
    """
    pass


@config.command("get")
@click.argument("key", required=False)
@click.option("--user", "-u", is_flag=True, help="Get from user configuration only")
@click.option("--project", "-p", is_flag=True, help="Get from project configuration only")
@click.option("--format", "-f", "output_format", type=click.Choice(["text", "json"]), default="text", help="Output format")
@click.pass_context
def config_get(ctx: click.Context, key: Optional[str], user: bool, project: bool, output_format: str) -> None:
    """
    Get configuration value(s).
    
    If KEY is provided, retrieves that specific configuration value using dot notation.
    If KEY is omitted, displays all configuration values.
    
    \b
    Examples:
      stride config get user.name
      stride config get project.agents
      stride config get --user
      stride config get --format json
    """
    quiet = ctx.parent.parent.params.get("quiet", False)
    config_manager = ConfigManager()
    
    try:
        if user and project:
            click.echo("❌ Cannot specify both --user and --project", err=True)
            sys.exit(1)
        
        # Determine which config to use
        if user:
            config_data = config_manager.get_user_config()
        elif project:
            config_data = config_manager.get_project_config()
        else:
            config_data = config_manager.get_merged_config()
        
        # Get specific key or full config
        if key:
            value = config_manager.get_value(key, config=config_data)
            if value is None:
                click.echo(f"❌ Configuration key '{key}' not found", err=True)
                sys.exit(1)
            
            if output_format == "json":
                click.echo(json.dumps(value, indent=2))
            else:
                if isinstance(value, (builtins.dict, builtins.list)):
                    click.echo(json.dumps(value, indent=2))
                else:
                    click.echo(value)
        else:
            # Show all config
            if output_format == "json":
                click.echo(json.dumps(config_data, indent=2))
            else:
                if RICH_AVAILABLE and not quiet:
                    _print_config_tree(config_data, "Configuration")
                else:
                    click.echo(json.dumps(config_data, indent=2))
    
    except ConfigError as e:
        click.echo(f"❌ {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"❌ Failed to get configuration: {e}", err=True)
        sys.exit(1)


@config.command("set")
@click.argument("key")
@click.argument("value")
@click.option("--user", "-u", is_flag=True, help="Set in user configuration")
@click.option("--project", "-p", is_flag=True, help="Set in project configuration")
@click.option("--json", "-j", "is_json", is_flag=True, help="Parse value as JSON")
@click.pass_context
def config_set(ctx: click.Context, key: str, value: str, user: bool, project: bool, is_json: bool) -> None:
    """
    Set a configuration value.
    
    Sets a configuration value using dot notation for nested keys.
    By default, sets in project configuration if it exists, otherwise user configuration.
    
    \b
    Examples:
      stride config set user.name "John Doe"
      stride config set user.email "john@example.com"
      stride config set project.name "MyProject" --project
      stride config set defaults.tags '["bug", "feature"]' --json --user
    """
    quiet = ctx.parent.parent.params.get("quiet", False)
    config_manager = ConfigManager()
    
    try:
        if user and project:
            click.echo("❌ Cannot specify both --user and --project", err=True)
            sys.exit(1)
        
        # Parse value if JSON flag is set
        parsed_value = value
        if is_json:
            try:
                parsed_value = json.loads(value)
            except json.JSONDecodeError as e:
                click.echo(f"❌ Invalid JSON: {e}", err=True)
                sys.exit(1)
        
        # Determine which config to update
        config_type = None
        if user:
            config_type = "user"
        elif project:
            config_type = "project"
        else:
            # Default to project if it exists, otherwise user
            project_config_path = Path.cwd() / "stride.config.yaml"
            config_type = "project" if project_config_path.exists() else "user"
        
        # Set the value
        config_manager.set_value(key, parsed_value, config_type)
        
        if not quiet:
            if RICH_AVAILABLE:
                rprint(f"[bold green]✓[/bold green] Set [bold cyan]{key}[/bold cyan] = [bold yellow]{parsed_value}[/bold yellow]")
                rprint(f"  📁 Configuration: {config_type}")
            else:
                click.echo(f"✓ Set {key} = {parsed_value}")
                click.echo(f"  📁 Configuration: {config_type}")
    
    except ConfigError as e:
        click.echo(f"❌ {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"❌ Failed to set configuration: {e}", err=True)
        sys.exit(1)


@config.command("list")
@click.option("--user", "-u", is_flag=True, help="List user configuration only")
@click.option("--project", "-p", is_flag=True, help="List project configuration only")
@click.option("--format", "-f", "output_format", type=click.Choice(["table", "json"]), default="table", help="Output format")
@click.pass_context
def config_list(ctx: click.Context, user: bool, project: bool, output_format: str) -> None:
    """
    List all configuration settings.
    
    Displays all configuration keys and values in a readable format.
    Use --user or --project to filter specific configuration levels.
    
    \b
    Examples:
      stride config list
      stride config list --user
      stride config list --format json
    """
    quiet = ctx.parent.parent.params.get("quiet", False)
    config_manager = ConfigManager()
    
    try:
        if user and project:
            click.echo("❌ Cannot specify both --user and --project", err=True)
            sys.exit(1)
        
        # Determine which config to list
        if user:
            config_data = config_manager.get_user_config()
            config_label = "User Configuration"
        elif project:
            config_data = config_manager.get_project_config()
            config_label = "Project Configuration"
        else:
            config_data = config_manager.get_merged_config()
            config_label = "Merged Configuration"
        
        if output_format == "json":
            click.echo(json.dumps(config_data, indent=2))
        else:
            if RICH_AVAILABLE and not quiet:
                _print_config_tree(config_data, config_label)
            else:
                click.echo(f"=== {config_label} ===")
                click.echo(json.dumps(config_data, indent=2))
    
    except ConfigError as e:
        click.echo(f"❌ {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"❌ Failed to list configuration: {e}", err=True)
        sys.exit(1)


@config.command("init")
@click.option("--user", "-u", is_flag=True, help="Initialize user configuration")
@click.option("--project", "-p", is_flag=True, help="Initialize project configuration")
@click.option("--name", help="Project name (for project config)")
@click.option("--force", is_flag=True, help="Overwrite existing configuration")
@click.pass_context
def config_init(ctx: click.Context, user: bool, project: bool, name: Optional[str], force: bool) -> None:
    """
    Initialize configuration files.
    
    Creates default configuration files with sensible defaults.
    Use --user for ~/.stride/config.yaml or --project for stride.config.yaml.
    
    \b
    Examples:
      stride config init --user
      stride config init --project --name "MyProject"
      stride config init --project --force
    """
    quiet = ctx.parent.parent.params.get("quiet", False)
    config_manager = ConfigManager()
    
    try:
        if not user and not project:
            click.echo("❌ Must specify either --user or --project", err=True)
            sys.exit(1)
        
        if user and project:
            click.echo("❌ Cannot specify both --user and --project", err=True)
            sys.exit(1)
        
        if user:
            config_path = config_manager.user_config_path
            if config_path.exists() and not force:
                click.echo(f"❌ User configuration already exists at {config_path}", err=True)
                click.echo("   Use --force to overwrite", err=True)
                sys.exit(1)
            
            if force and config_path.exists():
                config_path.unlink()
            
            config_manager.init_user_config()
            
            if not quiet:
                if RICH_AVAILABLE:
                    rprint(f"[bold green]✓[/bold green] Initialized user configuration")
                    rprint(f"  📁 Location: {config_path}")
                else:
                    click.echo(f"✓ Initialized user configuration")
                    click.echo(f"  📁 Location: {config_path}")
        
        elif project:
            config_path = config_manager.project_config_path
            if config_path.exists() and not force:
                click.echo(f"❌ Project configuration already exists at {config_path}", err=True)
                click.echo("   Use --force to overwrite", err=True)
                sys.exit(1)
            
            if force and config_path.exists():
                config_path.unlink()
            
            kwargs = {}
            if name:
                kwargs["project_name"] = name
            
            config_manager.init_project_config(**kwargs)
            
            if not quiet:
                if RICH_AVAILABLE:
                    rprint(f"[bold green]✓[/bold green] Initialized project configuration")
                    rprint(f"  📁 Location: {config_path}")
                else:
                    click.echo(f"✓ Initialized project configuration")
                    click.echo(f"  📁 Location: {config_path}")
    
    except ConfigError as e:
        click.echo(f"❌ {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"❌ Failed to initialize configuration: {e}", err=True)
        sys.exit(1)


@config.command("validate")
@click.option("--user", "-u", is_flag=True, help="Validate user configuration only")
@click.option("--project", "-p", is_flag=True, help="Validate project configuration only")
@click.option("--strict", is_flag=True, help="Enable strict validation mode")
@click.pass_context
def config_validate(ctx: click.Context, user: bool, project: bool, strict: bool) -> None:
    """
    Validate configuration files.
    
    Checks configuration files against schemas to ensure they are valid.
    Reports any errors or warnings found.
    
    \b
    Examples:
      stride config validate
      stride config validate --user
      stride config validate --project --strict
    """
    quiet = ctx.parent.parent.params.get("quiet", False)
    config_manager = ConfigManager()
    
    try:
        from stride.core.config_schemas import USER_CONFIG_SCHEMA, PROJECT_CONFIG_SCHEMA
        
        errors = []
        
        # Validate user config
        if user or not project:
            try:
                user_config = config_manager.get_user_config()
                config_manager.validate_config(user_config, USER_CONFIG_SCHEMA, strict=strict)
                if not quiet:
                    if RICH_AVAILABLE:
                        rprint(f"[bold green]✓[/bold green] User configuration is valid")
                    else:
                        click.echo("✓ User configuration is valid")
            except ConfigValidationError as e:
                errors.append(f"User configuration: {e}")
            except FileNotFoundError:
                if not quiet:
                    click.echo("⚠ User configuration not found (this is optional)")
        
        # Validate project config
        if project or not user:
            try:
                project_config = config_manager.get_project_config()
                config_manager.validate_config(project_config, PROJECT_CONFIG_SCHEMA, strict=strict)
                if not quiet:
                    if RICH_AVAILABLE:
                        rprint(f"[bold green]✓[/bold green] Project configuration is valid")
                    else:
                        click.echo("✓ Project configuration is valid")
            except ConfigValidationError as e:
                errors.append(f"Project configuration: {e}")
            except FileNotFoundError:
                if not quiet:
                    click.echo("⚠ Project configuration not found (this is optional)")
        
        if errors:
            click.echo("❌ Configuration validation failed:", err=True)
            for error in errors:
                click.echo(f"   - {error}", err=True)
            sys.exit(1)
    
    except Exception as e:
        click.echo(f"❌ Failed to validate configuration: {e}", err=True)
        sys.exit(1)


@config.command("reset")
@click.option("--user", "-u", is_flag=True, help="Reset user configuration")
@click.option("--project", "-p", is_flag=True, help="Reset project configuration")
@click.option("--force", is_flag=True, help="Skip confirmation prompt")
@click.pass_context
def config_reset(ctx: click.Context, user: bool, project: bool, force: bool) -> None:
    """
    Reset configuration to defaults.
    
    Restores configuration files to their default values.
    This action cannot be undone without a backup.
    
    \b
    Examples:
      stride config reset --user
      stride config reset --project --force
    """
    quiet = ctx.parent.parent.params.get("quiet", False)
    config_manager = ConfigManager()
    
    try:
        if not user and not project:
            click.echo("❌ Must specify either --user or --project", err=True)
            sys.exit(1)
        
        if user and project:
            click.echo("❌ Cannot specify both --user and --project", err=True)
            sys.exit(1)
        
        config_type = "user" if user else "project"
        config_path = config_manager.user_config_path if user else config_manager.project_config_path
        
        # Confirmation prompt
        if not force:
            if RICH_AVAILABLE:
                rprint(f"[bold yellow]⚠[/bold yellow] This will reset {config_type} configuration to defaults")
                rprint(f"  📁 Location: {config_path}")
            else:
                click.echo(f"⚠ This will reset {config_type} configuration to defaults")
                click.echo(f"  📁 Location: {config_path}")
            
            if not click.confirm("Do you want to continue?"):
                click.echo("Cancelled.")
                return
        
        # Reset the configuration
        config_manager.reset_config(config_type)
        
        if not quiet:
            if RICH_AVAILABLE:
                rprint(f"[bold green]✓[/bold green] Reset {config_type} configuration to defaults")
            else:
                click.echo(f"✓ Reset {config_type} configuration to defaults")
    
    except ConfigError as e:
        click.echo(f"❌ {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"❌ Failed to reset configuration: {e}", err=True)
        sys.exit(1)


def _print_config_tree(config: dict, title: str, indent: int = 0) -> None:
    """Helper function to print configuration as a tree using Rich."""
    if not RICH_AVAILABLE:
        return
    
    if indent == 0:
        rprint(f"\n[bold cyan]=== {title} ===[/bold cyan]\n")
    
    for key, value in config.items():
        prefix = "  " * indent
        if isinstance(value, dict):
            rprint(f"{prefix}[bold yellow]{key}:[/bold yellow]")
            _print_config_tree(value, title, indent + 1)
        elif isinstance(value, list):
            rprint(f"{prefix}[bold yellow]{key}:[/bold yellow] [dim]{value}[/dim]")
        else:
            rprint(f"{prefix}[bold yellow]{key}:[/bold yellow] {value}")


if __name__ == "__main__":
    cli()
