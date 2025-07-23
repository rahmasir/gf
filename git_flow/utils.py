import shutil
import typer

def check_git_installed():
    """
    Checks if the 'git' command is available in the system's PATH.
    If not, it prints an error message and exits the program.
    This is a cross-platform way to verify the installation.
    """
    if shutil.which("git") is None:
        typer.secho(
            "Error: 'git' command not found. Is Git installed and in your PATH?",
            fg=typer.colors.RED,
            bold=True
        )
        raise typer.Exit(code=1)
