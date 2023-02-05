#pathfinder/cli.py

import typer
app = typer.Typer(rich_markup_mode="rich")

from copieparfaite import __appname__, __version__, copieparfaite, view, working_session


@app.command()
def main() -> None:
    console = view.ConsoleManager()
    ws = working_session.WorkingSession()
    view.print_title1('COPIE PARFAITE - MAIN MENU')

    copieparfaite.run_sync_process()
    
    return None