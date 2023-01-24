import sys
import time

import view
import working_session

_MAIN_MENU_ACTIONS_ = {
    1: 'Start syncing tool',
    9: 'Exit',
    91: 'Show files in Test dir'
    }



def menu_manager(question_only=False):
    
    view.print_title1('COPIE PARFAITE - MAIN MENU')
    action = view.propose_choices(_MAIN_MENU_ACTIONS_, 
        choice_question='What do you want to do?')
    action_router(action)

def action_router(action):
    if not action:
        return False
    
    elif action == 1:
        run_sync_process()
        
    elif action == 9:
        view.print_msg('Exiting. See you soon!')
        time.sleep(2)
        sys.exit()
    
    elif action == 91:
        dir_tree = ws.gen_list_files('./test/')
        view.show_dir_tree(dir_tree)
        menu_manager()


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


if __name__=='__main__':
    ws = working_session.WorkingSession()
    menu_manager()


