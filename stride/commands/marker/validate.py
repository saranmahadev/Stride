"""
Implementation of 'stride marker validate' command.
"""

import typer
from rich.console import Console
from rich.table import Table
from typing import Optional, List
from stride.core.nice_parser import parse_directory, build_dependency_graph, NiceBlock
from stride.models import MarkerValidationResult

console = Console()

def validate_markers(
    path: str = typer.Argument(".", help="Path to validate"),
    sprint_id: Optional[str] = typer.Option(None, "--sprint", help="Validate markers for specific sprint"),
    strict: bool = typer.Option(False, "--strict", help="Enforce optional tags as required"),
    fix: bool = typer.Option(False, "--fix", help="Auto-fix common issues"),
    report_file: Optional[str] = typer.Option(None, "--report", help="Export report to file"),
):
    """
    Validate NICE marker correctness and completeness.
    """
    blocks = parse_directory(path)
    
    if not blocks:
        console.print("[yellow]No markers found to validate.[/yellow]")
        return

    errors = []
    warnings = []
    
    # 1. UID Uniqueness
    uids = {}
    for block in blocks:
        if block.uid in uids:
            errors.append(f"Duplicate UID found: {block.uid} in {block.file_path} and {uids[block.uid]}")
        uids[block.uid] = block.file_path

    # 2. Dependency Validation
    graph = build_dependency_graph(blocks)
    for uid, deps in graph.items():
        for dep in deps:
            if dep not in uids:
                errors.append(f"Broken dependency: {uid} depends on missing {dep}")

    # 3. Block Validation
    for block in blocks:
        res = validate_block(block, strict)
        errors.extend([f"{block.file_path}: {e}" for e in res.errors])
        warnings.extend([f"{block.file_path}: {w}" for w in res.warnings])

    # Output results
    if errors:
        console.print(f"[bold red]Validation Failed with {len(errors)} errors:[/bold red]")
        for err in errors:
            console.print(f"  - {err}")
    else:
        console.print("[bold green]Validation Passed![/bold green]")
        
    if warnings:
        console.print(f"\n[bold yellow]{len(warnings)} Warnings:[/bold yellow]")
        for warn in warnings:
            console.print(f"  - {warn}")

def validate_block(block: NiceBlock, strict: bool) -> MarkerValidationResult:
    errors = []
    warnings = []
    
    # Check UID format
    parts = block.uid.split(':')
    if not block.uid.startswith('nice:'):
        errors.append(f"UID {block.uid} must start with 'nice:'")
    elif len(parts) < 4:
        errors.append(f"UID {block.uid} invalid format. Expected nice:type:domain:id:vN")
        
    # Check required tags
    if 'desc' not in block.tags:
        if strict:
            errors.append(f"Missing @desc tag in {block.uid}")
        else:
            warnings.append(f"Missing @desc tag in {block.uid}")
            
    # Check intent type match
    if len(parts) > 1 and parts[1].upper() != block.intent_type.upper():
        errors.append(f"UID type '{parts[1]}' does not match intent '{block.intent_type}'")

    return MarkerValidationResult(
        is_valid=len(errors) == 0,
        errors=errors,
        warnings=warnings,
        suggestions=[]
    )
