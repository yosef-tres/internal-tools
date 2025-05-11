#!/usr/bin/env zsh

# ZSH Tools Installer
# Author: Yosef Abraham
# Usage: curl -fsSL https://raw.githubusercontent.com/yosef-tres/zsh-tools/main/install.zsh | zsh

# Color definitions
COL_GREEN="\033[0;32m"
COL_YELLOW="\033[0;33m"
COL_RED="\033[0;31m"
COL_BLUE="\033[0;34m"
COL_RESET="\033[0m"

# Install directory
ZSH_TOOLS_DIR="${HOME}/.zsh-tools"
UTILS_DIR="${ZSH_TOOLS_DIR}/utils"
GITHUB_REPO="https://raw.githubusercontent.com/yosef-tres/zsh-tools/main"

# Message functions
print_info() {
  echo "${COL_BLUE}INFO:${COL_RESET} $1"
}

print_success() {
  echo "${COL_GREEN}SUCCESS:${COL_RESET} $1"
}

print_warning() {
  echo "${COL_YELLOW}WARNING:${COL_RESET} $1"
}

print_error() {
  echo "${COL_RED}ERROR:${COL_RESET} $1"
}

# Check if ZSH is running
if [ -z "$ZSH_VERSION" ]; then
  print_error "This script requires zsh to run. Please run with zsh: zsh install.zsh"
  exit 1
fi

# Create installation directories
print_info "Setting up ZSH Tools in ${ZSH_TOOLS_DIR}..."
mkdir -p "${UTILS_DIR}"

# Function to download a file
download_file() {
  local url="$1"
  local dest="$2"
  
  if command -v curl >/dev/null 2>&1; then
    curl -fsSL "$url" -o "$dest"
  elif command -v wget >/dev/null 2>&1; then
    wget -q "$url" -O "$dest"
  else
    print_error "Neither curl nor wget found. Please install one of them and try again."
    exit 1
  fi
}

# Download utility files
print_info "Downloading utility files..."

# Try to download from GitHub
LOCAL_INSTALL=false
DOWNLOAD_SUCCESS=false

# Function to find all utility files in the directory
find_utils_files() {
  local dir="$1"
  find "$dir" -type f -name "*-utils.zsh"
}

# Try GitHub download first
if [ "$LOCAL_INSTALL" = false ]; then
  # Download list of files from GitHub repo
  print_info "Downloading from GitHub repository..."
  # Start with known utility: docker-utils.zsh
  if download_file "${GITHUB_REPO}/utils/docker-utils.zsh" "${UTILS_DIR}/docker-utils.zsh"; then
    DOWNLOAD_SUCCESS=true
    # Try to find other utility files by checking common ones
    COMMON_UTILS=("git" "aws" "k8s" "terraform")
    for util in "${COMMON_UTILS[@]}"; do
      download_file "${GITHUB_REPO}/utils/${util}-utils.zsh" "${UTILS_DIR}/${util}-utils.zsh" 2>/dev/null || true
    done
  fi
fi

# If GitHub download failed or we're running locally
if [ "$DOWNLOAD_SUCCESS" = false ]; then
  # If download fails and we're running the script from a local repo, copy files directly
  SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
  if [ -d "${SCRIPT_DIR}/utils" ]; then
    print_warning "GitHub download failed, using local files instead..."
    # Find all utility files and copy them
    for util_file in $(find_utils_files "${SCRIPT_DIR}/utils"); do
      cp "$util_file" "${UTILS_DIR}/$(basename "$util_file")"
      DOWNLOAD_SUCCESS=true
    done
    LOCAL_INSTALL=true
  fi
fi

# Check if installation was successful
if [ "$DOWNLOAD_SUCCESS" = false ] || [ ! -f "${UTILS_DIR}/docker-utils.zsh" ]; then
  print_error "Failed to install utility files."
  exit 1
fi

# Make utilities executable
chmod +x "${UTILS_DIR}"/*.zsh

print_success "Utility files downloaded successfully."

# Update .zshrc to source the utilities
ZSHRC="${HOME}/.zshrc"
SOURCE_LINE="# Source ZSH Tools"

# Create a source block for all utility files
TOOLS_SOURCE_BLOCK="# Source ZSH Tools\n"
TOOLS_SOURCE_BLOCK+="for util_file in \"\${HOME}/.zsh-tools/utils\"/*-utils.zsh; do\n"
TOOLS_SOURCE_BLOCK+="  source \"\$util_file\"\n"
TOOLS_SOURCE_BLOCK+="done"

# Check if .zshrc exists
if [ ! -f "$ZSHRC" ]; then
  print_warning ".zshrc not found. Creating a new one."
  touch "$ZSHRC"
fi

# Check if source line already exists and update it
if grep -q "source.*zsh-tools" "$ZSHRC"; then
  print_info "Updating existing ZSH Tools source line in .zshrc..."
  # Use sed to replace existing source line
  sed -i.bak -E "s|source.*zsh-tools.*|${TOOLS_SOURCE_LINE}|g" "$ZSHRC"
  rm -f "${ZSHRC}.bak"
else
  # Add source line to .zshrc
  print_info "Adding ZSH Tools source line to .zshrc..."
  echo "" >> "$ZSHRC"
  echo "$SOURCE_LINE" >> "$ZSHRC"
  echo "$TOOLS_SOURCE_LINE" >> "$ZSHRC"
fi

print_success "Installation complete!"
print_info "To start using ZSH Tools now, run: source ${ZSHRC}"
print_info "Or simply restart your terminal."

# Source the utilities in the current shell if interactive
if [[ $- == *i* ]]; then
  source "${UTILS_DIR}/docker-utils.zsh"
  print_success "ZSH Tools loaded in the current shell."
  print_info "Try running 'd' to see available Docker commands."
fi
