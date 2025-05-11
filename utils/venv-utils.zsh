#!/bin/zsh

function cd() {
    builtin cd "$@"

    if [ -z "$VIRTUAL_ENV" ]; then
        # If env folder is found then activate the virtualenv
        if [ -d ./.venv ]; then
            source ./.venv/bin/activate
        fi
    else
        # Check if the current folder belongs to earlier VIRTUAL_ENV folder
        # If yes then do nothing, else deactivate
        parentdir="$(dirname "$VIRTUAL_ENV")"
        if [[ "$PWD"/ != "$parentdir"/* ]]; then
            deactivate
            if [ -d ./.venv ]; then
                source ./.venv/bin/activate
                GREEN='\033[0;32m'  # Green color
                NC='\033[0m'        # No color (reset)

                # Construct the string with colors
                EXEC="$(pwd)/.venv/bin/activate"
                printf "Switch venv to ${GREEN}$EXEC${NC}\n"
            fi
        fi
    fi
}