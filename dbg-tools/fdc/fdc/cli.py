#!/usr/bin/env python3
"""Command-line interface for the Fast & Dirty Commit tool."""

import subprocess
import sys
import webbrowser

import click


@click.group(invoke_without_command=True)
@click.pass_context

def cli(ctx):
    """Fast & Dirty Commit - A quick way to commit and serve changes."""
    if ctx.invoked_subcommand is None:
        # Run the default command sequence
        # 1. Add the domain to /etc/hosts (using the existing dev tool)
        click.echo("Adding `dbg.dev.local` domain to /etc/hosts...")
        click.echo("This may require sudo permissions.")
        # Execute the dev add command using zsh with proper environment setup
        subprocess.run(["zsh", "-c", "source ~/.zprofile && dev add dbg 8501 --path=/fdc"], check=True)
        
        # 2. Start the server
        ctx.invoke(serve)
        
        # 3. Open the browser
        webbrowser.open("https://dbg.dev.local/fdc")


@cli.command()
def serve():
    """Start the FDC Streamlit server."""
    click.echo("Starting FDC server on 0.0.0.0:8501")
    
    # Import here to avoid circular imports
    import subprocess
    import sys
    from pathlib import Path
    
    # Get the path to the app.py file
    app_path = Path(__file__).parent / "app.py"
    
    # Run the Streamlit app
    streamlit_cmd = [
        sys.executable, "-m", "streamlit", "run",
        str(app_path),
        "--server.address", '0.0.0.0',
        "--server.port", str(8501),
        "--server.headless", "true",
        "--browser.baseUrlPath", "/fdc",
        "--browser.serverAddress", "dbg.dev.local",
        ""
    ]
    
    # Execute the Streamlit command
    subprocess.run(streamlit_cmd)


def main():
    """Entry point for the CLI."""
    try:
        cli()
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

# Migration-related commands
@cli.group()
def migrate():
    """Database migration commands (similar to npm run)."""
    pass


@migrate.command("new")
@click.argument("message")
def create_migration(message):
    """Create a new migration (alembic revision --autogenerate)."""
    click.echo(f"Creating new migration: {message}")
    subprocess.run(
        ["alembic", "revision", "--autogenerate", "-m", message],
        cwd=str(Path(__file__).parent.parent)
    )


@migrate.command("up")
@click.option("--revision", default="head", help="Migration revision to upgrade to (default: head)")
def upgrade(revision):
    """Upgrade database to specified revision (alembic upgrade)."""
    click.echo(f"Upgrading database to revision: {revision}")
    subprocess.run(
        ["alembic", "upgrade", revision],
        cwd=str(Path(__file__).parent.parent)
    )


@migrate.command("down")
@click.option("--revision", default="-1", help="Number of revisions to downgrade (default: -1)")
def downgrade(revision):
    """Downgrade database by specified number of revisions (alembic downgrade)."""
    click.echo(f"Downgrading database by {revision}")
    subprocess.run(
        ["alembic", "downgrade", revision],
        cwd=str(Path(__file__).parent.parent)
    )


@migrate.command("history")
@click.option("--verbose", "-v", is_flag=True, help="Show detailed information")
def history(verbose):
    """Show migration history (alembic history)."""
    click.echo("Migration history:")
    cmd = ["alembic", "history"]
    if verbose:
        cmd.append("--verbose")
    subprocess.run(
        cmd,
        cwd=str(Path(__file__).parent.parent)
    )


@migrate.command("current")
@click.option("--verbose", "-v", is_flag=True, help="Show detailed information")
def current(verbose):
    """Show current migration version (alembic current)."""
    click.echo("Current migration version:")
    cmd = ["alembic", "current"]
    if verbose:
        cmd.append("--verbose")
    subprocess.run(
        cmd,
        cwd=str(Path(__file__).parent.parent)
    )


if __name__ == "__main__":
    main()
