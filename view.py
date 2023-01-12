"""Possible CLI UI:
cursa
https://github.com/Textualize/rich    - /rich-cli    - /textual"""

_SCREENWIDTH_ = 60
_TITLE_FILLER_ = '#'
_TITLE2_FILLER_ = '_'
_MENU_PREFIX_ = '# '
_INDENT_ = '  '


def print_title1(msg):
    print(f' {msg} '.center(_SCREENWIDTH_, _TITLE_FILLER_))
    
def print_title2(msg):
    print(f' {msg} '.center(_SCREENWIDTH_, _TITLE2_FILLER_))

def print_msg(*args, indent=0):
    print(indent*_INDENT_, *args, sep='')

def show_menu(question_only=False):
    if not question_only:
        print_title1('COPIE PARFAITE - MAIN MENU')
        print(_MENU_PREFIX_ + '1. Start syncing tool')
        print(_MENU_PREFIX_ + '9. Exit')
        print(_MENU_PREFIX_ + '91. Select folder')
    return input('What to do?  ')

def ask_select_dir(msg, indent=0):
    return input(indent*_INDENT_ + msg + _INDENT_)

def show_dir_tree(dir_tree):
    _ = [print(f) for f in dir_tree]