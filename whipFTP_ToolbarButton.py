#Custom button class for whipFTP, Copyrights Vishnu Shankar B,

from tkinter import *
from tkinter import ttk
from tkinter import PhotoImage

#Custum button class that uses the 'Label' widget
class Button(ttk.Label):

    def __init__(self, parent, image, image_hover, command):
       #Save reference to icon
        self.icon = image
        self.hover_icon = image_hover
       #save reference to the function
        self.command = command
       #Create the label
        super().__init__(parent, image = self.icon)
       #Bind events
        super().bind('<Enter>', self.hover)
        super().bind('<Leave>', self.left)
        super().bind('<Button-1>', self.click)

    def click(self, event):
        super().configure(image = self.icon)
        if self.command is not None: self.command()
        super().configure(image = self.hover_icon)

    def hover(self, event):
        super().configure(image = self.hover_icon)

    def left(self, event):
        super().configure(image = self.icon)