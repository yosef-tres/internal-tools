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
  # Download all utility files from GitHub repo
  print_info "Downloading all utility files from GitHub repository..."
  
  # GitHub repo details
  GITHUB_OWNER="yosef-tres"
  GITHUB_REPO_NAME="zsh-tools"
  GITHUB_PATH="utils"
  
  # Use GitHub API to get contents of the utils directory
  print_info "Retrieving utility files list from GitHub..."
  if command -v curl >/dev/null 2>&1; then
    # Get directory listing with curl and extract filenames ending with -utils.zsh
    # This will work even without authentication for public repos
    FILES_JSON=$(curl -s "https://api.github.com/repos/${GITHUB_OWNER}/${GITHUB_REPO_NAME}/contents/${GITHUB_PATH}")
    
    # Make sure we got a valid response
    if echo "$FILES_JSON" | grep -q "name"; then
      print_info "Found utility files, downloading..."
      
      # Extract filenames and download each one
      echo "$FILES_JSON" | grep -o '"name":"[^"]*-utils\.zsh"' | cut -d '"' -f 4 | while read -r file; do
        print_info "Downloading $file..."
        if download_file "${GITHUB_REPO}/utils/${file}" "${UTILS_DIR}/${file}" 2>/dev/null; then
          print_success "Downloaded $file"
          DOWNLOAD_SUCCESS=true
        fi
      done
    else
      print_warning "Could not retrieve utils directory listing from GitHub API. Response: ${FILES_JSON}"
    fi
  else
    print_warning "curl not available, falling back to local install method"
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
if [ "$DOWNLOAD_SUCCESS" = false ] || [ ! "$(ls -A "${UTILS_DIR}" 2>/dev/null)" ]; then
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
  print_info "Updating existing ZSH Tools source in .zshrc..."
  # Remove any existing ZSH Tools source lines
  sed -i.bak '/source.*zsh-tools/d' "$ZSHRC"
  sed -i.bak '/Source ZSH Tools/d' "$ZSHRC"
  sed -i.bak '/for util_file in.*zsh-tools.*utils/d' "$ZSHRC"
  sed -i.bak '/done/d' "$ZSHRC"
  rm -f "${ZSHRC}.bak"
  
  # Add new source block
  print_info "Adding new ZSH Tools source block to .zshrc..."
  echo "" >> "$ZSHRC"
  echo "$SOURCE_LINE" >> "$ZSHRC"
  echo "for util_file in \"\${HOME}/.zsh-tools/utils\"/*-utils.zsh; do" >> "$ZSHRC"
  echo "  source \"\$util_file\"" >> "$ZSHRC"
  echo "done" >> "$ZSHRC"
else
  # Add source block to .zshrc
  print_info "Adding ZSH Tools source block to .zshrc..."
  echo "" >> "$ZSHRC"
  echo "$SOURCE_LINE" >> "$ZSHRC"
  echo "for util_file in \"\${HOME}/.zsh-tools/utils\"/*-utils.zsh; do" >> "$ZSHRC"
  echo "  source \"\$util_file\"" >> "$ZSHRC"
  echo "done" >> "$ZSHRC"
fi

print_success "Installation complete!"
print_info "To start using ZSH Tools now, run: source ${ZSHRC}"
print_info "Or simply restart your terminal."

# Source the utilities in the current shell if interactive
if [[ $- == *i* ]]; then
  for util_file in "${UTILS_DIR}"/*-utils.zsh; do
    source "$util_file"
  done
  print_success "ZSH Tools loaded in the current shell."
  print_info "Try using any of the loaded utility commands."
fi
