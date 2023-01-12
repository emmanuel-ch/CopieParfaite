import glob
import os


class WorkingSession():
    def __init__(self):
        self.dir1_path = None
        self.dir2_path = None
    
    
    def gen_dir_tree(self, dirpath='./Test/**/*'):
        dir_tree = glob.glob(dirpath, recursive=True)
        return dir_tree
    
    def validate_dirpath(self, dirpath):
        return os.path.exists(dirpath)


