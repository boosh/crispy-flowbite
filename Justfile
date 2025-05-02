# Make sure to activate the virtualenv before running commands (i.e. with: . ./venv/bin/activate)
set dotenv-load := true

name := ""
path := ""

system_env := env('ENV', 'dev')

# List available upgrades of pip packages
list-upgrades:
    pip list --outdated --format=columns

# Run tests (optionally pass path/wildcard to a specific test file(s) to run)
test *ARGS='':
  pytest {{ARGS}}

freeze:
  pip freeze > requirements.txt

# Run ruff format
format:
  ruff format --exclude=venv .

aider:
    aider .aider.prompt.md --no-suggest-shell-commands --analytics-disable --no-auto-lint

# Compile all requirements.in files to their corresponding requirements.txt. Requires pip-tools to be installed
compile-reqs:
    #!/usr/bin/env bash
    set -euo pipefail
    for req in $(find . -maxdepth 2 -name "requirements*.in"); do
        echo "Compiling $req..."
        pip-compile --quiet --upgrade $req
    done

# Sync virtualenv with requirements.txt files for current environment without updating them
sync-reqs:
    #!/usr/bin/env bash
    set -euo pipefail
    if [ -z "${VIRTUAL_ENV:-}" ]; then
        echo "No virtualenv activated! Please activate one first."
        exit 1
    fi
    mapfile -t req_files < <(find . -maxdepth 2 \( -name "requirements.txt" -o -name "requirements-{{system_env}}.txt" \))
    if [ ${#req_files[@]} -eq 0 ]; then
        echo "No matching requirements*.txt files found!"
        exit 1
    fi
    echo "Syncing: ${req_files[*]}"
    "${VIRTUAL_ENV}/bin/pip-sync" "${req_files[@]}"
    echo "Successfully synced: ${req_files[*]}"

# Update requirements then sync your virtualenv with them
update-reqs: compile-reqs sync-reqs
