import typer
import questionary
from git_flow.commands import ac

def _handle_ac():
    """Handles the 'Stage and commit all changes' action."""
    typer.secho("\nTip: You can run this command directly with 'gf ac'", fg=typer.colors.CYAN)
    commit_message = questionary.text("Enter commit message (leave blank for default):").ask()
    
    # Create a context to invoke the 'ac' command function.
    ctx = typer.Context(ac.app)
    ctx.invoke(ac.ac, message=commit_message or None)

def _handle_coming_soon():
    """Placeholder for features that are not yet implemented."""
    typer.secho("This feature is not yet implemented.", fg=typer.colors.YELLOW)

def _handle_exit():
    """Handles exiting the application."""
    typer.secho("Exiting.", fg=typer.colors.MAGENTA)
    raise typer.Exit()

# A dictionary that maps the menu option text to its handler function.
# This avoids a messy if/elif/else block.
MENU_OPTIONS = {
    "Stage and commit all changes (ac)": _handle_ac,
    "Check repository status (coming soon)": _handle_coming_soon,
    "Push changes to remote (coming soon)": _handle_coming_soon,
    "Exit": _handle_exit,
}

def show_menu():
    """
    Displays the interactive menu and calls the appropriate handler function.
    """
    # The keys of the dictionary are used as the choices.
    # The strings use Rich-style markup for color, which questionary supports.
    selected_choice = questionary.select(
        "Welcome to Git Flow! What would you like to do?",
        choices=list(MENU_OPTIONS.keys()),
        use_indicator=True,
    ).ask()

    if selected_choice is None:
        # Handles the case where the user presses Ctrl+C.
        _handle_exit()

    # Retrieve the correct function from the dictionary and execute it.
    action_to_run = MENU_OPTIONS[selected_choice]
    action_to_run()
