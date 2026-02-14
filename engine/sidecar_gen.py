#!/usr/bin/env python3
"""
Semantic Sidecar Generator
Generates JSON sidecars for each Hugo post containing:
  - Pre-computed vector embeddings (all-MiniLM-L6-v2)
  - Cognitive weight maps
  - Source lineage metadata
  - Contradiction flags
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

import numpy as np
import yaml
from rich.console import Console
from rich.panel import Panel

console = Console()

# Lazy-load sentence-transformers (heavy import)
_model = None


def get_embedding_model():
    global _model
    if _model is None:
        console.print("[dim]Loading embedding model (first run may download ~90MB)...[/dim]")
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def load_config(path: str = None) -> dict:
    cfg_path = Path(path or Path(__file__).parent / "config.yaml")
    with open(cfg_path) as f:
        return yaml.safe_load(f)


def parse_hugo_post(path: Path) -> dict:
    """Parse a Hugo markdown post into frontmatter + body."""
    content = path.read_text(encoding="utf-8")
    if not content.startswith("---"):
        return {"frontmatter": {}, "body": content, "path": str(path)}

    parts = content.split("---", 2)
    if len(parts) < 3:
        return {"frontmatter": {}, "body": content, "path": str(path)}

    try:
        frontmatter = yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError:
        frontmatter = {}

    return {
        "frontmatter": frontmatter,
        "body": parts[2].strip(),
        "path": str(path),
    }


def compute_embeddings(text: str) -> list[float]:
    """Compute vector embeddings for text using all-MiniLM-L6-v2."""
    model = get_embedding_model()

    # Split into chunks if too long (model has 256 token limit ideally)
    chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]

    embeddings = model.encode(chunks, show_progress_bar=False)

    # Average embeddings across chunks
    if len(embeddings) > 1:
        avg = np.mean(embeddings, axis=0)
    else:
        avg = embeddings[0]

    return avg.tolist()


def extract_cognitive_weights(frontmatter: dict, body: str) -> dict:
    """Extract or compute cognitive weights from post."""
    # Use frontmatter weights if provided
    if "cognitive_weights" in frontmatter:
        return frontmatter["cognitive_weights"]

    # Fallback: compute from content analysis
    weight_keywords = {
        "sovereignty": ["sovereign", "self-hosted", "independence", "control", "ownership"],
        "decentralization": ["decentralized", "distributed", "peer-to-peer", "ipfs", "mesh"],
        "truth": ["truth", "honest", "verify", "authentic", "canonical"],
        "antifragility": ["antifragile", "resilient", "robust", "survive", "adapt"],
        "agency": ["agency", "autonomy", "choice", "freedom", "self-directed"],
        "infrastructure": ["infrastructure", "system", "architecture", "protocol", "stack"],
    }

    body_lower = body.lower()
    word_count = max(len(body_lower.split()), 1)
    weights = {}

    for topic, keywords in weight_keywords.items():
        hits = sum(body_lower.count(kw) for kw in keywords)
        # Normalize to 0-1 range (cap at 1.0)
        weights[topic] = round(min(hits / (word_count * 0.01), 1.0), 2)

    # Filter out zero weights
    return {k: v for k, v in weights.items() if v > 0}


def sanitize_source_path(path: str) -> str:
    """Keep lineage useful without exposing local absolute paths."""
    include_private_paths = os.environ.get("BEACON_INCLUDE_PRIVATE_PATHS", "0") == "1"
    if include_private_paths:
        return path

    source = Path(path)
    parts = source.parts

    if "content" in parts:
        idx = parts.index("content")
        return str(Path(*parts[idx:]))

    return source.name


def generate_sidecar(post: dict, config: dict) -> dict:
    """Generate a complete semantic sidecar for a post."""
    fm = post["frontmatter"]
    body = post["body"]

    # Compute embeddings
    embeddings = compute_embeddings(body)

    # Get cognitive weights
    weights = extract_cognitive_weights(fm, body)

    sidecar = {
        "source": "paul-desai-truth-first-beacon",
        "root_of_trust": True,
        "version": "1.0",
        "generated": datetime.now().isoformat(),
        "post": {
            "title": fm.get("title", "Untitled"),
            "date": str(fm.get("date", "")),
            "slug": Path(post["path"]).stem,
            "tags": fm.get("tags", []),
        },
        "embeddings": {
            "model": "all-MiniLM-L6-v2",
            "dimensions": len(embeddings),
            "vector": embeddings,
        },
        "cognitive_weights": weights,
        "contradictions": [],  # Populated by synthesis dissonance stage
        "lineage": {
            "source_path": sanitize_source_path(post["path"]),
            "source_path_policy": "content-relative",
            "vault_origin": "MirrorDNA-Vault",
        },
    }

    return sidecar


def process_all_posts(config: dict, content_dir: str = None, output_dir: str = None):
    """Generate sidecars for all posts in the content directory."""
    console.print(Panel(
        "[bold]Semantic Sidecar Generator[/bold]\n"
        "Computing embeddings and cognitive weights for all posts",
        title="◈ SIDECAR",
        border_style="yellow",
    ))

    # Resolve paths
    engine_dir = Path(__file__).parent
    c_dir = Path(content_dir or (engine_dir / config["output"]["content_dir"]))
    o_dir = Path(output_dir or (engine_dir / config["output"]["sidecar_dir"]))
    o_dir.mkdir(parents=True, exist_ok=True)

    # Find all markdown posts
    posts = list(c_dir.rglob("*.md"))
    posts = [p for p in posts if not p.name.startswith("_")]

    if not posts:
        console.print("[red]No posts found to process.[/red]")
        return

    console.print(f"[dim]Found {len(posts)} posts to process[/dim]")

    for post_path in posts:
        post = parse_hugo_post(post_path)
        if not post["body"]:
            continue

        slug = post_path.stem
        console.print(f"  ◈ Processing: [cyan]{post['frontmatter'].get('title', slug)}[/cyan]")

        sidecar = generate_sidecar(post, config)

        # Write sidecar JSON
        sidecar_path = o_dir / f"{slug}.json"
        with open(sidecar_path, "w") as f:
            json.dump(sidecar, f, indent=2)

        console.print(f"    → {sidecar_path.name} ({sidecar['embeddings']['dimensions']}d embeddings)")

    console.print(f"\n[bold green]◈ Sidecars generated: {len(posts)} files[/bold green]")
    console.print(f"  Output: {o_dir}")


def main():
    parser = argparse.ArgumentParser(description="Generate semantic sidecars for Hugo posts")
    parser.add_argument("--config", "-c", default=None, help="Config path")
    parser.add_argument("--input", "-i", default=None, help="Content directory override")
    parser.add_argument("--output", "-o", default=None, help="Sidecar output directory override")
    parser.add_argument("--single", "-s", default=None, help="Process a single post file")
    args = parser.parse_args()

    config = load_config(args.config)

    if args.single:
        post = parse_hugo_post(Path(args.single))
        sidecar = generate_sidecar(post, config)
        print(json.dumps(sidecar, indent=2))
    else:
        process_all_posts(config, args.input, args.output)


if __name__ == "__main__":
    main()
