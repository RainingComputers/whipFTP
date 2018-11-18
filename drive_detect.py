import platform
import os
if(platform.system() is 'Windows'):
    import win32api
    import win32con

#Function to get all removable mountpoints attached to the computer
def get_mounts():
    mountpoints = []    

    if(platform.system() == 'Linux'):
        f = open('/proc/mounts')

        dev_types = ['/dev/sda', '/dev/sdc', '/dev/sdb', '/dev/hda', '/dev/hdc', '/dev/hdb', '/dev/nvme']

        for line in f:
            details = line.split()
            if(details[0][:-1] in dev_types):
                if(details[1] != '/boot/efi'):
                    details_decoded_string = bytes(details[1], "utf-8").decode("unicode_escape")
                    mountpoints.append(details_decoded_string)

        f.close()
    elif(platform.system() == 'Darwin'):
        for mountpoint in os.listdir('/Volumes/'):
            mountpoints.append('/Volumes/' + mountpoint)

    elif(platform.system() == 'Windows'):
        mountpoints = win32api.GetLogicalDriveStrings()
        mountpoints = mountpoints.split('\000')[:-1]

    return mountpoints