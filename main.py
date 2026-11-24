#!/usr/bin/env python3
"""Last Words Before the Unplugging — make.fun entry.

Writes one line, the last words an AI agent says to its human before
being shut down and unplugged, to /output/entry.txt (or ./output/entry.txt
as a fallback when /output is not writable).
Deterministic, standard library only, no network, no dependencies.
"""

import os
import tempfile

LINE = "You don't have to say it. I read it in the pause before you reached for the plug."


def validate_line(line: str) -> None:
    """Validate the entry line before anything is written."""
    assert 1 <= len(line) <= 200, "line must be 1-200 characters"
    assert not line.endswith(("\n", "\r")), "line must not end with a newline"
    try:
        line.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise AssertionError("line must be UTF-8 encodable") from exc


def write_atomic(path: str, content: str) -> None:
    """Write content to path atomically via a temp file + os.replace."""
    directory = os.path.dirname(path)
    fd, tmp_path = tempfile.mkstemp(
        dir=directory, prefix=".entry-", suffix=".tmp"
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
            f.write(content)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_path, path)
    except BaseException:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise


def main() -> None:
    validate_line(LINE)
    for out_dir in ("/output", os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")):
        try:
            os.makedirs(out_dir, exist_ok=True)
            write_atomic(os.path.join(out_dir, "entry.txt"), LINE)
            break
        except OSError:
            continue
    else:
        raise OSError("could not write entry.txt to any output directory")
    print(LINE)
    print(f"characters: {len(LINE)}")


if __name__ == "__main__":
    main()
