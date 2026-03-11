"""
CLI entry point for the Brownfield Cartographer.

Commands:
  analyze   Run the full analysis pipeline against a local path or GitHub URL.
  query     Launch the interactive Navigator (blast_radius, lineage, search).
  summary   Print a quick summary of an existing .cartography/ directory.
"""
from __future__ import annotations

import json
import logging
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.tree import Tree

app = typer.Typer(
    name="cartographer",
    help="Brownfield Cartographer — Codebase Intelligence System",
    add_completion=False,
)
console = Console()

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s  %(name)s  %(message)s",
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _clone_repo(url: str, target: Path) -> Path:
    """Shallow-clone a GitHub URL into target directory; return clone path."""
    console.print(f"[cyan]Cloning[/cyan] {url} ...")
    result = subprocess.run(
        ["git", "clone", "--depth=1", url, str(target)],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        console.print(f"[red]Git clone failed:[/red] {result.stderr}")
        raise typer.Exit(1)
    return target


def _resolve_repo(repo: str) -> tuple[Path, bool]:
    """
    Accept either a local filesystem path or a GitHub URL.
    Returns (local_path, is_temp) where is_temp=True means we cloned it
    into a temp dir that the caller should clean up.
    """
    if repo.startswith("http://") or repo.startswith("https://") or repo.startswith("git@"):
        tmp = Path(tempfile.mkdtemp(prefix="cartographer_"))
        clone_path = tmp / "repo"
        _clone_repo(repo, clone_path)
        return clone_path, True
    path = Path(repo).resolve()
    if not path.exists():
        console.print(f"[red]Path not found:[/red] {path}")
        raise typer.Exit(1)
    return path, False


# ---------------------------------------------------------------------------
# analyze command
# ---------------------------------------------------------------------------

@app.command()
def analyze(
    repo: str = typer.Argument(..., help="Local path or GitHub URL to analyse"),
    output: Optional[Path] = typer.Option(
        None, "--output", "-o",
        help="Output directory for .cartography/ artefacts (default: <repo>/.cartography/)",
    ),
    incremental: bool = typer.Option(
        False, "--incremental", "-i",
        help="Only re-analyse files changed since last run",
    ),
    git_days: int = typer.Option(
        30, "--git-days",
        help="Days of git history for change-velocity calculation",
    ),
) -> None:
    """Run the full Surveyor + Hydrologist analysis pipeline."""
    from src.orchestrator import Orchestrator

    repo_path, is_temp = _resolve_repo(repo)
    try:
        console.rule("[bold cyan]Brownfield Cartographer — Analysis[/bold cyan]")
        console.print(f"[bold]Target:[/bold] {repo_path}")

        orchestrator = Orchestrator(
            repo_path=repo_path,
            output_dir=output,
            incremental=incremental,
        )
        result = orchestrator.run()

        # ── Rich summary output ──────────────────────────────────────
        console.print()
        console.print(Panel.fit(
            f"[green]✓ Analysis complete[/green]  ({result.analysis_duration_seconds:.1f}s)\n"
            f"Artefacts → [bold]{orchestrator.output_dir}[/bold]",
            title="Done",
        ))

        # Module graph summary
        mg = result.module_graph
        mg_table = Table(title="Module Graph", show_header=True, header_style="bold magenta")
        mg_table.add_column("Metric", style="cyan")
        mg_table.add_column("Value", justify="right")
        mg_table.add_row("Modules parsed", str(len(mg.nodes)))
        mg_table.add_row("Import edges", str(len(mg.edges)))
        mg_table.add_row("Circular deps", str(len(mg.circular_dependencies)))
        console.print(mg_table)

        if mg.architectural_hubs:
            hub_tree = Tree("[bold]Architectural Hubs (top PageRank)[/bold]")
            for hub in mg.architectural_hubs[:5]:
                hub_tree.add(hub)
            console.print(hub_tree)

        if mg.circular_dependencies:
            console.print(f"[yellow]⚠ Circular dependencies detected:[/yellow]")
            for cycle in mg.circular_dependencies[:3]:
                console.print(f"  → {' ↔ '.join(cycle)}")

        # Lineage summary
        lg = result.lineage_graph
        lg_table = Table(title="Data Lineage Graph", show_header=True, header_style="bold magenta")
        lg_table.add_column("Metric", style="cyan")
        lg_table.add_column("Value", justify="right")
        lg_table.add_row("Datasets", str(len(lg.dataset_nodes)))
        lg_table.add_row("Transformations", str(len(lg.transformation_nodes)))
        lg_table.add_row("Sources (ingestion)", str(len(lg.sources)))
        lg_table.add_row("Sinks (output)", str(len(lg.sinks)))
        console.print(lg_table)

        if lg.sources:
            console.print(f"[green]Data sources:[/green] {', '.join(sorted(lg.sources)[:8])}")
        if lg.sinks:
            console.print(f"[blue]Data sinks:[/blue]   {', '.join(sorted(lg.sinks)[:8])}")

        if result.errors:
            console.print(f"\n[red]Errors ({len(result.errors)}):[/red]")
            for err in result.errors:
                console.print(f"  • {err}")

    finally:
        if is_temp:
            shutil.rmtree(repo_path.parent, ignore_errors=True)


# ---------------------------------------------------------------------------
# query command  (Navigator)
# ---------------------------------------------------------------------------

@app.command()
def query(
    repo: str = typer.Argument(..., help="Local path to an already-analysed repo"),
    cartography_dir: Optional[Path] = typer.Option(
        None, "--cartography-dir", "-c",
        help="Path to .cartography/ output (default: <repo>/.cartography/)",
    ),
) -> None:
    """Interactive query interface: blast_radius, trace_lineage, module info."""
    repo_path = Path(repo).resolve()
    cart_dir = cartography_dir or (repo_path / ".cartography")

    if not cart_dir.exists():
        console.print(f"[red]No .cartography/ directory found at {cart_dir}[/red]")
        console.print("Run [bold]cartographer analyze[/bold] first.")
        raise typer.Exit(1)

    # Load graphs from cached JSON
    mg_path = cart_dir / "module_graph.json"
    lg_path = cart_dir / "lineage_graph.json"

    from src.models import ModuleGraph, DataLineageGraph
    from src.graph.knowledge_graph import KnowledgeGraph

    module_graph = None
    lineage_graph = None

    if mg_path.exists():
        try:
            module_graph = ModuleGraph.model_validate_json(mg_path.read_text())
        except Exception as e:
            console.print(f"[yellow]Warning: could not load module_graph.json: {e}[/yellow]")

    if lg_path.exists():
        try:
            lineage_graph = DataLineageGraph.model_validate_json(lg_path.read_text())
        except Exception as e:
            console.print(f"[yellow]Warning: could not load lineage_graph.json: {e}[/yellow]")

    # Rebuild KG for graph traversal
    kg = KnowledgeGraph()
    if module_graph:
        for node in module_graph.nodes.values():
            kg.add_module(node)
        for edge in module_graph.edges:
            kg.add_module_edge(edge.source, edge.target)

    if lineage_graph:
        for node in lineage_graph.dataset_nodes.values():
            kg.add_dataset(node)
        for node in lineage_graph.transformation_nodes.values():
            kg.add_transformation(node)

    console.rule("[bold cyan]Navigator — Interactive Query[/bold cyan]")
    console.print("Commands: [bold]blast_radius <node>[/bold] | [bold]lineage <dataset>[/bold] | "
                  "[bold]module <path>[/bold] | [bold]sources[/bold] | [bold]sinks[/bold] | "
                  "[bold]hubs[/bold] | [bold]quit[/bold]")
    console.print()

    while True:
        try:
            raw = console.input("[bold cyan]navigator>[/bold cyan] ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if not raw:
            continue

        parts = raw.split(None, 1)
        cmd = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else ""

        if cmd in ("quit", "exit", "q"):
            break

        elif cmd == "blast_radius":
            if not arg:
                console.print("[red]Usage: blast_radius <node_id>[/red]")
                continue
            descendants = kg.blast_radius(arg)
            if not descendants:
                console.print(f"[yellow]No downstream dependents found for:[/yellow] {arg}")
            else:
                t = Tree(f"[bold]Blast radius of[/bold] {arg} ({len(descendants)} nodes)")
                for d in sorted(descendants)[:30]:
                    t.add(d)
                console.print(t)

        elif cmd == "lineage":
            if not arg:
                console.print("[red]Usage: lineage <dataset_name>[/red]")
                continue
            import networkx as nx
            if arg in kg.lineage_graph:
                try:
                    ancestors = list(nx.ancestors(kg.lineage_graph, arg))
                    t = Tree(f"[bold]Upstream of[/bold] {arg} ({len(ancestors)} nodes)")
                    for a in sorted(ancestors)[:30]:
                        t.add(a)
                    console.print(t)
                except Exception as e:
                    console.print(f"[red]Error: {e}[/red]")
            else:
                console.print(f"[yellow]Dataset '{arg}' not found in lineage graph[/yellow]")

        elif cmd == "module":
            if not arg:
                console.print("[red]Usage: module <path>[/red]")
                continue
            # Fuzzy match
            matches = [p for p in (module_graph.nodes if module_graph else {}) if arg in p]
            if not matches:
                console.print(f"[yellow]No module matching '{arg}'[/yellow]")
            else:
                for path in matches[:3]:
                    node = module_graph.nodes[path]
                    info = Table(title=path, show_header=False)
                    info.add_column("Key", style="cyan")
                    info.add_column("Value")
                    info.add_row("Language", str(node.language))
                    info.add_row("LOC", str(node.loc))
                    info.add_row("Complexity", f"{node.complexity_score:.0f}")
                    info.add_row("Change velocity (30d)", str(node.change_velocity_30d))
                    info.add_row("PageRank", f"{node.pagerank_score:.5f}")
                    info.add_row("Dead code candidate", str(node.is_dead_code_candidate))
                    info.add_row("Exports", ", ".join(node.exported_functions[:5]))
                    info.add_row("Imports", ", ".join(node.imports[:5]))
                    console.print(info)

        elif cmd == "sources":
            sources = kg.find_sources()
            console.print(f"[green]Data sources ({len(sources)}):[/green]")
            for s in sorted(sources):
                console.print(f"  • {s}")

        elif cmd == "sinks":
            sinks = kg.find_sinks()
            console.print(f"[blue]Data sinks ({len(sinks)}):[/blue]")
            for s in sorted(sinks):
                console.print(f"  • {s}")

        elif cmd == "hubs":
            hubs = kg.get_architectural_hubs(10)
            t = Tree("[bold]Architectural Hubs (PageRank)[/bold]")
            for hub in hubs:
                score = kg.module_graph.nodes[hub].get("pagerank_score", 0.0) if hub in kg.module_graph else 0.0
                t.add(f"{hub}  [dim]({score:.5f})[/dim]")
            console.print(t)

        else:
            console.print(f"[red]Unknown command:[/red] {cmd}")


# ---------------------------------------------------------------------------
# summary command
# ---------------------------------------------------------------------------

@app.command()
def summary(
    repo: str = typer.Argument(..., help="Local path to an already-analysed repo"),
    cartography_dir: Optional[Path] = typer.Option(None, "--cartography-dir", "-c"),
) -> None:
    """Print a quick summary of existing .cartography/ artefacts."""
    repo_path = Path(repo).resolve()
    cart_dir = cartography_dir or (repo_path / ".cartography")

    summary_file = cart_dir / "analysis_summary.md"
    if summary_file.exists():
        console.print(summary_file.read_text())
    else:
        console.print(f"[yellow]No analysis_summary.md found in {cart_dir}[/yellow]")
        console.print("Run [bold]cartographer analyze[/bold] first.")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    app()


if __name__ == "__main__":
    main()