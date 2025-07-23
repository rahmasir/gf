import typer
import subprocess
from typing import Optional

app = typer.Typer()

def get_current_remote():
    return subprocess.run(
        ["git", "remote"],
        check=True, capture_output=True, text=True
    ).stdout.strip()
    
def get_current_branch():
    return subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        check=True, capture_output=True, text=True
    ).stdout.strip()


@app.callback(invoke_without_command=True)
def push(
    branch: Optional[str] = typer.Argument(None, help="The branch to push."),
    remote: Optional[str] = typer.Argument(None, help="The remote repository to push to.")
):
    """
    Pushes changes to a remote repository.
    - If remote and branch are specified, pushes that specific branch.
    - If only a branch is specified, pushes that branch to the current remote.
    - If nothing is specified, performs a default 'git push'.
    """
    command = ["git", "push"]
    feedback = ""
    current_remote = get_current_remote()
    current_branch = get_current_branch()

    try:
        if remote and branch:
            command.extend([remote, branch])
            feedback = f"Pushing branch '{branch}' to remote '{remote}'..."
        elif branch:
            command.extend([current_remote, branch])
            feedback = f"Pushing branch ('{branch}') to current remote '{current_remote}'..."
        else:
            command.extend([current_remote, current_branch])
            feedback = f"Pushing current branch ('{branch}') to current remote '{current_remote}'..."

        typer.secho(feedback, fg=typer.colors.YELLOW)
        
        # We run the command and capture its output to give better feedback.
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            typer.secho(f"Error: Git push failed.", fg=typer.colors.RED, bold=True)
            # Print stdout and stderr from the git command for detailed context.
            if stdout:
                typer.secho(f"Output:\n{stdout}", fg=typer.colors.WHITE)
            if stderr:
                typer.secho(f"Details:\n{stderr}", fg=typer.colors.RED)
            raise typer.Exit(code=1)
        
        typer.secho("✔ Push successful.", fg=typer.colors.GREEN, bold=True)
        if stdout:
             typer.secho(stdout, fg=typer.colors.WHITE)

    except subprocess.CalledProcessError as e:
        # This will catch errors from the 'git rev-parse' command if it fails.
        error_message = e.stderr.decode().strip()
        typer.secho(f"Error: Could not determine current branch.", fg=typer.colors.RED, bold=True)
        typer.secho(f"Details: {error_message}", fg=typer.colors.RED)
        raise typer.Exit(code=1)
