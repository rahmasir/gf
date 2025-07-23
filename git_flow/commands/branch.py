import typer
import subprocess
import questionary
from questionary import Choice

app = typer.Typer()

@app.callback(invoke_without_command=True)
def branch():
    """
    Displays an interactive menu to switch between local git branches.
    """
    try:
        # Get the list of all local branches from git.
        branch_proc = subprocess.run(
            ["git", "branch"],
            check=True, capture_output=True, text=True
        )
        
        branches_raw = [b.strip() for b in branch_proc.stdout.split('\n') if b]
        
        current_branch = ""
        branch_choices = []

        # Parse the raw branch list to find the current branch and create Choice objects.
        for b in branches_raw:
            if b.startswith('* '):
                # This is the current branch.
                branch_name = b[2:]
                current_branch = branch_name
                # Add a visual indicator to the display text.
                display_text = f"{branch_name} (current)"
                branch_choices.append(Choice(title=display_text, value=branch_name))
            else:
                branch_choices.append(Choice(title=b, value=b))

        if not branch_choices:
            typer.secho("No branches found in this repository.", fg=typer.colors.YELLOW)
            raise typer.Exit()

        # Ask the user to select a branch, with the current one pre-selected.
        selected_branch = questionary.select(
            "Select a branch to checkout to:",
            choices=branch_choices,
            use_indicator=True,
            default=current_branch
        ).ask()

        if selected_branch is None:
            typer.secho("No branch selected. Aborting.", fg=typer.colors.MAGENTA)
            raise typer.Exit()

        if selected_branch == current_branch:
            typer.secho(f"Already on branch '{current_branch}'.", fg=typer.colors.YELLOW)
            raise typer.Exit()

        # Execute 'git checkout' for the selected branch.
        typer.secho(f"Switching to branch '{selected_branch}'...", fg=typer.colors.YELLOW)
        subprocess.run(["git", "checkout", selected_branch], check=True, capture_output=True)
        typer.secho(f"✔ Switched to branch '{selected_branch}'.", fg=typer.colors.GREEN, bold=True)

    except subprocess.CalledProcessError as e:
        error_message = e.stderr.decode().strip()
        typer.secho(f"Error: Git command failed.", fg=typer.colors.RED, bold=True)
        typer.secho(f"Details: {error_message}", fg=typer.colors.RED)
        raise typer.Exit(code=1)
