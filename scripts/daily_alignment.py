#!/usr/bin/env python3
"""
Daily AI Alignment Capsule generator.

Creates a private, machine-readable daily snapshot so different AI tools can
sync from one canonical context file.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import List, Optional


DEFAULT_REPOS_ROOT = Path("/Users/mirror-admin/repos")
DEFAULT_OUTPUT_DIR = Path("/Users/mirror-admin/MirrorDNA-Vault/00_CANONICAL/AI_ALIGNMENT_CAPSULES")
DEFAULT_LATEST_PATH = Path("/Users/mirror-admin/MirrorDNA-Vault/00_CANONICAL/AI_ALIGNMENT_LATEST.md")
DEFAULT_BEACON_DEPLOY_LOG = Path("/Users/mirror-admin/repos/truth-first-beacon/deploy.log")
PRIVATE_VAULT_ROOT = Path("/Users/mirror-admin/MirrorDNA-Vault").resolve()

SERVICE_PATTERN = re.compile(
    r"(mirror|mirrordna|activemirror|beacon|kubo|ollama|redis|syncthing)",
    re.IGNORECASE,
)


@dataclass
class RepoSnapshot:
    name: str
    path: str
    branch: str
    last_commit_ts: int
    last_commit_iso: str
    last_commit_hash: str
    last_commit_subject: str
    dirty_files: int


@dataclass
class ServiceSnapshot:
    label: str
    pid: Optional[int]
    exit_status: Optional[int]
    state: str


def run_cmd(cmd: List[str]) -> str:
    proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        return ""
    return proc.stdout.strip()


def parse_int(value: str) -> Optional[int]:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def list_git_repos(root: Path) -> List[Path]:
    repos: List[Path] = []
    if not root.exists():
        return repos
    for child in sorted(root.iterdir()):
        if child.is_dir() and (child / ".git").exists():
            repos.append(child)
    return repos


def repo_snapshot(repo: Path) -> Optional[RepoSnapshot]:
    last = run_cmd(
        [
            "git",
            "-C",
            str(repo),
            "log",
            "-1",
            "--pretty=format:%ct|%cI|%h|%s",
        ]
    )
    if not last or "|" not in last:
        return None
    parts = last.split("|", 3)
    if len(parts) != 4:
        return None

    ts_raw, iso, commit_hash, subject = parts
    ts = parse_int(ts_raw)
    if ts is None:
        return None

    branch = run_cmd(["git", "-C", str(repo), "rev-parse", "--abbrev-ref", "HEAD"]) or "unknown"
    dirty_raw = run_cmd(["git", "-C", str(repo), "status", "--porcelain"])
    dirty_files = len([line for line in dirty_raw.splitlines() if line.strip()])

    return RepoSnapshot(
        name=repo.name,
        path=str(repo),
        branch=branch,
        last_commit_ts=ts,
        last_commit_iso=iso,
        last_commit_hash=commit_hash,
        last_commit_subject=subject,
        dirty_files=dirty_files,
    )


def collect_repos(root: Path) -> List[RepoSnapshot]:
    snapshots: List[RepoSnapshot] = []
    for repo in list_git_repos(root):
        snap = repo_snapshot(repo)
        if snap:
            snapshots.append(snap)
    snapshots.sort(key=lambda item: item.last_commit_ts, reverse=True)
    return snapshots


def collect_services() -> List[ServiceSnapshot]:
    raw = run_cmd(["launchctl", "list"])
    services: List[ServiceSnapshot] = []
    for line in raw.splitlines():
        if not SERVICE_PATTERN.search(line):
            continue

        cols = [col for col in line.split("\t") if col != ""]
        if len(cols) < 3:
            cols = line.split()
        if len(cols) < 3:
            continue

        pid_raw, status_raw, label = cols[0], cols[1], cols[2]
        pid = parse_int(pid_raw) if pid_raw != "-" else None
        exit_status = parse_int(status_raw) if status_raw != "-" else None
        state = "running" if pid is not None and pid > 0 else "loaded"

        services.append(
            ServiceSnapshot(
                label=label,
                pid=pid,
                exit_status=exit_status,
                state=state,
            )
        )
    services.sort(key=lambda item: (item.state != "running", item.label))
    return services


def parse_beacon_last_publish(deploy_log: Path) -> Optional[dict]:
    if not deploy_log.exists():
        return None
    lines = [line.strip() for line in deploy_log.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not lines:
        return None
    last = lines[-1]
    pieces = [part.strip() for part in last.split("|")]
    if len(pieces) < 3:
        return {"raw": last}
    ts = pieces[0]
    cid = pieces[1].replace("CID:", "").strip()
    content_hash = pieces[2].replace("Hash:", "").strip()
    return {"timestamp": ts, "cid": cid, "content_hash": content_hash}


def assert_private_path(path: Path) -> None:
    resolved = path.expanduser().resolve()
    if not resolved.is_relative_to(PRIVATE_VAULT_ROOT):
        raise ValueError(
            f"Refusing to write outside private vault root: {resolved} "
            f"(expected under {PRIVATE_VAULT_ROOT})"
        )


def format_capsule(
    now: dt.datetime,
    repos: List[RepoSnapshot],
    services: List[ServiceSnapshot],
    beacon_status: Optional[dict],
    max_repos: int,
) -> str:
    ts_now = int(now.timestamp())
    recent_24h = [r for r in repos if ts_now - r.last_commit_ts <= 24 * 3600]
    recent_7d = [r for r in repos if ts_now - r.last_commit_ts <= 7 * 24 * 3600]
    open_loops = [r for r in repos if r.dirty_files > 0]
    running_services = [s for s in services if s.state == "running"]

    lines: List[str] = []
    lines.append("---")
    lines.append("capsule_type: ai_alignment")
    lines.append("privacy: private-local")
    lines.append(f"generated_at: {now.isoformat()}")
    lines.append("source: local-machine-scan")
    lines.append("---")
    lines.append("")
    lines.append(f"# AI Alignment Capsule ({now.strftime('%Y-%m-%d')})")
    lines.append("")
    lines.append("Use this file as first-read context for all AI copilots.")
    lines.append("")
    lines.append("## System Snapshot")
    lines.append(f"- Host time: {now.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    lines.append(f"- Repos scanned: {len(repos)}")
    lines.append(f"- Active in last 24h: {len(recent_24h)}")
    lines.append(f"- Active in last 7 days: {len(recent_7d)}")
    lines.append(f"- Open loops (dirty repos): {len(open_loops)}")
    lines.append(f"- Services tracked: {len(services)} ({len(running_services)} running)")
    lines.append("")
    lines.append("## Daily Accomplishments (From Last Commit Per Active Repo)")
    if recent_24h:
        for item in recent_24h[:max_repos]:
            lines.append(
                f"- `{item.name}` ({item.last_commit_iso}): {item.last_commit_subject} [{item.last_commit_hash}]"
            )
    else:
        lines.append("- No repo commits detected in the last 24 hours.")
    lines.append("")
    lines.append("## Open Loops (Needs Attention)")
    if open_loops:
        for item in sorted(open_loops, key=lambda x: x.dirty_files, reverse=True)[:max_repos]:
            lines.append(f"- `{item.name}`: {item.dirty_files} uncommitted changes on `{item.branch}`")
    else:
        lines.append("- All scanned repos are clean.")
    lines.append("")
    lines.append("## Running Services")
    for service in running_services[:max_repos]:
        lines.append(f"- `{service.label}` (pid={service.pid}, exit={service.exit_status})")
    lines.append("")
    lines.append("## Beacon Publish State")
    if beacon_status:
        if "raw" in beacon_status:
            lines.append(f"- Last deploy log entry: `{beacon_status['raw']}`")
        else:
            lines.append(
                f"- Last publish: {beacon_status['timestamp']} | CID `{beacon_status['cid']}` | Hash `{beacon_status['content_hash']}`"
            )
    else:
        lines.append("- No publish record found.")
    lines.append("")
    lines.append("## Top Active Repos (7-Day)")
    for item in recent_7d[:max_repos]:
        lines.append(
            f"- `{item.name}` on `{item.branch}`: {item.last_commit_iso} | {item.last_commit_subject}"
        )
    lines.append("")
    lines.append("## Machine Context (JSON)")
    payload = {
        "generated_at": now.isoformat(),
        "repos_scanned": len(repos),
        "active_last_24h": [asdict(r) for r in recent_24h[:max_repos]],
        "active_last_7d": [asdict(r) for r in recent_7d[:max_repos]],
        "open_loops": [asdict(r) for r in sorted(open_loops, key=lambda x: x.dirty_files, reverse=True)[:max_repos]],
        "running_services": [asdict(s) for s in running_services[:max_repos]],
        "beacon_publish": beacon_status or {},
    }
    lines.append("```json")
    lines.append(json.dumps(payload, indent=2))
    lines.append("```")
    lines.append("")
    lines.append("> Policy: This capsule is private. Do not publish raw vault content.")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a daily AI alignment capsule.")
    parser.add_argument("--repos-root", default=str(DEFAULT_REPOS_ROOT))
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument("--latest-path", default=str(DEFAULT_LATEST_PATH))
    parser.add_argument("--beacon-deploy-log", default=str(DEFAULT_BEACON_DEPLOY_LOG))
    parser.add_argument("--max-repos", type=int, default=25)
    args = parser.parse_args()

    # Strict default perms for all files created by this process.
    os.umask(0o077)

    now = dt.datetime.now().astimezone()
    repos = collect_repos(Path(args.repos_root).expanduser())
    services = collect_services()
    beacon_status = parse_beacon_last_publish(Path(args.beacon_deploy_log).expanduser())

    capsule = format_capsule(now, repos, services, beacon_status, max_repos=args.max_repos)

    output_dir = Path(args.output_dir).expanduser()
    latest_path = Path(args.latest_path).expanduser()

    assert_private_path(output_dir)
    assert_private_path(latest_path)

    output_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
    os.chmod(output_dir, 0o700)
    out_md = output_dir / f"{now.strftime('%Y-%m-%d')}.md"
    out_json = output_dir / f"{now.strftime('%Y-%m-%d')}.json"
    latest_path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    os.chmod(latest_path.parent, 0o700)

    payload = {
        "generated_at": now.isoformat(),
        "repos_scanned": len(repos),
        "services_tracked": len(services),
        "repos": [asdict(r) for r in repos],
        "services": [asdict(s) for s in services],
        "beacon_publish": beacon_status or {},
    }

    out_md.write_text(capsule, encoding="utf-8")
    out_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    latest_path.write_text(capsule, encoding="utf-8")

    os.chmod(out_md, 0o600)
    os.chmod(out_json, 0o600)
    os.chmod(latest_path, 0o600)

    print(f"Capsule written: {out_md}")
    print(f"JSON written: {out_json}")
    print(f"Latest pointer updated: {latest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
