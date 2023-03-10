import os
import shutil
from pathlib import Path


class WorkingSession():
    def __init__(self):
        self.dirA_path = None
        self.dirB_path = None
        
        self.unified_filetree = None
        
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
        dir_tree = dirpath.glob('**/*')
        return dir_tree
    
    
    def validate_record_dirpath(self, dirpath, which):
        tested_dir = Path(dirpath).resolve()
        if tested_dir.is_dir(): # Also tests for existence
            if which == 'A':
                self.dirA_path = tested_dir
            elif which == 'B':
                self.dirB_path = tested_dir
            else:
                return False
            return True
        else:
            return False
    
    
    def get_file_specs(self, filepath, hash=0):
        """Returns file specifications:
            - isDir
            - Filesize: 0 if it's a directory'
            - Hash: 0=None; 1=on first 1024 bytes; 2=on whole file"""
         
        if filepath.is_dir():
            return_var = True, 0,
        else:
            return_var = False, filepath.stat().st_size,
        if hash == 0:
            return return_var
        else:
            print(f'/!\\ get_file_specs(..., hash={hash}): Program not written yet!')
    
    
    def make_tree(self, dirA_path, dirB_path):
        dirA_filelist = list(self.gen_list_files(dirA_path))
        dirB_filelist = list(self.gen_list_files(dirB_path))
        
        unified_filetree = dict()
        
        for entry in dirA_filelist:
            relative_path = entry.relative_to(dirA_path)
            potential_onB = dirB_path / relative_path
            exists_in_treeB = potential_onB in dirB_filelist
            
            this_entry = {'inA': True, 'A_specs': self.get_file_specs(entry)}
            if exists_in_treeB:
                this_entry['inB'] = True
                this_entry['B_specs'] = self.get_file_specs(potential_onB)
                
                this_entry['_ID_'] = this_entry['A_specs'] == this_entry['B_specs']
            else:
                this_entry['_ID_'] = False
            unified_filetree[relative_path] = this_entry
        
        for entry in dirB_filelist:
            relative_path = entry.relative_to(dirB_path)
            
            if not relative_path in list(unified_filetree.keys()):
                this_entry = {'inB': True, 'B_specs': self.get_file_specs(entry), '_ID_': False}
                unified_filetree[relative_path] = this_entry
        
        unified_filetree = dict(sorted(unified_filetree.items()))
        return unified_filetree
    
    
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
    
    
    def copy_it(self, src, dst, isDir):
        if isDir:
            out_copy = shutil.copytree(src, dst, dirs_exist_ok=True)
        else:
            out_copy = shutil.copy2(src, dst)
        return out_copy
    
    
    def run_synchronizer(self, auto_copy, solve_all_conflicts_by_AB_suffix):
        todo_dict = {k: True for k in self.unified_filetree.keys()}
        
        for entry, entry_details in self.unified_filetree.items():
            status_code, status_msg = self.get_filediff_status(entry, entry_details)
            
            if not todo_dict[entry]:
                continue
            todo_dict[entry] = False
            
            if status_code == 0:
                pass
            
            if status_code in [1, 2]: # File is missing in A or in B => Copy to the other side
                if status_code == 1:
                    src_file, dst_file = self.dirA_path / entry, self.dirB_path / entry
                    str_X_specs = 'A_specs'
                else:
                    src_file, dst_file = self.dirB_path / entry, self.dirA_path / entry
                    str_X_specs = 'B_specs'
                
                if auto_copy: # Do the auto-copy A -> B 
                    
                    if self.copy_it(src_file, dst_file, entry_details[str_X_specs][0]):
                        # No need to copy files that where in this folder anymore
                        todo_dict = {k: False if k.is_relative_to(entry) else True \
                                     for k, v in todo_dict.items()}
                    else:
                        print(r'  /!\ COPY NOT OK', end='\n\n')
                else: # Manual resolution
                    print(entry, '|| MANUAL', status_code, status_msg, '\n', entry_details, end='\n\n')
                    print(r'/!\ Not covered yet!')
            
            elif status_code in [3, 4, 5]:
                if solve_all_conflicts_by_AB_suffix:
                    rel_dir = entry.parent
                    
                    # Rename A and B
                    A_path = self.dirA_path / entry
                    A_new_name = A_path.stem + '(A)' + A_path.suffix
                    A_new_path = A_path.with_name(A_new_name)
                    os.rename(A_path, A_new_path)
                    
                    B_path = self.dirB_path / entry
                    B_new_name = B_path.stem + '(B)' + B_path.suffix
                    B_new_path = B_path.with_name(B_new_name)
                    os.rename(B_path, B_new_path)
                    
                    # Take care of the items (and their children)
                    A_isDir = True if status_code == 3 else False
                    B_isDir = not A_isDir if status_code == 4 else False
                    self.copy_it(A_new_path, self.dirB_path / rel_dir / A_new_name, A_isDir)
                    self.copy_it(B_new_path, self.dirA_path / rel_dir / B_new_name, B_isDir)
                    
                    # No need to work on the children anymore
                    todo_dict = {k: False if k.is_relative_to(entry) else True \
                                 for k, v in todo_dict.items()}
                else:
                    print(entry, '|| MANUAL', status_code, status_msg, '\n', entry_details, end='\n\n')
                    print(r'/!\ Not covered yet!')
                    # + Handling of children

