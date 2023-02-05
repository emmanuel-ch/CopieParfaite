import sys
import time

from copieparfaite import view


def run_sync_process():
    view.print_title2('Syncronization process starting')
    view.print_msg('(Info) This software only check identical filepath & filesize.')
    
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
    
    # Auto-copy?
    auto_copy = view.YN_question('Do you want to automatically copy files which aren\'t mirrored?', 'Y')
    solve_all_conflicts_by_AB_suffix = True
    ws.run_synchronizer(auto_copy, solve_all_conflicts_by_AB_suffix)
    view.print_msg('[i] Synchronization finished.')
    
    menu_manager()

