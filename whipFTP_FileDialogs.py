'''
    Custom file dialogs for whipFTP, Copyrights Vishnu Shankar B,
'''

import os
from os.path import expanduser
from os import listdir
from os.path import isfile, join
import platform
import psutil
from tkinter import *
from tkinter import font
from tkinter import ttk
from tkinter import PhotoImage
from tkinter import messagebox
from TkDND_wrapper import *
if(platform.system() is 'Windows'):
    import win32api
    import win32con


class floating_message_dialog:

    def __init__(self, master, Title, icon, message):
       #Create a new dialog box window
        self.floating_message_dialog_window = Toplevel()

       #Make it non-resizeble, set title
        self.floating_message_dialog_window.resizable(False, False)
        self.floating_message_dialog_window.title(Title)

       #Create frames 
        self.icon_frame = ttk.Frame(self.floating_message_dialog_window)
        self.icon_frame.pack(side = 'left', fill = Y)
        self.entry_frame = ttk.Frame(self.floating_message_dialog_window)
        self.entry_frame.pack(side = 'left', fill = Y)

       #Create the label showing rename icon
        ttk.Label(self.icon_frame, image = icon).pack(padx = 3, pady = 3)

       #Create the label
        ttk.Label(self.entry_frame, text = message, anchor = 'w').pack(padx = 3, fill = X, expand = True)

       #No window border
        self.floating_message_dialog_window.overrideredirect(1)

       #center the window
        self.floating_message_dialog_window.withdraw()
        self.floating_message_dialog_window.update()
        x = master.winfo_rootx()
        y = master.winfo_rooty()
        main_height =master.winfo_height()
        main_width = master.winfo_width()
        window_height = self.floating_message_dialog_window.winfo_reqheight()
        window_width = self.floating_message_dialog_window.winfo_reqwidth()
        geom = '+%d+%d' % ((x + main_width//2 - window_width//2), (y + main_height//2 - window_height//2))  
        self.floating_message_dialog_window.geometry(geom)
        self.floating_message_dialog_window.deiconify()

       #Prevent new task in taskbar
        self.floating_message_dialog_window.transient(master)  

       #Focus on the dialog box, freeze controll of main window
        self.floating_message_dialog_window.focus_force()
        while True:
            try:
                self.floating_message_dialog_window.grab_set()
                break
            except: continue

    def destroy(self):
        self.floating_message_dialog_window.destroy()


class message_dialog:

    def __init__(self, master, Title, icon, message):

       #Create a new dialog box window
        self.message_dialog_window = Toplevel()

       #Make it non-resizeble, set title
        self.message_dialog_window.resizable(False, False)
        self.message_dialog_window.title(Title)

       #Create frames 
        self.icon_frame = ttk.Frame(self.message_dialog_window)
        self.icon_frame.pack(side = 'left', fill = Y)
        self.entry_frame = ttk.Frame(self.message_dialog_window)
        self.entry_frame.pack(side = 'left', fill = Y)

       #Create the label showing rename icon
        ttk.Label(self.icon_frame, image = icon).pack(padx = 3, pady = 3)

       #Create the label
        ttk.Label(self.entry_frame, text = message, anchor = 'w').pack(padx = 3, fill = X, expand = True)

       #Create buttons
        self.rename_ok_button = ttk.Button(self.entry_frame, text = 'OK', command = self.destroy)
        self.rename_ok_button.pack(side = 'right', pady = 3, padx = 3 )

       #center the window
        self.message_dialog_window.withdraw()
        self.message_dialog_window.update()
        x = master.winfo_rootx()
        y = master.winfo_rooty()
        main_height =master.winfo_height()
        main_width = master.winfo_width()
        window_height = self.message_dialog_window.winfo_reqheight()
        window_width = self.message_dialog_window.winfo_reqwidth()
        geom = '+%d+%d' % ((x + main_width//2 - window_width//2), (y + main_height//2 - window_height//2))  
        self.message_dialog_window.geometry(geom)
        self.message_dialog_window.deiconify()

       #Prevent new task in taskbar
        self.message_dialog_window.transient(master)  

       #Focus on the dialog box, freeze controll of main window
        self.message_dialog_window.focus_force()
        while True:
            try:
                self.message_dialog_window.grab_set()
                break
            except: continue

    def destroy(self):
        self.message_dialog_window.destroy()
        

class warning_dialog:

    def __init__(self, master, Title, func_command, icon, message):
       #Create a new dialog box window
        self.warning_dialog_window = Toplevel(master)

       #Make it non-resizeble, set title
        self.warning_dialog_window.resizable(False, False)
        self.warning_dialog_window.title(Title)

       #Create frames 
        self.icon_frame = ttk.Frame(self.warning_dialog_window)
        self.icon_frame.pack(side = 'left', fill = Y)
        self.entry_frame = ttk.Frame(self.warning_dialog_window)
        self.entry_frame.pack(side = 'left', fill = Y)

       #Create the label showing rename icon
        ttk.Label(self.icon_frame, image = icon).pack()

       #Create the label
        ttk.Label(self.entry_frame, text = message, anchor = 'w').pack(padx = 3, fill = X, expand = True)

       #Create buttons
        self.cancel_ok_button = ttk.Button(self.entry_frame, text = 'Cancel', command = self.warning_dialog_window.destroy)
        self.cancel_ok_button.pack(side = 'right', pady = 3, padx = 3 )
        self.rename_ok_button = ttk.Button(self.entry_frame, text = 'OK', command = func_command)
        self.rename_ok_button.pack(side = 'right', pady = 3, padx = 3 )

       #center the window
        self.warning_dialog_window.withdraw()
        self.warning_dialog_window.update()
        x = master.winfo_rootx()
        y = master.winfo_rooty()
        main_height =master.winfo_height()
        main_width = master.winfo_width()
        window_height = self.warning_dialog_window.winfo_reqheight()
        window_width = self.warning_dialog_window.winfo_reqwidth()
        geom = '+%d+%d' % ((x + main_width//2 - window_width//2), (y + main_height//2 - window_height//2))  
        self.warning_dialog_window.geometry(geom)
        self.warning_dialog_window.deiconify()

       #Prevent new task in taskbar
        self.warning_dialog_window.transient(master)  

      #Focus on the dialog box, freeze controll of main window
        self.warning_dialog_window.focus_force()
        while True:
            try:
                self.warning_dialog_window.grab_set()
                break
            except: continue

    def destroy(self):
        self.warning_dialog_window.destroy()   
      

class name_dialog:

    def __init__(self, master, Title, func_command, icon, message = 'Enter new name:'):
       #Create a new dialog box window
        self.name_dialog_window = Toplevel(master)

       #Make it non-resizeble, set title
        self.name_dialog_window.resizable(False, False)
        self.name_dialog_window.title(Title)

       #Create frames 
        self.icon_frame = ttk.Frame(self.name_dialog_window)
        self.icon_frame.pack(side = 'left', fill = Y)
        self.entry_frame = ttk.Frame(self.name_dialog_window)
        self.entry_frame.pack(side = 'left', fill = Y)

       #Create the label showing rename icon
        ttk.Label(self.icon_frame, image = icon).pack(padx = 3, pady = 3)

       #Create the label
        ttk.Label(self.entry_frame, text = message, anchor = 'w').pack(padx = 3, fill = X, expand = True)

       #Create the entry and set focus on entry
        self.rename_entry = ttk.Entry(self.entry_frame)
        self.rename_entry.pack(padx = 3, pady = 3, fill = X, expand = True)
        self.rename_entry.focus()

       #Create buttons
        self.cancel_ok_button = ttk.Button(self.entry_frame, text = 'Cancel', command = self.name_dialog_window.destroy)
        self.cancel_ok_button.pack(side = 'right', pady = 3, padx = 3 )
        self.rename_ok_button = ttk.Button(self.entry_frame, text = 'OK', command = func_command)
        self.rename_ok_button.pack(side = 'right', pady = 3, padx = 3 )

       #center the window
        self.name_dialog_window.withdraw()
        self.name_dialog_window.update()
        x = master.winfo_rootx()
        y = master.winfo_rooty()
        main_height =master.winfo_height()
        main_width = master.winfo_width()
        window_height = self.name_dialog_window.winfo_reqheight()
        window_width = self.name_dialog_window.winfo_reqwidth()
        geom = '+%d+%d' % ((x + main_width//2 - window_width//2), (y + main_height//2 - window_height//2))  
        self.name_dialog_window.geometry(geom)
        self.name_dialog_window.deiconify()

       #Bind events
        self.rename_entry.bind('<Return>', func_command)

       #Prevent new task in taskbar
        self.name_dialog_window.transient(master) 

       #Focus on the dialog box, freeze controll of main window
        self.name_dialog_window.focus_force()
        while True:
            try:
                self.name_dialog_window.grab_set()
                break
            except: continue 

    def destroy(self):
        self.name_dialog_window.destroy()     


class replace_dialog:

    def __init__(self, master, Title, icon, message):
       #Variable to tell which button has been pressed
        self.command = 0       
       
       #Create a new dialog box window
        self.replace_dialog_window = Toplevel(master)

       #Make it non-resizeble, set title
        self.replace_dialog_window.resizable(False, False)
        self.replace_dialog_window.title(Title)

       #Overide [x] button
        self.replace_dialog_window.protocol('WM_DELETE_WINDOW', self.skip)

       #Create frames 
        self.icon_frame = ttk.Frame(self.replace_dialog_window)
        self.icon_frame.pack(side = 'left', fill = Y)
        self.entry_frame = ttk.Frame(self.replace_dialog_window)
        self.entry_frame.pack(side = 'left', fill = Y)

       #Create the label showing icon
        ttk.Label(self.icon_frame, image = icon).pack(padx = 3, pady = 3)

       #Create the label
        ttk.Label(self.entry_frame, text = message, anchor = 'w').pack(padx = 3, fill = X, expand = True)

       #Create buttons
        self.skip_button = ttk.Button(self.entry_frame, text = 'Skip', command = self.skip)
        self.skip_button.pack(side = 'left', pady = 3, padx = 3 )
        self.replace_button = ttk.Button(self.entry_frame, text = 'Replace', command = self.replace)
        self.replace_button.pack(side = 'left', pady = 3, padx = 3 )
        self.skip_all_button = ttk.Button(self.entry_frame, text = 'Skip all', command = self.skip_all)
        self.skip_all_button.pack(side = 'left', pady = 3, padx = 3 )
        self.replace_all_button = ttk.Button(self.entry_frame, text = 'Replace all', command = self.replace_all)
        self.replace_all_button.pack(side = 'left', pady = 3, padx = 3 )

       #center the window
        self.replace_dialog_window.withdraw()
        self.replace_dialog_window.update()
        x = master.winfo_rootx()
        y = master.winfo_rooty()
        main_height =master.winfo_height()
        main_width = master.winfo_width()
        window_height = self.replace_dialog_window.winfo_reqheight()
        window_width = self.replace_dialog_window.winfo_reqwidth()
        geom = '+%d+%d' % ((x + main_width//2 - window_width//2), (y + main_height//2 - window_height//2))  
        self.replace_dialog_window.geometry(geom)
        self.replace_dialog_window.deiconify()

       #Prevent new task in taskbar
        self.replace_dialog_window.transient(master)  

       #Focus on the dialog box, freeze controll of main window
        self.replace_dialog_window.focus_force()
        while True:
            try:
                self.replace_dialog_window.grab_set()
                break
            except: continue

    def skip(self):
        self.command = 1
        self.replace_dialog_window.destroy()

    def replace(self):
        self.command = 2
        self.replace_dialog_window.destroy()

    def skip_all(self):
        self.command = 3
        self.replace_dialog_window.destroy()

    def replace_all(self):
        self.command = 4
        self.replace_dialog_window.destroy()

    def destroy(self):
        self.replace_dialog_window.destroy()


class file_properties_dialog:

    def __init__(self, master, Title, rename_command, chmod_command, icon, message):
       #Create a new dialog box window
        self.file_properties_dialog_window = Toplevel(master)

       #Make it non-resizeble, set title
        self.file_properties_dialog_window.resizable(False, False)
        self.file_properties_dialog_window.title(Title)

       #Create frames 
        self.icon_frame = ttk.Frame(self.file_properties_dialog_window)
        self.icon_frame.pack(side = 'left', fill = Y)
        self.entry_frame = ttk.Frame(self.file_properties_dialog_window)
        self.entry_frame.pack(side = 'left', fill = Y)

       #Create the label showing rename icon
        ttk.Label(self.icon_frame, image = icon).pack()

       #Create the label
        ttk.Label(self.entry_frame, text = message, anchor = 'w').pack(padx = 3, fill = X, expand = True)

       #Create buttons
        self.cancel_ok_button = ttk.Button(self.entry_frame, text = 'Close', command = self.file_properties_dialog_window.destroy)
        self.cancel_ok_button.pack(side = 'right', pady = 3, padx = 3 )
        self.chmod_ok_button = ttk.Button(self.entry_frame, text = 'Chmod', command = chmod_command)
        self.chmod_ok_button.pack(side = 'right', pady = 3, padx = 3 )
        self.rename_ok_button = ttk.Button(self.entry_frame, text = 'Rename', command = rename_command)
        self.rename_ok_button.pack(side = 'right', pady = 3, padx = 3 )

       #center the window
        self.file_properties_dialog_window.withdraw()
        self.file_properties_dialog_window.update()
        x = master.winfo_rootx()
        y = master.winfo_rooty()
        main_height =master.winfo_height()
        main_width = master.winfo_width()
        window_height = self.file_properties_dialog_window.winfo_reqheight()
        window_width = self.file_properties_dialog_window.winfo_reqwidth()
        geom = '+%d+%d' % ((x + main_width//2 - window_width//2), (y + main_height//2 - window_height//2))  
        self.file_properties_dialog_window.geometry(geom)
        self.file_properties_dialog_window.deiconify()

       #Prevent new task in taskbar
        self.file_properties_dialog_window.transient(master)  

       #Focus on the dialog box, freeze controll of main window
        self.file_properties_dialog_window.focus_force()
        while True:
            try:
                self.file_properties_dialog_window.grab_set()
                break
            except: continue

    def destroy(self):
        self.file_properties_dialog_window.destroy()   


class terminal_dialog:
    
    def __init__(self, master, icon, func_command, terminal_prompt_name, destroy_func = None):
       #Save reference to destroy function
        self.destroy_function = destroy_func

       #Save reference to terminal prompt name and command
        self.terminal_prompt_name = terminal_prompt_name
        self.func_command = func_command

       #Save reference to icon
        self.icon = icon

       #Create a new dialog box window
        self.terminal_dialog_window = Toplevel(master)

       #Make it non-resizeble, set title
        self.terminal_dialog_window.resizable(False, False)
        self.terminal_dialog_window.title('Terminal')
        self.terminal_dialog_window.minsize(width = 420, height = 300)
        #self.terminal_dialog_window.maxsize(width = 420, height = 300)

       #Overide [x] button
        self.terminal_dialog_window.protocol('WM_DELETE_WINDOW', self.destroy)

       #Prevent new task in taskbar
        self.terminal_dialog_window.transient(master) 

       #Create frames
        self.label_frame = ttk.Frame(self.terminal_dialog_window)
        self.label_frame.pack(fill = X)
        self.pad_pad_frame = ttk.Frame(self.terminal_dialog_window)
        self.pad_pad_frame.pack(fill = BOTH, expand = True)
        self.pad_frame = ttk.Frame(self.pad_pad_frame, relief = 'groove')
        self.pad_frame.pack(fill = BOTH, expand = True, pady = 3, padx = 5)
        self.text_frame = ttk.Frame(self.pad_frame)
        self.text_frame.pack(fill = BOTH, expand = True, pady = 1, padx = 1)
        self.button_frame = ttk.Frame(self.terminal_dialog_window)
        self.button_frame.pack(fill = X)

       #Create icon and label
        ttk.Label(self.label_frame, image = icon).pack(padx = 3, side = 'left')
        ttk.Label(self.label_frame, text = 'Enter commands:', anchor = 'w').pack(fill = X, side = 'left', pady = 3)

       #Create scrollbar 
        self.vbar = ttk.Scrollbar(self.text_frame, orient=VERTICAL)
        self.vbar.pack(side=RIGHT,fill=Y)

       #Create text widget
        self.terminal_text = Text(self.text_frame, width = 80, relief = 'flat', highlightthickness=0, background = 'white')
        self.terminal_text.pack(fill = BOTH)
        self.vbar.config(command = self.terminal_text.yview, style = 'Whitehide.TScrollbar')
        self.terminal_text['yscrollcommand'] = self.vbar.set
        self.terminal_text.insert('end',terminal_prompt_name+'>')

       #Create close button
        self.close_button = ttk.Button(self.button_frame, text = 'Close', command = self.destroy)
        self.close_button.pack(side = 'right', pady = 3, padx = 3 )

       #Center the window
        self.terminal_dialog_window.withdraw()
        self.terminal_dialog_window.update()
        x = master.winfo_rootx()
        y = master.winfo_rooty()
        main_height =master.winfo_height()
        main_width = master.winfo_width()
        window_height = self.terminal_dialog_window.winfo_reqheight()
        window_width = self.terminal_dialog_window.winfo_reqwidth()
        geom = '+%d+%d' % ((x + main_width//2 - window_width//2), (y + main_height//2 - window_height//2 - 20))  
        self.terminal_dialog_window.geometry(geom)
        self.terminal_dialog_window.deiconify()
        
       #Bind events
        self.terminal_text.bind('<Return>', self.print_command)

       #Focus on the dialog box, freeze controll of main window
        self.terminal_dialog_window.focus_force()
        while True:
            try:
                self.terminal_dialog_window.grab_set()
                break
            except: continue

    def print_command(self, event):
        command = self.terminal_text.get('end-1c linestart+'+str(len(self.terminal_prompt_name)+1)+'c', 'end')
        command = command[:-1]
        self.func_command(command)
        self.terminal_text.insert('end','\n'+self.terminal_prompt_name+'>')
        self.terminal_text.see('end')
        if(int(self.terminal_text.index('end').split('.')[0]) is 26):
            self.vbar.config(style = 'TScrollbar')
        return 'break'

    def insert(self, line):
        self.terminal_text.insert('end',line)
        self.terminal_text.see('end')
        if(int(self.terminal_text.index('end').split('.')[0]) is 26):
            self.vbar.config(style = 'TScrollbar')

    def enable_close_button(self):
        self.closable = True
        self.close_button.config(state = NORMAL)

    def destroy(self):
        if(self.destroy_function is not None):
            self.destroy_function()
        self.terminal_dialog_window.destroy()


class console_dialog:

    def __init__(self, master, icon, destroy_func):                
       #Save reference to destroy function
        self.destroy_function = destroy_func

       #Save reference to icon
        self.icon = icon

       #Create a new dialog box window
        self.console_dialog_window = Toplevel(master)
       #Make it non-resizeble, set title
        self.console_dialog_window.resizable(False, False)
        self.console_dialog_window.title('Terminal')
        self.console_dialog_window.minsize(width = 420, height = 300)
        #self.console_dialog_window.maxsize(width = 420, height = 300)

       #Overide [x] button
        self.console_dialog_window.protocol('WM_DELETE_WINDOW', self.close_message)

       #Prevent new task in taskbar
        self.console_dialog_window.transient(master) 

       #Create frames
        self.label_frame = ttk.Frame(self.console_dialog_window)
        self.label_frame.pack(fill = X)
        self.pad_pad_frame = ttk.Frame(self.console_dialog_window)
        self.pad_pad_frame.pack(fill = BOTH, expand = True)
        self.pad_frame = ttk.Frame(self.pad_pad_frame, relief = 'groove')
        self.pad_frame.pack(fill = BOTH, expand = True, pady = 3, padx = 5)
        self.text_frame = ttk.Frame(self.pad_frame)
        self.text_frame.pack(fill = BOTH, expand = True, pady = 1, padx = 1)
        self.button_frame = ttk.Frame(self.console_dialog_window)
        self.button_frame.pack(fill = X)

       #Create icon and label
        ttk.Label(self.label_frame, image = icon).pack(padx = 3, side = 'left')
        ttk.Label(self.label_frame, text = 'Performing tasks....', anchor = 'w').pack(fill = X, side = 'left', pady = 3)

       #Create scrollbar
        self.vbar = ttk.Scrollbar(self.text_frame, orient=VERTICAL)
        self.vbar.pack(side=RIGHT,fill=Y)

       #Create text widget
        self.console_text = Text(self.text_frame, width = 80, relief = 'flat', highlightthickness=0, background = 'white')
        self.console_text.pack(fill = BOTH)
        self.vbar.config(command = self.console_text.yview, style = 'Whitehide.TScrollbar')
        self.console_text['yscrollcommand'] = self.vbar.set

       #Fix the mouse bug
        self.console_text.bind('<Button-1>', lambda e: 'break')
        self.console_text.bind('<Double-Button-1>' , lambda e: 'break')     
        self.console_text.bind('<Control-Button-1>', lambda e: 'break')
        self.console_text.bind('<B1-Motion>', lambda e: 'break')

       #Create close button
        self.close_button = ttk.Button(self.button_frame, text = 'Close', command = self.destroy, state = DISABLED)
        self.close_button.pack(side = 'right', pady = 3, padx = 3 )

       #Center the window
        self.console_dialog_window.withdraw()
        self.console_dialog_window.update()
        x = master.winfo_rootx()
        y = master.winfo_rooty()
        main_height =master.winfo_height()
        main_width = master.winfo_width()
        window_height = self.console_dialog_window.winfo_reqheight()
        window_width = self.console_dialog_window.winfo_reqwidth()
        geom = '+%d+%d' % ((x + main_width//2 - window_width//2), (y + main_height//2 - window_height//2 - 20))  
        self.console_dialog_window.geometry(geom)
        self.console_dialog_window.deiconify()

       #Focus on the dialog box, freeze controll of main window
        self.console_dialog_window.focus_force()
        while True:
            try:
                self.console_dialog_window.grab_set()
                break
            except: continue

    def insert(self, line):
        self.console_text.insert('end',line+'\n')
        self.console_text.see('end')
        if(int(self.console_text.index('end').split('.')[0]) is 26):
            self.vbar.config(style = 'TScrollbar')

    def progress(self, percentage):
        self.console_text.delete('insert linestart', 'insert lineend')
        self.console_text.insert('end', percentage)
        if(int(self.console_text.index('end').split('.')[0]) is 26):
            self.vbar.config(style = 'TScrollbar')

    def close_message(self):
        if(self.closable is True):
            self.destroy()

    def enable_close_button(self):
        self.closable = True
        self.close_button.config(state = NORMAL)

    def destroy(self):
        self.destroy_function()
        self.console_dialog_window.destroy()


class open_file_dialog:

    def __init__(self, master, Title, func_command, directory_mode = False):
       #/!\ Although the comments and variable names say 'file_list', or 'items' it inculdes folders also

       #Cell width of each cell
        self.cell_width = 190

       #Variable to hold the max no character name in file list (used for padding in GUIs)
        self.max_len = 0

       #List to store all file names that are currently being displayed and theit details
        self.file_list = []
       #An index that points to current file that the mouse is pointing
        self.current_file_index = 0

       #Variables for drawing and storing cursor position
        self.mouse_x = 0
        self.mouse_y = 0
        self.max_width = 0

       #Variable to store which cell cursor is currently pointeing
        self.x_cell_pos = 0
        self.y_cell_pos = 0

       #A dictionary to store indices and highlight rectangle references of selected files
        self.selected_file_indices = {}

       #Variable to store start cell position of drag select
        self.start_x = 0
        self.start_y = 0

       #Variable to tell weather directory mode or not
        self.directory_mode = False

       #Variable to tell weather hidden files are enabled
        self.hidden_files = False        

       #Variable to hold the file name with max characters
        self.max_len_name = ''

       #Variable for holding the font
        self.default_font = font.nametofont("TkDefaultFont")

        self.directory_mode = directory_mode
       #Change to script's directory
        abspath = os.path.abspath(__file__)
        dname = os.path.dirname(abspath)
        os.chdir(dname)

       #Load all icons
        self.folder_icon = PhotoImage(file='Icons/folder_big.png')
        self.textfile_icon = PhotoImage(file='Icons/textfile_big.png')
        self.up_icon = PhotoImage(file='Icons/up_small.png')
        self.dnd_glow_icon = PhotoImage(file='Icons_glow/gotopath_large_glow.png')

       #Create a new dialog box window and set minimum size
        self.open_file_dialog_window = Toplevel(master)
        self.open_file_dialog_window.title(Title)
        self.open_file_dialog_window.minsize(width = 640, height = 480)

       #Change to home directory
        if(platform.system() == 'Linux' or platform.system() == 'FreeBSD'):
            home = expanduser('~')
            os.chdir(os.getenv('HOME'))
            self.update_file_list()
        elif(platform.system() == 'Windows'):
            home = expanduser('~')
            os.chdir(home)
            self.update_file_list()

       #center the window
        x = master.winfo_rootx()
        y = master.winfo_rooty()
        main_height = master.winfo_height()
        main_width = master.winfo_width()
        geom = '+%d+%d' % (x+(main_width/2) - 320,y+(main_height/2) - 260)  
        self.open_file_dialog_window.geometry(geom)

       #Prevent new task in taskbar
        self.open_file_dialog_window.transient(master)

       #Create a new frame for text showing dirctory
        self.directory_frame = ttk.Frame(self.open_file_dialog_window)
        self.directory_frame.pack(fill = BOTH)

       #Create a label
        ttk.Label(self.directory_frame, text = 'Directory:').pack(side = 'left') 

       #Create a text bar for dirctory
        self.directory_text = ttk.Combobox(self.directory_frame)
        self.directory_text.pack(fill = X, expand = True, side = 'left')
        self.directory_text.insert(END, os.getcwd()) 
        
       #Add all partitions to the list
        if(platform.system() == 'Linux' or platform.system() == 'FreeBSD'):
            common_file_list = []
            for home_folders in ['', 'Desktop', 'Documents', 'Downloads', 'Music', 'Pictures', 'Videos']:
                common_file_list.append(os.getcwd()+'/'+home_folders)
            for drive in psutil.disk_partitions():
                common_file_list.append(drive.mountpoint)
            self.directory_text['values'] = common_file_list
        elif(platform.system() == 'Windows'):
            common_file_list = []
            for home_folders in ['', 'Desktop', 'Documents', 'Downloads', 'Music', 'Pictures', 'Videos']:
                common_file_list.append(os.getcwd()+'\\'+home_folders)
           #See SO link: https://stackoverflow.com/questions/827371/is-there-a-way-to-list-all-the-available-drive-letters-in-python
            drives = win32api.GetLogicalDriveStrings()
            drives = drives.split('\000')[:-1]
            for drive in drives:
                common_file_list.append(drive)
            self.directory_text['values'] = common_file_list

       #Create up button
        self.up_button = ttk.Button(self.directory_frame, image = self.up_icon, command = self.dir_up)
        self.up_button.pack(side = 'right', padx = 3, pady = 3)

       #Create frame for canvas and scrollbar
        self.pad_frame = ttk.Frame(self.open_file_dialog_window)
        self.pad_frame.pack(fill = BOTH, expand = True)
        self.canvas_frame = ttk.Frame(self.pad_frame, relief = 'groove', border = 1)
        self.canvas_frame.pack(fill = BOTH, expand = True, padx = 5, pady = 3)

       #Create scrollbar
        self.vbar = ttk.Scrollbar(self.canvas_frame, orient=VERTICAL)
        self.vbar.pack(side=RIGHT,fill=Y)

       #Create frame for buttons
        self.button_frame = ttk.Frame(self.open_file_dialog_window)
        self.button_frame.pack(fill = X)

       #Create buttons
        self.cancel_ok_button = ttk.Button(self.button_frame, text = 'Cancel', command = self.open_file_dialog_window.destroy)
        self.cancel_ok_button.pack(side = 'right', pady = 3, padx = 3 )
        self.rename_ok_button = ttk.Button(self.button_frame, text = 'OK', command = func_command)
        self.rename_ok_button.pack(side = 'right', pady = 3, padx = 3 )

       #Bind keyboard shortcuts
        self.open_file_dialog_window.bind('<Control-h>', self.toggle_hidden_files)
        self.open_file_dialog_window.bind('<Control-H>', self.toggle_hidden_files)

       #Create a canvas
        self.canvas = Canvas(self.canvas_frame, bg = 'white', bd=0, highlightthickness=0, relief='ridge')
        self.canvas.pack(fill = BOTH, expand = True)
        self.vbar.config(command = self.canvas.yview)
        self.canvas['yscrollcommand'] = self.vbar.set

       #Bind events, this part of code also tells what some of the functions do
        self.canvas.bind('<Button-4>', self.on_mouse_wheel)
        self.canvas.bind('<Button-5>', self.on_mouse_wheel)     
        self.canvas.bind('<MouseWheel>', self.on_mouse_wheel)
        self.canvas.bind('<Configure>', self.draw_icons)
        self.canvas.bind('<Motion>', self.update_status_and_mouse)
        self.canvas.bind('<Button-1>', self.mouse_select)
        self.canvas.bind('<Control-Button-1>', self.ctrl_select)
        self.canvas.bind('<Double-Button-1>' , self.change_dir) 
        self.canvas.bind('<B1-Motion>', self.drag_select)
        self.directory_frame.bind('<Motion>', self.stop_highlight)
        self.directory_text.bind('<Return>', self.change_dir_on_enter)
        self.directory_text.bind('<<ComboboxSelected>>', self.change_dir_on_enter)
        self.vbar.bind('<Motion>', self.stop_highlight) 
        self.button_frame.bind('<Motion>', self.stop_highlight)

       #Code for handling file/folder drag and drop, uses TkDND_wrapper.py
       #See link: https://mail.python.org/pipermail/tkinter-discuss/2005-July/000476.html
        if(directory_mode is True):
            self.dnd = TkDND(master)
            self.dnd.bindtarget(self.canvas_frame, 'text/uri-list', '<Drop>', self.handle_dnd, ('%A', '%a', '%T', '%W', '%X', '%Y', '%x', '%y','%D'))
            self.dnd.bindtarget(self.canvas_frame, 'text/uri-list', '<DragEnter>', self.show_dnd_icon, ('%A', '%a', '%T', '%W', '%X', '%Y', '%x', '%y','%D'))
            self.dnd.bindtarget(self.canvas_frame, 'text/uri-list', '<DragLeave>', lambda action, actions, type, win, X, Y, x, y, data:self.draw_icons(), ('%A', '%a', '%T', '%W', '%X', '%Y', '%x', '%y','%D'))

       #Focus on the dialog box, freeze controll of main window
        self.open_file_dialog_window.focus_force()
        while True:
            try:
                self.open_file_dialog_window.grab_set()
                break
            except: continue

    def folder_is_hidden(self, p):
       #See SO question: https://stackoverflow.com/questions/7099290/how-to-ignore-hidden-files-using-os-listdir
        if platform.system() is 'Windows':
            attribute = win32api.GetFileAttributes(p)
            return attribute & (win32con.FILE_ATTRIBUTE_HIDDEN | win32con.FILE_ATTRIBUTE_SYSTEM)
        else:
            return p.startswith('.') 

    def update_file_list(self):
        self.max_len = 0
        self.max_len_name = ''
        del self.file_list[:]
        for file in os.listdir():
            if(self.hidden_files is True or not self.folder_is_hidden(file)):
                self.file_list.append(file)
                if(len(file) > self.max_len):
                    self.max_len = len(file)
                    self.max_len_name = file

    def handle_dnd(self, action, actions, type, win, X, Y, x, y, data):
       #Deselect everything
        self.deselect_everything()
       #Get path from text field
        dir_path = self.dnd.parse_uri_list(data)[0]
       #Chack validity and change directory
        if os.path.isdir(dir_path): os.chdir(dir_path)
       #Change directory text
        self.directory_text.delete(0, 'end')
        self.directory_text.insert(END, os.getcwd()) 
       #Update file list and redraw icons
        self.update_file_list()
        self.draw_icons()        

    def show_dnd_icon(self, action, actions, type, win, X, Y, x, y, data):
        self.deselect_everything()
        self.canvas.delete("all")
        self.canvas.create_image(self.canvas_width/2, self.canvas_height/2, image = self.dnd_glow_icon)        

    def draw_icons(self, event = None):    
       #Calculate cell width
        #self.cell_width = 55 + self.max_len*12
        self.cell_width = 70 + self.default_font.measure(self.max_len_name)
        self.canvas_width = self.canvas.winfo_width() - 4
        self.canvas_height = self.canvas.winfo_height()
        if(self.cell_width > self.canvas_width):
            self.cell_width = self.canvas_width
       #Clear canvas
        self.canvas.delete('all')
        y = 0
        x = 0
       #Create a rectangle for upsate_status_mouse(self, event) function
        self.rect_id = self.canvas.create_rectangle(-1, -1, -1, -1, fill = '', outline = '')
       #Draw icons
        for file_name in self.file_list:
            if((x+1)*self.cell_width > self.canvas_width):
                y+=1
                x=0
           #Check types, draw appropriate icon
            if(not isfile(file_name)):
                self.canvas.create_image(25+(x*self.cell_width), 18+(y*35), image = self.folder_icon)
                canvas_id = self.canvas.create_text(45+(x*self.cell_width), 13+(y*35), anchor='nw')
                self.canvas.itemconfig(canvas_id, text= file_name)  
                x+=1
            else:
                self.canvas.create_image(25+(x*self.cell_width), 18+(y*35), image = self.textfile_icon)
                canvas_id = self.canvas.create_text(45+(x*self.cell_width), 13+(y*35), anchor='nw')
                self.canvas.itemconfig(canvas_id, text= file_name)  
                x+=1
       #Calculate scroll region
        if (y+1)*35 < self.canvas_height:
            scroll_region_y = self.canvas_height - 1
            self.vbar.configure(style = 'Whitehide.TScrollbar')
        else:
            scroll_region_y = ((y+1)*35)+13
            self.vbar.configure(style = 'TScrollbar')
        self.canvas.configure(scrollregion = '-1 -1 ' + str(self.canvas_width) + ' ' + str(scroll_region_y))
       #Redraw all selected-highlight rectangles
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
       #Use index = (y*width)+x to figure out the file index from canvas and mouse position
        self.x_cell_pos = int(self.mouse_x/self.cell_width)
        self.y_cell_pos = int(self.mouse_y/35)
        #Round canvas's width to nearest multiple of self.cell_width, width of each cell
        self.max_width = self.canvas_width - (self.canvas_width % self.cell_width)
        self.current_file_index = int(((self.max_width/self.cell_width)*self.y_cell_pos) + self.x_cell_pos)
       #Set status only if valid index, draw mouse-hover highlight rectangle
        if(self.current_file_index >= 0 and self.current_file_index < len(self.file_list) and self.mouse_x < self.max_width):
           #Configure the rectangle created in draw_icons() to highlight the current folder
            self.canvas.itemconfig(self.rect_id, outline = 'black')
            self.canvas.coords(self.rect_id, self.x_cell_pos*self.cell_width+2, self.y_cell_pos*35+2, (self.x_cell_pos+1)*self.cell_width-1, (self.y_cell_pos+1)*35-1) 
        else:
          #Stop mouse-hover highlighting
            self.canvas.itemconfig(self.rect_id, outline = '')
            self.canvas.coords(self.rect_id, -1, -1, -1, -1)  

    def stop_highlight(self, event):
       #Stop mouse-hover highlighting
        self.canvas.itemconfig(self.rect_id, outline = '')
        self.canvas.coords(self.rect_id, -1, -1, -1, -1)         

    def toggle_hidden_files(self, event):
        self.hidden_files = not self.hidden_files
        self.update_file_list()
        self.deselect_everything()

    def on_mouse_wheel(self, event):
        def delta(event):
            if event.num == 5 or event.delta < 0:
                return 1 
            return -1 

        self.canvas.yview_scroll(delta(event), 'units')
        
    def mouse_select(self, event):
       #Check for directory mode
        if(self.directory_mode is True): return
       #Store start position for drag select
        self.start_x = self.x_cell_pos
        self.start_y = self.y_cell_pos
       #Deselect everything
        self.deselect_everything()  
       #Set selected only if valid index
        if(self.current_file_index >= 0 and self.current_file_index < len(self.file_list) and self.mouse_x < self.max_width):   
           #Draw a 'selected' highlighting rectangle and save a reference to the rectangle in selected file dictionary
            self.selected_file_indices[self.current_file_index] = self.canvas.create_rectangle(self.x_cell_pos*self.cell_width+2, self.y_cell_pos*35+2,
                                                                                               (self.x_cell_pos+1)*self.cell_width-1, (self.y_cell_pos+1)*35-1,
                                                                                               fill = '', outline = 'Red')

    def ctrl_select(self, event):
       #Check for directory mode
        if(self.directory_mode is True): return
       #Set selected only if valid index
        if(self.current_file_index >= 0 and self.current_file_index < len(self.file_list) and self.mouse_x < self.max_width): 
          #If WAS NOT selected already
            if(self.current_file_index not in self.selected_file_indices):
               #Draw a 'selected' highlighting rectangle and save a reference to the rectangle in selected file dictionary
                self.selected_file_indices[self.current_file_index] = self.canvas.create_rectangle(self.x_cell_pos*self.cell_width+2, self.y_cell_pos*35+2,
                                                                                                   (self.x_cell_pos+1)*self.cell_width-1, (self.y_cell_pos+1)*35-1,
                                                                                                    fill = '', outline = 'Red')
          #If WAS selected already
            else:
               #Remove from selected file list
                del self.selected_file_indices[self.current_file_index]  
               #Redraw icons
                self.draw_icons()

    def drag_select(self, event):
       #Check for directory mode
        if(self.directory_mode is True): return
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
                    self.selected_file_indices[file_index] = self.canvas.create_rectangle(i*self.cell_width+2, j*35+2, (i+1)*self.cell_width-1, (j+1)*35-1, fill = '', outline = 'Red')

    def deselect_everything(self):
           #Delete selected file list
            self.selected_file_indices.clear()
           #Redraw all icons and remove any 'selected' highlighting rectangles
            self.draw_icons()

    def change_dir(self, event):
       #Delete selected file list
        self.selected_file_indices.clear()
       #Check for valid index
        if(self.current_file_index >= 0 and self.current_file_index < len(self.file_list) and self.mouse_x < self.max_width):
            if(not isfile(self.file_list[self.current_file_index])):
               #Change directory and update file list
                os.chdir(self.file_list[self.current_file_index])
                self.update_file_list()        
               #Redraw all icons        
                self.draw_icons()
               #Change directory text
                self.directory_text.delete(0, 'end')
                self.directory_text.insert(END, os.getcwd()) 

    def dir_up(self):   
       #Deselect everythin
        self.deselect_everything()
       #Change directory and update file list
        os.chdir('..')
        self.update_file_list()
       #Change directory text
        self.directory_text.delete(0, 'end')
        self.directory_text.insert(END, os.getcwd()) 
       #Redraw all icons        
        self.draw_icons()    

    def change_dir_on_enter(self, event):
       #Deselect everything
        self.deselect_everything()
       #Get path from text field
        dir_path = self.directory_text.get()
       #Chack validity and change directory
        if os.path.isdir(dir_path): os.chdir(dir_path)
       #Update file list and redraw icons
        self.update_file_list()
        self.draw_icons()

    def destroy(self):
        self.open_file_dialog_window.destroy()
