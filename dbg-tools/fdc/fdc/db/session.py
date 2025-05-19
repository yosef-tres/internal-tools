"""Database session and engine configuration."""

import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
import streamlit as st

# Database file path - stored in user's home directory to persist across sessions
DB_PATH = os.path.expanduser("~/.internal-tools/fdc-db.sqlite")
DB_DIR = os.path.dirname(DB_PATH)

# Create the directory if it doesn't exist
if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR)

# Create SQLite engine with connection string
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}  # Only needed for SQLite
)

Base = declarative_base()

# Create sessionmaker

Session = sessionmaker(engine)
