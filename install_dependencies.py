#!/usr/bin/env python3

import pip
import platform

print('Installing dependencies for whipftp...')
print('Platform:', platform.system())

pip.main(['install', 'paramiko'])

pip.main(['install', 'psutil'])

if(platform.system() == 'Windows'):
    pip.main(['install', 'pypiwin32'])
else:
    print('No need to install pypiwin32.')