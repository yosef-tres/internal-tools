function dev() {
  local action=$1
  local subdomain=$2
  local port=$3

  local domain="${subdomain}.dev.local"
  local base_domain="dev.local"
  local cert_dir="$HOME/.certs"
  local caddyfile="/opt/homebrew/etc/Caddyfile"

  if [[ "$action" != "add" && "$action" != "rm" ]]; then
    echo "Usage:"
    echo "  dev add <subdomain> <port>"
    echo "  dev rm <subdomain>"
    return 1
  fi

  if [[ "$action" == "add" && ( -z "$subdomain" || -z "$port" ) ]]; then
    echo "Usage: dev add <subdomain> <port>"
    return 1
  fi

  if [[ "$action" == "rm" && -z "$subdomain" ]]; then
    echo "Usage: dev rm <subdomain>"
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

    mkcert -cert-file "$cert_file" -key-file "$key_file" "*.$base_domain" "$base_domain"

    # /etc/hosts
    if ! grep -q "$domain" /etc/hosts; then
      echo "127.0.0.1 $domain" | sudo tee -a /etc/hosts
      echo "✅ Added $domain to /etc/hosts"
    else
      echo "ℹ️  $domain already exists in /etc/hosts"
    fi

    # Caddy
    local block="
$domain {
  tls $cert_file $key_file
  reverse_proxy localhost:$port
}
"
    if grep -q "$domain" "$caddyfile"; then
      echo "ℹ️  $domain already exists in $caddyfile"
    else
      echo "$block" | tee -a "$caddyfile"
      echo "✅ Added $domain to $caddyfile"
    fi

    caddy fmt --overwrite --config $caddyfile 
    caddy reload --config $caddyfile 
    echo "🎉 https://$domain → localhost:$port"

  elif [[ "$action" == "rm" ]]; then
    # /etc/hosts
    if grep -q "$domain" /etc/hosts; then
      sed -i '' "/$domain/d" /etc/hosts
      echo "✅ Removed $domain from /etc/hosts"
    else
      echo "ℹ️  $domain not found in /etc/hosts"
    fi

    # Caddyfile
    if grep -q "$domain" "$caddyfile"; then
      sed -i '' "/$domain {/,/^}/d" "$caddyfile"
      echo "✅ Removed $domain block from $caddyfile"
      caddy fmt --overwrite --config $caddyfile
      caddy reload --config $caddyfile
    else
      echo "ℹ️  $domain not found in $caddyfile"
    fi
  fi
}
