import typer
from typing_extensions import Optional

from git_flow.commands import hello, ac
from git_flow.utils import check_git_installed

app = typer.Typer()

app.add_typer(hello.app, name="hello")
app.add_typer(ac.app, name="ac")


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """
    A faster way to work with Git.
    Run `gf --help` to see available commands.
    """
    check_git_installed()
    
    # This function runs when `gf` is executed.
    if ctx.invoked_subcommand is None:
        # If no command is given, show the welcome message.
        typer.secho(
            "Welcome to Git Flow! Please specify a command, or use --help for a list of commands.",
            fg=typer.colors.BLUE,
            bold=True
        )

# This part allows the script to be run directly.
if __name__ == "__main__":
    app()
