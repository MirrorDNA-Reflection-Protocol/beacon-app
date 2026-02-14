#!/usr/bin/env python3
"""
Voice DNA Extractor
Analyzes Paul's existing writings to extract a voice profile
(tone, vocabulary, sentence structure) used as system context for synthesis.
"""

import json
import re
import sys
from collections import Counter
from pathlib import Path

import yaml
from rich.console import Console
from rich.panel import Panel

console = Console()


def load_config(path: str = None) -> dict:
    cfg_path = Path(path or Path(__file__).parent / "config.yaml")
    with open(cfg_path) as f:
        return yaml.safe_load(f)


def collect_writings(config: dict) -> list[str]:
    """Collect all markdown writings from vault for analysis."""
    writings = []
    sample_count = config["voice"].get("sample_count", 50)

    for vault_path in config["vault"]["paths"]:
        vp = Path(vault_path).expanduser()
        if not vp.exists():
            continue
        for fp in sorted(vp.rglob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True):
            try:
                content = fp.read_text(encoding="utf-8")
                # Strip YAML frontmatter if present
                if content.startswith("---"):
                    parts = content.split("---", 2)
                    if len(parts) >= 3:
                        content = parts[2]
                writings.append(content.strip())
            except Exception:
                continue
            if len(writings) >= sample_count:
                break

    return writings


def analyze_sentence_patterns(writings: list[str]) -> dict:
    """Analyze sentence length, structure, and patterns."""
    all_sentences = []
    for w in writings:
        sentences = re.split(r'[.!?]+', w)
        all_sentences.extend([s.strip() for s in sentences if len(s.strip()) > 10])

    lengths = [len(s.split()) for s in all_sentences]
    avg_length = sum(lengths) / max(len(lengths), 1)

    # Sentence starters
    starters = Counter()
    for s in all_sentences:
        words = s.split()
        if words:
            starters[words[0].lower()] += 1

    return {
        "avg_sentence_length": round(avg_length, 1),
        "total_sentences_analyzed": len(all_sentences),
        "preferred_length_range": f"{int(avg_length * 0.5)}-{int(avg_length * 1.5)} words",
        "top_sentence_starters": dict(starters.most_common(15)),
    }


def analyze_vocabulary(writings: list[str]) -> dict:
    """Extract vocabulary patterns and signature words."""
    all_words = []
    for w in writings:
        words = re.findall(r'\b[a-zA-Z]{3,}\b', w.lower())
        all_words.extend(words)

    word_freq = Counter(all_words)

    # Filter out common stop words
    stop_words = {
        "the", "and", "that", "this", "with", "for", "are", "but", "not",
        "you", "all", "can", "had", "from", "have", "was", "were", "they",
        "been", "has", "its", "will", "would", "about", "their", "what",
        "which", "when", "one", "your", "there", "how", "than", "into",
        "could", "more", "some", "other", "also", "just", "like", "over",
    }

    signature_words = {
        word: count for word, count in word_freq.most_common(100)
        if word not in stop_words
    }

    return {
        "unique_vocabulary_size": len(set(all_words)),
        "total_words_analyzed": len(all_words),
        "signature_words": dict(list(signature_words.items())[:30]),
    }


def analyze_tone(writings: list[str]) -> dict:
    """Detect tone markers."""
    total = len(writings)
    questions = sum(1 for w in writings if "?" in w)
    exclamations = sum(1 for w in writings if "!" in w)
    hedges = sum(
        1 for w in writings
        for h in ["maybe", "perhaps", "might", "could be", "i think", "possibly"]
        if h in w.lower()
    )
    directives = sum(
        1 for w in writings
        for d in ["must", "should", "need to", "have to", "will"]
        if d in w.lower()
    )

    return {
        "question_frequency": round(questions / max(total, 1), 3),
        "exclamation_frequency": round(exclamations / max(total, 1), 3),
        "hedge_frequency": round(hedges / max(total, 1), 3),
        "directive_frequency": round(directives / max(total, 1), 3),
        "tone_assessment": (
            "Direct and declarative"
            if hedges < directives
            else "Exploratory and questioning"
        ),
    }


def extract_voice_dna(config: dict) -> dict:
    """Full voice extraction pipeline."""
    console.print(Panel(
        "[bold]Voice DNA Extractor[/bold]\n"
        "Analyzing writings for tone, vocabulary, and structure",
        title="⟡ VOICE",
        border_style="yellow",
    ))

    writings = collect_writings(config)
    if not writings:
        console.print("[red]No writings found to analyze.[/red]")
        return {}

    console.print(f"[dim]Analyzing {len(writings)} documents...[/dim]")

    sentences = analyze_sentence_patterns(writings)
    vocabulary = analyze_vocabulary(writings)
    tone = analyze_tone(writings)

    profile = {
        "author": "Paul Desai",
        "extracted_from": f"{len(writings)} documents",
        "sentence_patterns": sentences,
        "vocabulary": vocabulary,
        "tone": tone,
        "summary": (
            f"Voice: Paul Desai — {tone['tone_assessment']}. "
            f"Average sentence length: {sentences['avg_sentence_length']} words. "
            f"Vocabulary size: {vocabulary['unique_vocabulary_size']} unique terms. "
            f"Signature words: {', '.join(list(vocabulary['signature_words'].keys())[:10])}. "
            f"Tone: {'Low hedge' if tone['hedge_frequency'] < 0.1 else 'Moderate hedge'}, "
            f"{'high directive' if tone['directive_frequency'] > 0.3 else 'moderate directive'}."
        ),
    }

    # Save profile
    profile_path = Path(__file__).parent / config["voice"]["profile_path"]
    with open(profile_path, "w") as f:
        json.dump(profile, f, indent=2)

    console.print(f"[green]⟡ Voice profile saved: {profile_path}[/green]")
    console.print(Panel(profile["summary"], title="Voice Summary", border_style="green"))

    return profile


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Extract Voice DNA from writings")
    parser.add_argument("--config", "-c", default=None, help="Config path")
    args = parser.parse_args()

    config = load_config(args.config)
    extract_voice_dna(config)


if __name__ == "__main__":
    main()
