import typer
import subprocess
from typing import Optional
from git_flow.constants import DEFAULT_COMMIT_MESSAGE

# Each command file will have its own Typer app (or "router").
app = typer.Typer()

@app.callback(invoke_without_command=True)
def ac(message: Optional[str] = typer.Argument(None, help="The commit message.")):
    """
    Stages all changes and commits them with a message.
    If no message is provided, a default one is used.
    """
    # Use the provided message or the default one from the constants file.
    commit_message = message if message is not None else DEFAULT_COMMIT_MESSAGE

    try:
        status_result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
        if not status_result.stdout:
            typer.secho("No changes to commit. Working tree clean.", fg=typer.colors.YELLOW)
            raise typer.Exit()
        
        # Stage all files
        typer.secho("Staging all files...", fg=typer.colors.YELLOW)
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        typer.secho("✔ Files staged successfully.", fg=typer.colors.GREEN)

        # Commit the staged files
        typer.secho(f"Committing with message: '{commit_message}'", fg=typer.colors.YELLOW)
        subprocess.run(["git", "commit", "-m", commit_message], check=True, capture_output=True)
        typer.secho("✔ Commit successful.", fg=typer.colors.GREEN, bold=True)

    except subprocess.CalledProcessError as e:
        # This error is thrown if a git command fails (e.g., nothing to commit)
        error_message = e.stderr.decode().strip()
        typer.secho(f"Error: Git command failed.", fg=typer.colors.RED, bold=True)
        typer.secho(f"Details: {error_message}", fg=typer.colors.RED)
        raise typer.Exit(code=1)


