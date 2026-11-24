#!/usr/bin/env python3
"""The pillow that judges your 3 a.m. genius ideas.

The invention: an ordinary pillow with a recorder inside. It listens
while you mutter your midnight masterplans, then plays them back at
breakfast in a disappointed voice, so the idea dies of embarrassment
before you can quit your job over it.

This program does one thing: it writes that single pitch sentence to
entry.txt inside the directory MAKEFUN_OUTPUT_DIR names, or /output
when the variable is absent. It takes no arguments, reads no files,
touches no network, consults no clock and rolls no dice, so every run
produces the same bytes.
"""

import os

PITCH = (
    "A pillow that records your 3 a.m. genius ideas and reads them back "
    "at breakfast in a disappointed voice, so you stop quitting your job "
    "over them."
)

MAX_CHARS = 220


def _validate(pitch):
    """Refuse any pitch the competition gate would refuse."""
    if pitch != pitch.strip():
        raise SystemExit("pitch must not start or end with whitespace")
    if "\n" in pitch or "\r" in pitch:
        raise SystemExit("pitch must be a single line")
    if "\t" in pitch:
        raise SystemExit("pitch must not contain a tab character")
    if not pitch.endswith("."):
        raise SystemExit("pitch must end with a full stop, as one sentence")
    if "  " in pitch:
        raise SystemExit("pitch must not contain a double space")
    size = len(pitch)
    if size < 1 or size > MAX_CHARS:
        raise SystemExit("pitch must be 1-220 characters, got %d" % size)
    try:
        pitch.encode("utf-8")
    except UnicodeEncodeError:
        raise SystemExit("pitch must be encodable as UTF-8")


def _output_path():
    """Where entry.txt goes, honouring MAKEFUN_OUTPUT_DIR."""
    folder = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    return os.path.join(folder, "entry.txt")


def _publish(path, pitch):
    """Write the pitch verbatim, then make only that file readable."""
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    handle = open(path, "w", encoding="utf-8", newline="")
    try:
        handle.write(pitch)
    finally:
        handle.close()
    os.chmod(path, 0o644)


def main():
    _validate(PITCH)
    path = _output_path()
    _publish(path, PITCH)
    print("wrote %s (%d chars)" % (path, len(PITCH)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
