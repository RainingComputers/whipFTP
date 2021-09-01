import re, os
from hashlib import sha256
# from ftplib import FTP
# ftp = FTP()
# ftp.connect('backupvip.com', 21)
# ftp.login('checker@backupvip.com', 'B@ck!@#$987')
uuidsys = os.popen('wmic path win32_computersystemproduct get uuid')
uuidst = uuidsys.read()
uuid = re.sub("UUID",'',re.sub('\s','',uuidst))
# s256 = sha256(uuid + "-is_for_4rT4_lic#").hexdigest()
# print(sha256(uuid).hexdigest())

def checkHash(hash, uuid_local_sys):
    s256 = sha256()
    s256.update(uuid_local_sys.encode())
    hash_local = s256.hexdigest()
    print(hash)
    print(hash_local)
    if hash_local == hash:
        return True
    return False

print(checkHash('1f2a1b41d1779f514cb4392050193eb0b262ba3e88aeb5c2e8ccaa21c96c0b7a', f"{uuid}-is_for_4rT4_lic#"))