#Function to get all removable drives attached to the computer
def get_mounts():
    mountpoints = []
    
    f = open('/proc/mounts')
    for line in f:
        details = line.split()
        if('/dev/sdb' in details[0] or '/dev/sda' in details[0]):
            if(details[1] != '/boot/efi'):
                details_decoded_string = bytes(details[1], "utf-8").decode("unicode_escape")
                mountpoints.append(details_decoded_string)

    f.close()
    return mountpoints