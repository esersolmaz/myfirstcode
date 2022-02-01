'''
Funcition to unzip a file.
'''

import os
import zipfile
import shutil

def unzip(file, path):
    '''
    Unzip a file.
    '''
    with zipfile.ZipFile(file, 'r') as zip_ref:
        zip_ref.extractall(path)

'''
Function to zip a file.
'''
def zip(file, path):
    '''
    Zip a file.
    '''
    with zipfile.ZipFile(file, 'w') as zip_ref:
        zip_ref.write(path)
