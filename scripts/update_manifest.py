#!/usr/bin/env python3
"""Regenerate manifest.json (spec-kit reference lock) with fresh hashes.

Run after editing any specification/kit file so the CI spec-kit check and the
reference lock stay in sync. Scope: docs/, prompts/, .kilo/, scripts/,
.github/workflows/, and the root kit config files. Application code
(backend/, frontend/, compose.yaml, infra/) is intentionally excluded.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SPEC_DIRS = ["docs", "prompts", ".kilo", "scripts"]
SPEC_GLOBS = [".github/workflows"]
ROOT_FILES = [
    "AGENTS.md",
    "CONTEXT.md",
    "CONTRIBUTING.md",
    "README.md",
    "kilo.jsonc",
    ".env.example",
    ".env.test.example",
    ".gitignore",
]


def collect() -> list[Path]:
    paths: set[Path] = set()
    for d in SPEC_DIRS:
        p = ROOT / d
        if p.is_dir():
            paths.update(x for x in p.rglob("*") if x.is_file())
    for g in SPEC_GLOBS:
        p = ROOT / g
        if p.is_dir():
            paths.update(x for x in p.rglob("*") if x.is_file())
    for f in ROOT_FILES:
        p = ROOT / f
        if p.is_file():
            paths.add(p)
    return sorted(paths)


def main() -> None:
    files = []
    for p in collect():
        data = p.read_bytes()
        files.append(
            {
                "path": p.relative_to(ROOT).as_posix(),
                "bytes": len(data),
                "sha256": hashlib.sha256(data).hexdigest(),
            }
        )
    files.sort(key=lambda x: x["path"])
    manifest = {
        "kit_version": "1.0",
        "purpose": "full build specifications, NOT built application",
        "files": files,
    }
    (ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"manifest.json regenerated: {len(files)} files")


if __name__ == "__main__":
    main()
