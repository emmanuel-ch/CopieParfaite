from rich.console import Console
from rich.panel import Panel
from rich.align import Align
# https://rich.readthedocs.io/en/stable/
# jobs; fullscreen; dynamic_progress; layout


class ConsoleManager():
    
    def __init__(self):
        self.console = Console()
    
    def show_welcome_message(self):
        self.console.print(
            Panel(
                Align.center("[bold blue]Copie Parfaite")
                , padding=1, subtitle="Make perfectly mirrored folders")
            )
        self.console.print('(Info) This software only check identical filepath & filesize.')




_SCREENWIDTH_ = 60
_TITLE_FILLER_ = '#'
_TITLE2_FILLER_ = '_'
_MENU_PREFIX_ = '# '
_INDENT_ = '  '


def print_title1(msg):
    print('\n' + f' {msg} '.center(_SCREENWIDTH_, _TITLE_FILLER_))
    
def print_title2(msg):
    print('\n' + f' {msg} '.center(_SCREENWIDTH_, _TITLE2_FILLER_))

def print_msg(*args, indent=0):
    print(indent*_INDENT_, *args, sep='')


def propose_choices(choices_dict, choice_question, validation_fn=None, default_answer=None, is_int=True):
    _ = {print(f'{k}. {v}') for k, v in choices_dict.items()}
    complete_question = choice_question
    if default_answer is not None:
        complete_question += f' (default {default_answer})'
    complete_question += '  '
    
    decision = input(complete_question)
    if (len(decision) == 0) and (default_answer is not None):
        return default_answer
    if is_int:
        decision = int(decision)
    
    while decision not in choices_dict.keys():
        print_msg(f'Choice impossible: {decision}. Try again.')
        decision = input(complete_question)
        if (len(decision) == 0) and (default_answer is not None):
            return default_answer
        if is_int:
            decision = int(decision)
    return decision


def YN_question(choice_question, default_answer=None):
    complete_question = choice_question
    if default_answer is None:
        complete_question += f' (y/n)'
    elif default_answer == 'Y':
        complete_question += f' ([Y]/n)'
    elif default_answer == 'N':
        complete_question += f' (y/[N])'
    complete_question += '  '
    
    decision = input(complete_question)
    
    if (len(decision) == 0) and (default_answer is not None):
        return default_answer=='Y'
    
    while decision.upper() not in ['Y', 'N']:
        print_msg(f'Choice impossible: {decision}. Try again.')
        decision = input(complete_question)
        if (len(decision) == 0) and (default_answer is not None):
            return default_answer=='Y'
    return decision=='Y'
        

def show_menu(question_only=False):
    
    if not question_only:
        
        print(_MENU_PREFIX_ + '1. Start syncing tool')
        print(_MENU_PREFIX_ + '9. Exit')
        print(_MENU_PREFIX_ + '91. Show files in Test dir')
    return input('What to do?  ')

def ask_select_dir(msg, indent=0):
    return input(indent*_INDENT_ + msg + _INDENT_)

def show_dir_tree(dir_tree):
    _ = [print(f) for f in dir_tree]

def get_readable_entrydiff(entry):
    if entry['_ID_']:
        return '(identical)'
    else:
        these_keys = list(entry.keys())
        if ('inA' in these_keys) and ('inB' in these_keys):
            if entry['A_specs'][0] != entry['B_specs'][0]:
                if entry['A_specs'][0] == True:
                    return 'Type difference: (A) Directory | File (B)'
                else:
                    return 'Type difference: (A) File | Directory (B)'
            return f"Size diffence: (A) {entry['A_specs'][1]} | {entry['B_specs'][1]} (B)"
        elif ('inA' in these_keys):
            return 'Only in (A)'
        elif ('inB' in these_keys):
            return 'Only in (B)'

def print_filetree(unified_filetree, diff_only=True):
    # pprint.pprint(unified_filetree, indent=4)
    if diff_only:
        print_title2('Unified tree diffs')
        tree_to_show = {k:get_readable_entrydiff(v) \
                        for k, v in unified_filetree.items() \
                        if not v['_ID_']}
    else:
        print_title2('Unified tree')
        tree_to_show = tree_to_show = {k:get_readable_entrydiff(v) \
                        for k, v in unified_filetree.items()}
    _ = {print(f'{k}:\t{v}') for k,v in tree_to_show.items()}
    # pprint.pprint(tree_to_show, indent=4)


