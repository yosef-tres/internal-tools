#!/bin/zsh

# Docker utility function
# Usage: d <cmd> [docker_container]
# Commands:
#  e - execute bash/sh inside container
#  l - display pretty logs
#  lf - follow pretty logs
#  d - docker-compose down
#  u - docker-compose up
#  s - stop container
#  r - restart container
#  t - start container
#  ps - list containers with status (use -a to show stopped containers)
d() {
  # Check if command argument is provided
  if [[ -z $1 ]]; then
    echo "Usage: d <cmd> [docker_container]"
    echo "Commands:"
    echo "  e - (e)xecute bash/sh inside container"
    echo "  l - display pretty (l)ogs"
    echo "  lf - (f)ollow pretty logs"
    echo "  d - (d)own (stop and remove containers)"
    echo "  u - (u)p (start containers with docker-compose)"
    echo "  s - (s)top container"
    echo "  r - (r)estart container"
    echo "  t - s(t)art container"
    echo "  ps - list containers with status (use -a to show stopped containers)"
    return 1
  fi

  local cmd=$1
  local container_pattern=$2
  local containers=()
  local cmd_str=""

  # Function to find docker-compose.yml (only needed for up/down commands)
  find_compose_file() {
    local compose_file=""
    local current_dir=$PWD
    while [[ "$current_dir" != "" ]]; do
      if [[ -f "$current_dir/docker-compose.yml" ]]; then
        compose_file="$current_dir/docker-compose.yml"
        break
      elif [[ -f "$current_dir/compose.yml" ]]; then
        compose_file="$current_dir/compose.yml"
        break
      fi
      current_dir=${current_dir%/*}
    done
    echo "$compose_file"
  }

  # Function to get docker container based on pattern
  get_docker_container() {
    local pattern=$1
    local containers=()
    local selected_container=""
    
    # Get container list from docker
    if [[ -n "$pattern" ]]; then
      # If pattern provided, filter containers
      containers=($(docker ps --format "{{.Names}}" | grep -i "$pattern"))
    else
      # If no pattern provided, get all containers
      containers=($(docker ps --format "{{.Names}}"))
    fi

    # Check if any containers were found
    if [[ ${#containers[@]} -eq 0 ]]; then
      echo "No running containers found matching '$pattern'"
      return 1
    fi

    # If multiple containers found, show menu
    if [[ ${#containers[@]} -gt 1 ]]; then
      select container in "${containers[@]}"; do
        if [[ -n "$container" ]]; then
          # Use the exact container name that was selected
          selected_container="$container"
          break
        elif [[ -n "$REPLY" ]] && [[ "$REPLY" =~ ^[0-9]+$ ]] && [[ "$REPLY" -le ${#containers[@]} ]] && [[ "$REPLY" -gt 0 ]]; then
          # Handle numeric selection - convert to 1-based index for ZSH arrays
          selected_container="${containers[$REPLY]}"
          break
        fi
      done
    else
      # If only one container found
      selected_container="${containers[1]}"
    fi

    # Validate container selection
    if [[ -z "$selected_container" ]]; then
      echo "No container selected"
      return 1
    fi
    
    # Return the selected container name
    echo "$selected_container"
  }

  # Function to get service from docker-compose
  get_compose_service() {
    local pattern=$1
    local containers=()
    local selected_container=""
    
    # Get list of available services from docker-compose
    if [[ -n "$pattern" ]]; then
      # If pattern provided, filter services
      containers=($(docker compose ps --services | grep -i "$pattern"))
    else
      # If no pattern provided, get all services
      containers=($(docker compose ps --services))
    fi

    # Check if any services were found
    if [[ ${#containers[@]} -eq 0 ]]; then
      echo "No services found matching '$pattern'"
      return 1
    fi

    # If multiple services found, show menu
    if [[ ${#containers[@]} -gt 1 ]]; then
      echo "Multiple services found. Please select one:"
      select container in "${containers[@]}"; do
        if [[ -n "$container" ]]; then
          selected_container=$container
          break
        fi
      done
    else
      # If only one service found
      selected_container=${containers[1]}
    fi

    # Validate service selection
    if [[ -z "$selected_container" ]]; then
      echo "No service selected"
      return 1
    fi
    
    echo "$selected_container"
  }

  # Execute the appropriate command based on the option
  case "$cmd" in
    e)
      # Get container selection first, silently
      local selected_container
      selected_container=$(get_docker_container "$container_pattern") || return 1
      
      cmd_str="docker exec -it $selected_container sh -c 'if command -v bash >/dev/null; then bash; else sh; fi'"
      eval $cmd_str
      ;;
    l)
      # Get container selection first, silently
      local selected_container
      selected_container=$(get_docker_container "$container_pattern") || return 1
      
      # Get logs into a temporary file first
      local tmpfile=$(mktemp)
      docker logs --tail=100 "$selected_container" > "$tmpfile" 2>/dev/null
      
      # Add timestamps to each line
      while IFS= read -r line; do
        printf "%s %s\n" "$(date +"%H:%M:%S")" "$line"
      done < "$tmpfile"
      
      # Clean up
      rm -f "$tmpfile"
      ;;
    lf)
      # Get container selection first, silently
      local selected_container
      selected_container=$(get_docker_container "$container_pattern") || return 1
      
      # Use direct command with proper quoting
      # For follow mode we can't use a temp file, so we pipe directly
      docker logs -f --tail=100 "$selected_container" 2>/dev/null | while IFS= read -r line; do
        printf "%s %s\n" "$(date +"%H:%M:%S")" "$line"
      done
      ;;
    s)
      # Get container selection first, silently
      local selected_container
      selected_container=$(get_docker_container "$container_pattern") || return 1
      
      echo "Stopping container $selected_container..."
      # Stop the container
      docker stop "$selected_container"
      ;;
    r)
      # Get container selection first, silently
      local selected_container
      selected_container=$(get_docker_container "$container_pattern") || return 1
      
      docker restart "$selected_container"
      ;;
    t)
      # Get container selection first, silently
      local selected_container
      selected_container=$(get_docker_container "$container_pattern") || return 1
      
      docker start "$selected_container"
      ;;
    d)
      # Find docker-compose.yml (required for down command)
      local compose_file
      compose_file=$(find_compose_file)
      if [[ -z "$compose_file" ]]; then
        echo "Error: No docker-compose.yml or compose.yml found in current directory or parent directories."
        return 1
      fi
      
      local selected_service
      selected_service=$(get_compose_service "$container_pattern") || return 1
      
      cmd_str="docker compose down $selected_service"
      eval $cmd_str
      ;;
    u)
      # Find docker-compose.yml (required for up command)
      local compose_file
      compose_file=$(find_compose_file)
      if [[ -z "$compose_file" ]]; then
        echo "Error: No docker-compose.yml or compose.yml found in current directory or parent directories."
        return 1
      fi
      
      local selected_service
      selected_service=$(get_compose_service "$container_pattern") || return 1
      
      cmd_str="docker compose up -d $selected_service"
      eval $cmd_str
      ;;
    ps)
      # Process optional flags
      local show_all=""
      if [[ "$container_pattern" == "-a" ]]; then
        show_all="-a"
        container_pattern=""
      fi
      
      # Define colors
      local COLOR_RESET="\033[0m"
      local COLOR_GREEN="\033[32m"
      local COLOR_YELLOW="\033[33m"
      local COLOR_RED="\033[31m"
      local COLOR_BLUE="\033[34m"
      local COLOR_CYAN="\033[36m"
      local COLOR_GRAY="\033[37m"
      local COLOR_BOLD="\033[1m"
      
      echo "${COLOR_BOLD}CONTAINER STATUS${COLOR_RESET}"
      echo "────────────────────────────────────────────────────────────────────────────────"
      
      # Format header
      printf "${COLOR_BOLD}%-20s %-20s %-15s %-15s %-20s${COLOR_RESET}\n" "CONTAINER ID" "NAME" "STATUS" "IMAGE" "PORTS"
      
      # Get container list using docker
      local docker_cmd="docker ps $show_all --format=\"{{.ID}}|{{.Names}}|{{.Status}}|{{.Image}}|{{.Ports}}\""
      if [[ -n "$container_pattern" ]]; then
        docker_cmd="$docker_cmd | grep -i $container_pattern"
      fi
      
      eval $docker_cmd | while IFS='|' read -r id name container_status image ports; do
        # Determine color based on container_status
        local status_color=$COLOR_GRAY
        if [[ "$container_status" == *"Up"* ]]; then
          status_color=$COLOR_GREEN
        elif [[ "$container_status" == *"Exited (0)"* ]]; then
          status_color=$COLOR_BLUE
        elif [[ "$container_status" == *"Exited"* ]]; then
          status_color=$COLOR_RED
        elif [[ "$container_status" == *"Created"* ]]; then
          status_color=$COLOR_YELLOW
        fi
        
        # Truncate long fields for better formatting
        local short_id="${id:0:12}"
        local short_name="${name:0:18}"
        local short_status="${container_status:0:13}"
        local short_image="${image:0:13}"
        local short_ports="${ports:0:18}"
        
        # Print formatted row with color
        printf "${COLOR_CYAN}%-20s${COLOR_RESET} %-20s ${status_color}%-15s${COLOR_RESET} %-15s %-20s\n" \
          "$short_id" "$short_name" "$short_status" "$short_image" "$short_ports"
      done
      ;;
    *)
      echo "Invalid command: $cmd"
      echo "Valid commands: e (execute), l (logs), lf (follow logs), d (down), u (up), s (stop), r (restart), t (start), ps (list containers)"
      return 1
      ;;
  esac
}
