import typer
from typing_extensions import Optional

from git_flow.commands import hello, ac, pwd, push, branch
from git_flow.utils import check_git_installed
from git_flow.menu import show_menu

app = typer.Typer()

app.add_typer(hello.app, name="hello")
app.add_typer(ac.app, name="ac")
app.add_typer(pwd.app, name="pwd")
app.add_typer(push.app, name="push")
app.add_typer(branch.app, name="branch")


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """
    A faster way to work with Git.
    Run `gf --help` to see available commands.
    """
    check_git_installed()
    
    # This function runs when `gf` is executed.
    if ctx.invoked_subcommand is None:
        show_menu()

# This part allows the script to be run directly.
if __name__ == "__main__":
    app()
