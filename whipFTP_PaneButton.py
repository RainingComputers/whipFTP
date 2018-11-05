#Custom button class for whipFTP, Copyrights Vishnu Shankar B,

from tkinter import *
from tkinter import ttk
from tkinter import PhotoImage

class Button(ttk.Label):
    def __init__(self, parent, name, icon, path, command):
        #Save reference to path and function
        self.path = path
        self.path_function = command
        #Create the label
        super().__init__(parent, text = name, image = icon, compound = 'left')
        super().pack(side = 'top', pady = 3, padx = 3, fill = X)
        #Bind events
        super().bind('<Button-1>', lambda path: self.path_function(self.path))
        super().bind('<Enter>', self.hover)
        super().bind('<Leave>', self.leave)

    def hover(self, event):
        super().configure(background = '#cfd6e6')
    
    def leave(self, event):
        super().configure(background = '#f5f6f7')