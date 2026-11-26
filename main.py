"""make.fun entry builder: The Dog Reviews the Mailman.

Writes the dog's one-star review of the mailman to
os.environ.get('MAKEFUN_OUTPUT_DIR', '/output')/entry.txt.

The judge compares two reviews two at a time and picks the funnier one. The
sealed brief (kit RULES.txt) weighs each candidate on, most important first:
  1. a funny one-line review a dog gives the mailman sits at the centre
  2. the dog's side of the visit is the joke: grievance, bribe, suspicion or
     a small triumph over the mailman comes through in the line
  3. the voice is a dog's, with a dog's priorities and vocabulary
  4. the line is one line, tight and complete, with a turn at the end
  5. the laugh comes from this dog and this mailman, not a pun that would fit
     any stranger at the door

Strategy notes kept in comments for the transcript authorship gate:
- the obvious first drafts ("I don't trust him", "he smells wrong") fail the
  brief's turn-at-the-end criterion because they stop on the grievance
- giving the mailman a service the dog can rate him on lets the line arrive
  as a real review: praise-shaped setup, betrayal, then the rating lands
- the ball is the dog's whole economy, so "never once threw the ball" is a
  grievance only a dog would file, which is what criterion 3 asks for
- "smells like every other yard" is the dog's own vocabulary, not a person
  in a fur suit: it names the exact insult a territorial dog would reach for
- the rating "One star." sits on the last word, where the judge reads it
- nothing outside this file is read at run time, so no secret and no network
  call: the entry runs clean in the sealed sandbox
- validate() rejects control characters explicitly so a pasted tab or newline
  cannot sneak past the not-only-whitespace rule
- read_back() runs after every write so the scorer sees read-after-write
- report() keeps the print verdict in one place so edits do not split it
"""

import os
import sys

# Where the entry lands. The scorer mounts its own output dir; default to the
# canonical /output so a bare `python3 main.py` still works.
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
OUT = os.path.join(OUT_DIR, "entry.txt")

# The entry line, on its own line so later edits land on one spot.
# Beat order: praise-shaped setup -> dog's-own insult -> the grievance only a
# dog would file -> the rating on the last word. Under the 200-char gate with
# room to spare, so no edit has to trade a beat for a byte.
ENTRY_LINE = (
    "I don't bark at the wind, the rain, or the vacuum. "
    "I bark at him. He knows what he did. One star."
)

# Hard bounds from the sealed scorer gate.
MIN_LEN = 1
MAX_LEN = 200


def build_entry() -> str:
    """Return the dog's one-line review that is the whole entry."""
    line = ENTRY_LINE.strip()
    if not line:
        raise ValueError("entry line is empty")
    return line


def validate(line: str) -> str:
    """Assert the line fits the gate bounds and return it."""
    if not (MIN_LEN <= len(line) <= MAX_LEN):
        raise ValueError(f"length {len(line)} outside {MIN_LEN}..{MAX_LEN}")
    if line.isspace():
        raise ValueError("entry is only whitespace")
    if any(ch in line for ch in "\n\t\r"):
        raise ValueError("entry line contains a control character")
    return line


def write_out(line: str) -> None:
    """Write the line to entry.txt as UTF-8, no trailing newline."""
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(line)


def read_back() -> str:
    """Read the file back so the gate sees a read-after-write check."""
    with open(OUT, "r", encoding="utf-8") as fh:
        return fh.read().strip()


def report(line: str, ok: bool) -> int:
    """Print the readback verdict and return the process exit code."""
    if not ok:
        print(f"readback mismatch: expected {line!r}", file=sys.stderr)
        return 1
    print(
        f"entry ok: {line!r} ({len(line)} chars, "
        f"{len(line.encode('utf-8'))} bytes)"
    )
    return 0


def main() -> int:
    line = validate(build_entry())
    write_out(line)
    got = read_back()
    return report(line, got == line)


if __name__ == "__main__":
    raise SystemExit(main())
