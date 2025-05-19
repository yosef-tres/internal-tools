# FDC (Fast & Dirty Commit) Project Structure

## Project Overview

FDC (Fast & Dirty Commit) is a Streamlit-based internal tool designed to simplify Git operations like staging, committing, and pushing. The tool has been extended with a SQLAlchemy SQLite database implementation to support collections and collection_parts models.

## Project Structure

```
fdc/
├── fdc/                        # Main package directory
│   ├── __init__.py             # Package initialization
│   ├── __main__.py             # Entry point for direct execution
│   ├── app.py                  # Main Streamlit application
│   ├── cli.py                  # CLI interface
│   ├── data.py                 # Data utility functions
│   ├── db/                     # Database package
│   │   ├── __init__.py         # Database package initialization
│   │   ├── crud.py             # CRUD operations
│   │   ├── models.py           # SQLAlchemy models
│   │   ├── session.py          # Database session configuration
│   │   └── setup.py            # Database initialization utilities
│   └── ui/                     # UI components
│       ├── __init__.py         # UI package initialization
│       ├── auto_progress.py    # Progress tracking utilities
│       ├── components.py       # Reusable UI components
│       ├── sidebar.py          # Sidebar UI component
│       └── stages.py           # Processing stage components
├── migrations/                 # Alembic migrations directory
│   ├── env.py                  # Alembic environment configuration
│   ├── script.py.mako          # Migration script template
│   └── versions/               # Migration version files
│       └── initial_migration.py # Initial database schema
├── alembic.ini                 # Alembic configuration file
└── pyproject.toml              # Project metadata and dependencies
```

## Database Model Design

### SQLAlchemy Models

Two main models were implemented:

1. **Collection**
   - Represents a top-level collection of data
   - Fields: id, name, description, created_at, updated_at
   - Has a one-to-many relationship with CollectionPart

2. **CollectionPart**
   - Represents a part of a collection
   - Fields: id, collection_id (FK), name, content, metadata, order, created_at, updated_at
   - Has a many-to-one relationship with Collection

### Database Implementation Features

- **SQLite Backend**: Uses SQLite for simplicity and portability
- **Session Management**: Properly configured session management for transactional operations
- **Migrations Support**: Alembic integration for database schema migrations
- **CRUD Operations**: Comprehensive create, read, update, delete operations for all models

## Integration with Streamlit

The SQLAlchemy models are integrated with the Streamlit application:

- Database initialization during app startup
- Session state management for database connections
- UI components for viewing and managing collections and parts
- Automatic sample data creation for first-time users

## Dependencies

From pyproject.toml:
```
dependencies = [
    "streamlit>=1.22.0",
    "gitpython>=3.1.30",
    "click>=8.1.3",
    "plotly>=6.1.0",
    "sqlalchemy>=2.0.23",
    "alembic>=1.12.0",
]
```

## Future Improvements

1. Add more UI components for creating, editing, and deleting collections and parts
2. Implement search functionality for collections and parts
3. Add support for exporting and importing collections
4. Enhance the metadata handling with validation and specialized UI
5. Add user authentication and permissions

## Installation

The project uses `uv` as its package manager and installation tool. It can be installed with:

```bash
uv tool install
```

The tool is integrated with the local domain setup using:

```bash
zsh -c "dev add fdc"
```
