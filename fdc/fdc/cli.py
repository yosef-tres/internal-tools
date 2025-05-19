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
        subprocess.run(["dev", "add", "fdc"], check=True)
        
        # 2. Start the server
        ctx.invoke(serve)
        
        # 3. Open the browser
        webbrowser.open("https://fdc.dev.local")


@cli.command()
@click.option("--port", "-p", default=8501, help="Port to run the Streamlit server on")
@click.option("--host", "-h", default="0.0.0.0", help="Host to run the Streamlit server on")
def serve(port, host):
    """Start the FDC Streamlit server."""
    click.echo(f"Starting FDC server on {host}:{port}")
    
    # Import here to avoid circular imports
    from fdc.app import run_app
    
    # Run the Streamlit app
    run_app(host=host, port=port)


def main():
    """Entry point for the CLI."""
    try:
        cli()
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
