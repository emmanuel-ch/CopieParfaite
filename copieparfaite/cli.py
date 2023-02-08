#pathfinder/cli.py

import typer
app = typer.Typer(rich_markup_mode="rich")

from copieparfaite import __appname__, __version__, view, working_session


@app.command()
def main(
    auto_copy: bool = typer.Option(True, '--auto_copy', '-a', help='Auto-copy files that aren\'t mirrored', rich_help_panel='Mirroring options'),
    solve_conflicts_by_suffixing = type.Option(True, '--suffix_conflicts', '-s', help='Append suffix upon conflicts (Only activated works)', rich_help_panel='Mirroring options')
) -> None:
    console = view.ConsoleManager()
    console.show_welcome_message()
    
    ws = working_session.WorkingSession()
    
    # Dir1 selection
    dirA_path = view.ask_select_dir('Please select 1st directory (A) to be synchronized:', indent=1)
    while not ws.validate_record_dirpath(dirA_path, 'A'):
        dirA_path = view.ask_select_dir('Please select 1st directory (A) to be synchronized (retry):', indent=1)
    
    # Dir 2 selection
    dirB_path = view.ask_select_dir('Please select 2nd directory (B) to be synchronized:', indent=1)
    while not ws.validate_record_dirpath(dirB_path, 'B'):
        dirB_path = view.ask_select_dir('Please select 2nd directory (B) to be synchronized (retry):', indent=1)
    
    view.print_msg('Directories to be synchronized:')
    view.print_msg(f'(A) {dirA_path}', indent=1)
    view.print_msg(f'(B) {dirB_path}', indent=1)
    
    ws.unified_filetree = ws.make_tree(ws.dirA_path, ws.dirB_path)
    view.print_filetree(ws.unified_filetree, diff_only=True)
    
    ws.run_synchronizer(auto_copy, solve_conflicts_by_suffixing)
    view.print_msg('[i] Synchronization finished.')
    
    return None