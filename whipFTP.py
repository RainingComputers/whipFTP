#!/usr/bin/env python3
#
#    whipFTP, Copyrights Vishnu Shankar B
#
#    List of Tk extensions used:
#        Arc theme (modified to red color and more styles were added) : https://wiki.tcl.tk/48689
#        TkDND : https://sourceforge.net/projects/tkdnd/
#

import os
from os.path import isfile, join
import threading
import queue
from tkinter import *
from tkinter import font
from tkinter import ttk
from tkinter import PhotoImage
from FTP_controller import *
from SFTP_controller import *
from TkDND_wrapper import *
import whipFTP_ToolbarButton as ToolbarButton
import whipFTP_FileDialogs as Filedialogs
import platform
if(platform.system() is 'Windows'):
    import ctypes


class app:
    def __init__(self, master):
        #/!\ Although the comments and variable names say 'file_list', or 'items' it inculdes folders also

        #Cell width of each cell
        self.cell_width = 190

        #List to store all item names (including folders) that are currently being displayed and their details
        self.file_list = []
        self.detailed_file_list = []
        #An index that points to current file that the mouse is pointing
        self.current_file_index = 0

        #Variables for drawing and storing cursor position
        self.mouse_x = 0
        self.mouse_y = 0
        self.max_width = 0

        #Variable to store which cell cursor is currently pointing
        self.x_cell_pos = 0
        self.y_cell_pos = 0

        #A dictionary to store indices and highlight rectangle references of selected files
        self.selected_file_indices = {}

        #A list to hold files that have been droped into the window
        self.dnd_file_list = []

        #Things in the clipboard
        self.cut = False
        self.copy = False
        self.clipboard_file_list = []
        self.clipboard_path_list = []
        self.detailed_clipboard_file_list = []

        #Variable to store start cell position of drag select
        self.start_x = 0
        self.start_y = 0

        #Variable to tell weather to change status, if false the current message will stay on status bar and status bar will ignore other status messages
        self.change_status = True

        #Variable to tell replace all has been selected
        self.replace_all = False

        #Variable to tell skip all has been selected
        self.skip_all = False

        #Variable to tell weather a search has been performes
        self.search_performed = False

        #Variable to tell weather hidden file are enabled
        self.hidden_files = False

        #Variable to tell a thread weather to replace a file
        self.replace_flag = False

        #For thread syncrhoniztion
        self.thread_lock = threading.Lock()

        #Save reference to the window
        self.master = master

        #Save reference to ftpcontroller
        self.ftpController = ftp_controller()
 
        #Set window title and size
        master.wm_title('whipFTP')
        master.minsize(width = 860, height = 560)

        #Variable for holding the font
        self.default_font = font.nametofont("TkDefaultFont")

        #Variable to tell weather to displat updatin file list dialog
        self.float_dialog_destroy = False

        #Set theme and style
        s = ttk.Style()
        s.theme_use('Arc')

        s.configure('Red.TLabel', foreground = 'Red')

        #Create frame for toolbar buttons
        self.toolbar = ttk.Frame(master)
        self.toolbar.pack(fill = X)

        #Create frame for text fields
        self.entry_bar = ttk.Frame(master)
        self.entry_bar.pack(fill = X)     

        #Create frame for canvas and scrollbar
        self.pad_frame = ttk.Frame(master)
        self.pad_frame.pack(fill = BOTH, expand = True)       
        self.canvas_frame = ttk.Frame(self.pad_frame, relief = 'groove', border = 1)
        self.canvas_frame.pack(fill = BOTH, expand = True, padx = 5, pady = 3)

        #Code for handling file/folder drag and drop, uses TkDND_wrapper.py
        #See link: https://mail.python.org/pipermail/tkinter-discuss/2005-July/000476.html
        self.dnd = TkDND(master)
        self.dnd.bindtarget(self.canvas_frame, 'text/uri-list', '<Drop>', self.handle_dnd, 
                            ('%A', '%a', '%T', '%W', '%X', '%Y', '%x', '%y','%D'))
        self.dnd.bindtarget(self.canvas_frame, 'text/uri-list', '<DragEnter>', self.show_dnd_icon, 
                            ('%A', '%a', '%T', '%W', '%X', '%Y', '%x', '%y','%D'))
        self.dnd.bindtarget(self.canvas_frame, 'text/uri-list', '<DragLeave>', lambda action, actions, type, win,
                            X, Y, x, y, data:self.draw_icons(), ('%A', '%a', '%T', '%W', '%X', '%Y', '%x', '%y','%D'))

        #Variables to kepp track of wain frame and animation
        self.wait_anim = False
        self.wait_frame_index = 1
        self.continue_wait = False

        #Load all icons
        self.connect_icon = PhotoImage(file='Icons/connect_big.png')
        self.upload_icon = PhotoImage(file='Icons/upload_big.png')
        self.download_icon = PhotoImage(file='Icons/download_big.png')
        self.newfolder_icon = PhotoImage(file='Icons/newfolder_big.png')
        self.up_icon = PhotoImage(file='Icons/up_big.png')
        self.info_icon = PhotoImage(file='Icons/info_big.png')
        self.delete_icon = PhotoImage(file='Icons/delete_big.png')
        self.properties_icon = PhotoImage(file='Icons/properties_big.png')
        self.cut_icon = PhotoImage(file='Icons/cut_big.png')
        self.copy_icon = PhotoImage(file='Icons/copy_big.png')
        self.paste_icon = PhotoImage(file='Icons/paste_big.png')
        self.permissions_icon = PhotoImage(file='Icons/permissions_big.png')
        self.folder_icon = PhotoImage(file='Icons/folder_big.png')
        self.textfile_icon = PhotoImage(file='Icons/textfile_big.png')
        self.console_icon = PhotoImage(file='Icons/console_big.png')
        self.search_icon = PhotoImage(file='Icons/search_big.png')
        self.rename_icon = PhotoImage(file='Icons/rename_big.png')
        self.whipFTP_icon = PhotoImage(file='Icons/whipFTP_large.png')
        self.goto_icon = PhotoImage(file='Icons/gotopath_big.png')

        #Load glow version of icons
        self.connect_glow_icon = PhotoImage(file='Icons_glow/connect_big_glow.png')
        self.upload_glow_icon = PhotoImage(file='Icons_glow/upload_big_glow.png')
        self.download_glow_icon = PhotoImage(file='Icons_glow/download_big_glow.png')
        self.newfolder_glow_icon = PhotoImage(file='Icons_glow/newfolder_big_glow.png')
        self.up_glow_icon = PhotoImage(file='Icons_glow/up_big_glow.png')
        self.info_glow_icon = PhotoImage(file='Icons_glow/info_big_glow.png')
        self.delete_glow_icon = PhotoImage(file='Icons_glow/delete_big_glow.png')
        self.properties_glow_icon = PhotoImage(file='Icons_glow/properties_big_glow.png')
        self.cut_glow_icon = PhotoImage(file='Icons_glow/cut_big_glow.png')
        self.copy_glow_icon = PhotoImage(file='Icons_glow/copy_big_glow.png')
        self.paste_glow_icon = PhotoImage(file='Icons_glow/paste_big_glow.png')
        self.console_glow_icon = PhotoImage(file='Icons_glow/console_big_glow.png')
        self.search_glow_icon = PhotoImage(file='Icons_glow/search_big_glow.png')
        self.whipFTP_glow_icon = PhotoImage(file='Icons_glow/whipFTP_large_glow.png')
        self.dnd_glow_icon = PhotoImage(file='Icons_glow/upload_large_glow.png')
        self.goto_glow_icon = PhotoImage(file='Icons_glow/gotopath_big_glow.png')

        #Load icons from the wait animations
        self.wait_frames = []
        self.wait_frames.append(PhotoImage(file='Icons_glow/wait_anim_frame_one.png'))
        self.wait_frames.append(PhotoImage(file='Icons_glow/wait_anim_frame_two.png'))
        self.wait_frames.append(PhotoImage(file='Icons_glow/wait_anim_frame_three.png'))
        self.wait_frames.append(PhotoImage(file='Icons_glow/wait_anim_frame_four.png'))
        self.problem_icon = PhotoImage(file='Icons_glow/problem.png')

        #Set window icon
        self.master.iconphoto(True, self.whipFTP_icon)

        #Create the connect button
        self.connect_button = ToolbarButton.Button(self.toolbar, image = self.connect_icon, image_hover = self.connect_glow_icon, command = self.connect_to_ftp)
        self.connect_button.pack(side = 'left', padx = 5)
        #Create the upload button
        self.upload_button = ToolbarButton.Button(self.toolbar, image = self.upload_icon, image_hover = self.upload_glow_icon, command = self.upload_window)
        self.upload_button.pack(side = 'left', padx = 5)
        #Create the download button
        self.download_button = ToolbarButton.Button(self.toolbar, image = self.download_icon, image_hover = self.download_glow_icon, command = self.download_window)
        self.download_button.pack(side = 'left', padx = 5)
        #Create the newfolder button
        self.newfolder_button = ToolbarButton.Button(self.toolbar, image = self.newfolder_icon, image_hover = self.newfolder_glow_icon, command = self.create_dir_window)
        self.newfolder_button.pack(side = 'left', padx = 5)
        #Create the up-directory button
        self.up_button = ToolbarButton.Button(self.toolbar, image = self.up_icon, image_hover = self.up_glow_icon, command = self.dir_up)
        self.up_button.pack(side = 'right', padx = 5)
        #Create the search button
        self.search_button = ToolbarButton.Button(self.toolbar, image = self.search_icon, image_hover = self.search_glow_icon, command = self.search_window_ask)
        self.search_button.pack(side = 'right', padx = 5)
        #Create the goto button
        self.goto_button = ToolbarButton.Button(self.toolbar, image = self.goto_icon, image_hover = self.goto_glow_icon, command = self.goto_window_ask)
        self.goto_button.pack(side = 'right', padx = 5)
        #Create the info button
        self.info_button = ToolbarButton.Button(self.toolbar, image = self.info_icon, image_hover = self.info_glow_icon, command = self.info)
        self.info_button.pack(side = 'right', padx = 5)
        #Create the delete button
        self.delete_button = ToolbarButton.Button(self.toolbar, image = self.delete_icon, image_hover = self.delete_glow_icon, command = self.delete_window)
        self.delete_button.pack(side = 'left', padx = 5)
        #Create the properties button
        self.properties_button = ToolbarButton.Button(self.toolbar, image = self.properties_icon, image_hover = self.properties_glow_icon, command = self.file_properties_window)
        self.properties_button.pack(side = 'left', padx = 5)
        #Create the cut button
        self.cut_button = ToolbarButton.Button(self.toolbar, image = self.cut_icon, image_hover = self.cut_glow_icon, command = self.clipboard_cut)
        self.cut_button.pack(side = 'left', padx = 5)
        #Create the copy button
        self.copy_button = ToolbarButton.Button(self.toolbar, image = self.copy_icon, image_hover = self.copy_glow_icon, command = self.clipboard_copy)
        self.copy_button.pack(side = 'left', padx = 5)
        #Create the paste button
        self.paste_button = ToolbarButton.Button(self.toolbar, image = self.paste_icon, image_hover = self.paste_glow_icon, command = self.clipboard_paste_thread_create)
        self.paste_button.pack(side = 'left', padx = 5)
        #Create label field for hostname
        self.label_hostname = ttk.Label(self.entry_bar, text = 'Host:')
        self.label_hostname.pack(side = 'left', padx = 2)
        #Create text field for hostname
        self.hostname_entry = ttk.Entry(self.entry_bar)
        self.hostname_entry.pack(side = 'left', expand = True, fill = X)
        #Create combobox
        self.connection_type = StringVar()
        self.type_combobox = ttk.Combobox(self.entry_bar, textvariable=self.connection_type, width = 5, state = 'readonly')
        self.connection_type.set('SFTP')
        self.type_combobox['values'] = ('FTP', 'SFTP')
        self.type_combobox.pack(side = 'left')
        #Create label for username
        self.label_usrname = ttk.Label(self.entry_bar, text = 'Username:')
        self.label_usrname.pack(side = 'left', padx = 2)
        #Create text field for username
        self.usrname_entry = ttk.Entry(self.entry_bar)
        self.usrname_entry.pack(side = 'left', expand = True, fill = X)
        #Create label for password
        self.label_pass = ttk.Label(self.entry_bar, text = 'Password:')
        self.label_pass.pack(side = 'left', padx = 2)
        #Create textfield for password
        self.pass_entry = ttk.Entry(self.entry_bar, show = '*')
        self.pass_entry.pack(side = 'left', expand = True, fill = X)
        #Create label for port
        self.label_port = ttk.Label(self.entry_bar, text = 'Port:')
        self.label_port.pack(side = 'left', padx = 2)
        #Create textfield for port
        self.port_entry = ttk.Entry(self.entry_bar, width = 4)
        self.port_entry.pack(side = 'left', padx = (0, 2))
        self.port_entry.insert(END, '22')
        #Create scrollbar
        self.vbar = ttk.Scrollbar(self.canvas_frame, orient=VERTICAL, style = 'Vertical.TScrollbar')
        self.vbar.pack(anchor = E,side=RIGHT,fill=Y)
        #Create drawing space for all file and folder icons
        self.canvas = Canvas(self.canvas_frame, relief = 'flat', bg = 'white', highlightthickness=0)
        self.canvas.pack(fill = BOTH, expand = True)
        self.vbar.config(command = self.canvas.yview)
        self.canvas['yscrollcommand'] = self.vbar.set
        #Create status text/bar and status sting viraiable
        self.current_status = StringVar()
        self.status_label = ttk.Label(master, textvariable = self.current_status, anchor = 'center')
        self.status_label.pack(fill = X)

        #Bind events
        self.bind_events()



    def bind_events(self):
        #Bind keyboard shortcuts
        self.master.bind('<Control-h>', self.toggle_hidden_files)
        self.master.bind('<Control-H>', self.toggle_hidden_files)
        self.master.bind('<Control-c>', self.clipboard_copy)
        self.master.bind('<Control-C>', self.clipboard_copy)
        self.master.bind('<Control-x>', self.clipboard_cut)
        self.master.bind('<Control-X>', self.clipboard_cut)
        self.master.bind('<Control-v>', self.clipboard_paste_thread_create)
        self.master.bind('<Control-V>', self.clipboard_paste_thread_create) 
        self.master.bind('<Delete>', self.delete_window)

        #Bind events for canvas, this part of code tells what some of the functions do
        self.canvas.bind('<Button-4>', self.on_mouse_wheel)
        self.canvas.bind('<Button-5>', self.on_mouse_wheel)     
        self.canvas.bind('<MouseWheel>', self.on_mouse_wheel)
        self.canvas.bind('<Configure>', self.draw_icons)
        self.canvas.bind('<Motion>', self.update_status_and_mouse)
        self.canvas.bind('<Button-1>', self.mouse_select)
        self.canvas.bind('<Double-Button-1>' , self.change_dir)     
        self.canvas.bind('<Control-Button-1>', self.ctrl_select)
        self.canvas.bind('<B1-Motion>', self.drag_select)

        #Bind events for statusbar and scroll bar
        self.vbar.bind('<Motion>', lambda event, arg = 'Scrollbar.': self.update_status(event, arg)) 
        self.status_label.bind('<Motion>', lambda event, arg = 'Statusbar.': self.update_status(event, arg)) 

        #Bind events for all buttons
        self.connect_button.bind('<Motion>', lambda event, arg = 'Start connection.': self.update_status(event, arg)) 
        self.upload_button.bind('<Motion>', lambda event, arg = 'Upload file(s) or folder(s).': self.update_status(event, arg)) 
        self.download_button.bind('<Motion>', lambda event, arg = 'Save/Download file(s) or folder(s).': self.update_status(event, arg)) 
        self.newfolder_button.bind('<Motion>', lambda event, arg = 'Create a new directory.': self.update_status(event, arg)) 
        self.delete_button.bind('<Motion>', lambda event, arg = 'Delete.': self.update_status(event, arg)) 
        self.properties_button.bind('<Motion>', lambda event, arg = 'Edit/View properties.': self.update_status(event, arg)) 
        self.cut_button.bind('<Motion>', lambda event, arg = 'Cut.': self.update_status(event, arg)) 
        self.copy_button.bind('<Motion>', lambda event, arg = 'Copy.': self.update_status(event, arg)) 
        self.paste_button.bind('<Motion>', lambda event, arg = 'Paste.': self.update_status(event, arg)) 
        self.search_button.bind('<Motion>', lambda event, arg = 'Find.': self.update_status(event, arg))
        self.goto_button.bind('<Motion>', lambda event, arg = 'Goto.': self.update_status(event, arg)) 
        self.up_button.bind('<Motion>', lambda event, arg = 'Go to parent directory.': self.update_status(event, arg)) 
        self.info_button.bind('<Motion>', lambda event, arg = 'About/Info.': self.update_status(event, arg)) 

        #Bind events for all labels
        self.toolbar.bind('<Motion>', lambda event, arg = ' ': self.update_status(event, arg)) 
        self.label_usrname.bind('<Motion>', lambda event, arg = ' ': self.update_status(event, arg)) 
        self.label_hostname.bind('<Motion>', lambda event, arg = ' ': self.update_status(event, arg)) 
        self.label_port.bind('<Motion>', lambda event, arg = ' ': self.update_status(event, arg)) 

        #Bind events for all entries/text fields
        self.hostname_entry.bind('<Motion>', lambda event, arg = 'Enter host address.': self.update_status(event, arg)) 
        self.type_combobox.bind('<Motion>', lambda event, arg = 'Select connection type': self.update_status(event, arg)) 
        self.type_combobox.bind('<Motion>', lambda event, arg = 'Select connection type': self.update_status(event, arg)) 
        self.type_combobox.bind('<<ComboboxSelected>>', self.handle_combobox)
        self.usrname_entry.bind('<Motion>', lambda event, arg = 'Enter your username.': self.update_status(event, arg))
        self.pass_entry.bind('<Motion>', lambda event, arg = 'Enter your password.': self.update_status(event, arg))
        self.port_entry.bind('<Motion>', lambda event, arg = 'Enter port.': self.update_status(event, arg))

        #Press enter key to connect
        self.hostname_entry.bind('<Return>', self.connect_to_ftp) 
        self.usrname_entry.bind('<Return>', self.connect_to_ftp)
        self.pass_entry.bind('<Return>', self.connect_to_ftp)
        self.port_entry.bind('<Return>', self.connect_to_ftp)  


    def handle_combobox(self, event):
        #Clear port entry
        self.port_entry.delete(0, 'end') 
        #Set default port   
        if(self.type_combobox.get() == 'FTP'): 
            self.port_entry.insert(END, '21')
        else: 
            self.port_entry.insert(END, '22')



    def connect_to_ftp(self, event = None):        
        #Show wait animation
        self.unlock_status_bar()
        self.start_wait()
        #Show 'Connecting' in status bar
        self.update_status(message = 'Connecting...')
        self.lock_status_bar()
        #Check connection type create appropriate controller
        try:
            self.ftpController.disconnect()
            del self.ftpController
        except:
            pass
        if(self.type_combobox.get() == 'FTP'): self.ftpController = ftp_controller()
        else: self.ftpController = sftp_controller()
        self.thread =  threading.Thread(target = self.connect_thread, args = (self.ftpController,
            self.hostname_entry.get(), self.usrname_entry.get(), self.pass_entry.get(), int(self.port_entry.get())))
        self.thread.daemon = True
        self.thread.start()
        self.process_thread_requests()
        

    def connect_thread(self, ftpController, host, usrname, passwd, port):
        try:
            ftpController.connect_to(host, usrname, passwd, port)   
            thread_request_queue.put(lambda:self.unlock_status_bar())
            thread_request_queue.put(lambda:self.cont_wait())         
            thread_request_queue.put(lambda:self.update_file_list())
            thread_request_queue.put(lambda:self.update_status(message = 'Connected.'))
        except:
            thread_request_queue.put(lambda:self.unlock_status_bar())
            thread_request_queue.put(lambda:self.update_status_red('Unable to connect, please check what you have entered.'))
            #Make sure unable to connect message stays on status bar
            thread_request_queue.put(lambda:self.lock_status_bar())
        #Need to focus on the main window and the entry due to a bug in ttk/tkinter (entries don't focis properly after creating and destroying windowless messagebox dialog)  
        thread_request_queue.put(lambda:self.hostname_entry.focus()) 
        thread_request_queue.put(lambda:self.master.focus())    


    def update_file_list(self):      
        #Disable toolbar
        self.start_wait()
        #Set search to false
        self.search_performed = False
        self.unlock_status_bar()
        self.update_status(message = 'Retrieving file list, Hidden files: {}, Please wait...'.format(self.ftpController.hidden_files))
        self.lock_status_bar()
        del self.file_list[:]
        del self.detailed_file_list[:]
        #start thread
        self.thread = threading.Thread(target = self.update_file_list_thread)
        self.thread.daemon = True
        self.thread.start()
        self.process_thread_requests()

    def update_file_list_thread(self):
        try:
            with self.thread_lock:
                self.detailed_file_list = self.ftpController.get_detailed_file_list()
                self.file_list = self.ftpController.get_file_list(self.detailed_file_list)
            #Set the window title to current path
            thread_request_queue.put(lambda:self.master.wm_title('whipFTP-'+self.ftpController.pwd()))
            thread_request_queue.put(lambda:self.unlock_status_bar())
            thread_request_queue.put(lambda:self.update_status(''))
        except:
            thread_request_queue.put(lambda:self.unlock_status_bar())
            thread_request_queue.put(lambda:self.update_status_red('Unable to retrieve file list, connection might be lost.'))
            thread_request_queue.put(lambda:self.lock_status_bar())
        thread_request_queue.put(lambda:self.draw_icons())
        #Enable toolbar
        thread_request_queue.put(lambda:self.end_wait())
        

        
    def draw_icons(self, event = None):    
        #Calculate cell width
        self.cell_width = 65 + self.default_font.measure(self.ftpController.max_len_name)
        self.canvas_width = self.canvas.winfo_width() - 4
        self.canvas_height = self.canvas.winfo_height()
        if(self.cell_width > self.canvas_width):
            self.cell_width = self.canvas_width
        #Clear canvas
        self.canvas.delete('all')
        y = 0
        x = 0
        #Create a rectangle for update_status_mouse(self, event) function
        self.rect_id = self.canvas.create_rectangle(-1, -1, -1, -1, fill = '', outline = '')
        #Draw icons
        #If there are no files, draw watermark
        if len(self.file_list) is 0:
            self.canvas.create_image(self.canvas_width/2, self.canvas_height/2, image = self.whipFTP_glow_icon)
        for file_name, file_details in zip(self.file_list, self.detailed_file_list):
            if((x+1)*self.cell_width > self.canvas_width):
                y+=1
                x=0
            #Check types, draw appropriate icon
            if(self.ftpController.is_dir(file_details)):
                self.canvas.create_image(25+(x*self.cell_width), 18+(y*35), image = self.folder_icon)
                canvas_id = self.canvas.create_text(45+(x*self.cell_width), 13+(y*35), anchor='nw')
                self.canvas.itemconfig(canvas_id, text= file_name)  
                x+=1
            else:
                self.canvas.create_image(25+(x*self.cell_width), 18+(y*35), image = self.textfile_icon)
                canvas_id = self.canvas.create_text(45+(x*self.cell_width), 13+(y*35), anchor='nw')
                self.canvas.itemconfig(canvas_id, text= file_name)  
                x+=1
        #Calculate scroll region for scroll bar
        if (y+1)*35 < self.canvas_height:
            scroll_region_y = self.canvas_height - 1
            self.vbar.configure(style = 'Whitehide.TScrollbar')
            self.vbar.bind('<Motion>', lambda event, arg = '': self.update_status(event, arg)) 
        else:
            scroll_region_y = ((y+1)*35)+13
            self.vbar.configure(style = 'TScrollbar')
            self.vbar.bind('<Motion>', lambda event, arg = 'Scrollbar.': self.update_status(event, arg)) 
        self.canvas.configure(scrollregion = '-1 -1 ' + str(self.canvas_width) + ' ' + str(scroll_region_y))
        #Redraw all selected-highlight rectangles for selected files
        for file_index in self.selected_file_indices:
            #Round canvas's width to nearest multiple of self.cell_width, width of each cell
            self.max_width = self.canvas_width - (self.canvas_width % self.cell_width) 
            max_no_cells_x  = self.max_width/self.cell_width 
            x = file_index%max_no_cells_x
            y = int(file_index/max_no_cells_x)
            self.selected_file_indices[file_index] = self.canvas.create_rectangle(x*self.cell_width+2, y*35+2, (x+1)*self.cell_width-1, (y+1)*35-1, fill = '', outline = 'Red')
        


    def update_status_and_mouse(self, event):
        #Get absolute mouse position on canvas
        self.mouse_x, self.mouse_y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y) 
        #Calculate cell row and cell column based on mouse's position
        self.x_cell_pos = int(self.mouse_x/self.cell_width)
        self.y_cell_pos = int(self.mouse_y/35)
        #Round canvas's width to nearest multiple of self.cell_width, width of each cell
        self.max_width = self.canvas_width - (self.canvas_width % self.cell_width)
        #Use index = (y*width)+x to figure out the file index from canvas and mouse position
        self.current_file_index = int(((self.max_width/self.cell_width)*self.y_cell_pos) + self.x_cell_pos)
        #Set status only if valid index, draw mouse-hover highlight rectangle
        if(self.current_file_index >= 0 and self.current_file_index < len(self.file_list) and self.mouse_x < self.max_width):
            self.update_status(event, self.detailed_file_list[self.current_file_index])
            #Configure the rectangle created in draw_icons() to highlight the current folder mose is pointing at
            self.canvas.itemconfig(self.rect_id, outline = 'black')
            self.canvas.coords(self.rect_id, self.x_cell_pos*self.cell_width+2, self.y_cell_pos*35+2, (self.x_cell_pos+1)*self.cell_width-1, (self.y_cell_pos+1)*35-1) 
        else:
            #Tell how many files are present and how many are selected in the status bar
            self.update_status(event, 'Total no. of items: ' + str(len(self.file_list)) + '   Selected: ' + str(len(self.selected_file_indices)))
            #Stop mouse-hover highlighting
            self.canvas.itemconfig(self.rect_id, outline = '')
            self.canvas.coords(self.rect_id, -1, -1, -1, -1)  
    
    def update_status(self, event = None, message = ' '):
        #Stop mouse-hover highlighting
        self.canvas.itemconfig(self.rect_id, outline = '')
        self.canvas.coords(self.rect_id, -1, -1, -1, -1) 
        #Display message in status bar in black color only if change_status is true else ignore it
        if self.change_status is True:
            self.status_label.configure(style = 'TLabel')
            self.current_status.set(message)

    def update_status_red(self, message):
        #Stop mouse-hover highlighting
        self.canvas.itemconfig(self.rect_id, outline = '')
        self.canvas.coords(self.rect_id, -1, -1, -1, -1) 
        #Display message in status bar in red color only if change_status is true else ignore it
        if self.change_status is True:
            self.status_label.configure(style = 'Red.TLabel')
            self.current_status.set(message)
            self.problem()

    def lock_status_bar(self):
        self.change_status = False

    def unlock_status_bar(self):
        self.change_status = True



    def toggle_hidden_files(self, event):
        self.ftpController.toggle_hidden_files()
        self.update_file_list()
        self.deselect_everything()



    def on_mouse_wheel(self, event):
        def delta(event):
            if event.num == 5 or event.delta < 0:
                return 1 
            return -1 
        self.canvas.yview_scroll(delta(event), 'units')

    def mouse_select(self, event):
        self.master.focus()
        #Store start position for drag select
        self.start_x = self.x_cell_pos
        self.start_y = self.y_cell_pos
        #Deselect everything
        self.deselect_everything()  
        #Set selected only if valid index
        if(self.current_file_index >= 0 and self.current_file_index < len(self.file_list) and self.mouse_x < self.max_width):   
            #Draw a 'selected' highlighting rectangle and save a reference to the rectangle in selected file list
            self.selected_file_indices[self.current_file_index] = self.canvas.create_rectangle(self.x_cell_pos*self.cell_width+2, self.y_cell_pos*35+2, 
            	                                                                               (self.x_cell_pos+1)*self.cell_width - 1, (self.y_cell_pos+1)*35 - 1, 
            	                                                                               fill = '', outline = 'Red')
        #Tell how many files are present and how many are selected in the status bar
        self.update_status(event, 'Total no. of items: ' + str(len(self.file_list)) + '   Selected: ' + str(len(self.selected_file_indices)))

    def ctrl_select(self, event):
        #Set selected only if valid index
        if(self.current_file_index >= 0 and self.current_file_index < len(self.file_list) and self.mouse_x < self.max_width): 
            #If WAS NOT selected already
            if(self.current_file_index not in self.selected_file_indices):
                #Draw a 'selected' highlighting rectangle and save a reference to the rectangle in selected file list
                self.selected_file_indices[self.current_file_index] = self.canvas.create_rectangle(self.x_cell_pos*self.cell_width+2, self.y_cell_pos*35+2,
                                                                                                   (self.x_cell_pos+1)*self.cell_width-1, (self.y_cell_pos+1)*35-1,
                                                                                                   fill = '', outline = 'Red')
            #If WAS selected already
            else:
                #Remove from selected file list
                del self.selected_file_indices[self.current_file_index]
                #Redraw icons
                self.draw_icons()  
        #Tell how many files are present and how many are selected in the status bar
        self.update_status(event, 'Total no. of items: ' + str(len(self.file_list)) + '   Selected: ' + str(len(self.selected_file_indices)))

    def drag_select(self, event):
        #Update to get current mouse position
        self.update_status_and_mouse(event)
        #Calculate steps and offsets for x-direction
        if(self.x_cell_pos <= self.start_x):
            start_x_offset =1
            step_x = 1
        else:
            start_x_offset =-1
            step_x = -1
        #Calculate steps and offsets for y-direction
        if(self.y_cell_pos <= self.start_y):
            start_y_offset =1
            step_y = 1
        else:
            start_y_offset =-1
            step_y = -1
        #Select items
        for i in range(self.x_cell_pos, self.start_x +start_x_offset, step_x):
            for j in range(self.y_cell_pos, self.start_y +start_y_offset, step_y):
                #Calculate index
                file_index = int(((self.max_width/self.cell_width)*j) + i)
                #Set selected only if valid index
                if(file_index >= 0 and file_index < len(self.file_list) and i < self.max_width/self.cell_width):   
                    #Draw a 'selected' highlighting rectangle and save a reference to the rectangle in selected file dictionary
                    self.selected_file_indices[file_index] = self.canvas.create_rectangle(i*self.cell_width+2, j*35+2, (i+1)*self.cell_width-1, (j+1)*35-1, fill = '',
                    outline = 'Red')
        #Tell how many files are present and how many are selected in the status bar
        self.update_status(event, 'Total no. of items: ' + str(len(self.file_list)) + '   Selected: ' + str(len(self.selected_file_indices)))

    def handle_dnd(self, action, actions, type, win, X, Y, x, y, data):
        #If there is another child window, disable dnd
        if(len(self.master.children) != 4): return
        del self.dnd_file_list[:]
        self.dnd_file_list = self.dnd.parse_uri_list(data)
        self.upload_thread_dnd()

    def show_dnd_icon(self, action, actions, type, win, X, Y, x, y, data):
        #If there is another child window, disable dnd
        if(len(self.master.children) != 4): return
        self.deselect_everything()
        self.canvas.delete("all")
        self.canvas.create_image(self.canvas_width/2, self.canvas_height/2, image = self.dnd_glow_icon)

    def deselect_everything(self):
            #Delete selected file dictionary
            self.selected_file_indices.clear()
            #Redraw all icons and remove any 'selected' highlighting rectangles
            self.draw_icons()



    def change_dir(self, event):
        #Delete selected file list
        self.selected_file_indices.clear()
        #Show message box
        if(self.current_file_index >= 0 and self.current_file_index < len(self.file_list) and self.mouse_x < self.max_width):
            if(self.ftpController.is_dir(self.detailed_file_list[self.current_file_index])):
                try:
                    self.ftpController.ftp.cwd(self.file_list[self.current_file_index])
                    self.update_file_list()       
                except:
                    self.update_status_red('Unable to open directory, try reconnecting.')
                    self.lock_status_bar()

    def goto_window_ask(self):
        self.goto_window = Filedialogs.name_dialog(self.master, 'Goto', self.goto_path, self.goto_icon, 'Enter path:')

    def goto_path(self):
        path = self.goto_window.rename_entry.get()
        self.goto_window.destroy()
        #Delete selected file list
        self.selected_file_indices.clear()
        #Show message box
        try:
            self.ftpController.ftp.cwd(path)
            self.update_file_list()       
        except:
            self.update_status_red('Unable to open directory, try reconnecting.')
            self.lock_status_bar()       



    def dir_up(self):
        #Delete selected file list
        self.selected_file_indices.clear()
        #Update GUI now, before mainloop, the following code takes a long time to execute
        self.master.update_idletasks() 
        try:
            if(self.search_performed is False):
                self.ftpController.ftp.cwd('..')
            self.update_file_list()     
        except:
            self.update_status_red('Unable to open parent directory, try reconnecting.')
            self.lock_status_bar()



    def file_properties_window(self):
        #Check number of files selected
        if(len(self.selected_file_indices) is not 1): return
        #Create the string that contains all the properties
        for key in self.selected_file_indices:
            file_details = self.ftpController.get_properties(self.detailed_file_list[key])
            #Get file name
            file_name = file_details[0] + '\n'
            #Get file attributes
            file_attribs = file_details[1]+ '\n'
            #Get date modified
            date_modified = file_details[2]
            if(self.ftpController.is_dir(self.detailed_file_list[key])):
                properties = 'Name: '+ file_name + 'Attributes: ' + file_attribs + 'Date: ' + date_modified
            else:    
                file_size = file_details[3] + ' bytes'
                properties = 'Name: '+ file_name + 'Attributes: ' + file_attribs + 'Date: ' + date_modified + '\n' + 'Size: ' + file_size
        #Display the created string in properties dialog
        self.properties_dialog = Filedialogs.file_properties_dialog(self.master, 'Properties', self.rename_window, self.change_permissions_window, self.properties_icon, properties)

    def rename_window(self):
        self.properties_dialog.destroy()
        self.rename_dialog =  Filedialogs.name_dialog(self.master, 'Rename', self.rename_file_thread, self.rename_icon)

    def rename_file_thread(self):
        rename_name = self.rename_dialog.rename_entry.get()
        #Destroy rename window
        self.rename_dialog.destroy()
        #Show message box
        self.start_wait()
        #start thread
        self.thread =  threading.Thread(target = self.rename_file, args = (self.ftpController, self.file_list, self.detailed_file_list, self.selected_file_indices, rename_name))
        self.thread.daemon = True
        self.thread.start()
        self.process_thread_requests()

    def rename_file(self, ftpController, file_list, detailed_file_list, selected_file_indices, rename_name):
        try:
            for key in selected_file_indices:
                file_name = ftpController.cwd_parent(file_list[key])
                #If a directory
                if(self.ftpController.is_dir(detailed_file_list[key])):
                    ftpController.rename_dir(file_name, rename_name)                   
                #If a file            
                else:
                    ftpController.ftp.rename(file_name, rename_name)
            #Deselect everything
            thread_request_queue.put(lambda:self.selected_file_indices.clear())
            #update file list and redraw icons
            thread_request_queue.put(lambda:self.cont_wait())
            thread_request_queue.put(lambda:self.update_file_list())
        except:
            thread_request_queue.put(lambda:self.update_status_red('Unable to rename, try a diffrent name or try reconnecting.'))
            thread_request_queue.put(lambda:self.lock_status_bar())

    def change_permissions_window(self):
        self.properties_dialog.destroy()
        self.permission_window =  Filedialogs.name_dialog(self.master, 'chmod', self.change_permissions_thread, self.permissions_icon, 'Enter octal notation:')

    def change_permissions_thread(self):
        octal_notation = self.permission_window.rename_entry.get()
        #Destroy permission window
        self.permission_window.destroy()
        #Show message box
        self.start_wait()
        #start thread
        self.thread = threading.Thread(target = self.change_permissions, args = (self.ftpController, self.file_list, self.selected_file_indices, octal_notation))
        self.thread.daemon = True
        self.thread.start()
        self.process_thread_requests()          

    def change_permissions(self, ftpController, file_list, selected_file_indices, octal_notation):
        try:
            for key in selected_file_indices:
               file_name = ftpController.cwd_parent(file_list[key])
               ftpController.chmod(file_name, int(octal_notation))
            #Deselect everything
            thread_request_queue.put(lambda:self.selected_file_indices.clear())
            #update file list and redraw icons
            thread_request_queue.put(lambda:self.cont_wait())
            thread_request_queue.put(lambda:self.update_file_list())
        except:
            thread_request_queue.put(lambda:self.update_status_red('Unable to change permissions.'))
            thread_request_queue.put(lambda:self.lock_status_bar())


    
    def create_dir_window(self):
        self.create_dir_dialog = Filedialogs.name_dialog(self.master, 'Create a new folder', self.create_dir_thread, self.newfolder_icon)

    def create_dir_thread(self):
        #Create thread
        self.thread = threading.Thread(target = self.create_dir, args = (self.ftpController, self.create_dir_dialog.rename_entry.get()))
        #Destroy rename window
        self.create_dir_dialog.destroy()
        #Show message box
        self.start_wait()
        #Start thread and process requests
        self.thread.daemon = True
        self.thread.start()
        self.process_thread_requests()

    def create_dir(self, ftpController, dir_name):
        try:
            #Deselect everything
            thread_request_queue.put(lambda:self.selected_file_indices.clear())
            ftpController.mkd(dir_name)
            #update file list and redraw icons
            thread_request_queue.put(lambda:self.cont_wait())
            thread_request_queue.put(lambda:self.update_file_list())
        except:
            thread_request_queue.put(lambda:self.update_status_red('Unable to create folder, either invalid characters or not having permission may be the reason or directory already exists.'))
            thread_request_queue.put(lambda:self.lock_status_bar())


    def upload_window(self):
        self.upload_dialog = Filedialogs.open_file_dialog(self.master, 'Choose file(s) or folder(s) to upload', self.upload_thread)

    def upload_thread(self):
        #Create console/terminal window
        self.create_progress_window()
        #Destroy upload window
        self.upload_dialog.destroy()
        #Set status
        self.update_status('Uploading file(s)...')
        #start thread
        self.thread =  threading.Thread(target = self.upload, args = (self.ftpController, self.upload_dialog.file_list, self.upload_dialog.selected_file_indices))
        self.thread.daemon = True
        self.thread.start()
        self.process_thread_requests()
        
    def upload(self, ftpController, file_list, selected_file_indices):     
        #Thread safe progress function
        def progress(file_name, status):
            thread_request_queue.put(lambda:self.progress(file_name, status))
        #Thread safe replace function
        def replace(file_name, status):
            thread_request_queue.put(lambda:self.thread_safe_replace(file_name, status))
            thread_request_queue.join()
            with self.thread_lock:
                return self.replace_flag
        #Loop through selected items and upload them            
        for index in selected_file_indices:
            if(isfile(file_list[index])):
                ftpController.upload_file(file_list[index], os.path.getsize(file_list[index]), progress, replace)
            else:
                ftpController.upload_dir(file_list[index], progress, replace)
        #Update file list and redraw icons
        thread_request_queue.put(lambda:self.update_file_list())
        thread_request_queue.put(lambda:self.update_status(' '))
        thread_request_queue.put(lambda:self.progress('You can now close the window', 'Done'))
        thread_request_queue.put(lambda:self.console_window.enable_close_button())

    def upload_thread_dnd(self):
        #Create console/terminal window
        self.create_progress_window()
        #Set status
        self.update_status('Uploading file(s)...')
        #start thread
        self.thread =  threading.Thread(target = self.upload_dnd, args = (self.ftpController, self.dnd_file_list))
        self.thread.daemon = True
        self.thread.start()
        self.process_thread_requests()
        
    def upload_dnd(self, ftpController, dnd_file_list):
        #Thread safe progress function
        def progress(file_name, status):
            thread_request_queue.put(lambda:self.progress(file_name, status))
        #Thread safe replace function
        def replace(file_name, status):
            thread_request_queue.put(lambda:self.thread_safe_replace(file_name, status))
            thread_request_queue.join()
            with self.thread_lock:
                return self.replace_flag
        #Loop through selected items and upload them         
        for file in dnd_file_list:
            os.chdir('/'.join(file.split('/')[:-1]))
            file = ''.join(file.split('/')[-1:])
            if(isfile(file)):
                ftpController.upload_file(file, os.path.getsize(file), progress, replace)
            else:
                ftpController.upload_dir(file, progress, replace)
        #Update file list and redraw icons
        thread_request_queue.put(lambda:self.update_file_list())
        thread_request_queue.put(lambda:self.update_status(' '))
        thread_request_queue.put(lambda:self.progress('You can now close the window', 'Done'))
        thread_request_queue.put(lambda:self.console_window.enable_close_button())        


    def download_window(self):
        #Check number of files selected
        if(len(self.selected_file_indices) < 1): return
        self.download_dialog = Filedialogs.open_file_dialog(self.master, 'Choose or Drag and Drop folder to download in', self.download_thread, True)

    def download_thread(self):
        #Destroy download window
        self.download_dialog.destroy()
        #Create console/terminal window
        self.create_progress_window()
        #Set status
        self.update_status('downloading file(s)...')
        #Create new thread for downloading
        self.thread =  threading.Thread(target = self.download, args = (self.ftpController, self.file_list, self.detailed_file_list, self.selected_file_indices))
        self.thread.daemon = True
        self.thread.start()
        self.process_thread_requests()

    def download(self, ftpController, file_list, detailed_file_list, selected_file_indices):                       
        #Thread safe progress function
        def progress(file_name, status):
            thread_request_queue.put(lambda:self.progress(file_name, status))
        #Thread safe replace function
        def replace(file_name, status):
            thread_request_queue.put(lambda:self.thread_safe_replace(file_name, status))
            thread_request_queue.join()
            with self.thread_lock:
                return self.replace_flag
        #Loop through selected items and download them
        for index in selected_file_indices:
        #Switch to parents 
            file_name = ftpController.cwd_parent(file_list[index])
            #If a file download it to the specified directory
            if(not self.ftpController.is_dir(detailed_file_list[index])):
                ftpController.download_file(file_name, int(self.ftpController.get_properties(detailed_file_list[index])[3]), progress, replace)
            else:
                ftpController.download_dir(file_name, progress, replace)
        #Update file list and redraw icons
        thread_request_queue.put(lambda:self.update_file_list())
        thread_request_queue.put(lambda:self.update_status(' '))
        thread_request_queue.put(lambda:self.progress('You can now close the window', 'Done'))
        thread_request_queue.put(lambda:self.console_window.enable_close_button())
        thread_request_queue.put(lambda:self.deselect_everything())



    def search_window_ask(self):
        self.search_window =  Filedialogs.name_dialog(self.master, 'Search', self.search_thread, self.search_icon, 'Enter file name:')

    def search_thread(self):
        #Create console/terminal window
        self.create_progress_window()
        #Create new thread for searching
        self.thread = threading.Thread(target = self.search_file, args = (self.ftpController, self.search_window.rename_entry.get()) )
        self.search_window.destroy()
        self.thread.daemon= True
        self.thread.start()
        self.process_thread_requests()

    def search_file(self, ftpController, search_file_name):
        #Thread safe progress function
        def progress(file_name, status):
            thread_request_queue.put(lambda:self.progress(file_name, status))        
        try:
            #Store the current path so that we can return to it after search
            path = ftpController.pwd()
            #Reset file lists
            thread_request_queue.put(lambda:self.selected_file_indices.clear())      
            #Start searching
            ftpController.clear_search_list()
            ftpController.search(path, progress, search_file_name)
            #Add the results to file list and redraw icons
            thread_request_queue.put(lambda:self.update_search_files())    
            thread_request_queue.put(lambda:self.update_status(' '))
            #Restore path
            ftpController.ftp.cwd(path)
            #Set search performed
            thread_request_queue.put(lambda:self.search_finished())
        except:
            thread_request_queue.put(lambda:self.update_status_red('Unable to search, try reconnecting.'))
            thread_request_queue.put(lambda:self.lock_status_bar())
            thread_request_queue.put(lambda:self.progress('Failed', 'Search'))
        thread_request_queue.put(lambda:self.progress('You can now close the window', 'Done'))
        thread_request_queue.put(lambda:self.console_window.enable_close_button())    

    def update_search_files(self):
        #Replace file lists with search results and redraw icons
        del self.file_list[:]
        del self.detailed_file_list[:]
        self.file_list = self.ftpController.get_search_file_list()
        self.detailed_file_list = self.ftpController.get_detailed_search_file_list()
        self.draw_icons()

    def search_finished(self):
        self.search_performed = True



    def delete_window(self, event = None):
        if(len(self.selected_file_indices) < 1): return
        self.delete_warning = Filedialogs.warning_dialog(self.master, 'Are you sure?', self.delete_thread, self.delete_icon, 'Delete selected files/folders?')

    def delete_thread(self):
        #Create console/terminal window
        self.create_progress_window()
        self.replace = threading.Event()
        self.replace.clear()
        #Destroy warning window
        self.delete_warning.destroy()
        #Set current status
        self.update_status('Deleting file(s)...')       
        #Start thread 
        self.thread = threading.Thread(target = self.delete_item, args = (self.ftpController, self.file_list, self.detailed_file_list, self.selected_file_indices))
        self.thread.daemon = True
        self.thread.start()
        self.process_thread_requests()

    def delete_item(self, ftpController, file_list, detailed_file_list, selected_file_indices):
        #Thread safe progress function
        def progress(file_name, status):
            thread_request_queue.put(lambda:self.progress(file_name, status))
        #Loop through all selected files and folders
        for index in selected_file_indices:
            file_name = ftpController.cwd_parent(file_list[index])
            #If directory
            if(self.ftpController.is_dir(detailed_file_list[index])):
                ftpController.delete_dir(file_name, progress)
            #If file                
            else:
                ftpController.delete_file(file_name, progress)
        #Deselect everything
        thread_request_queue.put(lambda:self.deselect_everything)
        #Update file list and redraw icons
        thread_request_queue.put(lambda:self.update_file_list())
        thread_request_queue.put(lambda:self.update_status(' '))
        thread_request_queue.put(lambda:self.progress('You can now close the window', 'Done'))
        thread_request_queue.put(lambda:self.console_window.enable_close_button())
        thread_request_queue.put(lambda:self.deselect_everything())




    def clipboard_cut(self, event = None):
        #Check number of files in clipboard
        if(len(self.selected_file_indices) < 1): return
        self.cut = True
        del self.clipboard_file_list[:]
        for index in self.selected_file_indices:
            #If it is a search result get the clipboard path from the search result
            if(self.search_performed is True):
                self.clipboard_path_list.append('/'.join(self.file_list[index].split('/')[:-1]))
                self.clipboard_file_list.append(''.join(self.file_list[index].split('/')[-1:]))
            else:
                self.clipboard_path_list.append(self.ftpController.pwd())
                self.clipboard_file_list.append(self.file_list[index])
            self.detailed_clipboard_file_list.append(self.detailed_file_list[index])
        self.deselect_everything()

    def clipboard_copy(self, event = None):
        #Check number of files in clipboard
        if(len(self.selected_file_indices) < 1): return      
        self.copy = True
        del self.clipboard_file_list[:]
        for index in self.selected_file_indices:
            #If it is a search result get the clipboard path from the search result
            if(self.search_performed is True):
                self.clipboard_path_list.append('/'.join(self.file_list[index].split('/')[:-1]))
                self.clipboard_file_list.append(''.join(self.file_list[index].split('/')[-1:]))
            else:
                self.clipboard_path_list.append(self.ftpController.pwd())
                self.clipboard_file_list.append(self.file_list[index])
            self.detailed_clipboard_file_list.append(self.detailed_file_list[index])
        self.deselect_everything()

    def clipboard_paste_thread_create(self, event = None):
        #Check number of files in clipboard
        if(len(self.clipboard_file_list) < 1): return
        #Create console/terminal window        
        self.create_progress_window()
        #start thread
        self.thread =  threading.Thread(target = self.clipboard_paste, args = (self.ftpController, self.clipboard_path_list, self.clipboard_file_list,
                                        self.detailed_clipboard_file_list, self.cut, self.copy))
        self.thread.daemon = True
        self.thread.start()
        self.process_thread_requests()

    def clipboard_paste(self, ftpController, clipboard_path_list, clipboard_file_list, detailed_clipboard_file_list, cut, copy):        
        #Set current status
        thread_request_queue.put(lambda:self.update_status('Moving file(s)...'))        
        if(cut is True):
            #Loop through all selected files and folders
            for clipboard_path, file_name in zip(clipboard_path_list, clipboard_file_list):
                ftpController.move_dir(clipboard_path +'/'+file_name, ftpController.pwd()+'/'+file_name, self.progress, self.ask_replace)
            thread_request_queue.put(lambda:self.clear_clipboard())
            thread_request_queue.put(lambda:self.progress('You can now close the window', 'Done'))
        elif (copy is True):
            #Set current status
            thread_request_queue.put(lambda:self.update_status('Copying file(s)...'))
            #Loop through all selected files and folders
            for clipboard_path, file_name, file_details in zip(clipboard_path_list, clipboard_file_list, detailed_clipboard_file_list):
                #Check for file or directory, use appropriate function
                try:
                    if(self.ftpController.is_dir(file_details)):
                        ftpController.copy_dir(clipboard_path, file_name, self.progress, self.ask_replace)
                    else:                    
                        ftpController.copy_file(clipboard_path, file_name, int(self.ftpController.get_properties(file_details)[3]), self.progress, self.ask_replace)
                except:
                    thread_request_queue.put(lambda:self.progress('Failed to copy file/folder', file_name))
            thread_request_queue.put(lambda:self.clear_clipboard())
            thread_request_queue.put(lambda:self.progress('You can now close the window', 'Done'))
        #update file list and redraw icons
        thread_request_queue.put(lambda:self.update_file_list())
        thread_request_queue.put(lambda:self.update_status(' '))
        thread_request_queue.put(lambda:self.console_window.enable_close_button())

    def clear_clipboard(self):
        del self.clipboard_file_list[:]
        del self.detailed_clipboard_file_list[:]
        del self.clipboard_path_list[:]  
        self.cut = False
        self.copy = False      


    def ask_replace(self, file_name, status):
        #Check if replace all has been selected
        if(self.replace_all is True): return True
        #Check if skip all has been selected
        if(self.skip_all is True): return False
        #Create replace dialog
        self.replace_window = Filedialogs.replace_dialog(self.console_window.console_dialog_window, 'Conflicting files', self.copy_icon, file_name+': '+status+', Replace?')
        #Loop till a button is pressed
        while self.replace_window.command is '':
            self.replace_window.replace_dialog_window.update()
        if (self.replace_window.command is 'skip'): return False
        elif (self.replace_window.command is 'replace'): return True
        elif (self.replace_window.command is 'skip_all'):
            self.skip_all = True            
            return False 
        elif (self.replace_window.command is 'replace_all'):
            self.replace_all = True            
            return True

    def thread_safe_replace(self, file_name, status):
        with self.thread_lock:
            self.replace_flag = self.ask_replace(file_name, status)

    def reset_replace(self):
        #Set replace all and skip all mode to false
        self.replace_all = False
        self.skip_all = False

    def process_thread_requests(self):
        while not thread_request_queue.empty():
            thread_request_queue.get()()
            thread_request_queue.task_done()
        if(self.thread.is_alive()):
            self.master.after(5, self.process_thread_requests)

    def create_progress_window(self):
        self.console_window = Filedialogs.console_dialog(self.master, self.console_icon, self.reset_replace)

    def progress(self, file_name, status):
        #If it is a progress
        if('%' in status):
            self.console_window.progress(status)
            return
        if(status == 'newline'):
            self.console_window.insert('')
            return
        #Print to console
        self.console_window.insert(status+': '+file_name)



    def info(self):
        self.info_window = Filedialogs.about_dialog(self.master, 'About', self.whipFTP_icon, 'whipFTP v5.0', '© Vishnu Shankar') 



    def disable_toolbar(self, event = None):
        #Disable all buttons
        self.canvas.grab_set()
        #Disable mouse action
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<Double-Button-1>")     
        self.canvas.unbind("<Control-Button-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<Motion>")

    def enable_toolbar(self, event = None):
        #Enable all buttons
        self.canvas.grab_release()
        #Enable mouse action
        self.canvas.bind("<Button-1>", self.mouse_select)
        self.canvas.bind("<Double-Button-1>" , self.change_dir)     
        self.canvas.bind("<Control-Button-1>", self.ctrl_select)
        self.canvas.bind("<B1-Motion>", self.drag_select)
        self.canvas.bind("<Motion>", self.update_status_and_mouse)

    def start_wait(self, event = None):
        if(self.change_status is False): return
        if(self.continue_wait is True):
            self.continue_wait = False
            return
        self.disable_toolbar()
        self.wait_anim = True
        self.wait_frame_index = 1
        self.master.after(100, self.do_wait)

    def cont_wait(self, event = None):
        self.continue_wait = True

    def do_wait(self, event = None):
        if(self.wait_anim is False): return
        #make sure frame index is not above 4
        if(self.wait_frame_index == 4):
            self.wait_frame_index = 0
        #clear and draw the correct frame
        self.canvas.delete('all')
        self.canvas.create_image(self.canvas_width/2, self.canvas_height/2, image = self.wait_frames[self.wait_frame_index])
        #update frame index
        self.wait_frame_index += 1
        #call the do wait function after some time to update the animation
        if(self.wait_frame_index == 1):
            self.master.after(400, self.do_wait)
        else:
            self.master.after(100, self.do_wait)

    def end_wait(self, event = None):
        self.wait_anim = False
        self.enable_toolbar()

    def problem(self, event = None):
        self.end_wait()
        self.canvas.delete('all')
        self.canvas.create_image(self.canvas_width/2, self.canvas_height/2, image = self.problem_icon)



#Program entry point
#Tell windows not to DPI scale this application
if(platform.system() is 'Windows' and platform.release() != '7'):
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
#Create root window
root = Tk()
#Include the theme and tkdnd libraries
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
arc_theme_path = (dname+'/Theme')
tkdnd_path = (dname+'/TkDND')
root.tk.eval('lappend auto_path {%s}' % arc_theme_path)
root.tk.eval('lappend auto_path {%s}' % tkdnd_path)
root.tk.eval('package require tkdnd')
#Queue for handling threads
global thread_request_queue
thread_request_queue = queue.Queue()
#Initilize the app
whipFTP = app(root)
#Initialize mainloop
root.mainloop()
