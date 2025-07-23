import typer

# Each command file will have its own Typer app (or "router").
app = typer.Typer()

@app.callback(invoke_without_command=True)
def hello():
    """
    just Says hello
    """
    typer.secho('Hello World from gf assistant!', fg=typer.colors.GREEN, bold=True)
