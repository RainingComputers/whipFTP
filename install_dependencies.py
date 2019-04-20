#!/usr/bin/env python3

#Dependencies to be installed:
#   pramiko
#   psutil (v3.4.2 for win XP)
#   pypiwin32 (219 for win XP)


import os
import platform
import sys

#Check if pip is installed
try:
    import pip
except ImportError:
    print('Please install pip. Failed to install dependencies.')
    input('Press enter to continue...')
    exit()

#if Windows
if(platform.system() == 'Windows'):
    print('Platform: Windows ' + platform.release())
    python_path = sys.executable
    if(python_path.split('\\')[-1:][0] == 'pythonw.exe'):
        print('Do not run this from IDLE. Double click the script to run it directly from python.exe')
        input('Press enter to continue...')
        exit()
    #if Windows 7/10
    if(platform.release() != 'XP' and platform.release() != '2003Server'):
        print('Upgrading pip...')
        os.system(python_path + ' -m pip install --upgrade pip')
        print('Installing pramiko...')
        os.system(python_path + ' -m pip install paramiko')
        print('Installing psutil...')
        os.system(python_path + ' -m pip install psutil')
        print('Installing pypiwin32...')
        os.system(python_path + ' -m pip install pypiwin32')
        input('Press enter to continue...')
    else:
    #if Windows XP
        print('Upgrading pip...')
        os.system(python_path + ' -m pip install --upgrade pip')
        print('Installing pramiko...')
        os.system(python_path + ' -m pip install paramiko')
        print('Installing psutil...')
        os.system(python_path + ' -m pip install psutil==3.4.2')
        print('Installing pypiwin32...')
        os.system(python_path + ' -m pip install pypiwin32==219')
        input('Press enter to continue...')       
#if Linux
elif(platform.system() == 'Linux'):
    print('Platform: Linux')
    print('Upgrading pip...')
    os.system('python3 -m pip install --upgrade pip --user')
    print('Installing pramiko...')
    os.system('python3 -m pip install paramiko --user')
    print('Installing psutil...')
    os.system('python3 -m pip install psutil --user')
    input('Press enter to continue...')
#if FreeBSD
elif(platform.system() == 'FreeBSD'):
    if(os.geteuid() != 0):
        print('You need to have root privileges to run this script.')
        input('Press enter to continue...')
    print('Platform: FreeBSD')
    print('Upgrading pip...')
    os.system('python3.6 -m pip install --upgrade pip')
    print('Installing tkinter...')
    os.system('pkg install py36-tkinter-3.6.5_6')
    print('Installing pramiko...')
    os.system('python3.6 -m pip install paramiko')
    print('Installing psutil...')
    os.system('python3.6 -m pip install psutil')
    input('Press enter to continue...')