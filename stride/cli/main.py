"""
Main CLI entry point for Stride.
"""
import click
import sys
import json
import time
from pathlib import Path
from typing import Optional

from stride import __version__
from stride.core.folder_manager import FolderManager, SprintStatus
from stride.core.sprint_manager import SprintManager
from stride.core.metadata_manager import MetadataManager
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


# Helper functions for dashboard display
def _calculate_sprint_age(created_str: str) -> int:
    """Calculate days since sprint creation."""
    from datetime import datetime, timezone
    try:
        # Handle both Z suffix and +00:00 suffix
        created_str = created_str.replace("Z", "+00:00")
        created = datetime.fromisoformat(created_str)
        now = datetime.now(timezone.utc)
        return (now - created).days
    except (ValueError, AttributeError):
        return 0


def _get_status_emoji(status: str) -> str:
    """Get emoji for sprint status."""
    status_map = {
        "proposed": "📝",
        "active": "🚀",
        "blocked": "🚫",
        "review": "👀",
        "completed": "✅"
    }
    return status_map.get(status, "❓")


def _get_status_color(status: str) -> str:
    """Get Rich color for sprint status."""
    color_map = {
        "proposed": "yellow",
        "active": "blue",
        "blocked": "red",
        "review": "magenta",
        "completed": "green"
    }
    return color_map.get(status, "white")


def _get_priority_emoji(priority: str) -> str:
    """Get emoji for priority level."""
    priority_map = {
        "critical": "🔥",
        "high": "⚡",
        "medium": "⭐",
        "low": "💤"
    }
    return priority_map.get(priority, "⭐")


def _display_dashboard(sprints: list, detailed: bool, team: bool, quiet: bool) -> None:
    """Display enhanced visual dashboard with sprint analytics."""
    from datetime import datetime
    from collections import Counter
    
    if RICH_AVAILABLE:
        from rich.panel import Panel
        from rich.progress import Progress, BarColumn, TextColumn
        from rich.layout import Layout
        from rich.text import Text
        
        # Calculate statistics
        total = len(sprints)
        status_counts = Counter()
        priority_counts = Counter()
        author_counts = Counter()
        oldest_sprint = None
        oldest_age = 0
        blocked_sprints = []
        
        for sprint in sprints:
            status_str = sprint["status"].value if hasattr(sprint["status"], "value") else sprint["status"]
            meta = sprint["metadata"] or {}
            
            status_counts[status_str] += 1
            priority_counts[meta.get("priority", "medium")] += 1
            
            if meta.get("author"):
                author_counts[meta["author"]] += 1
            
            # Track oldest sprint
            age = _calculate_sprint_age(meta.get("created", ""))
            if age > oldest_age:
                oldest_age = age
                oldest_sprint = sprint["id"]
            
            # Track blocked sprints
            if status_str == "blocked":
                blocked_sprints.append({
                    "id": sprint["id"],
                    "title": meta.get("title", "N/A"),
                    "age": age,
                    "reason": meta.get("reason", "No reason specified")
                })
        
        # Display header with summary
        rprint(f"\n[bold cyan]{'=' * 60}[/bold cyan]")
        rprint(f"[bold white]📊 Sprint Dashboard[/bold white]")
        rprint(f"[bold cyan]{'=' * 60}[/bold cyan]\n")
        
        # Sprint distribution with progress bars
        rprint("[bold]Sprint Distribution:[/bold]")
        for status_val in ["proposed", "active", "blocked", "review", "completed"]:
            count = status_counts.get(status_val, 0)
            percentage = (count / total * 100) if total > 0 else 0
            emoji = _get_status_emoji(status_val)
            color = _get_status_color(status_val)
            
            # Create visual bar
            bar_length = int(percentage / 2)  # Scale to 50 chars max
            bar = "█" * bar_length
            
            rprint(f"  {emoji} [{color}]{status_val.capitalize():<12}[/{color}] {count:>3} [{color}]{bar}[/{color}] {percentage:>5.1f}%")
        
        # Health metrics
        rprint(f"\n[bold]Health Metrics:[/bold]")
        rprint(f"  📈 Total Sprints: [cyan]{total}[/cyan]")
        rprint(f"  🔥 Active Sprints: [blue]{status_counts.get('active', 0)}[/blue]")
        rprint(f"  ✅ Completed: [green]{status_counts.get('completed', 0)}[/green]")
        rprint(f"  🚫 Blocked: [red]{status_counts.get('blocked', 0)}[/red]")
        
        if oldest_sprint and oldest_age > 0:
            rprint(f"  ⏰ Oldest Sprint: [yellow]{oldest_sprint}[/yellow] ([yellow]{oldest_age} days[/yellow])")
        
        if blocked_sprints:
            rprint(f"\n[bold red]⚠️  Blocked Sprints ({len(blocked_sprints)}):[/bold red]")
            for blocked in blocked_sprints[:3]:  # Show top 3
                rprint(f"    • {blocked['id']}: {blocked['title']}")
                rprint(f"      [dim]Blocked for {blocked['age']} days: {blocked['reason']}[/dim]")
        
        # Team analytics
        if team and author_counts:
            rprint(f"\n[bold]Team Activity:[/bold]")
            for author, count in author_counts.most_common(5):
                percentage = (count / total * 100) if total > 0 else 0
                bar_length = int(percentage / 2)
                bar = "█" * bar_length
                rprint(f"  👤 {author:<30} {count:>3} [cyan]{bar}[/cyan] {percentage:>5.1f}%")
        
        # Detailed sprint list
        if detailed:
            rprint(f"\n[bold]Detailed Sprint List:[/bold]")
            for sprint in sprints:
                status_str = sprint["status"].value if hasattr(sprint["status"], "value") else sprint["status"]
                meta = sprint["metadata"] or {}
                age = _calculate_sprint_age(meta.get("created", ""))
                emoji = _get_status_emoji(status_str)
                color = _get_status_color(status_str)
                priority_emoji = _get_priority_emoji(meta.get("priority", "medium"))
                
                rprint(f"\n  {emoji} [{color}]{sprint['id']}[/{color}] - {meta.get('title', 'N/A')}")
                rprint(f"     Status: [{color}]{status_str}[/{color}] | Priority: {priority_emoji} {meta.get('priority', 'N/A')}")
                rprint(f"     Author: [dim]{meta.get('author', 'N/A')}[/dim] | Age: [yellow]{age} days[/yellow]")
                if meta.get("tags"):
                    rprint(f"     Tags: [cyan]{', '.join(meta['tags'])}[/cyan]")
        
        rprint(f"\n[bold cyan]{'=' * 60}[/bold cyan]\n")
    
    else:
        # Fallback ASCII dashboard
        click.echo("\n" + "=" * 60)
        click.echo("Sprint Dashboard")
        click.echo("=" * 60 + "\n")
        
        # Calculate statistics
        total = len(sprints)
        status_counts = Counter()
        
        for sprint in sprints:
            status_str = sprint["status"].value if hasattr(sprint["status"], "value") else sprint["status"]
            status_counts[status_str] += 1
        
        click.echo("Sprint Distribution:")
        for status_val in ["proposed", "active", "blocked", "review", "completed"]:
            count = status_counts.get(status_val, 0)
            percentage = (count / total * 100) if total > 0 else 0
            emoji = _get_status_emoji(status_val)
            bar_length = int(percentage / 2)
            bar = "#" * bar_length
            click.echo(f"  {emoji} {status_val.capitalize():<12} {count:>3} {bar} {percentage:>5.1f}%")
        
        click.echo(f"\nTotal Sprints: {total}")
        click.echo(f"Active: {status_counts.get('active', 0)}")
        click.echo(f"Completed: {status_counts.get('completed', 0)}")
        click.echo(f"Blocked: {status_counts.get('blocked', 0)}")
        click.echo("\n" + "=" * 60 + "\n")


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
@click.option("--name", "-n", help="Your name")
@click.option("--email", "-e", help="Your email address")
@click.pass_context
def login(ctx: click.Context, name: Optional[str], email: Optional[str]) -> None:
    """
    Set your user identity for sprint authorship.
    
    Stores your name and email in ~/.stride/config.yaml.
    This information is used to track who creates and modifies sprints.
    
    \b
    Examples:
      stride login                               # Interactive mode
      stride login --name "John Doe" --email "john@example.com"
      stride login --email "newemail@example.com"  # Update email only
    """
    from stride.utils.validators import validate_email, validate_name
    
    config_manager = ConfigManager()
    quiet = ctx.obj.get("quiet", False)
    
    # Get current user info
    current_email, current_name = config_manager.get_user_info()
    
    # Interactive mode if no flags provided
    if not name and not email:
        if not quiet:
            if RICH_AVAILABLE:
                rprint("\n[bold cyan]📝 Setup User Identity[/bold cyan]")
                if current_name or current_email:
                    rprint(f"[dim]Current: {current_name or '(no name)'} <{current_email or '(no email)'}>[/dim]\n")
            else:
                click.echo("\n📝 Setup User Identity")
                if current_name or current_email:
                    click.echo(f"Current: {current_name or '(no name)'} <{current_email or '(no email)'}>\n")
        
        # Prompt for name
        name = click.prompt("Name", default=current_name or "", show_default=bool(current_name))
        if not name:
            name = current_name
        
        # Prompt for email
        email = click.prompt("Email", default=current_email or "", show_default=bool(current_email))
        if not email:
            email = current_email
    else:
        # Use current values if not provided
        if not name:
            name = current_name
        if not email:
            email = current_email
    
    # Validate name
    if name:
        is_valid, error = validate_name(name)
        if not is_valid:
            click.echo(f"❌ {error}", err=True)
            sys.exit(1)
    
    # Validate email
    if email:
        is_valid, error = validate_email(email)
        if not is_valid:
            click.echo(f"❌ {error}", err=True)
            sys.exit(1)
    
    # Store credentials
    try:
        user_config = config_manager.get_user_config()
        if "user" not in user_config:
            user_config["user"] = {}
        
        user_config["user"]["name"] = name
        user_config["user"]["email"] = email
        
        config_manager.save_config(config_manager.user_config_path, user_config)
        config_manager._clear_cache()
        
        if not quiet:
            if RICH_AVAILABLE:
                rprint(f"\n[bold green]✓[/bold green] Logged in as [bold]{name}[/bold] ([cyan]{email}[/cyan])")
                rprint(f"  📁 Config: {config_manager.user_config_path}")
            else:
                click.echo(f"\n✓ Logged in as {name} ({email})")
                click.echo(f"  📁 Config: {config_manager.user_config_path}")
    
    except Exception as e:
        click.echo(f"❌ Failed to save credentials: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option("--force", "-f", is_flag=True, help="Skip confirmation prompt")
@click.pass_context
def logout(ctx: click.Context, force: bool) -> None:
    """
    Clear your user identity.
    
    Removes your name and email from ~/.stride/config.yaml.
    
    \b
    Examples:
      stride logout           # With confirmation
      stride logout --force   # Skip confirmation
    """
    config_manager = ConfigManager()
    quiet = ctx.obj.get("quiet", False)
    
    # Check if user is logged in
    if not config_manager.is_user_authenticated():
        click.echo("❌ Not logged in", err=True)
        sys.exit(1)
    
    # Get current user for display
    email, name = config_manager.get_user_info()
    
    # Confirmation prompt
    if not force and not quiet:
        if RICH_AVAILABLE:
            rprint(f"\n[yellow]⚠️  You are currently logged in as:[/yellow]")
            rprint(f"   {name} ({email})")
            rprint()
        else:
            click.echo(f"\n⚠️  You are currently logged in as:")
            click.echo(f"   {name} ({email})\n")
        
        if not click.confirm("Are you sure you want to logout?"):
            click.echo("Cancelled.")
            return
    
    # Clear credentials
    try:
        user_config = config_manager.get_user_config()
        if "user" in user_config:
            user_config["user"]["name"] = None
            user_config["user"]["email"] = None
        
        config_manager.save_config(config_manager.user_config_path, user_config)
        config_manager._clear_cache()
        
        if not quiet:
            if RICH_AVAILABLE:
                rprint("[bold green]✓[/bold green] Logged out successfully")
            else:
                click.echo("✓ Logged out successfully")
    
    except Exception as e:
        click.echo(f"❌ Failed to logout: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.pass_context
def whoami(ctx: click.Context) -> None:
    """
    Display current user identity.
    
    Shows your name, email, and authentication status.
    
    \b
    Example:
      stride whoami
    """
    config_manager = ConfigManager()
    quiet = ctx.obj.get("quiet", False)
    
    if config_manager.is_user_authenticated():
        email, name = config_manager.get_user_info()
        
        if not quiet:
            if RICH_AVAILABLE:
                rprint(f"[bold green]✓[/bold green] Logged in as [bold]{name or '(no name)'}[/bold] ([cyan]{email}[/cyan])")
                rprint(f"  📁 Config: {config_manager.user_config_path}")
            else:
                click.echo(f"✓ Logged in as {name or '(no name)'} ({email})")
                click.echo(f"  📁 Config: {config_manager.user_config_path}")
        else:
            # In quiet mode, just print the basic info
            click.echo(f"{name or '(no name)'} ({email})")
    else:
        if not quiet:
            if RICH_AVAILABLE:
                rprint("[yellow]❌ Not logged in[/yellow]")
                rprint("  Run [cyan]stride login[/cyan] to set your identity")
            else:
                click.echo("❌ Not logged in")
                click.echo("  Run 'stride login' to set your identity")
        else:
            click.echo("Not logged in")
        
        sys.exit(1)


@cli.command()
@click.option("--name", "-n", help="Project name")
@click.option("--description", "-d", help="Project description")
@click.option("--agents", "-a", help="Comma-separated list of agent IDs (e.g., claude,copilot)")
@click.option("--force", "-f", is_flag=True, help="Force initialization even if Stride already exists")
@click.option("--no-interactive", is_flag=True, help="Skip interactive prompts")
@click.pass_context
def init(ctx: click.Context, name: Optional[str], description: Optional[str], agents: Optional[str], 
         force: bool, no_interactive: bool) -> None:
    """
    Initialize Stride in the current directory.
    
    Creates the necessary folder structure, configuration, and documentation files.
    If run without options, enters interactive mode to guide setup.
    
    \b
    Created Structure:
      - stride/sprints/{proposed,active,blocked,review,completed}/
      - stride/specs/
      - stride/introspection/
      - stride/project.md
      - stride.config.yaml
      - AGENTS.md
    
    \b
    Examples:
      stride init                                    # Interactive mode
      stride init --name "My Project"                # With project name
      stride init --agents claude,copilot            # With specific agents
      stride init --name "My App" --no-interactive   # Non-interactive
    """
    from stride.core.agent_manager import AgentManager
    from stride.core.template_engine import TemplateEngine
    from datetime import datetime, timezone
    
    fm: FolderManager = ctx.obj["folder_manager"]
    config_manager = ConfigManager()
    quiet = ctx.obj.get("quiet", False)
    
    # Check if already initialized
    if fm.stride_root.exists() and not force:
        click.echo("❌ Stride is already initialized in this directory.", err=True)
        click.echo("   Use --force to reinitialize.", err=True)
        sys.exit(1)
    
    # Interactive prompts if not in non-interactive mode
    if not no_interactive and not quiet:
        if RICH_AVAILABLE:
            rprint("\n[bold cyan]🚀 Welcome to Stride![/bold cyan]")
            rprint("[dim]Sprint-Powered, Spec-Driven Development for AI Agents[/dim]\n")
        else:
            click.echo("\n🚀 Welcome to Stride!")
            click.echo("Sprint-Powered, Spec-Driven Development for AI Agents\n")
        
        # Prompt for project name if not provided
        if not name:
            name = click.prompt("Project name", default=Path.cwd().name)
        
        # Prompt for description if not provided
        if not description:
            description = click.prompt("Project description (optional)", default="", show_default=False)
            if not description:
                description = None
        
        # Prompt for agents if not provided
        if not agents:
            if RICH_AVAILABLE:
                rprint("\n[bold]Available AI Agents:[/bold]")
                for agent in AgentManager.get_all_agents():
                    rprint(f"  • [cyan]{agent.id:12}[/cyan] - {agent.name}")
                    rprint(f"    [dim]{agent.description}[/dim]")
            else:
                click.echo("\nAvailable AI Agents:")
                for agent in AgentManager.get_all_agents():
                    click.echo(f"  • {agent.id:12} - {agent.name}")
                    click.echo(f"    {agent.description}")
            
            click.echo()
            agents_input = click.prompt(
                "Select agents (comma-separated IDs)",
                default="claude,copilot",
                show_default=True
            )
            agents = agents_input
    
    # Use defaults if still not provided
    if not name:
        name = Path.cwd().name
    if not agents:
        agents = "claude,copilot"  # Default agents
    
    # Parse and validate agents
    selected_agent_ids = AgentManager.parse_agent_string(agents)
    valid_agents, invalid_agents = AgentManager.validate_agent_ids(selected_agent_ids)
    
    if invalid_agents:
        click.echo(f"⚠️  Warning: Unknown agents will be ignored: {', '.join(invalid_agents)}", err=True)
    
    if not valid_agents:
        click.echo("❌ No valid agents selected. Using default: claude,copilot", err=True)
        valid_agents = ["claude", "copilot"]
    
    # Create folder structure
    try:
        fm.ensure_structure()
        
        # Initialize project configuration
        config_manager.init_project_config(
            project_name=name,
            version="1.0.0",
            agents=valid_agents,
            force=force
        )
        
        # Generate AGENTS.md
        agents_md_path = fm.project_root / "AGENTS.md"
        if not agents_md_path.exists() or force:
            template_engine = TemplateEngine()
            agent_objects = [AgentManager.get_agent(aid) for aid in valid_agents]
            agents_content = template_engine.render_template(
                "AGENTS.md.j2",
                {
                    "project_name": name,
                    "agents": agent_objects,
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
            )
            agents_md_path.write_text(agents_content, encoding="utf-8")
        
        # Generate stride/project.md
        project_md_path = fm.stride_root / "project.md"
        if not project_md_path.exists() or force:
            template_engine = TemplateEngine()
            agent_objects = [AgentManager.get_agent(aid) for aid in valid_agents]
            project_content = template_engine.render_template(
                "project.md.j2",
                {
                    "project_name": name,
                    "agents": agent_objects,
                    "agent_ids": valid_agents,
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
            )
            project_md_path.write_text(project_content, encoding="utf-8")
        
        # Success feedback
        if not quiet:
            if RICH_AVAILABLE:
                rprint(f"\n[bold green]✓[/bold green] Stride initialized successfully!")
                rprint(f"\n[bold]Created structure:[/bold]")
                rprint("  📁 stride/sprints/{proposed,active,blocked,review,completed}/")
                rprint("  📁 stride/specs/")
                rprint("  📁 stride/introspection/")
                rprint(f"  📄 stride/project.md")
                rprint(f"  📄 stride.config.yaml")
                rprint(f"  📄 AGENTS.md ([cyan]{len(valid_agents)}[/cyan] agent{'s' if len(valid_agents) != 1 else ''} configured)")
                
                rprint(f"\n[bold]Project:[/bold] {name}")
                rprint(f"[bold]Agents:[/bold] {', '.join([AgentManager.get_agent_display_name(a) for a in valid_agents])}")
                
                rprint("\n[bold cyan]📋 Next steps:[/bold cyan]")
                rprint("  1. Review and customize [cyan]AGENTS.md[/cyan]")
                rprint("  2. Edit [cyan]stride/project.md[/cyan] with project details")
                rprint("  3. Create your first sprint: [green]stride create[/green]")
            else:
                click.echo("\n✓ Stride initialized successfully!")
                click.echo("\nCreated structure:")
                click.echo("  📁 stride/sprints/{proposed,active,blocked,review,completed}/")
                click.echo("  📁 stride/specs/")
                click.echo("  📁 stride/introspection/")
                click.echo("  � stride/project.md")
                click.echo("  � stride.config.yaml")
                click.echo(f"  � AGENTS.md ({len(valid_agents)} agent{'s' if len(valid_agents) != 1 else ''} configured)")
                
                click.echo(f"\nProject: {name}")
                click.echo(f"Agents: {', '.join([AgentManager.get_agent_display_name(a) for a in valid_agents])}")
                
                click.echo("\n📋 Next steps:")
                click.echo("  1. Review and customize AGENTS.md")
                click.echo("  2. Edit stride/project.md with project details")
                click.echo("  3. Create your first sprint: stride create")
                
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
    
    # Get author from Stride user config, git config, or prompt
    if not author:
        # First try Stride user config
        config_manager = ConfigManager()
        if config_manager.is_user_authenticated():
            email, name = config_manager.get_user_info()
            author = email
            if not quiet:
                if RICH_AVAILABLE:
                    rprint(f"[dim]Using authenticated user: {name} <{email}>[/dim]")
                else:
                    click.echo(f"Using authenticated user: {name} <{email}>")
        else:
            # Fall back to git config
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
                    if not quiet:
                        if RICH_AVAILABLE:
                            rprint(f"[dim]Using git config email: {author}[/dim]")
                        else:
                            click.echo(f"Using git config email: {author}")
            except Exception:
                pass
            
            # Warn if no author found
            if not author:
                if not quiet:
                    if RICH_AVAILABLE:
                        rprint("[yellow]⚠️  No author configured. Run 'stride login' to set your identity.[/yellow]")
                    else:
                        click.echo("⚠️  No author configured. Run 'stride login' to set your identity.")
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
@click.option("--format", "-f", type=click.Choice(["table", "list", "json", "dashboard"]), default="dashboard", help="Output format")
@click.option("--detailed", "-d", is_flag=True, help="Show detailed sprint information")
@click.option("--team", "-t", is_flag=True, help="Show team analytics")
@click.option("--user", "-u", help="Filter by author email")
@click.option("--since", help="Filter sprints created since date (YYYY-MM-DD)")
@click.option("--until", help="Filter sprints created until date (YYYY-MM-DD)")
@click.option("--sort", type=click.Choice(["date", "priority", "status", "author", "title"]), default="date", help="Sort by field")
@click.pass_context
def list(ctx: click.Context, status: Optional[str], format: str, detailed: bool, team: bool, 
         user: Optional[str], since: Optional[str], until: Optional[str], sort: str) -> None:
    """
    List all sprints or sprints in a specific status with visual dashboard.
    
    By default, shows a visual dashboard with sprint distribution and health metrics.
    
    Examples:
      stride list
      stride list --status active
      stride list --status proposed --format list
      stride list --format json
      stride list --detailed
      stride list --team
      stride list --user alice@example.com
      stride list --since 2025-11-01 --until 2025-11-30
      stride list --sort priority
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
    
    # Apply user filter
    if user:
        sprints = [s for s in sprints if s["metadata"] and s["metadata"].get("author", "").lower() == user.lower()]
    
    # Apply date filters
    if since or until:
        from datetime import datetime
        filtered_sprints = []
        for sprint in sprints:
            if not sprint["metadata"] or not sprint["metadata"].get("created"):
                continue
            
            try:
                created_str = sprint["metadata"]["created"].replace("Z", "+00:00")
                created = datetime.fromisoformat(created_str).date()
                
                if since:
                    since_date = datetime.strptime(since, "%Y-%m-%d").date()
                    if created < since_date:
                        continue
                
                if until:
                    until_date = datetime.strptime(until, "%Y-%m-%d").date()
                    if created > until_date:
                        continue
                
                filtered_sprints.append(sprint)
            except (ValueError, AttributeError):
                # Skip sprints with invalid dates
                continue
        
        sprints = filtered_sprints
    
    # Sort sprints
    def get_sort_key(sprint):
        meta = sprint["metadata"] or {}
        if sort == "date":
            created = meta.get("created", "")
            return created if created else "9999-99-99"
        elif sort == "priority":
            # Sort order: critical, high, medium, low
            priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
            return priority_order.get(meta.get("priority", "medium"), 2)
        elif sort == "status":
            status_str = sprint["status"].value if hasattr(sprint["status"], "value") else sprint["status"]
            return status_str
        elif sort == "author":
            return meta.get("author", "").lower()
        elif sort == "title":
            return meta.get("title", "").lower()
        return ""
    
    sprints = sorted(sprints, key=get_sort_key, reverse=(sort == "date"))
    
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
    
    elif format == "dashboard":
        _display_dashboard(sprints, detailed, team, quiet)
            
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
@click.option("--file", "-f", help="Show specific file (proposal, plan, design, implementation, retrospective)")
@click.pass_context
def show(ctx: click.Context, sprint_id: str, file: Optional[str]) -> None:
    """
    Display complete sprint details with all files.
    
    Shows metadata and content of all sprint files. Use --file to display
    a specific file only.
    
    Examples:
      stride show SPRINT-A1B2
      stride show SPRINT-A1B2 --file plan
      stride show SPRINT-A1B2 --file proposal
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
    sprint_path = sprint_info["path"]
    
    # Available sprint files
    file_types = {
        "proposal": "proposal.md",
        "plan": "plan.md",
        "design": "design.md",
        "implementation": "implementation.md",
        "retrospective": "retrospective.md"
    }
    
    if not quiet:
        if RICH_AVAILABLE:
            from rich.panel import Panel
            from rich.syntax import Syntax
            from rich.markdown import Markdown
            
            # Show header with metadata
            rprint(f"\n[bold cyan]{'=' * 60}[/bold cyan]")
            rprint(f"[bold white]📋 Sprint Details: {sprint_id}[/bold white]")
            rprint(f"[bold cyan]{'=' * 60}[/bold cyan]\n")
            
            # Metadata section
            rprint(f"[bold]Title:[/bold] {meta.get('title', 'N/A')}")
            rprint(f"[bold]Status:[/bold] [{_get_status_color(status_val)}]{status_val}[/{_get_status_color(status_val)}] {_get_status_emoji(status_val)}")
            rprint(f"[bold]Author:[/bold] {meta.get('author', 'N/A')}")
            rprint(f"[bold]Priority:[/bold] {_get_priority_emoji(meta.get('priority', 'medium'))} {meta.get('priority', 'N/A')}")
            
            if meta.get('tags'):
                rprint(f"[bold]Tags:[/bold] [cyan]{', '.join(meta['tags'])}[/cyan]")
            
            rprint(f"\n[bold]Created:[/bold] {meta.get('created', 'N/A')}")
            if meta.get('updated'):
                rprint(f"[bold]Updated:[/bold] {meta.get('updated', 'N/A')}")
            
            rprint(f"[bold]Location:[/bold] [dim]{sprint_path}[/dim]")
            
            # Show specific file if requested
            if file:
                if file not in file_types:
                    click.echo(f"❌ Unknown file type: {file}", err=True)
                    click.echo(f"   Available: {', '.join(file_types.keys())}", err=True)
                    sys.exit(1)
                
                file_path = sprint_path / file_types[file]
                if file_path.exists():
                    rprint(f"\n[bold cyan]{'─' * 60}[/bold cyan]")
                    rprint(f"[bold]📄 {file.capitalize()}:[/bold]\n")
                    
                    content = file_path.read_text(encoding="utf-8")
                    md = Markdown(content)
                    rprint(md)
                else:
                    rprint(f"\n[yellow]⚠️  {file.capitalize()}.md not found[/yellow]")
            else:
                # Show all files
                rprint(f"\n[bold cyan]{'─' * 60}[/bold cyan]")
                rprint(f"[bold]📂 Sprint Files:[/bold]\n")
                
                for file_type, filename in file_types.items():
                    file_path = sprint_path / filename
                    if file_path.exists():
                        file_size = file_path.stat().st_size
                        rprint(f"  ✅ [green]{filename}[/green] [dim]({file_size} bytes)[/dim]")
                    else:
                        rprint(f"  ⚠️  [dim]{filename}[/dim] [yellow](not found)[/yellow]")
                
                rprint(f"\n[dim]💡 Tip: Use --file <name> to view a specific file[/dim]")
            
            rprint(f"\n[bold cyan]{'=' * 60}[/bold cyan]\n")
        
        else:
            # Fallback ASCII output
            click.echo(f"\n{'=' * 60}")
            click.echo(f"Sprint Details: {sprint_id}")
            click.echo(f"{'=' * 60}\n")
            
            click.echo(f"Title: {meta.get('title', 'N/A')}")
            click.echo(f"Status: {status_val}")
            click.echo(f"Author: {meta.get('author', 'N/A')}")
            click.echo(f"Priority: {meta.get('priority', 'N/A')}")
            
            if meta.get('tags'):
                click.echo(f"Tags: {', '.join(meta['tags'])}")
            
            click.echo(f"\nCreated: {meta.get('created', 'N/A')}")
            if meta.get('updated'):
                click.echo(f"Updated: {meta.get('updated', 'N/A')}")
            
            click.echo(f"Location: {sprint_path}")
            
            # Show specific file if requested
            if file:
                if file not in file_types:
                    click.echo(f"\n❌ Unknown file type: {file}", err=True)
                    click.echo(f"   Available: {', '.join(file_types.keys())}", err=True)
                    sys.exit(1)
                
                file_path = sprint_path / file_types[file]
                if file_path.exists():
                    click.echo(f"\n{'-' * 60}")
                    click.echo(f"{file.capitalize()}:\n")
                    
                    content = file_path.read_text(encoding="utf-8")
                    click.echo(content)
                else:
                    click.echo(f"\n⚠️  {file.capitalize()}.md not found")
            else:
                # Show all files
                click.echo(f"\n{'-' * 60}")
                click.echo(f"Sprint Files:\n")
                
                for file_type, filename in file_types.items():
                    file_path = sprint_path / filename
                    if file_path.exists():
                        file_size = file_path.stat().st_size
                        click.echo(f"  ✓ {filename} ({file_size} bytes)")
                    else:
                        click.echo(f"  ✗ {filename} (not found)")
                
                click.echo(f"\n💡 Tip: Use --file <name> to view a specific file")
            
            click.echo(f"\n{'=' * 60}\n")


@cli.command()
@click.argument("sprint_id")
@click.pass_context
def progress(ctx: click.Context, sprint_id: str) -> None:
    """
    Display detailed progress for a sprint.
    
    Shows task completion status, progress bars, and time estimates.
    Parses tasks from plan.md and tracks completion.
    
    Examples:
      stride progress SPRINT-A1B2
    """
    sm: SprintManager = ctx.obj["sprint_manager"]
    quiet = ctx.obj.get("quiet", False)
    
    try:
        sprint_info = sm.get_sprint(sprint_id)
        metadata = sprint_info["metadata"]
        sprint_path = sprint_info["path"]
        
        # Parse tasks from plan.md
        plan_file = sprint_path / "plan.md"
        tasks = []
        completed_count = 0
        total_count = 0
        
        if plan_file.exists():
            content = plan_file.read_text(encoding="utf-8")
            # Parse markdown checkboxes: - [ ] or - [x]
            import re
            task_pattern = r'^[\s]*[-*]\s+\[([ xX])\]\s+(.+)$'
            
            for line in content.split('\n'):
                match = re.match(task_pattern, line)
                if match:
                    is_complete = match.group(1).lower() == 'x'
                    task_text = match.group(2).strip()
                    tasks.append({
                        'text': task_text,
                        'completed': is_complete
                    })
                    total_count += 1
                    if is_complete:
                        completed_count += 1
        
        # Calculate progress
        progress_percentage = (completed_count / total_count * 100) if total_count > 0 else 0
        
        # Display using Rich if available
        if RICH_AVAILABLE:
            from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn
            from rich.table import Table
            
            rprint(f"\n[bold cyan]{'=' * 60}[/bold cyan]")
            rprint(f"[bold white]📊 Sprint Progress: {sprint_id}[/bold white]")
            rprint(f"[bold cyan]{'=' * 60}[/bold cyan]\n")
            
            # Metadata
            status_val = metadata.get("status", "unknown")
            rprint(f"[bold]Title:[/bold] {metadata.get('title', 'Untitled')}")
            rprint(f"[bold]Status:[/bold] [{_get_status_color(status_val)}]{status_val}[/{_get_status_color(status_val)}] {_get_status_emoji(status_val)}")
            rprint(f"[bold]Author:[/bold] {metadata.get('author', 'Unknown')}")
            
            # Progress summary
            rprint(f"\n[bold cyan]Progress Summary[/bold cyan]")
            rprint(f"[bold]Tasks Completed:[/bold] {completed_count} / {total_count}")
            rprint(f"[bold]Completion:[/bold] {progress_percentage:.1f}%\n")
            
            # Progress bar
            if total_count > 0:
                from rich.progress import Progress as ProgressBar
                progress_bar = ProgressBar()
                task_id = progress_bar.add_task("[cyan]Overall Progress", total=total_count)
                progress_bar.update(task_id, completed=completed_count)
                
                # Simple progress bar visualization
                bar_width = 40
                filled = int(bar_width * progress_percentage / 100)
                bar = "█" * filled + "░" * (bar_width - filled)
                
                if progress_percentage >= 75:
                    bar_color = "green"
                elif progress_percentage >= 50:
                    bar_color = "yellow"
                elif progress_percentage >= 25:
                    bar_color = "blue"
                else:
                    bar_color = "red"
                
                rprint(f"[{bar_color}]{bar}[/{bar_color}] {progress_percentage:.1f}%\n")
            
            # Task list
            if tasks:
                rprint(f"[bold cyan]Tasks:[/bold cyan]\n")
                
                table = Table(show_header=False, box=None, padding=(0, 2))
                table.add_column("Status", style="bold", width=3)
                table.add_column("Task")
                
                for task in tasks:
                    if task['completed']:
                        status_icon = "[green]✓[/green]"
                        task_text = f"[dim]{task['text']}[/dim]"
                    else:
                        status_icon = "[yellow]○[/yellow]"
                        task_text = task['text']
                    
                    table.add_row(status_icon, task_text)
                
                rprint(table)
            else:
                rprint("[yellow]⚠️  No tasks found in plan.md[/yellow]")
            
            # Timestamps
            rprint(f"\n[bold cyan]Timeline[/bold cyan]")
            rprint(f"[dim]Created:[/dim] {metadata.get('created', 'Unknown')}")
            rprint(f"[dim]Updated:[/dim] {metadata.get('updated', 'Unknown')}")
            
            rprint(f"\n[bold cyan]{'=' * 60}[/bold cyan]\n")
        
        else:
            # ASCII fallback
            click.echo(f"\n{'=' * 60}")
            click.echo(f"📊 Sprint Progress: {sprint_id}")
            click.echo(f"{'=' * 60}\n")
            
            click.echo(f"Title: {metadata.get('title', 'Untitled')}")
            click.echo(f"Status: {metadata.get('status', 'unknown')}")
            click.echo(f"Author: {metadata.get('author', 'Unknown')}")
            
            click.echo(f"\nProgress Summary:")
            click.echo(f"Tasks Completed: {completed_count} / {total_count}")
            click.echo(f"Completion: {progress_percentage:.1f}%")
            
            if total_count > 0:
                bar_width = 40
                filled = int(bar_width * progress_percentage / 100)
                bar = "█" * filled + "░" * (bar_width - filled)
                click.echo(f"\n{bar} {progress_percentage:.1f}%\n")
            
            if tasks:
                click.echo("\nTasks:\n")
                for task in tasks:
                    status_icon = "✓" if task['completed'] else "○"
                    click.echo(f"  {status_icon} {task['text']}")
            else:
                click.echo("\n⚠️  No tasks found in plan.md")
            
            click.echo(f"\nTimeline:")
            click.echo(f"Created: {metadata.get('created', 'Unknown')}")
            click.echo(f"Updated: {metadata.get('updated', 'Unknown')}")
            
            click.echo(f"\n{'=' * 60}\n")
    
    except FileNotFoundError:
        click.echo(f"Error: Sprint {sprint_id} not found", err=True)
        ctx.exit(1)
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        if ctx.obj.get("verbose"):
            import traceback
            traceback.print_exc()
        ctx.exit(1)


@cli.command()
@click.argument("sprint_id")
@click.option("--limit", "-n", type=int, help="Limit number of events to show")
@click.pass_context
def timeline(ctx: click.Context, sprint_id: str, limit: Optional[int]) -> None:
    """
    Display complete sprint timeline with all events.
    
    Shows chronological history of all sprint events including:
    - Sprint creation
    - Status changes
    - Updates and modifications
    
    Examples:
      stride timeline SPRINT-A1B2
      stride timeline SPRINT-A1B2 --limit 10
    """
    sm: SprintManager = ctx.obj["sprint_manager"]
    quiet = ctx.obj.get("quiet", False)
    
    try:
        sprint_info = sm.get_sprint(sprint_id)
        metadata = sprint_info["metadata"]
        sprint_path = sprint_info["path"]
        proposal_file = sprint_path / "proposal.md"
        
        # Get events
        events = MetadataManager.get_events(proposal_file)
        
        # Apply limit if specified
        if limit and limit > 0:
            events = events[-limit:]  # Show most recent N events
        
        # Display using Rich if available
        if RICH_AVAILABLE:
            from rich.table import Table
            from rich.panel import Panel
            
            rprint(f"\n[bold cyan]{'=' * 60}[/bold cyan]")
            rprint(f"[bold white]📅 Sprint Timeline: {sprint_id}[/bold white]")
            rprint(f"[bold cyan]{'=' * 60}[/bold cyan]\n")
            
            # Sprint info
            status_val = metadata.get("status", "unknown")
            rprint(f"[bold]Title:[/bold] {metadata.get('title', 'Untitled')}")
            rprint(f"[bold]Status:[/bold] [{_get_status_color(status_val)}]{status_val}[/{_get_status_color(status_val)}] {_get_status_emoji(status_val)}")
            rprint(f"[bold]Author:[/bold] {metadata.get('author', 'Unknown')}\n")
            
            # Events
            if events:
                rprint(f"[bold cyan]Event History ({len(events)} events):[/bold cyan]\n")
                
                # Create timeline table
                table = Table(show_header=True, box=None, padding=(0, 2))
                table.add_column("Time", style="dim", width=22)
                table.add_column("Event", style="bold")
                table.add_column("Details")
                
                # Event type icons
                event_icons = {
                    "created": "🎉",
                    "status_changed": "🔄",
                    "updated": "✏️",
                    "file_modified": "📝",
                    "blocked": "🚫",
                    "unblocked": "✅",
                    "completed": "🎯"
                }
                
                for event in events:
                    event_type = event.get("type", "unknown")
                    timestamp = event.get("timestamp", "Unknown")
                    message = event.get("message", "No description")
                    
                    # Format timestamp
                    try:
                        from datetime import datetime
                        dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
                        time_str = dt.strftime("%Y-%m-%d %H:%M:%S")
                    except:
                        time_str = timestamp
                    
                    # Get icon
                    icon = event_icons.get(event_type, "•")
                    
                    # Format event type
                    event_display = f"{icon} {event_type.replace('_', ' ').title()}"
                    
                    # Get additional details
                    details = ""
                    if "metadata" in event and event["metadata"]:
                        meta = event["metadata"]
                        if "from_status" in meta and "to_status" in meta:
                            details = f"{meta['from_status']} → {meta['to_status']}"
                        elif "priority" in meta:
                            details = f"Priority: {meta['priority']}"
                    
                    table.add_row(time_str, event_display, details)
                
                rprint(table)
            else:
                rprint("[yellow]⚠️  No events recorded yet[/yellow]")
                rprint("[dim]Events are automatically tracked when you create or modify sprints.[/dim]")
            
            # Summary
            rprint(f"\n[bold cyan]Summary[/bold cyan]")
            rprint(f"[dim]Created:[/dim] {metadata.get('created', 'Unknown')}")
            rprint(f"[dim]Last Updated:[/dim] {metadata.get('updated', 'Unknown')}")
            rprint(f"[dim]Total Events:[/dim] {len(events)}")
            
            rprint(f"\n[bold cyan]{'=' * 60}[/bold cyan]\n")
        
        else:
            # ASCII fallback
            click.echo(f"\n{'=' * 60}")
            click.echo(f"📅 Sprint Timeline: {sprint_id}")
            click.echo(f"{'=' * 60}\n")
            
            click.echo(f"Title: {metadata.get('title', 'Untitled')}")
            click.echo(f"Status: {metadata.get('status', 'unknown')}")
            click.echo(f"Author: {metadata.get('author', 'Unknown')}\n")
            
            if events:
                click.echo(f"Event History ({len(events)} events):\n")
                
                for i, event in enumerate(events, 1):
                    event_type = event.get("type", "unknown")
                    timestamp = event.get("timestamp", "Unknown")
                    message = event.get("message", "No description")
                    
                    # Format timestamp
                    try:
                        from datetime import datetime
                        dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
                        time_str = dt.strftime("%Y-%m-%d %H:%M:%S")
                    except:
                        time_str = timestamp
                    
                    click.echo(f"{i}. [{time_str}] {event_type}: {message}")
                
                click.echo()
            else:
                click.echo("⚠️  No events recorded yet\n")
            
            click.echo("Summary:")
            click.echo(f"Created: {metadata.get('created', 'Unknown')}")
            click.echo(f"Last Updated: {metadata.get('updated', 'Unknown')}")
            click.echo(f"Total Events: {len(events)}")
            
            click.echo(f"\n{'=' * 60}\n")
    
    except FileNotFoundError:
        click.echo(f"Error: Sprint {sprint_id} not found", err=True)
        ctx.exit(1)
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        if ctx.obj.get("verbose"):
            import traceback
            traceback.print_exc()
        ctx.exit(1)


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
@click.option("--detailed", "-d", is_flag=True, help="Show detailed validation report")
@click.pass_context
def validate(ctx: click.Context, sprint_id: Optional[str], validate_all: bool, status: Optional[str], strict: bool, detailed: bool) -> None:
    """
    Validate sprint structure, metadata, and content quality.
    
    Performs comprehensive validation including:
    - Structure checks (files and folders)
    - Metadata validation (required fields, consistency)
    - Content quality checks (completeness, formatting)
    - Suggestions for improvements
    
    Examples:
      stride validate SPRINT-A1B2
      stride validate SPRINT-A1B2 --detailed
      stride validate --all
      stride validate --status active --detailed
      stride validate --all --strict
    """
    from ..core.validators import SprintValidator
    from ..core.metadata_manager import MetadataManager
    
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
    
    # Validate sprints with enhanced validation
    results = []
    for sid in sprints_to_validate:
        # Find sprint
        result_tuple = fm.find_sprint(sid)
        if not result_tuple:
            results.append((sid, False, {"errors": [f"Sprint not found: {sid}"]}, None))
            continue
        
        sprint_path, _ = result_tuple
        proposal_file = sprint_path / "proposal.md"
        
        if not proposal_file.exists():
            results.append((sid, False, {"errors": ["Missing proposal.md"]}, None))
            continue
        
        # Parse metadata
        try:
            metadata, _ = MetadataManager.parse_file(proposal_file)
        except Exception as e:
            results.append((sid, False, {"errors": [f"Failed to parse metadata: {e}"]}, None))
            continue
        
        # Run enhanced validation
        validator = SprintValidator(sprint_path, metadata)
        validation_results = validator.validate_all()
        summary = validator.get_summary()
        
        is_valid = summary["is_valid"]
        results.append((sid, is_valid, validation_results, summary))
    
    # Report results
    valid_count = sum(1 for _, is_valid, _, _ in results if is_valid)
    invalid_count = len(results) - valid_count
    
    if not quiet:
        if RICH_AVAILABLE and detailed:
            # Detailed Rich output
            from rich.console import Console
            from rich.table import Table
            from rich.panel import Panel
            
            console = Console()
            
            for sid, is_valid, validation_results, summary in results:
                if not validation_results:
                    # Simple error case
                    console.print(f"\n[red]✗ {sid}[/red]")
                    if isinstance(validation_results, dict) and "errors" in validation_results:
                        for error in validation_results["errors"]:
                            console.print(f"  [red]• {error}[/red]")
                    continue
                
                # Create header
                status_icon = "✓" if is_valid else "✗"
                status_color = "green" if is_valid else "red"
                console.print(f"\n[{status_color} bold]{status_icon} {sid}[/{status_color} bold]")
                
                # Show summary stats
                console.print(f"  [dim]Checks: {summary['total_checks']} | "
                            f"Passed: {summary['passed']} | "
                            f"Warnings: {summary['warnings']} | "
                            f"Errors: {summary['errors']}[/dim]")
                
                # Show detailed results by category
                for category, result in validation_results.items():
                    console.print(f"\n  [bold]{category.title()}:[/bold]")
                    
                    # Show passed checks
                    for msg in result.passed:
                        console.print(f"    [green]✓[/green] {msg}")
                    
                    # Show warnings
                    for msg in result.warnings:
                        console.print(f"    [yellow]⚠[/yellow] {msg}")
                    
                    # Show errors
                    for msg in result.errors:
                        console.print(f"    [red]✗[/red] {msg}")
                    
                    # Show suggestions
                    if result.suggestions:
                        console.print(f"    [dim cyan]💡 Suggestions:[/dim cyan]")
                        for msg in result.suggestions:
                            console.print(f"      [dim cyan]• {msg}[/dim cyan]")
            
            # Overall summary
            console.print(f"\n[bold]Overall Summary:[/bold]")
            console.print(f"  Valid: [green]{valid_count}[/green]")
            console.print(f"  Invalid: [red]{invalid_count}[/red]")
            console.print(f"  Total: {len(results)}")
            
        elif RICH_AVAILABLE:
            # Simple Rich output
            for sid, is_valid, validation_results, summary in results:
                if is_valid:
                    rprint(f"[green]✓[/green] {sid}")
                else:
                    rprint(f"[red]✗[/red] {sid}")
                    if validation_results and summary:
                        rprint(f"    [dim]Errors: {summary['errors']}, Warnings: {summary['warnings']}[/dim]")
                        # Show first few errors
                        error_count = 0
                        for result in validation_results.values():
                            for error in result.errors:
                                if error_count < 3:  # Limit to 3 errors in simple view
                                    rprint(f"    [dim red]• {error}[/dim red]")
                                    error_count += 1
                        if summary['errors'] > 3:
                            rprint(f"    [dim]... and {summary['errors'] - 3} more errors (use --detailed)[/dim]")
                    elif isinstance(validation_results, dict) and "errors" in validation_results:
                        for error in validation_results["errors"]:
                            rprint(f"    [dim red]• {error}[/dim red]")
            
            rprint(f"\n[bold]Summary:[/bold] {valid_count} valid, {invalid_count} invalid")
            if invalid_count > 0 and not detailed:
                rprint("[dim]Tip: Use --detailed for full validation report[/dim]")
        else:
            # Plain text output
            for sid, is_valid, validation_results, summary in results:
                if is_valid:
                    click.echo(f"✓ {sid}")
                else:
                    click.echo(f"✗ {sid}")
                    if validation_results and summary:
                        click.echo(f"    Errors: {summary['errors']}, Warnings: {summary['warnings']}")
                        error_count = 0
                        for result in validation_results.values():
                            for error in result.errors:
                                if error_count < 3:
                                    click.echo(f"    • {error}")
                                    error_count += 1
                    elif isinstance(validation_results, dict) and "errors" in validation_results:
                        for error in validation_results["errors"]:
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


@cli.command()
@click.argument("sprint_id")
@click.option("--interval", "-i", default=1.0, type=float, help="Refresh interval in seconds")
@click.pass_context
def watch(ctx: click.Context, sprint_id: str, interval: float) -> None:
    """
    Watch a sprint for real-time file changes.
    
    Monitors sprint folder and displays live updates when files are modified,
    created, deleted, or moved. Shows sprint status, file list, and event log.
    
    Press Ctrl+C to stop watching.
    
    \b
    Examples:
      stride watch SPRINT-7K9P
      stride watch SPRINT-A1B2 --interval 0.5
      stride watch SPRINT-TIME -i 2.0
    """
    from ..core.watcher import SprintWatcher, SprintEvent
    from ..core.metadata_manager import MetadataManager
    from rich.live import Live
    from rich.panel import Panel
    from rich.table import Table
    from rich.layout import Layout
    from rich.console import Group
    from rich.text import Text
    from collections import deque
    import signal
    
    sm: SprintManager = ctx.obj["sprint_manager"]
    fm: FolderManager = ctx.obj["folder_manager"]
    quiet = ctx.obj.get("quiet", False)
    
    # Validate sprint exists
    sprint_path = None
    for status in SprintStatus:
        path = fm.sprints_root / status.value / sprint_id
        if path.exists():
            sprint_path = path
            break
    
    if not sprint_path:
        click.echo(f"❌ Sprint not found: {sprint_id}", err=True)
        sys.exit(1)
    
    # Load sprint metadata
    proposal_file = sprint_path / "proposal.md"
    if not proposal_file.exists():
        click.echo(f"❌ Sprint proposal not found: {sprint_id}", err=True)
        sys.exit(1)
    
    metadata, _ = MetadataManager.parse_file(proposal_file)
    
    # Event storage
    events = deque(maxlen=20)  # Keep last 20 events
    file_states = {}  # Track file sizes
    
    def on_event(event: SprintEvent):
        """Handle file system events."""
        events.append(event)
        if event.event_type in ['modified', 'created']:
            try:
                file_size = event.file_path.stat().st_size
                file_states[event.file_name] = file_size
            except:
                pass
    
    def generate_display() -> Layout:
        """Generate the live display layout."""
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=7),
            Layout(name="body"),
            Layout(name="footer", size=3),
        )
        
        # Header: Sprint info
        header_content = Table.grid(padding=(0, 2))
        header_content.add_column(style="bold cyan", justify="right")
        header_content.add_column()
        header_content.add_row("Sprint:", f"[bold]{metadata.get('id', sprint_id)}[/bold]")
        header_content.add_row("Title:", metadata.get('title', 'Untitled'))
        header_content.add_row("Status:", f"[yellow]{metadata.get('status', 'unknown')}[/yellow]")
        header_content.add_row("Watching:", str(sprint_path.relative_to(fm.project_root)))
        
        layout["header"].update(Panel(header_content, title="📡 Sprint Monitor", border_style="cyan"))
        
        # Body: Split into files and events
        body_layout = Layout()
        body_layout.split_row(
            Layout(name="files", ratio=1),
            Layout(name="events", ratio=1),
        )
        
        # Files panel
        files_table = Table(show_header=True, header_style="bold magenta", box=None)
        files_table.add_column("File", style="cyan")
        files_table.add_column("Size", justify="right", style="green")
        
        tracked_files = ['proposal.md', 'plan.md', 'design.md', 'implementation.md', 'retrospective.md', 'notes.md']
        for file_name in tracked_files:
            file_path = sprint_path / file_name
            if file_path.exists():
                size = file_path.stat().st_size
                size_str = f"{size:,} bytes" if size < 1024 else f"{size/1024:.1f} KB"
                status_icon = "✓"
            else:
                size_str = "-"
                status_icon = "·"
            
            files_table.add_row(f"{status_icon} {file_name}", size_str)
        
        body_layout["files"].update(Panel(files_table, title="📁 Files", border_style="magenta"))
        
        # Events panel
        if events:
            events_content = []
            for event in reversed(list(events)):
                timestamp = event.timestamp.strftime("%H:%M:%S")
                
                if event.event_type == "modified":
                    icon = "✏️"
                    color = "yellow"
                elif event.event_type == "created":
                    icon = "✨"
                    color = "green"
                elif event.event_type == "deleted":
                    icon = "🗑️"
                    color = "red"
                elif event.event_type == "moved":
                    icon = "📦"
                    color = "blue"
                else:
                    icon = "📝"
                    color = "white"
                
                event_text = Text()
                event_text.append(f"{timestamp} ", style="dim")
                event_text.append(icon + " ", style=color)
                event_text.append(event.file_name, style=f"bold {color}")
                
                if event.event_type == "moved" and event.src_path:
                    event_text.append(f" (from {event.src_path.name})", style="dim")
                
                events_content.append(event_text)
        else:
            events_content = [Text("Waiting for changes...", style="dim italic")]
        
        events_group = Group(*events_content)
        body_layout["events"].update(Panel(events_group, title="📋 Recent Events", border_style="yellow"))
        
        layout["body"].update(body_layout)
        
        # Footer
        footer_text = Text.from_markup(
            f"[dim]Monitoring every {interval}s • Press [bold]Ctrl+C[/bold] to stop[/dim]"
        )
        layout["footer"].update(Panel(footer_text, style="dim"))
        
        return layout
    
    # Signal handling for graceful shutdown
    stop_requested = False
    
    def signal_handler(sig, frame):
        nonlocal stop_requested
        stop_requested = True
    
    signal.signal(signal.SIGINT, signal_handler)
    
    # Start watching
    try:
        with SprintWatcher(sprint_path, on_event) as watcher:
            if not quiet:
                click.echo(f"👀 Watching sprint: {sprint_id}")
                click.echo(f"📂 Path: {sprint_path}")
                click.echo(f"⏱️  Refresh: {interval}s\n")
            
            with Live(generate_display(), refresh_per_second=1/interval, screen=True) as live:
                while not stop_requested:
                    live.update(generate_display())
                    time.sleep(interval)
    
    except KeyboardInterrupt:
        pass
    
    except Exception as e:
        click.echo(f"\n❌ Error watching sprint: {e}", err=True)
        sys.exit(1)
    
    finally:
        if not quiet:
            click.echo(f"\n✓ Stopped watching {sprint_id}")


@cli.command()
@click.option("--fix", is_flag=True, help="Attempt to auto-fix issues")
@click.option("--verbose", "-v", is_flag=True, help="Show detailed check information")
@click.option("--json", "output_json", is_flag=True, help="Output results as JSON")
@click.pass_context
def doctor(ctx: click.Context, fix: bool, verbose: bool, output_json: bool) -> None:
    """
    Run health checks on Stride installation and project.
    
    Performs comprehensive diagnostics including:
    - Installation (Python version, dependencies)
    - Project structure (folders, required files)
    - Sprint integrity (metadata, consistency)
    - Configuration (user/project configs)
    
    \b
    Examples:
      stride doctor
      stride doctor --verbose
      stride doctor --fix
      stride doctor --json > report.json
    """
    from ..core.health_checker import HealthChecker, CheckStatus
    
    quiet = ctx.obj.get("quiet", False)
    
    if not quiet and not output_json:
        click.echo("🏥 Running Stride Health Check...\n")
    
    # Run health checks
    checker = HealthChecker()
    report = checker.check_all()
    
    # JSON output
    if output_json:
        import json
        output = {
            "health_score": report.health_score,
            "health_grade": report.health_grade,
            "total_checks": report.total_checks,
            "passed": report.passed_count,
            "warnings": report.warning_count,
            "errors": report.error_count,
            "checks": [
                {
                    "category": r.category,
                    "check": r.check_name,
                    "status": r.status.value,
                    "message": r.message,
                    "details": r.details,
                    "fix_suggestion": r.fix_suggestion,
                    "auto_fixable": r.auto_fixable,
                }
                for r in report.results
            ]
        }
        click.echo(json.dumps(output, indent=2))
        sys.exit(0 if report.error_count == 0 else 1)
    
    # Rich output
    if RICH_AVAILABLE and not quiet:
        from rich.console import Console
        from rich.table import Table
        from rich.panel import Panel
        from rich.text import Text
        
        console = Console()
        
        # Group results by category
        categories = {}
        for result in report.results:
            if result.category not in categories:
                categories[result.category] = []
            categories[result.category].append(result)
        
        # Display each category
        for category, results in categories.items():
            # Category header
            status_icon = "✅" if all(r.status == CheckStatus.PASS or r.status == CheckStatus.INFO for r in results) else "⚠️" if any(r.status == CheckStatus.WARNING for r in results) else "❌"
            console.print(f"\n{status_icon} [bold]{category}[/bold]")
            
            # Display results
            for result in results:
                icon = result.icon
                
                if result.status == CheckStatus.PASS:
                    color = "green"
                elif result.status == CheckStatus.WARNING:
                    color = "yellow"
                elif result.status == CheckStatus.ERROR:
                    color = "red"
                else:
                    color = "cyan"
                
                console.print(f"   [{color}]{icon} {result.message}[/{color}]")
                
                # Show details in verbose mode
                if verbose and result.details:
                    for line in result.details.split('\n'):
                        console.print(f"     [dim]{line}[/dim]")
                
                # Show fix suggestions
                if result.fix_suggestion and result.status != CheckStatus.PASS:
                    console.print(f"     [dim]💡 {result.fix_suggestion}[/dim]")
        
        # Summary
        console.print("\n" + "━" * 60)
        console.print(f"📊 [bold]Health Score: {report.health_score}/100 ({report.health_grade})[/bold]\n")
        
        # Stats
        stats_text = f"Total Checks: {report.total_checks} | "
        stats_text += f"[green]✓ {report.passed_count}[/green] | "
        stats_text += f"[yellow]⚠ {report.warning_count}[/yellow] | "
        stats_text += f"[red]✗ {report.error_count}[/red]"
        console.print(stats_text)
        
        # Fixable issues
        fixable = report.get_fixable_issues()
        if fixable and not fix:
            console.print(f"\n💡 [dim]{len(fixable)} issue(s) can be auto-fixed with --fix flag[/dim]")
    
    else:
        # Plain text output
        click.echo("Health Check Results:")
        click.echo("=" * 60)
        
        for category in ["Installation", "Project Structure", "Sprints", "Configuration"]:
            results = report.get_by_category(category)
            if not results:
                continue
            
            click.echo(f"\n{category}:")
            for result in results:
                icon = result.icon
                click.echo(f"  {icon} {result.message}")
                
                if verbose and result.details:
                    for line in result.details.split('\n'):
                        click.echo(f"    {line}")
                
                if result.fix_suggestion and result.status != CheckStatus.PASS:
                    click.echo(f"    💡 {result.fix_suggestion}")
        
        click.echo("\n" + "=" * 60)
        click.echo(f"Health Score: {report.health_score}/100 ({report.health_grade})")
        click.echo(f"Passed: {report.passed_count}, Warnings: {report.warning_count}, Errors: {report.error_count}")
        
        fixable = report.get_fixable_issues()
        if fixable and not fix:
            click.echo(f"\n{len(fixable)} issue(s) can be auto-fixed with --fix flag")
    
    # Auto-fix
    if fix:
        fixable = report.get_fixable_issues()
        if fixable:
            if not quiet:
                click.echo(f"\n🔧 Attempting to fix {len(fixable)} issue(s)...")
            
            # TODO: Implement auto-fix logic
            # For now, just show what would be fixed
            for issue in fixable:
                if not quiet:
                    click.echo(f"  • {issue.check_name}: {issue.fix_suggestion}")
            
            if not quiet:
                click.echo("\n⚠️  Auto-fix not yet implemented. Please fix manually.")
        else:
            if not quiet:
                click.echo("\n✓ No auto-fixable issues found")
    
    # Exit code
    sys.exit(0 if report.error_count == 0 else 1)


# =============================================================================
# Agent Commands - Manage AI agents for Stride projects
# =============================================================================

@cli.group()
@click.pass_context
def agent(ctx: click.Context) -> None:
    """
    Manage AI agents for your Stride project.
    
    View available agents, add agents to your project, remove agents, and view detailed agent information.
    Agents help track which AI tools assist with development.
    
    \b
    Examples:
      stride agent list
      stride agent add claude copilot
      stride agent remove chatgpt
      stride agent info claude
    """
    pass


@agent.command("list")
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
@click.pass_context
def agent_list(ctx: click.Context, output_json: bool) -> None:
    """List all available AI agents and show which are configured."""
    from ..core.agent_manager import AgentManager
    from ..core.config_manager import ConfigManager
    
    cm = ConfigManager()
    configured_agents = set(cm.get_agents())
    all_agents = AgentManager.get_all_agents()
    
    if output_json:
        import json
        output = {
            "configured_count": len(configured_agents),
            "available_count": len(all_agents),
            "agents": [
                {
                    "id": agent.id,
                    "name": agent.name,
                    "description": agent.description,
                    "website": agent.website,
                    "configured": agent.id in configured_agents
                }
                for agent in all_agents
            ]
        }
        click.echo(json.dumps(output, indent=2))
        return
    
    # Rich output
    click.echo(f"🤖 AI Agents")
    click.echo(f"   {len(configured_agents)} configured • {len(all_agents)} available\n")
    
    for agent in all_agents:
        status = "✓" if agent.id in configured_agents else "·"
        click.echo(f" {status} {agent.name}")
        click.echo(f"   ID: {agent.id}")
        click.echo(f"   {agent.description}")
        if agent.website:
            click.echo(f"   Website: {agent.website}")
        click.echo()


@agent.command("add")
@click.argument("agent_id")
@click.option("--quiet", "-q", is_flag=True, help="Suppress non-essential output")
@click.pass_context
def agent_add(ctx: click.Context, agent_id: str, quiet: bool) -> None:
    """
    Add one or more AI agents to your project.
    
    \b
    Examples:
      stride agent add claude
      stride agent add claude copilot chatgpt
      stride agent add cursor --quiet
    """
    from ..core.agent_manager import AgentManager
    from ..core.config_manager import ConfigManager
    
    # Validate agent ID
    agent_id = agent_id.lower().strip()
    valid_ids, invalid_ids = AgentManager.validate_agent_ids([agent_id])
    
    if invalid_ids:
        click.echo(f"❌ Invalid agent ID: {agent_id}", err=True)
        click.echo(f"\nAvailable agents: {', '.join(AgentManager.get_agent_ids())}")
        click.echo("\nUse 'stride agent list' to see all available agents")
        sys.exit(1)
    
    # Add agent to config
    cm = ConfigManager()
    current_agents = set(cm.get_agents())
    
    if agent_id in current_agents:
        if not quiet:
            agent_name = AgentManager.get_agent_display_name(agent_id)
            click.echo(f"ℹ️  Already configured: {agent_name}")
    else:
        cm.add_agent(agent_id)
        if not quiet:
            agent_name = AgentManager.get_agent_display_name(agent_id)
            click.echo(f"✅ Added agent: {agent_name}")
            all_configured = cm.get_agents()
            click.echo(f"📋 Total configured agents: {len(all_configured)}")


@agent.command("remove")
@click.argument("agent_id")
@click.option("--quiet", "-q", is_flag=True, help="Suppress non-essential output")
@click.pass_context
def agent_remove(ctx: click.Context, agent_id: str, quiet: bool) -> None:
    """
    Remove an AI agent from your project.
    
    \b
    Example:
      stride agent remove claude
    """
    from ..core.agent_manager import AgentManager
    from ..core.config_manager import ConfigManager
    
    agent_id = agent_id.lower().strip()
    cm = ConfigManager()
    current_agents = set(cm.get_agents())
    
    if agent_id not in current_agents:
        if not quiet:
            click.echo(f"ℹ️  Agent not configured: {agent_id}")
    else:
        cm.remove_agent(agent_id)
        if not quiet:
            agent_name = AgentManager.get_agent_display_name(agent_id)
            click.echo(f"✅ Removed agent: {agent_name}")
            remaining = cm.get_agents()
            click.echo(f"📋 Remaining agents: {len(remaining)}")


@agent.command("info")
@click.argument("agent_id")
@click.pass_context
def agent_info(ctx: click.Context, agent_id: str) -> None:
    """
    Show detailed information about a specific AI agent.
    
    \b
    Example:
      stride agent info claude
    """
    from ..core.agent_manager import AgentManager
    from ..core.config_manager import ConfigManager
    
    agent_id = agent_id.lower().strip()
    agent = AgentManager.get_agent(agent_id)
    
    if not agent:
        click.echo(f"❌ Unknown agent: {agent_id}", err=True)
        click.echo(f"\nAvailable agents: {', '.join(AgentManager.get_agent_ids())}")
        click.echo("\nUse 'stride agent list' to see all available agents")
        sys.exit(1)
    
    cm = ConfigManager()
    configured_agents = cm.get_agents()
    is_configured = agent_id in configured_agents
    
    # Display agent info
    click.echo(f"\n🤖 {agent.name}")
    click.echo(f"{'='  * (len(agent.name) + 3)}")
    click.echo(f"\nID: {agent.id}")
    click.echo(f"Description: {agent.description}")
    if agent.website:
        click.echo(f"Website: {agent.website}")
    click.echo(f"\nConfigured: {'✓ Yes' if is_configured else '✗ No'}")
    
    if is_configured:
        click.echo("\n💡 Remove with: stride agent remove " + agent.id)
    else:
        click.echo("\n💡 Add to project with: stride agent add " + agent.id)
    click.echo()


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
                # Use type() comparison for better compatibility
                if type(value).__name__ in ('dict', 'list'):
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


# ============================================================================
# Export Command
# ============================================================================

@cli.command()
@click.option("--format", "-f", "output_format", type=click.Choice(["json", "markdown", "csv", "html"]), default="markdown", help="Export format")
@click.option("--status", "-s", type=click.Choice(["proposed", "active", "blocked", "review", "completed"]), multiple=True, help="Filter by status (can specify multiple)")
@click.option("--since", help="Filter sprints created since date (YYYY-MM-DD)")
@click.option("--until", help="Filter sprints created until date (YYYY-MM-DD)")
@click.option("--user", "-u", help="Filter by author email")
@click.option("--priority", "-p", type=click.Choice(["critical", "high", "medium", "low"]), help="Filter by priority")
@click.option("--tag", "-t", "tags", multiple=True, help="Filter by tag (can specify multiple)")
@click.option("--agent", "-a", "agents", multiple=True, help="Filter by agent (can specify multiple)")
@click.option("--output", "-o", type=click.Path(), help="Output file path (default: auto-generated)")
@click.option("--all", "export_all", is_flag=True, help="Export all sprints (no filters)")
@click.pass_context
def export(
    ctx: click.Context,
    output_format: str,
    status: tuple,
    since: Optional[str],
    until: Optional[str],
    user: Optional[str],
    priority: Optional[str],
    tags: tuple,
    agents: tuple,
    output: Optional[str],
    export_all: bool,
) -> None:
    """
    Export sprint data for reporting and integration.
    
    Supports multiple formats: JSON, Markdown, CSV, HTML.
    Use filters to export specific sprints or --all for complete export.
    
    Examples:
      stride export --format json --status completed
      stride export --format markdown --since 2025-01-01
      stride export --format html --user dev@example.com --output report.html
      stride export --all --format csv
    """
    from stride.export.export_engine import ExportEngine, ExportFilter
    from stride.export.formatters import JSONFormatter, MarkdownFormatter, CSVFormatter, HTMLFormatter
    from datetime import datetime
    from pathlib import Path
    
    sm: SprintManager = ctx.obj["sprint_manager"]
    fm: FolderManager = ctx.obj["folder_manager"]
    quiet = ctx.obj.get("quiet", False)
    
    try:
        # Create export engine
        engine = ExportEngine(sm, fm)
        
        # Register formatters
        engine.register_formatter("json", JSONFormatter(indent=2))
        engine.register_formatter("markdown", MarkdownFormatter())
        engine.register_formatter("csv", CSVFormatter())
        engine.register_formatter("html", HTMLFormatter())
        
        # Build filter
        filter_criteria = None
        if not export_all:
            # Parse dates
            since_date = None
            until_date = None
            
            if since:
                try:
                    since_date = datetime.strptime(since, "%Y-%m-%d")
                except ValueError:
                    click.echo(f"❌ Invalid date format for --since: {since} (use YYYY-MM-DD)", err=True)
                    sys.exit(1)
            
            if until:
                try:
                    until_date = datetime.strptime(until, "%Y-%m-%d")
                except ValueError:
                    click.echo(f"❌ Invalid date format for --until: {until} (use YYYY-MM-DD)", err=True)
                    sys.exit(1)
            
            # Convert status strings to SprintStatus
            status_enums = []
            if status:
                for s in status:
                    try:
                        status_enums.append(SprintStatus(s))
                    except ValueError:
                        click.echo(f"❌ Invalid status: {s}", err=True)
                        sys.exit(1)
            
            # Create filter if any criteria specified
            if any([status_enums, since_date, until_date, user, priority, tags, agents]):
                filter_criteria = ExportFilter(
                    status=status_enums or None,
                    since=since_date,
                    until=until_date,
                    author=user,
                    priority=priority,
                    tags=list(tags) if tags else None,
                    agents=list(agents) if agents else None,
                )
        
        # Determine output path
        if output:
            output_path = Path(output)
        else:
            # Auto-generate output path
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            formatter = engine.formatters[output_format]
            extension = formatter.get_extension()
            output_path = Path(f"stride-export-{timestamp}.{extension}")
        
        # Export data
        if not quiet:
            if RICH_AVAILABLE:
                rprint(f"[bold cyan]📤 Exporting sprints...[/bold cyan]")
            else:
                click.echo("📤 Exporting sprints...")
        
        export_data = engine.export(
            format_name=output_format,
            filter_criteria=filter_criteria,
            output_path=output_path,
        )
        
        # Success message
        if not quiet:
            if RICH_AVAILABLE:
                rprint(f"\n[bold green]✅ Export complete![/bold green]")
                rprint(f"   [dim]Output:[/dim] {output_path}")
                rprint(f"   [dim]Format:[/dim] {output_format}")
                rprint(f"   [dim]Size:[/dim] {len(export_data)} characters")
                
                # Show filter summary
                if filter_criteria:
                    rprint(f"\n[bold]Filters applied:[/bold]")
                    if filter_criteria.status:
                        status_names = [s.value for s in filter_criteria.status]
                        rprint(f"   • Status: {', '.join(status_names)}")
                    if filter_criteria.since:
                        rprint(f"   • Since: {filter_criteria.since.strftime('%Y-%m-%d')}")
                    if filter_criteria.until:
                        rprint(f"   • Until: {filter_criteria.until.strftime('%Y-%m-%d')}")
                    if filter_criteria.author:
                        rprint(f"   • Author: {filter_criteria.author}")
                    if filter_criteria.priority:
                        rprint(f"   • Priority: {filter_criteria.priority}")
                    if filter_criteria.tags:
                        rprint(f"   • Tags: {', '.join(filter_criteria.tags)}")
                    if filter_criteria.agents:
                        rprint(f"   • Agents: {', '.join(filter_criteria.agents)}")
            else:
                click.echo(f"\n✅ Export complete!")
                click.echo(f"   Output: {output_path}")
                click.echo(f"   Format: {output_format}")
    
    except ValueError as e:
        click.echo(f"❌ {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"❌ Export failed: {e}", err=True)
        sys.exit(1)


def _print_config_tree(config, title: str, indent: int = 0) -> None:
    """Helper function to print configuration as a tree using Rich."""
    if not RICH_AVAILABLE:
        return
    
    if indent == 0:
        rprint(f"\n[bold cyan]=== {title} ===[/bold cyan]\n")
    
    for key, value in config.items():
        prefix = "  " * indent
        # Use type() comparison instead of isinstance for better compatibility
        if type(value).__name__ == 'dict':
            rprint(f"{prefix}[bold yellow]{key}:[/bold yellow]")
            _print_config_tree(value, title, indent + 1)
        elif type(value).__name__ == 'list':
            rprint(f"{prefix}[bold yellow]{key}:[/bold yellow] [dim]{value}[/dim]")
        else:
            rprint(f"{prefix}[bold yellow]{key}:[/bold yellow] {value}")


if __name__ == "__main__":
    cli()
