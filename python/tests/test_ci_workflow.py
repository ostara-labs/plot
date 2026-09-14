"""Guard: the PR pipeline must keep the PostGIS integration job enabled.

The devtools ``ci`` workflow runs its database-backed ``test-postgis`` job
only when the caller passes a non-empty ``postgis-image`` input. When that
input is absent the job is silently *skipped* — so the integration suite
stops running in CI without any red check. This test fails on that
regression, which no test inside the suite can catch (the skipped job never
executes).
"""

import re
from pathlib import Path

PIPELINE = Path(__file__).resolve().parents[2] / ".github" / "workflows" / "pr-pipeline.yml"


def test_pr_pipeline_keeps_postgis_service_job_enabled() -> None:
    """The ``ci`` caller must pass a concrete, non-empty ``postgis-image``."""
    match = re.search(r"^\s*postgis-image:\s*(\S+)\s*$", PIPELINE.read_text("utf-8"), re.MULTILINE)
    assert match is not None, (
        "pr-pipeline.yml no longer passes postgis-image to the devtools ci "
        "workflow: the test-postgis job is skipped and DB-backed tests stop "
        "running in CI."
    )
    value = match.group(1)
    assert not value.startswith("${{"), (
        f"postgis-image must be a concrete image, got {value!r}: a computed "
        "value can resolve empty and skip the job silently."
    )
