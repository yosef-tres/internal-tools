# Tres Internal Tools

## Debugging Tools (`./dbg-tools`)

A collection of debugging tools for the Tres platform

## Fast & Dirty Commit (`fdc`)
### Installation

```bash
uv tool install yosef-tres/internal-tools/fdc
```

### Usage
```bash
fdc # alias for:
    # dev add fdc && \
    # fdc serve && \
    # open https://fdc.dev.local
```

## ZSH Utils

A collection of utility functions for ZSH to enhance your command-line experience.

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

#### Features:
- Automatically finds docker-compose.yml for compose operations
- Searches for containers by pattern
- Shows selection menu for multiple matches
- Pretty-prints logs with timestamps

### Development Utilities (`dev`)

A collection of utilities for local development.

- **Usage**: `dev <cmd> [domain]`
- **Commands**:
  - `a` - **a**dd domain
  - `rm` - **r**e**m**ove domain

### VirtualEnv Utilities (no manual invocation required)

Listens for directory change in zsh (not only when `cd`ing and activates the nearest (parent) .venv if found. Deactivates if none found.


## Installation

### Automatic Installation

```bash
curl -fsSL https://raw.githubusercontent.com/yosef-tres/internal-tools/main/zsh-utils/install.zsh | zsh
```

## Adding Your Own Utilities

You can add your own utility scripts to the `zsh-utils` directory. They'll be automatically sourced if you use the standard installation method. (after committing and pushing ofcourse)

## License

IDFK