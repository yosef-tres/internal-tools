# ZSH Utils Structure

## Overview

A collection of utility functions for ZSH to enhance the command-line experience, primarily focused on Docker container management and local development workflows.

## Directory Structure

```
zsh-utils/
├── utils/                  # Utility script files
└── install.zsh             # Installation script
```

## Key Components

### Docker Utilities (`d`)

A powerful Docker container management utility with the following features:

- **Usage**: `d <cmd> [docker_container]`
- **Commands**:
  - `e` - **e**xecute bash/sh inside container
  - `l` - display pretty **l**ogs
  - `lf` - **f**ollow pretty logs
  - `s` - **s**top container
  - `r` - **r**estart container
  - `t` - s**t**art container
  - `d` - **d**own (stop and remove containers with docker-compose)
  - `u` - **u**p (start containers with docker-compose)
  - `ps` - list containers with status (use -a to show stopped containers)

### Development Utilities (`dev`)

A collection of utilities for local development:

- **Usage**: `dev <cmd> [domain]`
- **Commands**:
  - `a` - **a**dd domain
  - `rm` - **r**e**m**ove domain

### VirtualEnv Utilities

Automatic virtual environment activation/deactivation:
- Listens for directory changes in zsh
- Activates the nearest (parent) .venv if found
- Deactivates if none found

## Installation

```bash
curl -fsSL https://raw.githubusercontent.com/yosef-tres/internal-tools/main/zsh-utils/install.zsh | zsh
```

## Adding Custom Utilities

Custom utility scripts can be added to the `zsh-utils` directory and will be automatically sourced if the standard installation method is used (after committing and pushing).
