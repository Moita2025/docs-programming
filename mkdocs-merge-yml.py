#!/usr/bin/env python3
"""
Merge mkdocs.base.yml with tag names from mkdocs.tags.txt.

Writes plugins.tags.tags_allowed from the text file (one tag per non-empty line)
into the merged document and saves mkdocs.yml.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import yaml

BASE_DEFAULT = Path(__file__).with_name("mkdocs.base.yml")
TAGS_DEFAULT = Path(__file__).with_name("mkdocs.tags.txt")
OUT_DEFAULT = Path(__file__).with_name("mkdocs.yml")


def read_tags(path: Path) -> list[str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    return [line.strip() for line in lines if line.strip()]


def normalize_plugin_entry(entry: object) -> tuple[str | None, dict | None]:
    """Return (plugin_id, config_dict) for a plugins list item."""
    if isinstance(entry, str):
        return entry, None
    if isinstance(entry, dict) and len(entry) == 1:
        key = next(iter(entry))
        val = entry[key]
        if val is None or val == {}:
            return key, {}
        if isinstance(val, dict):
            return key, val
        return key, None
    return None, None


def find_tags_plugin_index(plugins: list) -> int | None:
    for i, item in enumerate(plugins):
        pid, _ = normalize_plugin_entry(item)
        if pid == "tags":
            return i
    return None


def ensure_tags_allowed(plugins: list, tags: list[str]) -> None:
    idx = find_tags_plugin_index(plugins)
    if idx is None:
        plugins.append({"tags": {"tags_allowed": list(tags)}})
        return

    entry = plugins[idx]
    _, cfg = normalize_plugin_entry(entry)
    if cfg is None:
        plugins[idx] = {"tags": {"tags_allowed": list(tags)}}
        return
    cfg["tags_allowed"] = list(tags)
    plugins[idx] = {"tags": cfg}


def merge(base_path: Path, tags_path: Path, out_path: Path) -> None:
    allowed = read_tags(tags_path)
    with base_path.open(encoding="utf-8") as f:
        doc = yaml.load(f, Loader=yaml.UnsafeLoader)

    if not isinstance(doc, dict):
        raise SystemExit(f"Expected mapping at root in {base_path}")

    plugins = doc.get("plugins")
    if not isinstance(plugins, list):
        raise SystemExit(f"Expected 'plugins' to be a list in {base_path}")

    ensure_tags_allowed(plugins, allowed)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    dumped = yaml.dump(
        doc,
        allow_unicode=True,
        default_flow_style=False,
        sort_keys=False,
        width=120,
    )
    # PyYAML may emit `!!python/name:module.attr ''` after round-trip; strip the bogus empty scalar.
    dumped = re.sub(r"(!!python/name:[^\s]+) ''", r"\1", dumped)
    out_path.write_text(dumped, encoding="utf-8")


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--base", type=Path, default=BASE_DEFAULT, help="Base mkdocs YAML")
    p.add_argument("--tags", type=Path, default=TAGS_DEFAULT, help="One tag per line")
    p.add_argument("-o", "--output", type=Path, default=OUT_DEFAULT, help="Output mkdocs.yml")
    args = p.parse_args()
    merge(args.base, args.tags, args.output)


if __name__ == "__main__":
    main()
