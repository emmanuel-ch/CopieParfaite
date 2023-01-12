import sys

import view
import working_session


def menu_manager(question_only=False):
    action = view.show_menu(question_only)
    if not val_menu_action(action):
        view.print_msg(f'Choice impossible: {action}. Try again.')
        menu_manager(question_only=True)
    
    action_router(action)

def val_menu_action(action):
    action = int(action)
    valid_actions = [1, 9, 91]
    if action in valid_actions:
        return action
    return False


def action_router(action):
    action = val_menu_action(action)
    if not action:
        return False
    
    elif action == 1:
        run_sync_process()
        
    elif action == 9:
        view.print_msg('Exiting. See you soon!')
        sys.exit()
    
    elif action == 91:
        dir_tree = ws.gen_list_files('./Test/')
        view.show_dir_tree(dir_tree)
        menu_manager()


def run_sync_process():
    view.print_title2('\nSyncronization processing starting')
    view.print_msg('[1] Directory selection')
    
    # Dir1 selection
    dirA_path = view.ask_select_dir('Please select 1st directory (A) to be synchronized:', indent=1)
    while not ws.validate_dirpath(dirA_path):
        dirA_path = view.ask_select_dir('Please select 1st directory (A) to be synchronized (retry):', indent=1)
    
    # Dir 2 selection
    dirB_path = view.ask_select_dir('Please select 2nd directory (B) to be synchronized:', indent=1)
    while not ws.validate_dirpath(dirB_path):
        dirB_path = view.ask_select_dir('Please select 2nd directory (B) to be synchronized (retry):', indent=1)
    
    view.print_msg('Directories to be synchronized:')
    view.print_msg(f'(A) {dirA_path}', indent=1)
    view.print_msg(f'(B) {dirB_path}', indent=1)
    
    ws.make_tree(dirA_path, dirB_path)
    


if __name__=='__main__':
    ws = working_session.WorkingSession()
    menu_manager()


