import re, os
from hashlib import sha256
from ftplib import FTP
from time import sleep

# ================= FTP ====================
with open('copy_UNPS.bat', 'w') as cup:
    cup.write("@echo off\n")
os.startfile('copy_UNPS.bat')
with open('U&PF.txt', 'r') as up1 :
    username_ftp = up1.readline()
    password_ftp = up1.readline()

ftp = FTP()
ftp.connect('backupvip.com', 21)
ftp.login('checker@backupvip.com', 'B@ck!@#$987')
fileuuid = 'Lic.txt'
ftp.retrbinary('RETR Lic.txt', open(fileuuid, 'wb').write)
# ================= local UUID =======================
uuidsys = os.popen('wmic path win32_computersystemproduct get uuid')
uuidst = uuidsys.read()
uuid_local_sys = re.sub("UUID", '', re.sub('\s', '', uuidst))
uuid_salt = f"{uuid_local_sys}-is_for_4rT4_lic#"
varlic = open("Lic.txt", 'r')


def ok():
    print("OK")

def StopBackup():
    print("stop Backup")

def checkHash(hash):
    s256 = sha256()
    s256.update(uuid_salt.encode())
    hash_local = s256.hexdigest()
    if hash_local == hash:
        return True
    return False


for line in varlic:
    match = re.search(f'\A{username_ftp}', line)
    if match :
        re.sub(username_ftp, '', line)
        re.sub("-", '', line)
        if checkHash(line):
            ok()
            break
        else:
            StopBackup()

# ftp.storbinary('STOR Lic.txt', open(fileuuid, 'rb'))
varlic.close()
sleep(1)
os.remove("Lic.txt")
