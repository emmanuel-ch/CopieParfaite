import glob


class WorkingSession():
    def __init__(self):
        self.basedir1 = None
        self.basedir2 = None
    
    
    def gen_dir_tree(self, dirpath='./Test/**/*'):
        dir_tree = glob.glob(dirpath, recursive=True)
        return dir_tree