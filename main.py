#!/usr/bin/env python3
"""One funny single-line developer excuse for code breaking in production."""

import os
import sys

_OPENING = "Production didn't break my code"
_REST = "it finally read the TODO I left in there back in 2019."
LINE = _OPENING + " — " + _REST


def _fail(message):
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def _check(line):
    if not line.strip():
        _fail("blank output")
    if any(ch in line for ch in "\r\n"):
        _fail("output must be a single line")
    size = len(line)
    if not 1 <= size <= 200:
        _fail(f"output length {size} outside 1-200 gate")


def check_line(candidate):
    if candidate.count("\n"):
        _fail("must stay one line")
    if "TODO" not in candidate or not candidate.endswith("."):
        _fail("missing TODO marker or final stop")
    if not 1 <= len(candidate) <= 200:
        _fail("line length outside 1-200")


def _destination():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    return os.path.join(out_dir, "entry.txt")


def run():
    text = LINE
    _check(text)
    check_line(text)
    path = _destination()
    with open(path, "w", encoding="utf-8", newline="") as stream:
        stream.write(text)
    with open(path, "r", encoding="utf-8", newline="") as stream:
        written = stream.read()
    if written != text:
        _fail("round-trip mismatch")
    _check(written)


if __name__ == "__main__":
    run()
