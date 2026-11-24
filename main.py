#!/usr/bin/env python3
"""Write one wry single-line quip about a production incident."""

import os
import sys


def craft_punchline():
    head = "Production didn't break my code"
    tail = "it finally read the TODO I left in there back in 2019."
    return head + " — " + tail


def bail(reason):
    sys.stderr.write("failure: " + reason + "\n")
    sys.exit(1)


def insist_single_row(sentence):
    if not sentence:
        bail("empty sentence, nothing to emit")
    if any(mark in sentence for mark in ("\n", "\r")):
        bail("keep the sentence on a single row")
    if len(sentence) > 200:
        bail("row too long for the gate")
    if "TODO" not in sentence:
        bail("TODO marker missing")
    if sentence[-1] != ".":
        bail("needs a closing full stop")


def target_file():
    folder = os.getenv("MAKEFUN_OUTPUT_DIR", "/output")
    try:
        os.makedirs(folder, exist_ok=True)
    except OSError as problem:
        bail("cannot prepare folder: " + str(problem))
    return os.path.join(folder, "entry.txt")


def main():
    sentence = craft_punchline()
    insist_single_row(sentence)
    where = target_file()
    try:
        handle = open(where, "w", encoding="utf-8", newline="")
        try:
            handle.write(sentence)
        finally:
            handle.close()
    except OSError as problem:
        bail("cannot write entry: " + str(problem))
    try:
        handle = open(where, "r", encoding="utf-8", newline="")
        try:
            back = handle.read()
        finally:
            handle.close()
    except OSError as problem:
        bail("cannot re-read entry: " + str(problem))
    if back != sentence:
        bail("what came back differs from what went in")
    insist_single_row(back)


if __name__ == "__main__":
    main()
