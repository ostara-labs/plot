#!/usr/bin/env bash
#
# setup-rulesets.sh - provision branch protection on a fresh repository
# created from this template.
#
# "Use this template" copies FILES only - repository settings (rulesets)
# are not inherited. Run this once after creating your repo:
#
#   bash scripts/setup-rulesets.sh <owner>/<repo>
#
# Creates:
#   1. The "requires-human-review" label.
#   2. A "main-protection" branch ruleset: PRs required, force-pushes and
#      deletions blocked, CI status checks required, and code-owner approval
#      mandatory when trust-boundary paths change (see CODEOWNERS).
#
# Requires: gh CLI, authenticated with admin on the target repository.

set -euo pipefail

REPO="${1:?usage: bash scripts/setup-rulesets.sh <owner>/<repo>}"

echo "[setup-rulesets] ensuring requires-human-review label on $REPO"
gh label create requires-human-review \
  --repo "$REPO" \
  --color E99695 \
  --description "Touches trust-boundary files" \
  --force

echo "[setup-rulesets] creating main-protection ruleset on $REPO"
PAYLOAD="$(cat <<'JSON'
{
  "name": "main-protection",
  "target": "branch",
  "enforcement": "active",
  "conditions": {
    "ref_name": {
      "include": ["~DEFAULT_BRANCH"],
      "exclude": []
    }
  },
  "bypass_actors": [],
  "rules": [
    { "type": "deletion" },
    { "type": "non_fast_forward" },
    {
      "type": "pull_request",
      "parameters": {
        "required_approving_review_count": 0,
        "require_code_owner_review": true,
        "dismiss_stale_reviews_on_push": true,
        "require_last_push_approval": false,
        "required_review_thread_resolution": false
      }
    },
    {
      "type": "required_status_checks",
      "parameters": {
        "strict_required_status_checks_policy": false,
        "required_status_checks": [
          { "context": "gate" }
        ]
      }
    }
  ]
}
JSON
)"

# Idempotent: if the ruleset already exists, update it instead of failing.
EXISTING_ID="$(gh api "/repos/$REPO/rulesets" --jq '.[] | select(.name == "main-protection") | .id' || true)"
if [ -n "$EXISTING_ID" ]; then
  echo "[setup-rulesets] ruleset exists (id=$EXISTING_ID) - updating"
  gh api -X PUT "/repos/$REPO/rulesets/$EXISTING_ID" --input - <<<"$PAYLOAD" >/dev/null
else
  gh api -X POST "/repos/$REPO/rulesets" --input - <<<"$PAYLOAD" >/dev/null
fi

echo "[setup-rulesets] done. Trust-boundary paths now require code-owner"
echo "[setup-rulesets] approval (edit .github/CODEOWNERS to set your owners)."
