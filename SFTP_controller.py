#whipFTP, Copyrights Vishnu Shankar B,

import os
from os import listdir
from os.path import isfile, join
import shutil
import paramiko

class paramiko_sftp_client(paramiko.SFTPClient):
    def cwd(self, path):
        self.chdir(path)

    def go_to_home(self, username):
        try:
            self.cwd('/home/' + username)
        except:    
            self.cwd('/')



class sftp_controller:  
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

    def connect_to(self, Host, Username = ' ', Password = ' ', Port = 22): 
        self.transport = paramiko.Transport((Host, Port))
        self.transport.connect(username = Username, password = Password)
        self.ftp = paramiko_sftp_client.from_transport(self.transport)
        self.ftp.go_to_home(Username)

    def toggle_hidden_files(self):
        self.hidden_files = not self.hidden_files 

    def get_detailed_file_list(self, ignore_hidden_files_flag = False):
        files = []
        for attr in self.ftp.listdir_attr():
            if(self.hidden_files is True or str(attr).split()[8][0] is not '.') or ignore_hidden_files_flag == True:
                files.append(str(attr))
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
        self.ftp.chmod(filename, permissions)

    def is_there(self, path):
        try:
            self.ftp.stat(path)
            return True
        except:
            return False

    def rename_dir(self, rename_from, rename_to):
        self.ftp.rename(rename_from, rename_to)    

    def move_dir(self, rename_from, rename_to, status_command, replace_command):
        if(self.is_there(rename_to) is True):
            if(replace_command(rename_from, 'File/Folder exists in destination folder') is True):
                self.delete_dir(rename_to, status_command)
            else:
                return
        try:
            self.ftp.rename(rename_from, rename_to) 
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
        dir_path_to_copy = self.ftp.getcwd()
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
        dir_path_to_copy = self.ftp.getcwd()
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
            self.ftp.remove(file_name)
            status_command(file_name, 'Deleted')
        except:
            status_command(file_name, 'Failed to delete')

    def delete_dir(self, dir_name, status_command):
        #Go into the directory
        self.ftp.cwd(dir_name)
        #Get file lists
        try:
            detailed_file_list = self.get_detailed_file_list(True)
        except:
            status_command(dir_name, 'Failed to delete directory')
            return
        file_list = self.get_file_list(detailed_file_list)
        for file_name, file_details in zip(file_list, detailed_file_list):
            #If directory
            if(self.is_dir(file_details)):
                self.delete_dir(file_name, status_command)
            #If file
            else:
                self.delete_file(file_name, status_command)
        #Go back to parent directory and delete it
        try:
            self.ftp.cwd('..')
            status_command(dir_name, 'Deleting directory')
            self.ftp.rmdir(dir_name)
        except:
            status_command(dir_name, 'Failed to delete directory')

    def upload_file(self, file_name, file_size, status_command, replace_command):
        #Function to update status
        def upload_progress(transferred, remaining):
            status_command(file_name, str(min(round((transferred/file_size) * 100, 8), 100))+'%')
        #Check if the file is already present in ftp server
        if(self.is_there(file_name)):
            if(replace_command(file_name, 'File exists in destination folder') is False):
                return
        #Try to upload file
        try:
            status_command(file_name, 'Uploading')
            self.ftp.put(file_name, file_name, callback = upload_progress)
            status_command(None, 'newline')
        except:
            status_command(file_name, 'Upload failed')
            return

    def upload_dir(self, dir_name, status_command, replace_command):
        #Change to directory
        os.chdir(dir_name)
        #Create directory in server and go inside
        try:
            if(not self.is_there(dir_name)):
                self.ftp.mkdir(dir_name)
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
        #Function to update progress
        def download_progress(transferred, remaining):
            status_command(ftp_file_name, str(min(round((transferred/file_size) * 100, 8), 100))+'%')
        #Check if the file is already present in local directory
        if(isfile(ftp_file_name)):
            if(replace_command(ftp_file_name, 'File exists in destination folder') is False):
                return
        #Try to download file
        try:
            status_command(ftp_file_name, 'Downloading')
            self.ftp.get(ftp_file_name, ftp_file_name, callback = download_progress)
            status_command(None, 'newline')
        except:
            status_command(ftp_file_name, 'Download failed')

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
        detailed_file_list = self.get_detailed_file_list(True)
        file_list = self.get_file_list(detailed_file_list)
        for file_name, file_details in zip(file_list, detailed_file_list):
            #If directory
            if(self.is_dir(file_details)):
                self.download_dir(file_name, status_command, replace_command)
            #If file
            else:
                self.download_file(file_name, int(self.get_properties(file_details)[3]), status_command, replace_command)
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
                if(self.ftp.getcwd() == '/'):
                    dir = ''
                else:
                    dir = self.ftp.getcwd()
                self.search_file_list.append(dir+'/'+file_name)
                self.detailed_search_file_list.append(file_details)
                status_command(dir+'/'+file_name, 'Found')           
            #If directory, search it 
            if(self.is_dir(file_details)):
                status_command(file_name, 'Searching directory')
                self.search(file_name, status_command, search_file_name)
        #Goto to parent directory
        if(self.ftp.getcwd() != '/'):        
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
            if(self.is_dir(file_details)):
        	    size+=self.get_dir_size(file_name)
            else:
                size+=int(self.get_properties(file_details)[3])
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
        self.ftp.mkdir(name)

    def pwd(self):
        return(self.ftp.getcwd())

    def get_properties(self, file_details):
        details_list = file_details.split()
        #Get file attributes
        file_attribs = details_list[0]
        #Get date modified
        date_modified = ' '.join(details_list[5:8])
        #Remove the path from the name
        file_name = ' '.join(details_list[8:])
        #Get size if it is not a directory
        if('d' not in file_details[0]):
            file_size = details_list[4]
            return [file_name, file_attribs, date_modified, file_size]
        else:
            return [file_name, file_attribs, date_modified]

    def is_dir(self, file_details):
        return 'd' in file_details[0]

    def disconnect(self):
        if self.ftp:
            self.ftp.close()