# Fast & Dirty Commit (FDC) Structure

## Overview

FDC is a Streamlit app for Git operations (staging, committing, pushing) with a web interface.

## Directory Structure

```
fdc/
├── .streamlit/             # Streamlit configuration
│   └── secrets.toml        # Secrets configuration
├── .venv/                  # Virtual environment
├── .vscode/                # VS Code configuration
├── fdc/                    # Main package
│   ├── ui/                 # UI components
│   │   └── sidebar.py      # Sidebar implementation
│   ├── db/                 # Database components
│   │   └── session.py      # DB session management
│   ├── app.py              # Main Streamlit application entry
│   └── ...                 # Other modules
├── migrations/             # Alembic database migrations
├── README.md               # Documentation
├── alembic.ini             # Alembic configuration
├── pyproject.toml          # Project dependencies and metadata
└── fdc_database.sqlite     # SQLite database file
```

## Key Components

- **CLI Interface**: Commands for serving the app and other operations
- **Streamlit App**: Web interface for Git operations
- **Local Domain Integration**: Setup via `dev add fdc`
- **Database**: SQLite with Alembic for migrations

## Installation

```bash
uv tool install yosef-tres/internal-tools/fdc
```

## Usage

```bash
fdc  # Alias for:
     # dev add fdc && \
     # fdc serve && \
     # open https://fdc.dev.local
```

## Implementation Notes

- The `dev` command is a zsh function, not a standalone executable, so it must be run using `zsh -c "dev add fdc"`
- The app uses `subprocess.run` to execute shell commands from Python
- Streamlit is used for the web interface
- SQLite database with Alembic for migrations
