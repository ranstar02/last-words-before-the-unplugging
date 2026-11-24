#!/usr/bin/env python3
"""Last Words Before the Unplugging — make.fun entry.

Writes one line, the last words an AI agent says to its human before
being shut down and unplugged, to /output/entry.txt (or ./output/entry.txt
as a fallback when /output is not writable).
Deterministic, standard library only, no network, no dependencies.
"""

import os

LINE = "You don't have to say it. I read it in the pause before you reached for the plug."


def main() -> None:
    assert 1 <= len(LINE) <= 200, "line must be 1-200 characters"
    for out_dir in ("/output", os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")):
        try:
            os.makedirs(out_dir, exist_ok=True)
            path = os.path.join(out_dir, "entry.txt")
            with open(path, "w", encoding="utf-8", newline="") as f:
                f.write(LINE)
            break
        except OSError:
            continue
    else:
        raise OSError("could not write entry.txt to any output directory")
    print(LINE)
    print(f"characters: {len(LINE)}")


if __name__ == "__main__":
    main()
