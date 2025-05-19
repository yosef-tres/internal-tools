function dev() {
  local action=$1
  # if at-least one argument shift
  if [[ $# -gt 0 ]]; then
    shift
  fi
  
  # Parse arguments
  local subdomain=""
  local port=""
  local urlpath=""
  
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --path=*)
        urlpath="${1#*=}"
        shift
        ;;
      --path)
        urlpath="$2"
        shift 2
        ;;
      *)
        if [[ -z "$subdomain" ]]; then
          subdomain="$1"
        elif [[ -z "$port" ]]; then
          port="$1"
        fi
        shift
        ;;
    esac
  done

  local domain="${subdomain}.dev.local"
  local base_domain="dev.local"
  local cert_dir="$HOME/.certs"
  local caddyfile="/opt/homebrew/etc/Caddyfile"

  if [[ "$action" != "add" && "$action" != "rm" ]]; then
    echo "Usage:"
    echo "  dev add <subdomain> <port> [--path=<path>]"
    echo "  dev rm <subdomain> [--path=<path>]"
    return 1
  fi

  if [[ "$action" == "add" && ( -z "$subdomain" || -z "$port" ) ]]; then
    echo "Usage: dev add <subdomain> <port> [--path=<path>]"
    return 1
  fi

  if [[ "$action" == "rm" && -z "$subdomain" ]]; then
    echo "Usage: dev rm <subdomain> [--path=<path>]"
    return 1
  fi

  # Normalize urlpath format
  if [[ -n "$urlpath" && "$urlpath" != /* ]]; then
    urlpath="/$urlpath"
  fi

  # remove trailing slash if exists
  if [[ -n "$urlpath" && "$urlpath" == */ ]]; then
    urlpath="${urlpath%/}"
  fi

  if ! command -v caddy >/dev/null 2>&1; then
    echo "❌ caddy not installed. Run: brew install caddy"
    return 1
  fi

  # Check if caddy service is running - use caddy with a valid argument
  if ! pgrep -x "caddy" >/dev/null 2>&1; then
    echo "❌ caddy service is not running. Run: brew services start caddy"
    return 1
  fi

  if [[ "$action" == "add" ]]; then
    # Ensure mkcert
    if ! command -v mkcert >/dev/null 2>&1; then
      echo "❌ mkcert not installed. Run: brew install mkcert"
      return 1
    fi

    mkcert -install

    mkdir -p "$cert_dir"
    local cert_file="$cert_dir/wildcard.$base_domain.pem"
    local key_file="$cert_dir/wildcard.$base_domain-key.pem"

    # Check if files already exist and skip if they do
    if [[ -f "$cert_file" && -f "$key_file" ]]; then
      echo "ℹ️  $cert_file and $key_file already exist. Skipping mkcert."
    else
      mkcert -cert-file "$cert_file" -key-file "$key_file" "*.$base_domain" "$base_domain"
    fi

    # Check if already exists in /etc/hosts without sudo
    if ! grep -q "$domain" /etc/hosts; then
      echo "ℹ️  Adding $domain to /etc/hosts, this will require sudo"
      echo "127.0.0.1 $domain" | sudo tee -a /etc/hosts
      echo "✅ Added $domain to /etc/hosts"
    else
      echo "ℹ️  $domain already exists in /etc/hosts, skipping"
    fi





    # Check if domain not exist in caddyfile add the initial block with path and default catchall
    if ! grep -q "$domain" "$caddyfile"; then
      echo "
$domain {
  tls $cert_file $key_file

  handle_path ${urlpath}* {
    reverse_proxy localhost:$port
  }

  handle /* {
    respond \"404 Not Found\" 404
  }
}
" | tee -a "$caddyfile"

    else
      echo "ℹ️  $domain already exists in $caddyfile"
      # Check if path already mounted
      if grep -q "handle_path ${urlpath}\*" "$caddyfile"; then
        echo "ℹ️  $domain with path $urlpath already exists in $caddyfile"
        return 0
      else
        # Create a temporary file to build the new domain block
        local temp_file=$(mktemp)
        
        # Create the domain opening with TLS config
        echo "$domain {" > "$temp_file"
        echo "  tls $cert_file $key_file" >> "$temp_file"
        echo "" >> "$temp_file"
        
        # Extract all existing handle_path blocks and add them to our new config
        # This approach preserves all existing path handlers
        sed -n "/$domain {/,/^}/p" "$caddyfile" | 
        awk '/handle_path/ {
          # Found a handle_path line, now collect the entire block
          print $0
          in_block = 1
          next
        }
        in_block && /}/ {
          # End of the handle_path block
          print $0
          in_block = 0
          next
        }
        in_block {
          # Lines inside the handle_path block
          print $0
        }' >> "$temp_file"
        
        # Add the new path handler
        cat << EOF >> "$temp_file"
  handle_path ${urlpath}* {
    reverse_proxy localhost:$port
  }

  handle /* {
    respond "404 Not Found" 404
  }
}
EOF
        
        # Remove the existing domain block
        sed -i '' "/$domain {/,/^}/d" "$caddyfile"
        
        # Add our new combined block
        cat "$temp_file" >> "$caddyfile"
        
        # Clean up
        rm "$temp_file"
        
        echo "✅ Added $domain with path $urlpath to $caddyfile"
      fi
    fi

    caddy fmt --overwrite --config $caddyfile 
    caddy reload --config $caddyfile 
    if [[ -n "$urlpath" ]]; then
      echo "🎉 https://$domain$urlpath → localhost:$port"
    else
      echo "🎉 https://$domain → localhost:$port"
    fi

  elif [[ "$action" == "rm" ]]; then
    # /etc/hosts
    # Only remove from hosts if no paths are left for this domain
    local path_identifier=""
    if [[ -n "$urlpath" ]]; then
      path_identifier=" ${urlpath}"
      path_identifier="${path_identifier// /_}"
    fi
    
    local domain_path_pattern="${domain}${path_identifier}"
    
    if [[ -n "$urlpath" ]]; then
      # Only remove the specific path block
      if grep -q "$domain_path_pattern" "$caddyfile"; then
        sed -i '' "/$domain_path_pattern {/,/^}/d" "$caddyfile"
        echo "✅ Removed $domain with path $urlpath block from $caddyfile"
        caddy fmt --overwrite --config $caddyfile
        caddy reload --config $caddyfile
      else
        echo "ℹ️  $domain with path $urlpath not found in $caddyfile"
      fi
      
      # Check if any other paths for this domain exist
      if ! grep -q "$domain" "$caddyfile"; then
        if grep -q "$domain" /etc/hosts; then
          sudo sed -i '' "/$domain/d" /etc/hosts
          echo "✅ Removed $domain from /etc/hosts"
        else
          echo "ℹ️  $domain not found in /etc/hosts"
        fi
      else
        echo "ℹ️  Other paths for $domain still exist, keeping it in /etc/hosts"
      fi
    else
      # Remove all blocks for this domain
      if grep -q "$domain" /etc/hosts; then
        sudo sed -i '' "/$domain/d" /etc/hosts
        echo "✅ Removed $domain from /etc/hosts"
      else
        echo "ℹ️  $domain not found in /etc/hosts"
      fi

      # Caddyfile - remove all blocks containing this domain
      if grep -q "$domain" "$caddyfile"; then
        sed -i '' "/$domain {/,/^}/d" "$caddyfile"
        echo "✅ Removed all $domain blocks from $caddyfile"
        caddy fmt --overwrite --config $caddyfile
        caddy reload --config $caddyfile
      else
        echo "ℹ️  $domain not found in $caddyfile"
      fi
    fi
  fi
}
