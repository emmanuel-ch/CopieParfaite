import glob
import os
import shutil


class WorkingSession():
    def __init__(self):
        self.dirA_path = None
        self.dirB_path = None
        
        self._FILEDIFF_STATUS_ = {
            0: 'No difference',
            1: 'Exists in A but not in B', # For file or folder
            2: 'Exists in B but not in A', # For file or folder
            3: 'Different type, (A directory and B file)',
            4: 'Different type, (A file and B directory)',
            5: 'Different filesize', # For file only, n/a to directories
            9: 'Unknown', # Needed?
            }
    
    
    def gen_list_files(self, dirpath): # Turn this into a generator?
        if dirpath[-1] not in ['/', '\\']:
            dirpath += '/'
        dir_tree = glob.glob(dirpath + '**/*', recursive=True)
        dir_tree = [filepath.replace('\\', '/') for filepath in dir_tree]
        return dir_tree
    
    def validate_dirpath(self, dirpath):
        return os.path.exists(dirpath)
    
    
    def get_file_specs(self, filepath, hash=0):
        """Returns file specifications:
            - isDir
            - Filesize
            - Hash: 0=None; 1=on first 1024 bytes; 2=on whole file"""
        return_var = os.path.isdir(filepath), os.path.getsize(filepath), 
        if hash == 0:
            return return_var
        else:
            print(f'/!\ get_file_specs(..., hash={hash}): Program not written yet!')
    
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
            exists_in_treeB = (self.dirB_path + relative_path) in self.dirB_filelist
            this_entry = {'inA': True, 'A_specs': self.get_file_specs(entry)}
            if exists_in_treeB:
                this_entry['inB'] = True
                this_entry['B_specs'] = self.get_file_specs(self.dirB_path + relative_path)
                this_entry['_ID_'] = this_entry['A_specs'] == this_entry['B_specs']
            else:
                this_entry['_ID_'] = False
            self.unified_filetree[relative_path] = this_entry
        
        for entry in self.dirB_filelist:
            relative_path = entry.replace(self.dirB_path, '')
            already_reviewed = relative_path in list(self.unified_filetree.keys())
            if not already_reviewed:
                this_entry = {'inB': True, 'B_specs': self.get_file_specs(entry), '_ID_': False}
                self.unified_filetree[relative_path] = this_entry
        
        self.unified_filetree = dict(sorted(self.unified_filetree.items()))
        return self.unified_filetree
    
    
    def get_filediff_status(self, entry, entry_details):
        """Provides reason why there is a conflict.
        Return status code and message."""
        if entry_details['_ID_']:
            return 0, '-'
        else:
            k_entry_details = entry_details.keys()
            if ('inA' in k_entry_details) and ('inB' in k_entry_details):
                if entry_details['A_specs'][0] != entry_details['B_specs'][0]:
                    if entry_details['A_specs'][0] == True:
                        return 3, 'Type difference: (A) Directory | File (B)'
                    else:
                        return 4, 'Type difference: (A) File | Directory (B)'
                return 5, f"Size diffence: (A) {entry_details['A_specs'][1]} | {entry_details['B_specs'][1]} (B)"
            elif ('inA' in k_entry_details):
                return 1, 'Only in (A)'
            elif ('inB' in k_entry_details):
                return 2, 'Only in (B)'
    
    
    def copy_it(self, isDir, src, dst):
        if isDir:
            out_copy = shutil.copytree(src, dst)
        else:
            out_copy = shutil.copy2(src, dst)
        return out_copy == dst
    
    
    def run_synchronizer(self, auto_copy):
        
        todo_dict = {k: True for k in self.unified_filetree.keys()}
        for entry, entry_details in self.unified_filetree.items():
            status_code, status_msg = self.get_filediff_status(entry, entry_details)
            
            print(f'\n__ ENTRY: {entry}', status_msg)
            if not todo_dict[entry]:
                print('SKIPPED')
                continue
            todo_dict[entry] = False
            
            # print(f'todo_dict ({len(todo_dict)}):', todo_dict.items())
            
            if status_code == 0:
                pass
            if status_code == 1: 
                if auto_copy: # Do the auto-copy A -> B
                    print('  COPY:', self.dirA_path + entry, ' -> ', self.dirB_path + entry, end='\n')
                    if self.copy_it(entry_details['A_specs'][0], self.dirA_path + entry, self.dirB_path + entry):
                        # No need to copy files that where in this folder anymore
                        todo_dict = {k: False if k.startswith(entry) else True \
                                     for k, v in todo_dict.items()}
                        print('  COPY OK', end='\n\n')
                else:
                    # Manual resolution
                    print(entry, '|| MANUAL', status_code, status_msg, '\n', entry_details, end='\n\n')
            elif status_code == 2:
                if auto_copy: # Do the auto-copy B -> A
                    print('  COPY:', self.dirB_path + entry, ' -> ', self.dirA_path + entry, end='\n')
                    if self.copy_it(entry_details['B_specs'][0], self.dirB_path + entry, self.dirA_path + entry):
                        # No need to copy files that where in this folder anymore
                        todo_dict = {k: False if k.startswith(entry) else True \
                                     for k, v in todo_dict.items()}
                        print('  COPY OK', end='\n\n')
                else:
                    # Manual resolution
                    print(entry, '|| MANUAL', status_code, status_msg, '\n', entry_details, end='\n\n')
            elif status_code == 3:
                # Manual resolution
                print(entry, '|| MANUAL', status_code, status_msg, '\n', entry_details, end='\n\n')
            elif status_code == 4:
                # Manual resolution
                print(entry, '|| MANUAL', status_code, status_msg, '\n', entry_details, end='\n\n')
            elif status_code == 5:
                # Manual resolution
                print(entry, '|| MANUAL', status_code, status_msg, '\n', entry_details, end='\n\n')

