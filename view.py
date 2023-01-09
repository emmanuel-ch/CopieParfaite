"""Possible CLI UI:
cursa
https://github.com/Textualize/rich
- /rich-cli
- /textual"""

_SCREENWIDTH_ = 60
_TITLE_FILLER_ = '#'
_MENU_PREFIX_ = '# '

def print_msg(*args):
    print(*args)

def show_menu(question_only=False):
    if not question_only:
        print()
        print(' MAIN MENU '.center(_SCREENWIDTH_, _TITLE_FILLER_))
        print(_MENU_PREFIX_ + '1. Select folder')
        print(_MENU_PREFIX_ + '9. Exit')
    return input('What to do?  ')

def show_dir_tree(dir_tree):
    _ = [print(f) for f in dir_tree]