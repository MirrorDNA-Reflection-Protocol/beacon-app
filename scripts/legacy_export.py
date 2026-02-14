#!/usr/bin/env python3
"""
Legacy Export Script — Truth-First Beacon
Bundles the Obsidian Vault into a sanitized Parquet file for future AI re-instantiation.
"""

import os
import re
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd
from rich.console import Console
from rich.panel import Panel

console = Console()

# ─── Sanitization Logic ───────────────────────────────────────────
def sanitize_content(content: str) -> str:
    """Scrub sensitive data from vault content."""
    # Scrub potential keys/passwords
    content = re.sub(r'([a-zA-Z0-9]{32,})', '[SCRUBBED_KEY]', content)
    # Scrub email addresses
    content = re.sub(r'[\w\.-]+@[\w\.-]+\.\w+', '[SCRUBBED_EMAIL]', content)
    # Scrub potential IP addresses
    content = re.sub(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', '[SCRUBBED_IP]', content)
    return content


def export_vault(vault_path: str, output_path: str):
    """Scan vault and export to Parquet."""
    console.print(Panel(
        f"[bold]Legacy Export Protocol[/bold]\nIngesting: {vault_path}\nTarget: {output_path}",
        title="⟡ LEGACY",
        border_style="red",
    ))

    vault_dir = Path(vault_path).expanduser()
    if not vault_dir.exists():
        console.print(f"[red]Vault not found at {vault_path}[/red]")
        return

    data = []
    files_processed = 0

    for fp in vault_dir.rglob("*.md"):
        try:
            content = fp.read_text(encoding="utf-8")
            sanitized = sanitize_content(content)
            
            # Metadata
            stat = fp.stat()
            data.append({
                "name": fp.stem,
                "path": str(fp.relative_to(vault_dir)),
                "content": sanitized,
                "created_at": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                "modified_at": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "size_bytes": stat.st_size,
            })
            files_processed += 1
        except Exception as e:
            console.print(f"[dim]Skipping {fp}: {e}[/dim]")

    if not data:
        console.print("[yellow]No data to export.[/yellow]")
        return

    df = pd.DataFrame(data)
    df.to_parquet(output_path, compression="snappy")
    
    console.print(f"[bold green]✓ Export successful.[/bold green]")
    console.print(f"  Processed: {files_processed} files")
    console.print(f"  Legacy Pulse: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python legacy_export.py <vault_path> <output.parquet>")
        sys.exit(1)
    
    export_vault(sys.argv[1], sys.argv[2])
