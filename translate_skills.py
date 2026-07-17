#!/usr/bin/env python3
"""
Translate Superpowers skills and README from English to Simplified Chinese
using the DeepL Free API. Translated files are placed in zh/ subdirectories.

Usage:
  python translate_skills.py [--dry-run] [--only-readme] [--skill <name>]
"""

import re
import sys
import time
import argparse
from pathlib import Path
import requests

# ── Config ────────────────────────────────────────────────────────────────────

DEEPL_API_KEY = "6d5e5128-da15-4156-a8e7-93e7caab14bd:fx"
DEEPL_URL = "https://api-free.deepl.com/v2/translate"
DEEPL_USAGE_URL = "https://api-free.deepl.com/v2/usage"
TARGET_LANG = "ZH"
MAX_CHARS_PER_REQUEST = 100_000  # well below 128KB limit

ROOT = Path(__file__).parent
SKILLS_DIR = ROOT / "skills"

# Files to skip (internal dev logs, pressure-test docs)
SKIP_PATTERNS = {
    "CREATION-LOG.md",
    "test-pressure-1.md",
    "test-pressure-2.md",
    "test-pressure-3.md",
    "test-academic.md",
}

# ── DeepL helpers ─────────────────────────────────────────────────────────────

def _deepl_post(url, data):
    resp = requests.post(url, data=data, headers={
        "Authorization": f"DeepL-Auth-Key {DEEPL_API_KEY}",
    }, timeout=30)
    resp.raise_for_status()
    return resp.json()


def check_usage():
    resp = requests.get(DEEPL_USAGE_URL, headers={
        "Authorization": f"DeepL-Auth-Key {DEEPL_API_KEY}",
    }, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    used = data["character_count"]
    limit = data["character_limit"]
    remaining = limit - used
    print(f"  [DeepL usage] {used:,} / {limit:,} chars used, {remaining:,} remaining")
    if remaining < 50_000:
        print("  WARNING: fewer than 50k characters remaining!")
    return remaining


def translate_chunk(text):
    """Send one text chunk to DeepL and return the translated string."""
    if not text.strip():
        return text
    result = _deepl_post(DEEPL_URL, {
        "text": text,
        "target_lang": TARGET_LANG,
        "source_lang": "EN",
        "preserve_formatting": "1",
    })
    return result["translations"][0]["text"]


# ── Markdown protection helpers ────────────────────────────────────────────────

# Matches fenced code blocks (``` ... ```) including language specifier
FENCED_BLOCK_RE = re.compile(r"(```[\w.]*\n[\s\S]*?```|~~~[\w.]*\n[\s\S]*?~~~)", re.MULTILINE)
# Matches inline code
INLINE_CODE_RE = re.compile(r"(`[^`\n]+`)")
# Matches custom ALL-CAPS XML-like tag names (e.g., <HARD-GATE>, </HARD-GATE>)
# Only protects the opening/closing tag itself, not the content (so content IS translated)
CUSTOM_TAG_RE = re.compile(r"(</?[A-Z][A-Z0-9-]*>)")
# Matches HTML/XML-like tags we want to pass through untranslated (e.g., tag names)
PLACEHOLDER_PREFIX = "ZZZPH"
PLACEHOLDER_SUFFIX = "ZZZ"


def protect_code_blocks(text):
    """Replace fenced + inline code and custom XML tags with placeholders."""
    blocks = {}
    counter = [0]

    def replacer(m):
        ph = f"{PLACEHOLDER_PREFIX}{counter[0]}{PLACEHOLDER_SUFFIX}"
        blocks[ph] = m.group(0)
        counter[0] += 1
        return ph

    text = FENCED_BLOCK_RE.sub(replacer, text)
    text = INLINE_CODE_RE.sub(replacer, text)
    text = CUSTOM_TAG_RE.sub(replacer, text)
    return text, blocks


def restore_code_blocks(text, blocks):
    for ph, original in blocks.items():
        text = text.replace(ph, original)
    return text


# ── YAML frontmatter ───────────────────────────────────────────────────────────

FRONTMATTER_RE = re.compile(r"^---\n([\s\S]*?)\n---\n", re.MULTILINE)


def translate_frontmatter(fm_text, dry_run=False):
    """Translate only the `description:` value in YAML frontmatter."""
    lines = fm_text.split("\n")
    result = []
    for line in lines:
        m = re.match(r'^(description:\s*)(\"?)(.*?)(\2)\s*$', line)
        if m:
            prefix, q, value, _ = m.group(1), m.group(2), m.group(3), m.group(4)
            if value.strip() and not dry_run:
                translated = translate_chunk(value)
                line = f'{prefix}{q}{translated}{q}'
        result.append(line)
    return "\n".join(result)


# ── Chunked translation ────────────────────────────────────────────────────────

def split_into_sections(text):
    """Split text on blank lines into paragraphs for chunking."""
    return re.split(r"\n\n+", text)


def translate_body(text, dry_run=False):
    """Translate body text, respecting the max-chars-per-request limit."""
    if dry_run:
        return text

    sections = split_into_sections(text)
    chunks = []
    current = []
    current_len = 0

    for section in sections:
        if current_len + len(section) + 2 > MAX_CHARS_PER_REQUEST:
            if current:
                chunks.append("\n\n".join(current))
            current = [section]
            current_len = len(section)
        else:
            current.append(section)
            current_len += len(section) + 2

    if current:
        chunks.append("\n\n".join(current))

    translated_parts = []
    for i, chunk in enumerate(chunks):
        if len(chunks) > 1:
            print(f"    chunk {i+1}/{len(chunks)} ({len(chunk):,} chars)...", end=" ", flush=True)
        result = translate_chunk(chunk)
        if len(chunks) > 1:
            print("done")
        translated_parts.append(result)
        time.sleep(0.1)  # small pause to be polite

    return "\n\n".join(translated_parts)


# ── Main file translator ───────────────────────────────────────────────────────

def translate_markdown_file(src: Path, dst: Path, dry_run=False):
    content = src.read_text(encoding="utf-8")

    # 1. Handle YAML frontmatter
    fm_match = FRONTMATTER_RE.match(content)
    if fm_match:
        fm_text = fm_match.group(1)
        translated_fm = translate_frontmatter(fm_text, dry_run)
        body = content[fm_match.end():]
        header = f"---\n{translated_fm}\n---\n"
    else:
        header = ""
        body = content

    # 2. Protect code blocks
    protected_body, blocks = protect_code_blocks(body)

    # 3. Wrap custom XML tags so DeepL preserves tag names but translates contents
    #    We use <keep> tags around them to skip them (DeepL ignore_tags=keep)
    #    Actually we want their TEXT content translated but tag names preserved.
    #    Strategy: leave them as-is; DeepL xml mode will treat them as tags and
    #    translate the text nodes inside, which is what we want.

    # 4. Translate body
    translated_body = translate_body(protected_body, dry_run)

    # 5. Restore code blocks
    translated_body = restore_code_blocks(translated_body, blocks)

    # 6. Write output
    final = header + translated_body

    if not dry_run:
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(final, encoding="utf-8")


# ── File discovery ─────────────────────────────────────────────────────────────

def collect_skill_files(only_skill=None):
    """Yield (src, dst) pairs for all skill markdown files."""
    for skill_dir in sorted(SKILLS_DIR.iterdir()):
        if not skill_dir.is_dir():
            continue
        if only_skill and skill_dir.name != only_skill:
            continue
        zh_dir = skill_dir / "zh"
        for md_file in sorted(skill_dir.rglob("*.md")):
            # Skip files already in a zh/ directory
            if "zh" in md_file.parts:
                continue
            if md_file.name in SKIP_PATTERNS:
                continue
            # Compute destination path mirroring the structure under zh/
            rel = md_file.relative_to(skill_dir)
            dst = zh_dir / rel
            yield md_file, dst


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Translate Superpowers docs via DeepL")
    parser.add_argument("--dry-run", action="store_true", help="Print plan without calling API")
    parser.add_argument("--only-readme", action="store_true", help="Translate README.md only")
    parser.add_argument("--skill", metavar="NAME", help="Translate one skill directory only")
    args = parser.parse_args()

    dry_run = args.dry_run

    if dry_run:
        print("DRY RUN — no API calls will be made\n")

    # Collect files
    files = []

    # README
    readme_src = ROOT / "README.md"
    readme_dst = ROOT / "README.zh.md"
    files.append((readme_src, readme_dst))

    if not args.only_readme:
        files.extend(collect_skill_files(only_skill=args.skill))

    # Summary
    total_chars = sum(p.read_text(encoding="utf-8").__len__() for p, _ in files)
    print(f"Files to translate: {len(files)}")
    print(f"Estimated characters: {total_chars:,}\n")

    if dry_run:
        for src, dst in files:
            print(f"  {src.relative_to(ROOT)}  →  {dst.relative_to(ROOT)}")
        return

    # Check usage before starting
    check_usage()
    print()

    # Translate
    for i, (src, dst) in enumerate(files, 1):
        rel = src.relative_to(ROOT)
        print(f"[{i}/{len(files)}] {rel} ({src.stat().st_size // 1024}KB) ...", end=" ", flush=True)
        try:
            translate_markdown_file(src, dst, dry_run=False)
            print(f"→ {dst.relative_to(ROOT)}")
        except requests.HTTPError as e:
            print(f"\n  ERROR {e.response.status_code}: {e.response.text}")
            sys.exit(1)
        except Exception as e:
            print(f"\n  ERROR: {e}")
            sys.exit(1)

    print("\nAll done!")
    check_usage()


if __name__ == "__main__":
    main()