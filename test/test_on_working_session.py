import pytest
# from pytest import tmpdir

import shutil

from working_session import WorkingSession


@pytest.fixture
def setup_test_dir(tmpdir):
    
    dirA_path = str(tmpdir.join('dirA'))
    dirB_path = str(tmpdir.join('dirB'))
    
    # Copy the file structure
    shutil.copytree('test/test_dirA/', dirA_path)
    shutil.copytree('test/test_dirB/', dirB_path)
    
    ws = WorkingSession()
    ws.validate_record_dirpath(dirA_path, 'A')
    ws.validate_record_dirpath(dirB_path, 'B')
    ws.unified_filetree = ws.make_tree(ws.dirA_path, ws.dirB_path)
    
    yield ws, dirA_path, dirB_path
    
    

def test_run_synchronizer_fullauto(setup_test_dir):
    ws, dirA_path, dirB_path = setup_test_dir
    ws.run_synchronizer(True, True)
    new_tree = ws.make_tree(ws.dirA_path, ws.dirB_path)
    
    # Check 1: File names are mirrored
    missing_files = [k for k,v in new_tree.items() if ('inA' not in v.keys()) or ('inB' not in v.keys())]
    assert len(missing_files) == 0, 'Not all file names are the same.'
    
    # Check 2: File content are mirrored
    inequal_files = [k for k,v in new_tree.items() if not v['_ID_']]
    assert len(inequal_files) == 0, 'Files after sync differ.'
    
    
    