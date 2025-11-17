"""
Main CLI entry point for Stride.
"""
import click
from pathlib import Path

from stride import __version__


@click.group()
@click.version_option(version=__version__, prog_name="stride")
@click.pass_context
def cli(ctx: click.Context) -> None:
    """
    Stride - Sprint-Powered, Spec-Driven Development for AI Agents
    
    A framework that combines spec-first development with agile sprint methodology,
    designed to work seamlessly with AI coding agents.
    """
    ctx.ensure_object(dict)
    ctx.obj["project_root"] = Path.cwd()


@cli.command()
def version() -> None:
    """Display Stride version information."""
    click.echo(f"Stride version {__version__}")
    click.echo("Sprint-Powered, Spec-Driven Development for AI Agents")


if __name__ == "__main__":
    cli()
