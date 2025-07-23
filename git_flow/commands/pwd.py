import typer
import subprocess

app = typer.Typer()

@app.callback(invoke_without_command=True)
def pwd():
    """
    Displays the current branch and remote URL.
    """
    try:
        # Get current branch name
        branch_process = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            check=True,
            capture_output=True,
            text=True
        )
        current_branch = branch_process.stdout.strip()
        typer.secho(f"Current Branch: ", nl=False, fg=typer.colors.WHITE)
        typer.secho(current_branch, fg=typer.colors.CYAN, bold=True)

        current_remote = subprocess.run(
            ["git", "remote"],
            check=True,
            capture_output=True,
            text=True
        ).stdout.strip()
        
        remote_process = subprocess.run(
            ["git", "remote", "get-url", current_remote],
            check=True,
            capture_output=True,
            text=True
        )
        remote_url = remote_process.stdout.strip()
        
        typer.secho(f"Remote URL (", nl=False, fg=typer.colors.WHITE)
        typer.secho(current_remote, nl=False, fg=typer.colors.CYAN, bold=True)
        typer.secho("): ", nl=False, fg=typer.colors.WHITE)
        typer.secho(remote_url, fg=typer.colors.CYAN, bold=True)

    except subprocess.CalledProcessError as e:
        error_message = e.stderr.decode().strip().lower()
        if "not a git repository" in error_message:
            typer.secho("Error: Not a git repository.", fg=typer.colors.RED, bold=True)
            raise typer.Exit(code=1)
        
        typer.secho(f"Error: Git command failed.", fg=typer.colors.RED, bold=True)
        typer.secho(f"Details: {e.stderr.decode().strip()}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

