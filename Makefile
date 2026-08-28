# Makefile - canonical developer workflow for repos built from repo-template.
#
# Thin aggregator: the actual recipes live in the devtools submodule
# (.devtools/makefiles/). Deleting a stack directory still requires zero
# edits — its targets print "[<target>] skipped" and aggregates keep working.
#
# Update the shared tooling deliberately:
#   make devtools-update        # move the submodule to the latest devtools tag
#   git add .devtools && git commit   # then ship the bump in a PR
#
# Windows: GNU Make >= 4 (choco install make); recipes are POSIX (Git Bash).
# Shell config (bash + pipefail) is provided by Makefile.common.

include .devtools/makefiles/Makefile.common
include .devtools/makefiles/Makefile.rust
include .devtools/makefiles/Makefile.typescript
include .devtools/makefiles/Makefile.elixir
include .devtools/makefiles/Makefile.python

format: format-rust format-typescript format-elixir format-python ## Format code in all present stacks
deps: deps-rust deps-typescript deps-elixir deps-python ## Install dependencies in all present stacks
lint: lint-rust lint-typescript lint-elixir lint-python ## Lint all present stacks
test: test-rust test-typescript test-elixir test-python ## Test all present stacks
build: build-rust build-typescript build-elixir build-python ## Build all present stacks
ci: lint test ## Run lint + test (CI gate)
clean: clean-rust clean-typescript clean-elixir clean-python ## Clean build artifacts in all present stacks

.PHONY: format deps lint test build ci clean
