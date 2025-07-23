import typer

# Each command file will have its own Typer app (or "router").
app = typer.Typer()

@app.callback(invoke_without_command=True)
def hello():
    """
    Says hello.
    """
    print("Hello World!")

