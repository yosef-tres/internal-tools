#!/usr/bin/env zsh

# ZSH Tools Installer
# Author: Yosef Abraham
# Usage: curl -fsSL https://raw.githubusercontent.com/yosef-tres/internal-tools/main/zsh-utils/install.zsh | zsh

# ─────────────────────────────────────────────────────────────
# Color definitions
COL_GREEN="\033[0;32m"
COL_YELLOW="\033[0;33m"
COL_RED="\033[0;31m"
COL_BLUE="\033[0;34m"
COL_RESET="\033[0m"

# ─────────────────────────────────────────────────────────────
# Constants
ZSH_TOOLS_DIR="$HOME/.zsh-utils"
ZSHRC="$HOME/.zshrc"
GITHUB_USER="yosef-tres"
GITHUB_REPO="internal-tools"
GITHUB_ZIP_URL="https://github.com/$GITHUB_USER/$GITHUB_REPO/archive/refs/heads/main.zip"
GITHUB_CLONE_URL="https://github.com/$GITHUB_USER/$GITHUB_REPO.git"

# ─────────────────────────────────────────────────────────────
# Utility functions
print_msg() {
  local type=$1 msg=$2
  case $type in
    info)    echo "${COL_BLUE}INFO:${COL_RESET} $msg" ;;
    success) echo "${COL_GREEN}SUCCESS:${COL_RESET} $msg" ;;
    warn)    echo "${COL_YELLOW}WARNING:${COL_RESET} $msg" ;;
    error)   echo "${COL_RED}ERROR:${COL_RESET} $msg" ;;
  esac
}

abort() {
  print_msg error "$1"
  exit 1
}

ensure_zsh() {
  [[ -n $ZSH_VERSION ]] || abort "This script must be run with zsh."
}

safe_download() {
  local url=$1 dest=$2
  if command -v curl >/dev/null; then
    curl -fsSL "$url" -o "$dest" || return 1
  elif command -v wget >/dev/null; then
    wget -q "$url" -O "$dest" || return 1
  else
    return 1
  fi
}

source_utilities() {
  for util_file in "$ZSH_TOOLS_DIR"/*-utils.zsh(N); do
    source "$util_file"
  done
}

add_to_zshrc() {
  grep -q '# Source ZSH Tools' "$ZSHRC" && return

  print_msg info "Adding source block to .zshrc..."
  cat >> "$ZSHRC" <<EOF

# Source ZSH Tools
for util_file in "\$HOME/.zsh-utils"/*-utils.zsh(N); do
  source "\$util_file"
done
EOF
}

install_from_git() {
  print_msg info "Attempting to clone via git..."
  command -v git >/dev/null || return 1
  local temp_dir=$(mktemp -d)
  git clone --depth=1 "$GITHUB_CLONE_URL" "$temp_dir" >/dev/null 2>&1 || return 1
  [[ -d "$temp_dir/zsh-utils" ]] || return 1
  cp -r "$temp_dir/zsh-utils"/* "$ZSH_TOOLS_DIR/" || return 1
  rm -rf "$temp_dir"
  return 0
}

install_from_zip() {
  print_msg info "Falling back to ZIP download..."
  command -v curl >/dev/null || return 1
  command -v unzip >/dev/null || return 1
  local temp_dir=$(mktemp -d)
  local zip_file="$temp_dir/tools.zip"
  curl -fsSL "$GITHUB_ZIP_URL" -o "$zip_file" || return 1
  unzip -q "$zip_file" -d "$temp_dir" || return 1
  local extract_dir=$(find "$temp_dir" -type d -name "$GITHUB_REPO-*" | head -n1)
  [[ -d "$extract_dir/zsh-utils" ]] || return 1
  cp -r "$extract_dir/zsh-utils"/* "$ZSH_TOOLS_DIR/" || return 1
  rm -rf "$temp_dir"
  return 0
}

install_from_local() {
  local script_dir="$(cd -- "$(dirname "$0")" && pwd)"
  [[ -d "$script_dir" ]] || return 1
  cp "$script_dir"/* "$ZSH_TOOLS_DIR/" || return 1
  print_msg warn "Installed from local directory."
  return 0
}

# ─────────────────────────────────────────────────────────────
# Main
ensure_zsh

print_msg info "Installing ZSH Tools to $ZSH_TOOLS_DIR..."
mkdir -p "$ZSH_TOOLS_DIR"

if install_from_git || install_from_zip || install_from_local; then
  chmod +x "$ZSH_TOOLS_DIR"/*.zsh(N)
  print_msg success "Utility scripts installed."
else
  abort "All download methods failed."
fi

add_to_zshrc

if [[ $- == *i* ]]; then
  source_utilities
  print_msg success "ZSH Tools loaded in current shell."
fi

print_msg success "Installation complete!"
print_msg info "To activate now: source $ZSHRC"
print_msg info "Or just restart your terminal."
