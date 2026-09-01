"""Naming guard: reject vague variable names in the source tree (27.27).

Lint enforces casing (ruff ``N`` rules); this test enforces the semantic
half of the naming convention — identifiers must reveal intent. The banned
list catches the classic offenders; extend it rather than adding ignores.
"""

import re
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parents[1] / "src"

# Vague names that never reveal intent. Keyword arguments to third-party
# libraries (e.g. ``data=``) are allowed; assignments to these names are not.
BANNED_NAMES = {
    "data",
    "tmp",
    "temp",
    "res",
    "obj",
    "foo",
    "bar",
    "baz",
    "stuff",
    "thing",
    "val",
    "vals",
}

# ``name =`` or ``for name in`` at a statement start (attribute or keyword
# arguments are out of scope — see module docstring).
ASSIGNMENT = re.compile(rf"^\s*(?:for\s+)?({'|'.join(sorted(BANNED_NAMES))})\s*=")


def _source_files() -> list[Path]:
    return sorted(SRC_DIR.rglob("*.py"))


def test_no_vague_variable_names():
    offenders: list[str] = []
    for path in _source_files():
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            match = ASSIGNMENT.match(line)
            if match:
                offenders.append(f"{path.relative_to(SRC_DIR.parent)}:{lineno}: {match.group(1)}")
    assert not offenders, "Vague variable names found (27.27):\n" + "\n".join(offenders)
