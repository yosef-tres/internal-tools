#!/bin/zsh

# Docker utility command
# Usage: d <command> [pattern] [extra docker flags...]
# Commands:
#   e   - exec into container (bash/sh)
#   l   - tail logs with timestamps
#   lf  - follow logs with timestamps
#   d   - docker compose down
#   u   - docker compose up -d
#   s   - stop container
#   r   - restart container
#   t   - start container
#   ps  - show container status (use -a to include stopped)

# Shortcuts
unalias dps 2>/dev/null
alias dps='d ps'
alias du='d u'
alias dd='d d'
alias de='d e'
alias dl='d l'
alias dlf='d lf'
alias ds='d s'
alias dr='d r'
alias dt='d t'

function d() {
  if [[ -z $1 ]]; then
    echo "Usage: d <command> [pattern] [extra flags...]"
    return 1
  fi

  local cmd=$1
  shift
  local pattern=""
  local extra=()

  if [[ $# -gt 0 ]]; then
    if [[ $1 == -* ]]; then
      extra=($@)
    else
      pattern=$1
      shift
      extra=($@)
    fi
  fi

  select_container() {
    local pattern="$1"
    local filter_status="$2"  # optional: "running", "stopped", or "all"
    local containers=()

    if [[ "$filter_status" == "stopped" ]]; then
      containers=($(docker ps -a --filter "status=exited" --filter "status=created" --format '{{.Names}}' | grep -i "$pattern" 2>/dev/null))
    elif [[ "$filter_status" == "running" ]]; then
      containers=($(docker ps --format '{{.Names}}' | grep -i "$pattern" 2>/dev/null))
    else
      containers=($(docker ps -a --format '{{.Names}}' | grep -i "$pattern" 2>/dev/null))
    fi

    [[ ${#containers[@]} -eq 0 ]] && echo "No containers found matching '$pattern' with status '$filter_status'" && return 1
    [[ ${#containers[@]} -eq 1 ]] && echo ${containers[1]} && return 0

    echo "Multiple containers found:" >&2
    select c in "${containers[@]}"; do
      [[ -n $c ]] && echo "$c" && return 0
    done
    return 1
  }

  select_service() {
    local services=($(docker compose config --services 2>/dev/null | grep -i "$1"))
    [[ ${#services[@]} -eq 0 ]] && echo "No service matching '$1'" && return 1
    [[ ${#services[@]} -eq 1 ]] && echo ${services[1]} && return 0
    echo "Multiple services found:" >&2
    select s in "${services[@]}"; do
      [[ -n $s ]] && echo "$s" && return 0
    done
    return 1
  }

  timestamp_log() {
    while IFS= read -r line; do
      echo "$(date +%H:%M:%S) $line"
    done
  }

  case "$cmd" in
    e)
      local c=$(select_container "$pattern" "running") || return 1
      docker exec -it "$c" ${extra[@]} sh -c 'command -v bash >/dev/null && exec bash || exec sh'
      ;;
    l)
      local c=$(select_container "$pattern" "running") || return 1
      docker logs --tail=100 ${extra[@]} "$c" 2>/dev/null | timestamp_log
      ;;
    lf)
      local c=$(select_container "$pattern" "running") || return 1
      docker logs -f --tail=100 ${extra[@]} "$c" 2>/dev/null | timestamp_log
      ;;
    d)
      local s=""
      [[ -n "$pattern" ]] && s=$(select_service "$pattern") || s=""
      docker compose down $s ${extra[@]}
      ;;
    u)
      local s=""
      [[ -n "$pattern" ]] && s=$(select_service "$pattern") || s=""
      docker compose up -d $s ${extra[@]}
      ;;
    s)
      local c=$(select_container "$pattern" "running") || return 1
      docker stop ${extra[@]} "$c"
      ;;
    r)
      local c=$(select_container "$pattern" "running") || return 1
      docker restart ${extra[@]} "$c"
      ;;
    t)
      local c=$(select_container "$pattern" "stopped") || return 1
      docker start ${extra[@]} "$c"
      ;;
    ps)
      local show_all=""
      local filter_pattern=""

      for arg in "$pattern" "${extra[@]}"; do
        if [[ "$arg" == "-a" ]]; then
          show_all="-a"
        else
          filter_pattern="$arg"
        fi
      done

      local GREEN='\033[0;32m'
      local RED='\033[0;31m'
      local YELLOW='\033[1;33m'
      local BLUE='\033[0;34m'
      local BOLD='\033[1m'
      local RESET='\033[0m'

      printf "${BOLD}%-20s %-25s %-20s %-20s %-30s${RESET}\n" "CONTAINER ID" "NAME" "STATUS" "IMAGE" "PORTS"
      docker ps $show_all --format '{{.ID}}|{{.Names}}|{{.Status}}|{{.Image}}|{{.Ports}}' |
      { [[ -n "$filter_pattern" ]] && grep -i "$filter_pattern" || cat; } |
      while IFS='|' read -r id name container_status image ports; do
        local color="$RESET"
        if [[ "$container_status" == *"Up"* ]]; then
          color=$GREEN
        elif [[ "$container_status" == *"Exited (0)"* ]]; then
          color=$BLUE
        elif [[ "$container_status" == *"Exited"* ]]; then
          color=$RED
        elif [[ "$container_status" == *"Created"* ]]; then
          color=$YELLOW
        fi
        printf "${color}%-20s %-25s %-20s %-20s %-30s${RESET}\n" "$id" "$name" "$container_status" "$image" "$ports"
      done
      ;;
    *)
      echo "Unknown command: $cmd"
      return 1
      ;;
  esac
}

