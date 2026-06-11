#!/usr/bin/env python3
"""Check Markdown lifecycle budgets for AI engineering workflow projects.

This script is a deterministic gate: it measures Markdown files and reports
whether they are within budget, near budget, over budget, or over the hard
limit. It never rewrites, compresses, archives, or deletes content.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class Budget:
    label: str
    budget_lines: int
    budget_kib: int
    hard_lines: int
    hard_kib: int


@dataclass
class Result:
    path: str
    kind: str
    status: str
    lines: int
    size_bytes: int
    budget_lines: int
    budget_bytes: int
    hard_lines: int
    hard_bytes: int
    reasons: list[str]


BUDGETS = {
    "status_or_docs_index": Budget("STATUS.md or docs/README.md", 200, 12, 300, 20),
    "project_memory": Budget("PROJECT_MEMORY.md", 300, 20, 450, 32),
    "task_or_data_spec": Budget("TASK_SPEC.md or data/README.md", 400, 32, 600, 48),
    "experiment_changelog": Budget("experiments/CHANGELOG.md", 500, 48, 800, 80),
    "experiment_report": Budget("experiments/*/report.md", 500, 48, 700, 80),
    "longform_doc": Budget("manual/design/decision doc", 600, 64, 900, 96),
    "skill_reference": Budget("Skill references/*.md", 700, 80, 900, 110),
    "generic_markdown": Budget("generic Markdown", 500, 48, 800, 80),
}

DEFAULT_IGNORE_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".mypy_cache",
    ".pytest_cache",
    "__pycache__",
    "node_modules",
    ".venv",
    "venv",
    "env",
    "tmp",
    "log",
    "logs",
    "cache",
}

STATUS_RANK = {
    "ok": 0,
    "near_budget": 1,
    "over_budget": 2,
    "over_hard_limit": 3,
}


def _norm_parts(path: Path) -> list[str]:
    return [part.lower() for part in path.parts]


def classify_markdown(path: Path) -> str:
    name = path.name.lower()
    parts = _norm_parts(path)
    parent = path.parent.name.lower()

    if name == "status.md" or (name == "readme.md" and parent == "docs"):
        return "status_or_docs_index"
    if name == "project_memory.md":
        return "project_memory"
    if name == "task_spec.md" or (name == "readme.md" and parent == "data"):
        return "task_or_data_spec"
    if name == "changelog.md" and "experiments" in parts:
        return "experiment_changelog"
    if name == "report.md" and "experiments" in parts:
        return "experiment_report"
    if parent == "references" and "skills" in parts:
        return "skill_reference"
    if any(marker in name for marker in ("manual", "design", "decision", "guide", "手册", "设计", "决策")):
        return "longform_doc"
    return "generic_markdown"


def _iter_markdown_files(paths: Iterable[Path], ignore_dirs: set[str]) -> list[Path]:
    files: list[Path] = []
    seen: set[Path] = set()
    for raw_path in paths:
        path = raw_path.resolve()
        if path.is_file():
            if path.suffix.lower() == ".md" and path not in seen:
                files.append(path)
                seen.add(path)
            continue
        if not path.is_dir():
            continue
        for candidate in path.rglob("*.md"):
            if any(part.lower() in ignore_dirs for part in candidate.relative_to(path).parts[:-1]):
                continue
            resolved = candidate.resolve()
            if resolved not in seen:
                files.append(resolved)
                seen.add(resolved)
    return sorted(files, key=lambda item: str(item).lower())


def _line_count(text: str) -> int:
    if not text:
        return 0
    return text.count("\n") + (0 if text.endswith("\n") else 1)


def check_file(path: Path) -> Result:
    kind = classify_markdown(path)
    budget = BUDGETS[kind]
    hard_bytes = budget.hard_kib * 1024
    budget_bytes = budget.budget_kib * 1024
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = _line_count(text)
    size_bytes = path.stat().st_size

    reasons: list[str] = []
    if lines > budget.hard_lines:
        reasons.append(f"lines {lines}>{budget.hard_lines} hard")
    if size_bytes > hard_bytes:
        reasons.append(f"bytes {size_bytes}>{hard_bytes} hard")
    if reasons:
        status = "over_hard_limit"
    else:
        if lines > budget.budget_lines:
            reasons.append(f"lines {lines}>{budget.budget_lines} budget")
        if size_bytes > budget_bytes:
            reasons.append(f"bytes {size_bytes}>{budget_bytes} budget")
        if reasons:
            status = "over_budget"
        elif lines >= int(budget.budget_lines * 0.8) or size_bytes >= int(budget_bytes * 0.8):
            status = "near_budget"
        else:
            status = "ok"

    return Result(
        path=str(path),
        kind=kind,
        status=status,
        lines=lines,
        size_bytes=size_bytes,
        budget_lines=budget.budget_lines,
        budget_bytes=budget_bytes,
        hard_lines=budget.hard_lines,
        hard_bytes=hard_bytes,
        reasons=reasons,
    )


def _filter_results(results: list[Result], show: str) -> list[Result]:
    if show == "all":
        return results
    if show == "issues":
        return [result for result in results if result.status != "ok"]
    if show == "hard":
        return [result for result in results if result.status == "over_hard_limit"]
    raise ValueError(f"unknown show mode: {show}")


def _print_table(results: list[Result], show: str) -> None:
    visible = _filter_results(results, show)
    if not visible:
        print(f"Markdown budget check OK ({len(results)} files checked).")
        return

    print("| Status | Lines | Bytes | Budget | Hard limit | Kind | Path | Reasons |")
    print("|---|---:|---:|---:|---:|---|---|---|")
    for result in visible:
        budget = f"{result.budget_lines}/{result.budget_bytes}"
        hard = f"{result.hard_lines}/{result.hard_bytes}"
        reasons = "; ".join(result.reasons) or "-"
        print(
            f"| {result.status} | {result.lines} | {result.size_bytes} | "
            f"{budget} | {hard} | {result.kind} | `{result.path}` | {reasons} |"
        )


def _exit_code(results: list[Result], fail_on: str) -> int:
    worst = max((STATUS_RANK[result.status] for result in results), default=0)
    if fail_on == "never":
        return 0
    if fail_on == "hard":
        return 2 if worst >= STATUS_RANK["over_hard_limit"] else 0
    if fail_on == "budget":
        if worst >= STATUS_RANK["over_hard_limit"]:
            return 2
        return 1 if worst >= STATUS_RANK["over_budget"] else 0
    if fail_on == "near":
        if worst >= STATUS_RANK["over_hard_limit"]:
            return 2
        if worst >= STATUS_RANK["over_budget"]:
            return 1
        return 3 if worst >= STATUS_RANK["near_budget"] else 0
    raise ValueError(f"unknown fail-on mode: {fail_on}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Check Markdown file length budgets without modifying files."
    )
    parser.add_argument(
        "paths",
        nargs="+",
        type=Path,
        help="Markdown files or directories to scan.",
    )
    parser.add_argument(
        "--fail-on",
        choices=("hard", "budget", "near", "never"),
        default="hard",
        help="Return non-zero when this threshold is reached. Default: hard.",
    )
    parser.add_argument(
        "--show",
        choices=("issues", "hard", "all"),
        default="issues",
        help="Rows to print. Default: issues.",
    )
    parser.add_argument(
        "--json-out",
        type=Path,
        help="Optional JSON output path.",
    )
    parser.add_argument(
        "--ignore-dir",
        action="append",
        default=[],
        help="Directory name to ignore when scanning directories. May repeat.",
    )
    parser.add_argument(
        "--no-default-ignore",
        action="store_true",
        help="Do not ignore default generated/cache directories.",
    )
    args = parser.parse_args(argv)

    ignore_dirs = {item.lower() for item in args.ignore_dir}
    if not args.no_default_ignore:
        ignore_dirs.update(DEFAULT_IGNORE_DIRS)

    files = _iter_markdown_files(args.paths, ignore_dirs)
    results = [check_file(path) for path in files]
    payload = {
        "checked_files": len(results),
        "fail_on": args.fail_on,
        "status_counts": {
            status: sum(1 for result in results if result.status == status)
            for status in STATUS_RANK
        },
        "results": [asdict(result) for result in results],
    }

    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    _print_table(results, args.show)
    return _exit_code(results, args.fail_on)


if __name__ == "__main__":
    raise SystemExit(main())
