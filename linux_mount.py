#Function to get all removable drives attached to the computer
def get_mounts():
    mountpoints = []
    
    f = open('/proc/mounts')

    dev_types = ['/dev/sda', '/dev/sdc', '/dev/sdb', '/dev/hda', '/dev/hdc', '/dev/hdb', '/dev/nvme']

    for line in f:
        details = line.split()
        if(details[0][:-1] in dev_types):
            if(details[1] != '/boot/efi'):
                details_decoded_string = bytes(details[1], "utf-8").decode("unicode_escape")
                mountpoints.append(details_decoded_string)

    f.close()
    return mountpoints