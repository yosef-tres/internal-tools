# ZSH Tools

A collection of utility functions for ZSH to enhance your command-line experience.

## Features

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

### Features:
- Automatically finds docker-compose.yml for compose operations
- Searches for containers by pattern
- Shows selection menu for multiple matches
- Pretty-prints logs with timestamps

## Installation

### Automatic Installation

```bash
curl -fsSL https://raw.githubusercontent.com/yosef-tres/zsh-tools/main/install.zsh | zsh
```

### Manual Installation

1. Clone the repository:
```bash
git clone https://github.com/yosef-tres/zsh-tools.git "$HOME/.zsh-tools"
```

2. Add the source line to your `.zshrc`:
```bash
echo 'source "$HOME/.zsh-tools/utils/docker-utils.zsh"' >> ~/.zshrc
```

3. Apply changes:
```bash
source ~/.zshrc
```

## Adding Your Own Utilities

You can add your own utility scripts to the `utils` directory. They'll be automatically sourced if you use the standard installation method.

## License

MIT
