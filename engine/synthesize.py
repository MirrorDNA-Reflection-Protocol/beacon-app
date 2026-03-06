#!/usr/bin/env python3
"""
Truth-First Beacon — Synthesis Engine
Multi-stage recursive prompt pipeline:
  1. REFLECT  — Analyze day's fragments against the Obsidian Vault
  2. DISSONANCE — Identify contradictions with previous "Truths"
  3. SYNTHESIZE — Write in the Paul Desai voice

Runs locally on Ollama (qwen2.5:7b) with Groq API fallback.
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from textwrap import dedent

import httpx
import yaml
from rich.console import Console
from rich.panel import Panel
from slugify import slugify

console = Console()

# ─── Config ────────────────────────────────────────────────────────
def load_config(path: str = None) -> dict:
    cfg_path = Path(path or Path(__file__).parent / "config.yaml")
    with open(cfg_path) as f:
        return yaml.safe_load(f)


# ─── Vault Reader ──────────────────────────────────────────────────
def read_vault_fragments(config: dict, since_days: int = 7) -> list[dict]:
    """Read recent markdown fragments from vault paths."""
    fragments = []
    cutoff = datetime.now().timestamp() - (since_days * 86400)

    for vault_path in config["vault"]["paths"]:
        vp = Path(vault_path).expanduser()
        if not vp.exists():
            console.print(f"[dim]⟡ Vault path not found: {vp}[/dim]")
            continue

        extensions = config["vault"].get("extensions", [".md"])
        excludes = config["vault"].get("exclude_patterns", [])

        for fp in vp.rglob("*"):
            if not fp.is_file():
                continue
            if fp.suffix not in extensions:
                continue
            if any(fp.match(pat) for pat in excludes):
                continue
            if fp.stat().st_mtime < cutoff:
                continue

            try:
                content = fp.read_text(encoding="utf-8")
                fragments.append({
                    "path": str(fp),
                    "name": fp.stem,
                    "content": content,
                    "modified": datetime.fromtimestamp(fp.stat().st_mtime).isoformat(),
                })
            except Exception as e:
                console.print(f"[red]Error reading {fp}: {e}[/red]")

    # Also read explicit extra files (e.g., CONTINUITY.md)
    for extra in config["vault"].get("extra_files", []):
        fp = Path(extra).expanduser()
        if fp.exists() and fp.is_file():
            try:
                content = fp.read_text(encoding="utf-8")
                fragments.append({
                    "path": str(fp),
                    "name": fp.stem,
                    "content": content,
                    "modified": datetime.fromtimestamp(fp.stat().st_mtime).isoformat(),
                })
            except Exception as e:
                console.print(f"[red]Error reading {fp}: {e}[/red]")

    return sorted(fragments, key=lambda x: x["modified"], reverse=True)


# ─── LLM Interface ────────────────────────────────────────────────
def query_ollama(prompt: str, config: dict) -> str:
    """Query local Ollama instance."""
    endpoint = config["ollama"]["endpoint"]
    model = config["ollama"]["model"]

    try:
        resp = httpx.post(
            f"{endpoint}/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": config["ollama"].get("temperature", 0.7),
                    "num_predict": config["ollama"].get("max_tokens", 4096),
                },
            },
            timeout=300.0,
        )
        resp.raise_for_status()
        return resp.json()["response"]
    except Exception as e:
        console.print(f"[yellow]⟡ Ollama failed ({e}), trying Groq fallback...[/yellow]")
        return query_groq(prompt, config)


def query_groq(prompt: str, config: dict) -> str:
    """Fallback to Groq API."""
    if not config.get("groq", {}).get("enabled"):
        raise RuntimeError("Groq fallback disabled and Ollama failed")

    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY not set in environment")

    resp = httpx.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}"},
        json={
            "model": config["groq"]["model"],
            "messages": [{"role": "user", "content": prompt}],
            "temperature": config["groq"].get("temperature", 0.6),
            "max_tokens": config["groq"].get("max_tokens", 4096),
        },
        timeout=60.0,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]


def query_claude(prompt: str, config: dict) -> str:
    """Query Claude via CLI (uses Claude Pro/Max subscription, no API key needed)."""
    import subprocess
    import tempfile

    model = config["claude"].get("model", "claude-sonnet-4-5-20250929")

    # Write prompt to temp file to avoid shell escaping issues
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        f.write(prompt)
        prompt_file = f.name

    try:
        # Clean env: remove CLAUDECODE var to avoid nested session detection
        clean_env = {k: v for k, v in os.environ.items() if "CLAUDECODE" not in k.upper() and "CLAUDE_CODE" not in k.upper()}
        # Read prompt from temp file to avoid CLI argument length limits
        with open(prompt_file, "r") as pf:
            prompt_text = pf.read()
        result = subprocess.run(
            [
                "claude", "--print",
                "--model", model,
                "--max-budget-usd", "0.50",
            ],
            input=prompt_text,
            capture_output=True, text=True,
            timeout=180,
            cwd="/tmp",  # Avoid CLAUDE.md boot protocol
            env=clean_env,
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
        else:
            raise RuntimeError(f"Claude CLI failed: {result.stderr[:200]}")
    finally:
        os.unlink(prompt_file)


def query_llm(prompt: str, config: dict, stage: str = None) -> str:
    """Route to the best available LLM based on stage config."""
    # Check stage-specific routing
    if stage and "stage_models" in config:
        backend = config["stage_models"].get(stage, "ollama")
    else:
        backend = "ollama"

    if backend == "claude" and config.get("claude", {}).get("enabled"):
        try:
            return query_claude(prompt, config)
        except Exception as e:
            console.print(f"[yellow]⟡ Claude failed ({e}), falling back to Ollama...[/yellow]")
            return query_ollama(prompt, config)
    elif backend == "groq" and config.get("groq", {}).get("enabled"):
        try:
            return query_groq(prompt, config)
        except Exception as e:
            console.print(f"[yellow]⟡ Groq failed ({e}), falling back to Ollama...[/yellow]")
            return query_ollama(prompt, config)
    else:
        return query_ollama(prompt, config)


# ─── Voice DNA ─────────────────────────────────────────────────────
def load_voice_profile(config: dict) -> str:
    """Load or describe the voice profile for synthesis."""
    profile_path = Path(__file__).parent / config["voice"]["profile_path"]
    if profile_path.exists():
        with open(profile_path) as f:
            profile = json.load(f)
        return profile.get("summary", "")

    # Default voice description
    return dedent("""
        Voice: Paul Desai
        Tone: Calm, direct, warm, precise. High-signal, polymathic, minimalist.
        Style: Short paragraphs. Declarative sentences. No hedging.
        Vocabulary: Technical but accessible. Systems thinking metaphors.
        Avoids: Corporate jargon, sycophancy, unnecessary qualifiers.
        Signature: Uses "sovereign" as an adjective for self-controlled systems.
        Structure: State the thesis. Support with architecture. End with principle.
    """).strip()


# ─── Prompt Matrix (The Three Stages) ─────────────────────────────

def stage_reflect(fragments: list[dict], config: dict) -> str:
    """Stage 1: Analyze fragments against vault context."""
    fragment_text = "\n\n---\n\n".join(
        f"## {f['name']} ({f['modified']})\n{f['content'][:2000]}"
        for f in fragments[:10]
    )

    prompt = dedent(f"""
        You are a cognitive analyst. Your task is to find the SIGNAL in these fragments.

        FRAGMENTS FROM THE LAST 7 DAYS:
        {fragment_text}

        INSTRUCTIONS:
        1. Identify the 2-3 strongest threads of thought across all fragments
        2. Note any emerging patterns, obsessions, or recurring themes
        3. Flag any incomplete thoughts that need resolution
        4. Rank the threads by cognitive weight (how much mental energy they represent)

        Output a structured analysis. Be precise. No filler.
    """).strip()

    console.print("[cyan]⟡ Stage 1: REFLECT — analyzing fragments...[/cyan]")
    return query_llm(prompt, config, stage="reflect")


def stage_dissonance(reflection: str, fragments: list[dict], config: dict) -> str:
    """Stage 2: Check for contradictions with previous truths."""
    # Pull older fragments as "established truths"
    older_texts = "\n".join(
        f"- {f['name']}: {f['content'][:500]}"
        for f in fragments[10:20]  # Older fragments
    )

    prompt = dedent(f"""
        You are a dissonance detector. Your task is to find CONTRADICTIONS.

        CURRENT REFLECTION ANALYSIS:
        {reflection}

        ESTABLISHED TRUTHS (older writings):
        {older_texts if older_texts else "No older writings available for comparison."}

        INSTRUCTIONS:
        1. Compare the current reflection against established truths
        2. Identify any direct contradictions (belief A then, belief B now)
        3. Identify any evolved positions (same direction, refined)
        4. Note which contradictions represent GROWTH vs DRIFT

        For each finding, rate severity: [GROWTH] [DRIFT] [CONTRADICTION]
        Be honest. Intellectual integrity requires tracking changes in belief.
    """).strip()

    console.print("[cyan]⟡ Stage 2: DISSONANCE — checking for contradictions...[/cyan]")
    return query_llm(prompt, config, stage="dissonance")


def stage_synthesize(
    reflection: str,
    dissonance: str,
    voice: str,
    config: dict,
    title_hint: str = None,
) -> dict:
    """Stage 3: Write the article in Paul's voice."""
    prompt = dedent(f"""
        You are ghostwriting a reflection for Paul Desai's Truth-First Beacon.

        VOICE PROFILE:
        {voice}

        REFLECTION ANALYSIS (what's on his mind):
        {reflection}

        DISSONANCE CHECK (contradictions & growth):
        {dissonance}

        INSTRUCTIONS:
        1. Write a 600-1200 word reflection that synthesizes the strongest thread
        2. If there are contradictions, ADDRESS THEM — don't hide evolution
        3. Match the voice profile EXACTLY — read it carefully
        4. Structure: Opening thesis → Supporting evidence/architecture → Closing principle
        5. Include a pull quote (a single sentence that captures the core truth)

        OUTPUT FORMAT (strict):
        TITLE: [Your chosen title]
        TAGS: [comma-separated tags]
        COGNITIVE_WEIGHTS: [JSON object with topic:weight pairs, weights 0-1]
        ---
        [The full article body in markdown]
    """).strip()

    console.print("[cyan]⟡ Stage 3: SYNTHESIZE — writing in Paul's voice (via Claude)...[/cyan]")
    raw = query_llm(prompt, config, stage="synthesize")

    # Parse the structured output
    return parse_synthesis(raw, title_hint)


def parse_synthesis(raw: str, title_hint: str = None) -> dict:
    """Parse the LLM's structured output into components."""
    lines = raw.strip().split("\n")
    title = title_hint or "Untitled Reflection"
    tags = []
    weights = {}
    body_lines = []
    in_body = False

    for line in lines:
        if line.startswith("TITLE:"):
            title = line.replace("TITLE:", "").strip().strip('"')
        elif line.startswith("TAGS:"):
            raw_tags = line.replace("TAGS:", "").strip()
            tags = [t.strip().lower() for t in raw_tags.split(",")]
        elif line.startswith("COGNITIVE_WEIGHTS:"):
            raw_weights = line.replace("COGNITIVE_WEIGHTS:", "").strip()
            try:
                weights = json.loads(raw_weights)
            except json.JSONDecodeError:
                weights = {"reflection": 0.8}
        elif line.strip() == "---":
            in_body = True
        elif in_body:
            body_lines.append(line)

    return {
        "title": title,
        "tags": tags,
        "cognitive_weights": weights,
        "body": "\n".join(body_lines).strip(),
    }


# ─── Output: Hugo-Compatible Markdown ─────────────────────────────

def write_hugo_post(synthesis: dict, config: dict) -> Path:
    """Write the synthesized article as a Hugo post with frontmatter."""
    slug = slugify(synthesis["title"])
    date = datetime.now().astimezone()
    output_dir = Path(__file__).parent / config["output"]["content_dir"]
    output_dir.mkdir(parents=True, exist_ok=True)

    frontmatter = {
        "title": synthesis["title"],
        "date": date.isoformat(),
        "description": synthesis["body"][:200].replace("\n", " ").strip() + "...",
        "tags": synthesis["tags"],
        "signed": False,  # Will be true after PGP signing
        "sidecar": f"{slug}.json",
        "cognitive_weights": synthesis["cognitive_weights"],
        "draft": True,  # Always draft first, Paul reviews
    }

    post_path = output_dir / f"{slug}.md"
    with open(post_path, "w") as f:
        f.write("---\n")
        yaml.dump(frontmatter, f, default_flow_style=False, allow_unicode=True)
        f.write("---\n\n")
        f.write(synthesis["body"])
        f.write("\n")

    console.print(f"[green]⟡ Post written: {post_path}[/green]")
    return post_path


# ─── Main Pipeline ─────────────────────────────────────────────────

def run_pipeline(config: dict, since_days: int = 7, dry_run: bool = False):
    """Execute the full Truth-First synthesis pipeline."""
    console.print(Panel(
        "[bold]Truth-First Beacon — Synthesis Engine[/bold]\n"
        f"Model: {config['ollama']['model']} | Fallback: Groq\n"
        f"Scanning last {since_days} days of vault fragments",
        title="⟡ BEACON",
        border_style="yellow",
    ))

    # Step 1: Read fragments
    fragments = read_vault_fragments(config, since_days)
    if not fragments:
        console.print("[red]⟡ No fragments found in vault paths. Nothing to synthesize.[/red]")
        return

    console.print(f"[dim]Found {len(fragments)} fragments[/dim]")

    if dry_run:
        console.print("\n[yellow]─── DRY RUN ─── Showing fragments only ───[/yellow]")
        for f in fragments[:5]:
            console.print(f"  • {f['name']} ({f['modified']}) — {len(f['content'])} chars")
        return

    # Step 2: Load voice profile
    voice = load_voice_profile(config)

    # Step 3: REFLECT
    reflection = stage_reflect(fragments, config)
    console.print(Panel(reflection[:500] + "...", title="Reflection", border_style="cyan"))

    # Step 4: DISSONANCE
    dissonance = stage_dissonance(reflection, fragments, config)
    console.print(Panel(dissonance[:500] + "...", title="Dissonance", border_style="magenta"))

    # Step 5: SYNTHESIZE
    synthesis = stage_synthesize(reflection, dissonance, voice, config)
    console.print(Panel(
        f"Title: {synthesis['title']}\n"
        f"Tags: {', '.join(synthesis['tags'])}\n"
        f"Weights: {json.dumps(synthesis['cognitive_weights'], indent=2)}\n\n"
        f"{synthesis['body'][:300]}...",
        title="Synthesis",
        border_style="green",
    ))

    # Step 6: Write Hugo post
    post_path = write_hugo_post(synthesis, config)

    console.print(f"\n[bold green]⟡ Pipeline complete.[/bold green]")
    console.print(f"  Post: {post_path}")
    console.print(f"  Status: [yellow]DRAFT[/yellow] — review before publishing")
    console.print(f"  Next: Run sidecar_gen.py to generate embeddings")

    return synthesis


# ─── CLI ───────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Truth-First Beacon — Synthesis Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--config", "-c",
        default=None,
        help="Path to config.yaml (default: engine/config.yaml)",
    )
    parser.add_argument(
        "--days", "-d",
        type=int,
        default=7,
        help="Number of days to look back for fragments (default: 7)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show fragments without running synthesis",
    )
    parser.add_argument(
        "--input", "-i",
        default=None,
        help="Override vault path with a specific directory",
    )
    args = parser.parse_args()

    config = load_config(args.config)

    if args.input:
        config["vault"]["paths"] = [args.input]

    run_pipeline(config, since_days=args.days, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
