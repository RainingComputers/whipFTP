#!/usr/bin/env python3

try:
    import pip
    import platform
except:
    print('/!\ Failed to install dependencies, is pip installed?')
    input('Press Enter to continue...')
    exit()

print('Installing dependencies for whipftp...')
print('Platform:', platform.system())

pip.main(['install', 'paramiko'])

pip.main(['install', 'psutil'])

if(platform.system() == 'Windows'):
    pip.main(['install', 'pypiwin32'])
else:
    print('No need to install pypiwin32.')

input('Press Enter to continue...')