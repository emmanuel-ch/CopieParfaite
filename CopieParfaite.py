import sys

import view
import copy_session


def menu_manager(question_only=False):
    action = view.show_menu(question_only)
    if not val_menu_action(action):
        view.print_msg(f'Choice impossible: {action}. Try again.')
        menu_manager(question_only=True)
    
    action_router(action)

def val_menu_action(action):
    action = int(action)
    valid_actions = [1, 9]
    if action in valid_actions:
        return action
    return False


def action_router(action):
    action = val_menu_action(action)
    if not action:
        return False
    
    if action == 1:
        dir_tree = copier.gen_dir_tree()
        view.show_dir_tree(dir_tree)
        menu_manager()
        
    elif action == 9:
        view.print_msg('Exiting. See you soon!')
        sys.exit()
    

if __name__=='__main__':
    copier = copy_session.CopySession()
    menu_manager()


