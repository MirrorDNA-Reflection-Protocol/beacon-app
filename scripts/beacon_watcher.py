#!/usr/bin/env python3
"""
Beacon Watcher — Truth-First Pipeline
Monitors the Obsidian Vault for new fragments and triggers synthesis.
"""

import os
import sys
import subprocess
import time
from pathlib import Path

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from rich.console import Console

console = Console()

VAULT_WATCH_PATH = Path("~/MirrorDNA-Vault/Daily Briefs").expanduser()
ENGINE_PATH = Path(__file__).parent.parent / "engine" / "synthesize.py"
PUBLISH_PATH = Path(__file__).parent.parent / "scripts" / "publish.sh"
SIDECAR_PATH = Path(__file__).parent.parent / "engine" / "sidecar_gen.py"

class BeaconHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith(".md"):
            self.trigger_pipeline(event.src_path)

    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith(".md"):
            self.trigger_pipeline(event.src_path)

    def trigger_pipeline(self, file_path):
        console.print(f"[bold yellow]⟡ Change detected in vault: {file_path}[/bold yellow]")
        
        # Debounce to allow multiple rapid writes
        time.sleep(2)
        
        try:
            # 1. Run Synthesis
            console.print("[cyan]→ Triggering Synthesis Engine...[/cyan]")
            subprocess.run([sys.executable, str(ENGINE_PATH)], check=True)
            
            # 2. Generate Sidecars
            console.print("[cyan]→ Regenerating Semantic Sidecars...[/cyan]")
            subprocess.run([sys.executable, str(SIDECAR_PATH)], check=True)
            
            # 3. Notify (Local macOS notification)
            self.notify("Beacon Ready", "A new reflection has been synthesized. Review draft at ~/repos/truth-first-beacon/content/reflections/")
            
            console.print("[bold green]✓ Pipeline triggered successfully.[/bold green]")
        except subprocess.CalledProcessError as e:
            console.print(f"[red]Pipeline failed: {e}[/red]")
            self.notify("Beacon Error", f"Synthesis pipeline failed: {e}")

    def notify(self, title, message):
        """Send a macOS system notification."""
        cmd = f'display notification "{message}" with title "{title}"'
        subprocess.run(["osascript", "-e", cmd])

if __name__ == "__main__":
    import sys
    
    if not VAULT_WATCH_PATH.exists():
        console.print(f"[red]Error: Watch path {VAULT_WATCH_PATH} does not exist.[/red]")
        sys.exit(1)

    console.print(f"[bold green]⟡ Beacon Watcher active.[/bold green]")
    console.print(f"  Monitoring: {VAULT_WATCH_PATH}")
    
    event_handler = BeaconHandler()
    observer = Observer()
    observer.schedule(event_handler, str(VAULT_WATCH_PATH), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
