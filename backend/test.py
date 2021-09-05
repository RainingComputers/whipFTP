from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import PhotoImage
from ftplib import FTP
import ftplib
import os
import shutil
import re
from hashlib import sha256
import webbrowser
# ----------------Set Font------------------
Label_font = ("IRANSans", 15, "normal")
entry_font = ("IRANSans", 10, "normal")
# # -----------------Functions-------------------
# def web_info_buy(url):
#     webbrowser.open_new(url)
# # local_hash
# uuidsys = os.popen('wmic path win32_computersystemproduct get uuid')
# uuidst = uuidsys.read()
# uuid_local_sys = re.sub("UUID", '', re.sub('\s', '', uuidst))
# uuid_salt = f"{uuid_local_sys}-is_for_4rT4_lic#"
# s256 = sha256()
# s256.update(uuid_salt.encode())
# hash_local = s256.hexdigest()
# def delall():
#     pass
#
# def search_hash(hash_sys, line_searche) :
#     check = re.search(hash_sys, line_searche)
#     if check == hash_sys :
#         messagebox.showerror("Error", "You was Setup Software")
#         delall()
#     else :
#         messagebox.askyesnocancel("Change SYS","You can not back up 2 systems on one host.\nYou have already registered a system in -Backupvip-. Do you want to replace this system or keep the backup work on the previous system?\n\nClick For more for more information and to buy a host")
#
# def ftp_work():
#     ftp = FTP()
#     ftp.connect('backupvip.com', 21)
#     ftp.login('checker@backupvip.com', 'B@ck!@#$987')
#     fileuuid = 'Lic.txt'
#     ftp.retrbinary('RETR Lic.txt', open(fileuuid, 'wb').write)
#     with open('Lic.txt', 'a+') as lic:
#         for line in lic.read:
#             match = re.search(f'\A{username_ftp}', line)
#             if match:
#                 re.sub(username_ftp, '', line)
#                 re.sub("-", '', line)
#                 if line == '':
#                     lic.write(hash_local)
#                 elif search_hash(hash_local, line):
#                     pass
#
#
#
#
#
# def CheckFTP():
#     if username_ftp == "" or pass_ftp == "":
#         messagebox.showerror("Error", "You should to Write Your Username and Password")
#     else:
#         try:
#             ftp = FTP()
#             ftp.connect('194.9.80.139', 21)
#             ftp.login(username_ftp, pass_ftp)
#             files = []
#             try:
#                 files = ftp.nlst()
#             except ftplib.error_perm as resp:
#                 if str(resp) == "550 No files found":
#                     messagebox.showinfo("Ok", "You Connected")
#                     with open("U&PF.txt", 'w') as wup:
#                         wup.write(f"{username_ftp}\n{pass_ftp}")
#                     ftp_work()
#                     delall()
#             else:
#                 messagebox.showinfo("Ok", "You Connected")
#                 with open('U&PF.txt', 'w') as wup:
#                     wup.write(f"{username_ftp}\n{pass_ftp}")
#                 ftp_work()
#                 delall()
#         except ftplib.error_perm as lf:
#             if str(lf) == "530 Login authentication failed":
#                 messagebox.showerror("Connect Failed", "Your Username or Password is incorrect")
#
#
#
# ----------------create TK ----------------
Ftp_Ge = Tk()
Ftp_Ge.wm_title('FTP Information')
Ftp_Ge.minsize(width = 480, height = 100)
Ftp_Ge.config(bg = 'white')
# ----------------Frames---------------------
# pad_frame = ttk.Frame(Ftp_Ge)
# pad_frame.pack(fill=BOTH, expand=True)
canvas = Frame(Ftp_Ge, bg = 'white')
canvas.pack(fill = X)
canvas_frame = Frame(Ftp_Ge, bg = 'white')
canvas_frame.pack(fill = X, padx = 5, pady = 3)
canvas_frame_Bo = Frame(Ftp_Ge, bg = 'white')
canvas_frame_Bo.pack(fill = X, padx = 5, pady = 3)
# ----------------import Image------------------
Arta_Im = PhotoImage(file='Arta_Im.png')
Connect_Im = PhotoImage(file='Connect_Im.png')
# Ftp_Ge.iconphoto(True, Arta_Im)
# # -----------------Labels & Buttons ------------
# Ftp_Ge.wm_resizable(width=False, height=False)
# label_usrname = ttk.Label(canvas, text = 'FTP Username:', font = Label_font)
# label_usrname.configure(background = 'white')
# label_usrname.pack(side = 'left', padx = 20)
# ftp_usrname_entry = ttk.Entry(canvas, font = entry_font)
# ftp_usrname_entry.pack(side = 'left', expand = True, fill = X)
# label_Null_User =Label(canvas, text = '.', bg = 'white', fg = 'white')
# label_Null_User.pack(side = 'left', padx = 40)
# label_pass = ttk.Label(canvas_frame, text = 'FTP Password:', font = Label_font)
# label_pass.configure(background = 'white')
# label_pass.pack(side = 'left', padx = 20)
# ftp_pass_entry = ttk.Entry(canvas_frame, show='*', font = entry_font)
# ftp_pass_entry.pack(side = 'left', expand = True, fill = X)
# label_Null_Pass =Label(canvas_frame, text = '.', bg = 'white', fg = 'white')
# label_Null_Pass.pack(side = 'left', padx = 40)
# username_ftp = ftp_usrname_entry.get()
# pass_ftp = ftp_pass_entry.get()
# callButton = Button(canvas_frame_Bo, text = "Check", command = CheckFTP, image = Connect_Im)
# callButton.pack(side = 'left', padx = 150)
#
#
#
#

def messageWindow():
    win = Toplevel()
    win.title('warning')
    win.minsize(width=40, height=20)
    win.configure(bg='white')
    win.iconphoto(True, Arta_Im)
    message = "You Can't Backup 2 Systems on one Host."
    message2 = "You have already registered a system in BACKUPVIP.\n Do you want to replace this system or keep the backup work on the previous system?\n\nClick on MORE INFORMATION to more information and to buy a host"
    Label(win, text=message, font = ("IRANSans", 11,'bold'), bg= 'white').pack(padx = 5)
    Label(win, text=message2, font = ("IRANSans", 11,'normal'), bg= 'white').pack(padx = 5)
    Button(win, text='Keep on Previous System', command=win.destroy).pack()
    Button(win, text='Keep on Previous System', command=win.destroy).pack()
Button(canvas, text='Bring up Message', command=messageWindow).pack()

Ftp_Ge.mainloop()