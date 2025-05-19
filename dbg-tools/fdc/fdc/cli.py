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
        "--browser.serverAddress", "dbg.dev.local"
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


if __name__ == "__main__":
    main()
