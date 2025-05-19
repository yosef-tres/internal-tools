# General Repository Structure

## Repository Organization

This repository contains various internal tools developed by the Tres team:

- `dbg-tools/` - Contains debugging tools for the Tres platform
- `fdc/` - Fast & Dirty Commit tool (a Streamlit app for Git operations)
- `zsh-utils/` - Collection of ZSH utility functions
- `install.zsh` - Installation script for ZSH utilities

## Common Practices

- Each tool follows its own directory structure depending on its needs
- Tools are designed to be easily installable and usable in the development workflow
- Many tools integrate with the `dev` command system for local domain setup
- Python tools use UV for dependency management

## Installation

Most tools in this repository can be installed using one of these methods:

1. Direct installation via UV tool:
```bash
uv tool install yosef-tres/internal-tools/<tool-name>
```

2. For ZSH utilities:
```bash
curl -fsSL https://raw.githubusercontent.com/yosef-tres/internal-tools/main/zsh-utils/install.zsh | zsh
```

## Development Guidelines

- Add documentation for each tool
- Follow the standard structure for the respective tool type
- Make sure tools are easily installable
- Include examples in the README
