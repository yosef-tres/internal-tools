function chpwd() {
    local GREEN='\033[0;32m'
    local RED='\033[0;31m'
    local NC='\033[0m'

    local dir="$PWD"
    local found_venv=""
    local venv_activate=""
    local realpath_cmd

    if command -v realpath &>/dev/null; then
        realpath_cmd="realpath"
    else
        realpath_cmd="python3 -c 'import os,sys; print(os.path.realpath(sys.argv[1]))'"
    fi

    # Search upwards for nearest .venv
    while [ "$dir" != "/" ]; do
        if [ -f "$dir/.venv/bin/activate" ]; then
            found_venv="$($realpath_cmd "$dir/.venv")"
            venv_activate="$found_venv/bin/activate"
            break
        fi
        dir="$(dirname "$dir")"
    done

    # Normalize current VIRTUAL_ENV
    local current_venv=""
    if [ -n "$VIRTUAL_ENV" ]; then
        current_venv="$($realpath_cmd "$VIRTUAL_ENV" 2>/dev/null || echo "")"
    fi

    # Decide action
    if [ -n "$current_venv" ]; then
        if [ -z "$found_venv" ]; then
            deactivate
            echo "${RED}Deactivated virtualenv${NC}"
        elif [ "$found_venv" != "$current_venv" ]; then
            deactivate
            source "$venv_activate"
            echo "Switched to virtualenv: ${GREEN}$found_venv${NC}"
        fi
    else
        if [ -n "$found_venv" ]; then
            source "$venv_activate"
            echo "Activated virtualenv: ${GREEN}$found_venv${NC}"
        fi
    fi
}
