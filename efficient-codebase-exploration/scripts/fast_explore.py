#!/usr/bin/env python3
"""
Fast Codebase Explorer (Token-Conscious)

Scans project trees to produce concise, high-signal architectural overviews
while strictly pruning dependency directories (node_modules, vendor, .git, venv).

Usage:
    python3 fast_explore.py [target-directory] [--max-depth 3] [--json]
"""

import os
import sys
import json
import argparse
from typing import Dict, List, Any

BANNED_DIRS = {
    "node_modules", "vendor", ".git", ".venv", "venv", "env",
    "site-packages", "__pycache__", "dist", "build", ".next",
    ".nuxt", ".svelte-kit", "coverage", ".idea", ".vscode"
}

LAYER_HEURISTICS = {
    "Routing & Endpoints": ["route", "router", "routes", "api", "endpoint", "endpoints"],
    "Controllers & Handlers": ["controller", "controllers", "handler", "handlers"],
    "Business Logic & Services": ["service", "services", "usecase", "usecases", "action", "actions"],
    "Models & Schemas": ["model", "models", "schema", "schemas", "entity", "entities", "dto", "dtos"],
    "Configuration & Entry": ["config", "settings", "main", "index", "app", "server"],
    "UI & Views": ["component", "components", "view", "views", "pages", "templates"]
}

def scan_directory(base_dir: str, max_depth: int = 3) -> Dict[str, Any]:
    base_dir = os.path.abspath(base_dir)
    structure: Dict[str, List[str]] = {category: [] for category in LAYER_HEURISTICS}
    structure["Other Source Files"] = []
    
    total_files = 0
    skipped_dirs = 0

    for root, dirs, files in os.walk(base_dir):
        # Calculate current relative depth
        rel_path = os.path.relpath(root, base_dir)
        current_depth = 0 if rel_path == "." else rel_path.count(os.sep) + 1
        
        # Prune banned directories
        banned = [d for d in dirs if d in BANNED_DIRS or d.startswith(".")]
        for d in banned:
            dirs.remove(d)
            skipped_dirs += 1

        if current_depth > max_depth:
            dirs.clear()
            continue

        for f in files:
            if f.startswith(".") or f.endswith((".pyc", ".min.js", ".map", ".lock")):
                continue

            file_rel_path = os.path.relpath(os.path.join(root, f), base_dir)
            total_files += 1

            lower_path = file_rel_path.lower()
            categorized = False
            for layer, keywords in LAYER_HEURISTICS.items():
                if any(kw in lower_path for kw in keywords):
                    structure[layer].append(file_rel_path)
                    categorized = True
                    break

            if not categorized:
                structure["Other Source Files"].append(file_rel_path)

    return {
        "base_directory": base_dir,
        "total_source_files": total_files,
        "skipped_banned_directories": skipped_dirs,
        "layers": {k: sorted(v) for k, v in structure.items() if v}
    }

def main():
    parser = argparse.ArgumentParser(description="Fast Token-Conscious Codebase Explorer")
    parser.add_argument("directory", nargs="?", default=".", help="Target directory to inspect")
    parser.add_argument("--max-depth", type=int, default=3, help="Max directory recursion depth")
    parser.add_argument("--json", action="store_true", help="Output machine-readable JSON")
    args = parser.parse_args()

    result = scan_directory(args.directory, args.max_depth)

    if args.json:
        print(json.dumps(result, indent=2))
        return

    print("=" * 80)
    print(f"FAST CODEBASE EXPLORER: {result['base_directory']}")
    print(f"Total Source Files: {result['total_source_files']} | Pruned Dependency Dirs: {result['skipped_banned_directories']}")
    print("=" * 80)

    for layer, files in result["layers"].items():
        print(f"\n📂 [{layer.upper()}] ({len(files)} files)")
        # Show first 15 files per category to keep token consumption tight
        for f in files[:15]:
            print(f"  • {f}")
        if len(files) > 15:
            print(f"  ... and {len(files) - 15} more files")

    print("\n" + "=" * 80)
    print("EXPLORATION TIP: Group candidate files from above and read in a single batch turn.")
    print("=" * 80)

if __name__ == "__main__":
    main()
