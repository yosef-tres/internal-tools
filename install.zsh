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
  TEMP_DIR=$(mktemp -d)
  
  # Method 1: Try git clone (fastest and most reliable)
  if command -v git >/dev/null 2>&1; then
    print_info "Using git to download files..."
    if git clone --depth=1 "https://github.com/${GITHUB_OWNER}/${GITHUB_REPO_NAME}.git" "$TEMP_DIR" >/dev/null 2>&1; then
      # Copy just the utils directory
      if [ -d "${TEMP_DIR}/utils" ]; then
        cp -r "${TEMP_DIR}/utils"/* "${UTILS_DIR}/"
        print_success "Successfully downloaded utility files using git"
        DOWNLOAD_SUCCESS=true
      else
        print_warning "Utils directory not found in the repository"
      fi
    else
      print_warning "Git clone failed, trying alternative method"
    fi
  # Method 2: Try downloading ZIP file
  elif command -v curl >/dev/null 2>&1; then
    print_info "Using curl to download repository ZIP..."
    ZIP_URL="https://github.com/${GITHUB_OWNER}/${GITHUB_REPO_NAME}/archive/refs/heads/main.zip"
    ZIP_FILE="${TEMP_DIR}/repo.zip"
    
    if curl -sL "$ZIP_URL" -o "$ZIP_FILE"; then
      # Check if unzip is available
      if command -v unzip >/dev/null 2>&1; then
        print_info "Extracting ZIP file..."
        unzip -q "$ZIP_FILE" -d "$TEMP_DIR"
        # Find the extracted directory (it might have a suffix like -main)
        EXTRACT_DIR=$(find "$TEMP_DIR" -type d -name "${GITHUB_REPO_NAME}*" | head -n 1)
        
        if [ -d "${EXTRACT_DIR}/utils" ]; then
          cp -r "${EXTRACT_DIR}/utils"/* "${UTILS_DIR}/"
          print_success "Successfully downloaded utility files using ZIP"
          DOWNLOAD_SUCCESS=true
        else
          print_warning "Utils directory not found in the ZIP file"
        fi
      else
        print_warning "unzip command not available, falling back to local install"
      fi
    else
      print_warning "Failed to download ZIP file"
    fi
  else
    print_warning "Neither git nor curl available, falling back to local install method"
  fi
  
  # Clean up temp directory
  rm -rf "$TEMP_DIR"
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
if grep -q "# Source ZSH Tools" "$ZSHRC"; then
  # Skip
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
