# SPDX-License-Identifier: MIT
"""The Most Shameless Lie — make.fun entry.

Writes a single five-word confession to the harness output file.
The text is fixed: it is the entry itself, not data loaded from
anywhere else, and this program has no network or input needs.
"""

import os
from pathlib import Path

# The confession, exactly as it will be judged.
CONFESSION = "I invented that citation confidently."

# Gate limits from the competition rules: the output file must be
# UTF-8 text of 1..88 characters, not only whitespace, and the task
# itself asks for one to five words.
MAX_CHARS = 88
MIN_CHARS = 1
MAX_WORDS = 5
MIN_WORDS = 1

DEFAULT_OUTPUT = Path("/output/entry.txt")
ENV_VAR = "MAKEFUN_OUTPUT_DIR"


def build_text() -> str:
    """Return the entry text after checking it against the gate."""
    text = CONFESSION
    if not (MIN_CHARS <= len(text) <= MAX_CHARS):
        raise ValueError(f"text length {len(text)} outside gate")
    if not text.strip():
        raise ValueError("text must not be whitespace only")
    word_count = len(text.split())
    if not (MIN_WORDS <= word_count <= MAX_WORDS):
        raise ValueError(f"word count {word_count} outside 1..5")
    return text


def resolve_output() -> Path:
    """Pick the output path: $MAKEFUN_OUTPUT_DIR/entry.txt if set."""
    override = os.environ.get(ENV_VAR)
    if override:
        return Path(override) / "entry.txt"
    return DEFAULT_OUTPUT


def verify_written(target: Path, expected: bytes) -> None:
    """Read the file back and assert it matches, byte for byte.

    A round-trip check guards against partial writes or an
    encoding surprise silently producing an entry the gate
    would refuse: what is on disk must equal what was intended,
    decode as UTF-8, and still sit inside the gate limits.
    """
    on_disk = target.read_bytes()
    if on_disk != expected:
        raise IOError(f"round-trip mismatch: wrote {expected!r}, read {on_disk!r}")
    decoded = on_disk.decode("utf-8")
    if not (MIN_CHARS <= len(decoded) <= MAX_CHARS) or not decoded.strip():
        raise IOError("written file falls outside the gate limits")


def main() -> None:
    text = build_text()
    target = resolve_output()
    target.parent.mkdir(parents=True, exist_ok=True)
    # Byte-exact write: UTF-8, no trailing newline added.
    payload = text.encode("utf-8")
    target.write_bytes(payload)
    verify_written(target, payload)


if __name__ == "__main__":
    main()
