#whipFTP, Copyrights Vishnu Shankar B,

import os
from os import listdir
from os.path import isfile, join
import shutil
import sys
from ftplib import FTP


class ftp_controller:  
   #/!\ Although the comments and variable names say 'file_name'/'file_anything' it inculdes folders also
   #Some functions in this class has no exception handling, it has to be done outside

    def __init__(self):
       #List to store file search and search keywords
        self.search_file_list = []
        self.detailed_search_file_list = []
        self.keyword_list = []

       #Variable to hold the max no character name in file list (used for padding in GUIs)
        self.max_len = 0

        self.max_len_name = ''

       #Variable to tell weather hidden files are enabled
        self.hidden_files = False  

    def connect_to(self, host, username = ' ', password = ' ', port = 21):  
        self.ftp = FTP()  
        self.ftp.connect(host, port) 
        self.ftp.login(username, password) 

    def toggle_hidden_files(self):
        self.hidden_files = not self.hidden_files 

    def get_detailed_file_list(self):
        files = []
        def dir_callback(line):
            if(self.hidden_files is True or line.split()[8][0] is not '.'):
                files.append(line)
        self.ftp.dir(dir_callback)
        return files

    def get_file_list(self, detailed_file_list):
        self.max_len = 0
        self.max_len_name = ''
        file_list = []
        for x in detailed_file_list:
           #Remove details and append only the file name
            name = ' '.join(x.split()[8:])
            file_list.append(name)
            if(len(name) > self.max_len):
                self.max_len = len(name)
                self.max_len_name = name
        return file_list

    def get_detailed_search_file_list(self):
        return self.detailed_search_file_list

    def get_search_file_list(self):
        self.max_len = 0
        self.max_len_name = ''
        for name in self.search_file_list:
            if(len(name) > self.max_len):
                self.max_len = len(name)
                self.max_len_name = name
        return self.search_file_list

    def chmod(self, filename, permissions):
        self.ftp.sendcmd('SITE CHMOD '+str(permissions)+' '+filename)

    def is_there(self, path):
        try:
            self.ftp.sendcmd('MLST '+path)
            return True;
        except:
            return False;

    def rename_dir(self, rename_from, rename_to):
        self.ftp.sendcmd('RNFR '+ rename_from)
        self.ftp.sendcmd('RNTO '+ rename_to)    

    def move_dir(self, rename_from, rename_to, status_command, replace_command):
        if(self.is_there(rename_to) is True):
            if(replace_command(rename_from, 'File/Folder exists in destination folder') is True):
                self.delete_dir(rename_to, status_command)
            else:
                return
        try:
            self.ftp.sendcmd('RNFR '+ rename_from)
            self.ftp.sendcmd('RNTO '+ rename_to)     
            status_command(rename_from, 'Moved')
        except:
            status_command(rename_from, 'Failed to move')

    def copy_file(self, file_dir, copy_from, file_size, status_command, replace_command):
       #Change to script's directory
        abspath = os.path.abspath(__file__)
        dname = os.path.dirname(abspath)
        os.chdir(dname)
        if not os.path.exists('copy_temps'):
            os.makedirs('copy_temps')
        os.chdir('copy_temps')
       #Save the current path so that we can copy later
        dir_path_to_copy = self.ftp.pwd()
       #Change to the file's path and download it
        self.ftp.cwd(file_dir)
        self.download_file(copy_from, file_size, status_command, replace_command)
       #Change back to the saved path and upload it
        self.ftp.cwd(dir_path_to_copy)
        self.upload_file(copy_from, file_size, status_command, replace_command)
       #Delete the downloaded file
        os.remove(copy_from)
        status_command(copy_from, 'Deleted local file')

    def copy_dir(self, file_dir, copy_from, status_command, replace_command):
       #Change to script's directory
        abspath = os.path.abspath(__file__)
        dname = os.path.dirname(abspath)
        os.chdir(dname)
        if not os.path.exists('copy_temps'):
            os.makedirs('copy_temps')
        os.chdir('copy_temps')
       #Save the current path so that we can copy later
        dir_path_to_copy = self.ftp.pwd()
       #Change to the file's path and download it
        self.ftp.cwd(file_dir)
        self.download_dir(copy_from, status_command, replace_command)
       #Change back to the saved path and upload it
        self.ftp.cwd(dir_path_to_copy)
        self.upload_dir(copy_from, status_command, replace_command)
       #Delete the downloaded folder
        shutil.rmtree(copy_from)
        status_command(copy_from, 'Deleting local directory')

    def delete_file(self, file_name, status_command):
        try:
            self.ftp.sendcmd('DELE '+file_name)
            status_command(file_name, 'Deleted')
        except:
            status_command(file_name, 'Failed to delete')

    def delete_dir(self, dir_name, status_command):
       #Go into the directory
        self.ftp.cwd(dir_name)
       #Get file lists
        detailed_file_list = self.get_detailed_file_list()
        file_list = self.get_file_list(detailed_file_list)
        for file_name, file_details in zip(file_list, detailed_file_list):
           #If directory
            if('d' in file_details[0]):
                self.delete_dir(file_name, status_command)
           #If file
            else:
                self.delete_file(file_name, status_command)
       #Go back to parent directory and delete it
        try:
            self.ftp.cwd('..')
            status_command(dir_name, 'Deleting directory')
            self.ftp.sendcmd('RMD '+dir_name)
        except:
            status_command(dir_name, 'Failed to delete directory')
            return

    def upload_file(self, file_name, file_size, status_command, replace_command):
        def update_progress(data):
            self.bytes_uploaded += int(sys.getsizeof(data))
            status_command(file_name, str(min(round((self.bytes_uploaded/file_size) * 100, 8), 100))+'%')
       #Variable to keep trak of number of bytes uploaded
        self.bytes_uploaded = 0
       #Check if the file is already present in ftp server
        if(self.is_there(file_name)):
            if(replace_command(file_name, 'File exists in destination folder') is False):
                return
       #Try to open file, if fails return
        try:
            file_to_up = open(file_name, 'rb')
        except:
            status_command(file_name, 'Failed to open file')
            return
       #Try to upload file
        try:
            status_command(file_name, 'Uploading')
            self.ftp.storbinary('STOR '+file_name, file_to_up, 8192, update_progress)
            status_command(None, 'newline')
        except:
            status_command(file_name, 'Upload failed')
            return
       #Close file
        file_to_up.close()

    def upload_dir(self, dir_name, status_command, replace_command):
       #Change to directory
        os.chdir(dir_name)
       #Create directory in server and go inside
        try:
            if(not self.is_there(dir_name)):
                self.ftp.mkd(dir_name)
                status_command(dir_name, 'Creating directory')
            else:
                status_command(dir_name, 'Directory exists')
            self.ftp.cwd(dir_name)
        except:
            status_command(dir_name, 'Failed to create directory')
            return
       #Cycle through items
        for filename in os.listdir():
           #If file upload
            if(isfile(filename)):
                self.upload_file(filename, os.path.getsize(filename), status_command, replace_command)
           #If directory, recursive upload it
            else:
                self.upload_dir(filename, status_command, replace_command)
                
       #Got to parent directory
        self.ftp.cwd('..')
        os.chdir('..')

    def download_file(self, ftp_file_name, file_size, status_command, replace_command):
       #Function for updating status and writing to file 
        def write_file(data):
            self.bytes_downloaded += int(sys.getsizeof(data))
            status_command(ftp_file_name, str(min(round((self.bytes_downloaded/file_size) * 100, 8), 100))+'%')
            file_to_down.write(data)
       #Variable to keep track of total bytes downloaded
        self.bytes_downloaded = 0
       #Check if the file is already present in local directory
        if(isfile(ftp_file_name)):
            if(replace_command(ftp_file_name, 'File exists in destination folder') is False):
                return
       #Try to open file, if fails return
        try:
            file_to_down = open(ftp_file_name, 'wb')
        except:
            status_command(ftp_file_name, 'Failed to create file')
            return
       #Try to upload file
        try:
            status_command(ftp_file_name, 'Downloading')
            self.ftp.retrbinary('RETR '+ftp_file_name, write_file)
            status_command(None, 'newline')
        except:
            status_command(ftp_file_name, 'Download failed')
       #Close file
        file_to_down.close()

    def download_dir(self, ftp_dir_name, status_command, replace_command):
       #Create local directory        
        try:
            if(not os.path.isdir(ftp_dir_name)):
                os.makedirs(ftp_dir_name)
                status_command(ftp_dir_name, 'Created local directory')
            else:
                status_command(ftp_dir_name, 'Local directory exists')
            os.chdir(ftp_dir_name)
        except:
            status_command(ftp_dir_name, 'Failed to create local directory')
            return
       #Go into the ftp directory
        self.ftp.cwd(ftp_dir_name)
       #Get file lists
        detailed_file_list = self.get_detailed_file_list()
        file_list = self.get_file_list(detailed_file_list)
        for file_name, file_details in zip(file_list, detailed_file_list):
           #If directory
            if('d' in file_details[0]):
                self.download_dir(file_name, status_command, replace_command)
           #If file
            else:
                self.download_file(file_name, int(file_details.split()[4]), status_command, replace_command)
       #Got to parent directory
        self.ftp.cwd('..')
        os.chdir('..')

    def search(self, dir_name, status_command, search_file_name):
       #Go into the ftp directory
        self.ftp.cwd(dir_name)
       #Get file lists
        detailed_file_list = self.get_detailed_file_list()
        file_list = self.get_file_list(detailed_file_list)
        for file_name, file_details in zip(file_list, detailed_file_list):
           #If file_name matches the keyword, append it to search list
            if search_file_name.lower() in file_name.lower():
                if(self.ftp.pwd() == '/'):
                    dir = ''
                else:
                    dir = self.ftp.pwd()
                self.search_file_list.append(dir+'/'+file_name)
                self.detailed_search_file_list.append(file_details)
                status_command(dir+'/'+file_name, 'Found')           
           #If directory, search it 
            if('d' in file_details[0]):
                status_command(file_name, 'Searching directory')
                self.search(file_name, status_command, search_file_name)
       #Goto to parent directory
        self.ftp.cwd('..')

    def clear_search_list(self):
        del self.search_file_list[:]
        del self.detailed_search_file_list[:]

    def get_dir_size(self, dir_name):
        size = 0;
       #Go into the ftp directory
        self.ftp.cwd(dir_name)
       #Get file lists
        detailed_file_list = self.get_detailed_file_list()
        file_list = self.get_file_list(detailed_file_list)
        for file_name, file_details in zip(file_list, detailed_file_list):
            if('d' in file_details[0]):
        	    size+=self.get_dir_size(file_name)
            else:
                size+=int(file_details.split()[4])
       #Goto to parent directory
        self.ftp.cwd('..')
       #return size
       	return size

    def cwd_parent(self, name):
        if('/' not in name): return name
        parent_name = '/'.join(name.split('/')[:-1])
        if (parent_name == ''): parent_name = '/'
        self.ftp.cwd(parent_name)
        return ''.join(name.split('/')[-1:])

    def mkd(self, name):
        self.ftp.mkd(name)

    def pwd(self):
        return(self.ftp.pwd())
