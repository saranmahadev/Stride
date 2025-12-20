"""
Implementation of 'stride marker view' command.
"""

import typer
from rich.console import Console
from rich.table import Table
from rich.tree import Tree
from rich.panel import Panel
from rich.syntax import Syntax
from typing import Optional
from pathlib import Path
from stride.core.nice_parser import parse_directory, parse_file, build_dependency_graph, NiceBlock

console = Console()

def view_markers(
    path: str = typer.Argument(".", help="Path to scan for markers"),
    intent_type: Optional[str] = typer.Option(None, "--type", "-t", help="Filter by intent type"),
    uid_pattern: Optional[str] = typer.Option(None, "--uid", "-u", help="Filter by UID pattern"),
    domain: Optional[str] = typer.Option(None, "--domain", "-d", help="Filter by domain"),
    graph: bool = typer.Option(False, "--graph", "-g", help="Display dependency graph"),
    stats: bool = typer.Option(False, "--stats", "-s", help="Show coverage statistics"),
    missing: bool = typer.Option(False, "--missing", "-m", help="Show files without markers"),
    file_path: Optional[str] = typer.Option(None, "--file", "-f", help="View markers in specific file"),
):
    """
    Visualize and navigate NICE markers.
    """
    target_path = file_path if file_path else path
    
    if file_path:
        blocks = parse_file(file_path)
    else:
        blocks = parse_directory(target_path)

    if not blocks:
        console.print(f"[yellow]No NICE markers found in {target_path}[/yellow]")
        return

    # Filtering
    if intent_type:
        blocks = [b for b in blocks if b.intent_type.upper() == intent_type.upper()]
    
    if uid_pattern:
        import fnmatch
        blocks = [b for b in blocks if fnmatch.fnmatch(b.uid, uid_pattern)]
        
    if domain:
        blocks = [b for b in blocks if f":{domain}:" in b.uid]

    if not blocks:
        console.print("[yellow]No markers matched the filters.[/yellow]")
        return

    if graph:
        show_graph(blocks)
    elif stats:
        show_stats(blocks, target_path)
    elif missing:
        show_missing(blocks, target_path)
    elif uid_pattern and len(blocks) == 1:
        show_detail(blocks[0])
    else:
        show_list(blocks)

def show_list(blocks):
    table = Table(title="NICE Markers")
    table.add_column("Location", style="cyan")
    table.add_column("UID", style="green")
    table.add_column("Type", style="magenta")
    table.add_column("Description")

    for block in blocks:
        desc = block.tags.get('desc', '')
        rel_path = Path(block.file_path).name
        location = f"{rel_path}:{block.line_range[0]}"
        table.add_row(location, block.uid, block.intent_type, desc)

    console.print(table)

def show_detail(block: NiceBlock):
    console.print(Panel(f"[bold green]{block.uid}[/bold green]", title="NICE Marker Detail"))
    
    console.print(f"[bold]Type:[/bold] {block.intent_type}")
    console.print(f"[bold]File:[/bold] {block.file_path}:{block.line_range[0]}-{block.line_range[1]}")
    
    console.print("\n[bold]Tags:[/bold]")
    for key, value in block.tags.items():
        console.print(f"  @{key}: {value}")

    # Show code snippet if possible
    try:
        with open(block.file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            # Show a bit of context around the marker
            start = max(0, block.line_range[0] - 2)
            end = min(len(lines), block.line_range[1] + 5)
            code = "".join(lines[start:end])
            syntax = Syntax(code, "python", theme="monokai", line_numbers=True, start_line=start+1)
            console.print(Panel(syntax, title="Code Context"))
    except Exception:
        pass

def show_graph(blocks):
    graph = build_dependency_graph(blocks)
    tree = Tree("Dependency Graph")
    
    # Create a map for quick lookup
    block_map = {b.uid: b for b in blocks}
    
    processed = set()
    
    def add_node(parent_node, uid):
        if uid in processed:
            parent_node.add(f"[yellow]{uid} (recursive)[/yellow]")
            return
        
        processed.add(uid)
        node = parent_node.add(f"[green]{uid}[/green]")
        
        deps = graph.get(uid, [])
        for dep in deps:
            add_node(node, dep)
            
    # Find root nodes (nodes with no incoming edges or just pick all)
    # For simplicity, just list all top-level blocks
    for block in blocks:
        if block.uid not in processed:
             # Check if it's a root (not depended on by others in this set)
             # This is a simplification
             node = tree.add(f"[bold blue]{block.uid}[/bold blue]")
             deps = graph.get(block.uid, [])
             for dep in deps:
                 # Simple tree view, not full graph
                 node.add(f"[dim]{dep}[/dim]")

    console.print(tree)

def show_stats(blocks, path):
    total = len(blocks)
    types = {}
    domains = {}
    
    for block in blocks:
        types[block.intent_type] = types.get(block.intent_type, 0) + 1
        parts = block.uid.split(':')
        if len(parts) > 2:
            domain = parts[2]
            domains[domain] = domains.get(domain, 0) + 1

    console.print(Panel(f"""
[bold]Total Markers:[/bold] {total}

[bold]By Type:[/bold]
{chr(10).join([f"  {k}: {v}" for k, v in types.items()])}

[bold]By Domain:[/bold]
{chr(10).join([f"  {k}: {v}" for k, v in domains.items()])}
    """, title="NICE Marker Statistics"))

def show_missing(blocks, path):
    # This would require scanning all files and checking which ones don't have markers
    # For now, just a placeholder
    console.print("[yellow]Missing marker detection not fully implemented yet.[/yellow]")
