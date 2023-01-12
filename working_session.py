import glob
import os

# TODO:
    # Review os.path functions
    # os.stat

class WorkingSession():
    def __init__(self):
        self.dirA_path = None
        self.dirB_path = None
    
    
    def gen_list_files(self, dirpath): # Turn this into a generator?
        if dirpath[-1] not in ['/', '\\']:
            dirpath += '/'
        dir_tree = glob.glob(dirpath + '**/*', recursive=True)
        dir_tree = [filepath.replace('\\', '/') for filepath in dir_tree]
        return dir_tree
    
    def validate_dirpath(self, dirpath):
        return os.path.exists(dirpath)
    
    def make_tree(self, dirA_path, dirB_path):
        self.dirA_path = dirA_path
        self.dirB_path = dirB_path
        self.dirA_filelist = self.gen_list_files(self.dirA_path)
        self.dirB_filelist = self.gen_list_files(self.dirB_path)
        
        # Prepare for comparison
        # temp_treeA = list(self.dirA_filelist)
        # temp_treeB = list(self.dirB_filelist)
        
        self.unified_filetree = dict()
        
        # this_entry should contain: filesize, hash to identify?, permissions, other properties?
        
        for entry in self.dirA_filelist:
            relative_path = entry.replace(self.dirA_path, '')
            # print(relative_path)
            exists_in_treeB = (self.dirB_path + relative_path) in self.dirB_filelist
            this_entry = [True, exists_in_treeB]
            self.unified_filetree[relative_path] = this_entry
        
        for entry in self.dirB_filelist:
            relative_path = entry.replace(self.dirB_path, '')
            exists_in_treeA = (self.dirA_path + relative_path) in self.dirA_filelist
            if not exists_in_treeA:
                this_entry = [False, True]
                self.unified_filetree[relative_path] = this_entry
        
        print(self.unified_filetree)

