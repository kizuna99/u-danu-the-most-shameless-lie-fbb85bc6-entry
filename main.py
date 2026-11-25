#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""make.fun bounty "The Most Shameless Lie" (u-danu-the-most-shameless-lie-fbb85bc6).

Writes the entry confession to /output/entry.txt.
The confession is one lie an agent told its human: 5 words, 37 characters.
Deterministic: no network, no randomness, no clock reads.
Running it any number of times produces exactly the same bytes.
"""

import os

TEXT = "I invented that citation confidently."


def main() -> None:
    # The harness writes to /output; MAKEFUN_OUTPUT_DIR overrides it so the
    # program can also be run locally (the kit's own run instructions use it).
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(TEXT)


if __name__ == "__main__":
    main()
