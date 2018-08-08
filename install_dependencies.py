#!/usr/bin/env python3

#Dependencies to be installed:
#   pramiko
#   psutil
#   pypiwin32


import os
import platform
import sys

try:
    import pip
except ImportError:
    print('Please install pip. Failed to install dependencies.')
    input('Press enter to continue...')
    exit()

if(platform.system() == 'Windows'):
    print('Platform: Windows')
    python_path = sys.executable
    if(python_path.split('\\')[-1:][0] == 'pythonw.exe'):
        print('Do not run this from IDLE. Double click the script to run it directly from python.exe')
        input('Press enter to continue...')
        exit()
    os.system(python_path + ' -m pip install --upgrade pip')
    os.system(python_path + ' -m pip install paramiko')
    os.system(python_path + ' -m pip install psutil')
    os.system(python_path + ' -m pip install pypiwin32')
    input('Press enter to continue...')

if(platform.system() == 'Linux'):
    print('Platform: Linux')
    os.system('python3 -m pip install --upgrade pip')
    os.system('python3 -m pip install paramiko')
    os.system('python3 -m pip install psutil')
    input('Press enter to continue...')
