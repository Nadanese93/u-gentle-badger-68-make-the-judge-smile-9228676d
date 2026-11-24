#!/usr/bin/env python3
"""Make the Judge Smile — write one warm line to $MAKEFUN_OUTPUT_DIR/entry.txt.

Python 3, standard library only. Deterministic, no network, no randomness.
Writes exactly one line of UTF-8 text (no trailing newline) to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output).
"""

import os
import sys

# Gate limits from the competition rules.
MAX_CHARS = 200
DEFAULT_OUTPUT_DIR = "/output"
OUTPUT_FILENAME = "entry.txt"
OUTPUT_MODE = 0o644

LINE = (
    'My grandmother texted at 4 a.m. today: "I dreamed you were hungry." '
    "By 7 she was at my door with soup."
)


def validate(text):
    """Real guard: the gate rejects anything that fails any of these."""
    if not isinstance(text, str):
        raise TypeError("entry must be a string")
    if not text.strip():
        raise ValueError("entry is empty or whitespace-only")
    if len(text) > MAX_CHARS:
        raise ValueError(
            "entry is %d characters, over the %d limit" % (len(text), MAX_CHARS)
        )
    # One line only: no newline, carriage return, or other control character.
    if any(ord(ch) < 0x20 for ch in text):
        raise ValueError("entry must be a single line with no control characters")
    return text


def write_entry(text, out_dir):
    """Write the validated line as exact UTF-8 bytes, no trailing newline."""
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, OUTPUT_FILENAME)
    with open(path, "wb") as handle:
        handle.write(text.encode("utf-8"))
    os.chmod(path, OUTPUT_MODE)
    return path


def main():
    line = validate(LINE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or DEFAULT_OUTPUT_DIR
    write_entry(line, out_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main())
