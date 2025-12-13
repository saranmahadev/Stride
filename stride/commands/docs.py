"""
Implementation of 'stride docs' command for serving documentation.
"""

import typer
import subprocess
import sys
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from ..core.documentation_generator import DocumentationGenerator
from ..constants import STRIDE_DIR, PROJECT_FILE
from ..core.user_context import get_username_display

console = Console()


def docs(
    port: int = typer.Option(8000, "--port", "-p", help="Port to serve documentation on"),
):
    """
    Start the MkDocs documentation server.

    Serves the project documentation at http://127.0.0.1:PORT
    """
    generator = DocumentationGenerator()

    # Check if docs directory exists
    if not generator.docs_dir.exists():
        console.print("[yellow]No 'docs/' directory found.[/yellow]")
        console.print(
            "[dim]Run the /stride:docs agent command to generate documentation first.[/dim]"
        )
        raise typer.Exit(code=1)

    # Check if mkdocs.yml exists
    if not generator.has_mkdocs_config():
        console.print("[yellow]No 'mkdocs.yml' found in docs directory.[/yellow]")
        console.print("[dim]Creating a basic MkDocs configuration...[/dim]\n")

        # Get project name
        project_name = "Project"
        project_file = Path.cwd() / STRIDE_DIR / PROJECT_FILE
        if project_file.exists():
            try:
                content = project_file.read_text(encoding="utf-8")
                lines = content.split("\n")
                for line in lines:
                    if line.startswith("# "):
                        project_name = line[2:].strip()
                        break
            except Exception:
                pass

        # Create basic config
        if generator.create_basic_mkdocs_config(project_name):
            console.print(
                "[green]✓[/green] Created basic mkdocs.yml configuration.\n"
            )
            console.print(
                "[dim]You can customize mkdocs.yml to fit your needs.[/dim]\n"
            )
        else:
            console.print("[red]Failed to create mkdocs.yml configuration.[/red]")
            raise typer.Exit(code=1)

    # Check if mkdocs is installed
    try:
        subprocess.run(
            ["mkdocs", "--version"],
            capture_output=True,
            check=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        console.print("[red]MkDocs is not installed.[/red]\n")
        console.print("Install MkDocs with:")
        console.print("  [cyan]pip install mkdocs mkdocs-material[/cyan]\n")
        console.print("Or install Stride with docs extras:")
        console.print("  [cyan]pip install stridekit[docs][/cyan]")
        raise typer.Exit(code=1)

    # Display startup message with personalized greeting
    username = get_username_display()
    info_panel = Panel(
        f"[bold cyan]Starting docs server for {username}...[/bold cyan]\n\n"
        f"[white]URL:[/white] [blue]http://127.0.0.1:{port}[/blue]\n"
        f"[white]Docs:[/white] {generator.docs_dir}\n\n"
        f"[cyan]Happy reading, {username}! 📚[/cyan]\n\n"
        f"[dim]Press Ctrl+C to stop the server[/dim]",
        border_style="blue",
        title="[bold]Documentation Server[/bold]",
    )
    console.print(info_panel)
    console.print()

    # Start MkDocs server
    try:
        subprocess.run(
            ["mkdocs", "serve", "--dev-addr", f"127.0.0.1:{port}"],
            cwd=generator.docs_dir,
        )
    except KeyboardInterrupt:
        console.print("\n[yellow]Documentation server stopped.[/yellow]")
    except subprocess.CalledProcessError as e:
        console.print(f"\n[red]Error starting MkDocs server: {e}[/red]")
        raise typer.Exit(code=1)
