#!/usr/bin/env bash
# validate_skill.sh — Validate the ui-clone-skill structure and frontmatter.
#
# Usage:
#   bash scripts/validate_skill.sh [--skill-dir /path/to/skill]
#
# What it checks:
#   1. SKILL.md exists
#   2. Frontmatter has required name + description fields
#   3. name matches directory name
#   4. SKILL.md is under 500 lines
#   5. All reference files listed in SKILL.md actually exist
#   6. scripts/ files are executable (or at least have execute permission hint)
#
# Dependencies: bash, grep, awk, wc, find (all standard Unix tools)
# Exit codes:
#   0 — all checks passed
#   1 — one or more checks failed

set -euo pipefail

SKILL_DIR="${1:-$(cd "$(dirname "$0")/.." && pwd)}"
SKILL_MD="$SKILL_DIR/SKILL.md"
PASS=0
FAIL=0
WARNS=0

green() { printf '\033[0;32m✓ %s\033[0m\n' "$*"; }
red()   { printf '\033[0;31m✗ %s\033[0m\n' "$*"; }
warn()  { printf '\033[0;33m⚠ %s\033[0m\n' "$*"; }

echo "=== ui-clone-skill validation ==="
echo "Skill dir: $SKILL_DIR"
echo ""

# 1. SKILL.md exists
if [[ -f "$SKILL_MD" ]]; then
    green "SKILL.md found"
    ((PASS++))
else
    red "SKILL.md NOT found at $SKILL_MD"
    ((FAIL++))
    echo ""
    echo "RESULT: FAILED ($FAIL checks failed)"
    exit 1
fi

# 2. Has 'name:' in frontmatter
NAME_LINE=$(awk '/^---/{fm++} fm==1 && /^name:/' "$SKILL_MD" | head -1)
if [[ -n "$NAME_LINE" ]]; then
    SKILL_NAME=$(echo "$NAME_LINE" | sed 's/name: *//')
    green "name field found: '$SKILL_NAME'"
    ((PASS++))

    # 3. name matches directory name
    DIR_NAME=$(basename "$SKILL_DIR")
    if [[ "$SKILL_NAME" == "$DIR_NAME" ]]; then
        green "name matches directory name ('$DIR_NAME')"
        ((PASS++))
    else
        red "name '$SKILL_NAME' does NOT match directory name '$DIR_NAME'"
        ((FAIL++))
    fi

    # name format check: lowercase, digits, hyphens
    if echo "$SKILL_NAME" | grep -qE '^[a-z0-9]+(-[a-z0-9]+)*$'; then
        green "name format is valid (lowercase, hyphens only)"
        ((PASS++))
    else
        red "name '$SKILL_NAME' contains invalid characters (use lowercase letters, numbers, hyphens only)"
        ((FAIL++))
    fi
else
    red "No 'name:' field found in SKILL.md frontmatter"
    ((FAIL++))
fi

# 4. Has 'description:' in frontmatter
if awk '/^---/{fm++} fm==1 && /^description:/' "$SKILL_MD" | grep -q .; then
    DESC_LEN=$(awk '/^---/{fm++} fm==1 && /^description:/{found=1} found && fm==1{print}' "$SKILL_MD" | \
               awk 'NF || /^---/{if(/^---/ && NR>1)exit; print}' | wc -c)
    green "description field found (~${DESC_LEN} chars)"
    ((PASS++))
    if [[ "$DESC_LEN" -gt 1024 ]]; then
        warn "description may exceed 1024 character limit — check manually"
        ((WARNS++))
    fi
else
    red "No 'description:' field found in SKILL.md frontmatter"
    ((FAIL++))
fi

# 5. Line count
LINE_COUNT=$(wc -l < "$SKILL_MD")
if [[ "$LINE_COUNT" -le 500 ]]; then
    green "SKILL.md is $LINE_COUNT lines (under 500-line limit)"
    ((PASS++))
else
    warn "SKILL.md is $LINE_COUNT lines — spec recommends under 500. Move content to references/"
    ((WARNS++))
fi

# 6. References directory exists if referenced in SKILL.md
if grep -q "references/" "$SKILL_MD"; then
    if [[ -d "$SKILL_DIR/references" ]]; then
        green "references/ directory exists"
        ((PASS++))

        # 7. Each references/file.md mentioned in SKILL.md actually exists
        echo ""
        echo "--- Checking referenced files ---"
        while IFS= read -r ref; do
            if [[ -f "$SKILL_DIR/$ref" ]]; then
                green "  $ref"
                ((PASS++))
            else
                red "  $ref — FILE MISSING"
                ((FAIL++))
            fi
        done < <(grep -oE 'references/[a-zA-Z0-9_-]+\.md' "$SKILL_MD" | sort -u)
    else
        red "references/ directory missing but references/ paths found in SKILL.md"
        ((FAIL++))
    fi
fi

# 8. scripts/ check
if [[ -d "$SKILL_DIR/scripts" ]]; then
    SCRIPT_COUNT=$(find "$SKILL_DIR/scripts" -maxdepth 1 -type f | wc -l)
    green "scripts/ directory exists with $SCRIPT_COUNT file(s)"
    ((PASS++))

    find "$SKILL_DIR/scripts" -maxdepth 1 -type f | while read -r script; do
        name=$(basename "$script")
        if [[ -x "$script" ]] || head -1 "$script" 2>/dev/null | grep -q '^#!'; then
            green "  $name (has shebang or exec bit)"
        else
            warn "  $name — consider adding a shebang line (#!/usr/bin/env python3)"
            ((WARNS++))
        fi
    done
fi

echo ""
echo "=== Results ==="
echo "  Passed:   $PASS"
echo "  Warnings: $WARNS"
echo "  Failed:   $FAIL"
echo ""

if [[ "$FAIL" -gt 0 ]]; then
    red "VALIDATION FAILED — fix the issues above"
    exit 1
else
    green "VALIDATION PASSED"
    if [[ "$WARNS" -gt 0 ]]; then
        warn "$WARNS warning(s) — review above"
    fi
    exit 0
fi
