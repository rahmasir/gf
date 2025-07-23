import typer
from typing_extensions import Optional
from git_flow.commands import hello

app = typer.Typer()

app.add_typer(hello.app, name="hello")


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """
    A faster way to work with Git.
    Run `gf --help` to see available commands.
    """
    # This function runs when `gf` is executed.
    # We check if a subcommand (like 'hello') was invoked.
    if ctx.invoked_subcommand is None:
        print("Welcome to Git Flow! Please specify a command, or use --help for a list of commands.")

# This part allows the script to be run directly,
# but it's the 'app' object that pip uses for the 'gf' command.
if __name__ == "__main__":
    app()
