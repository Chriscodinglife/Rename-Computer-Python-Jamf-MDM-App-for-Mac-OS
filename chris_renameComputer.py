#!/usr/bin/python

"""
Christian Orellana
Rename Computer Python Script

"""

import AppKit
import sys
import os
import Tkinter
import tkFont
import tkMessageBox
import subprocess
import plistlib

# Path to Jamf binary
JAMF = "/usr/local/bin/jamf"
# Path to scutil
scutil = "/usr/sbin/scutil"
# base64-encoded GIF for "icon" at the top of the GUI
# MUST BE A GIF!
icon = '''
<insert Base64 Image data here>
'''

class App:
    def __init__(self, master):
        """Main GUI window"""
        self.master = master
        self.master.resizable(False, False)
        self.master.title("Rename Computer")

        self.master.protocol("WM_DELETE_WINDOW", self.cancel)
        self.master.call('wm', 'attributes', '.', '-topmost', True)
        x = (self.master.winfo_screenwidth() - self.master.winfo_reqwidth()) / 2
        y = (self.master.winfo_screenheight() - self.master.winfo_reqheight()) / 3
        self.master.geometry("+{0}+{1}".format(x, y))
        # w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        # self.master.overrideredirect(1)
        # self.master.geometry("%dx%d+0+0" % (w, h))

        bgcolor = '#F0F0F0'
        self.master.tk_setPalette(background=bgcolor,
                                  highlightbackground=bgcolor)

        font = tkFont.nametofont('TkDefaultFont')
        font.config(family='system',
                    size=14)
        self.master.option_add("*Font", font)

        menu_bar = Tkinter.Menu(self.master)
        self.master.config(menu=menu_bar)

        print('Starting app')

        # Input variables
        self.input_computer_name = Tkinter.StringVar()
   
        # Get icon
        self.icon_data = Tkinter.PhotoImage(data=mbp_icon)

        # Icon Frame
        self.frame1 = Tkinter.Frame(self.master)
        self.photo_canvas = Tkinter.Canvas(self.frame1, width=250, height=150)
        self.photo_canvas.pack()
        self.icon = self.photo_canvas.create_image(0, 0, anchor="nw", image=self.icon_data)
        self.frame1.pack(padx=40, pady=(30, 5))

        # Title Frame
        self.frame2 = Tkinter.Frame(self.master)
        title_label = Tkinter.Label(self.frame2, text="Rename Computer")
        title_label.grid(row=0, column=0)
        self.frame2.pack(padx=40, pady=(10,5))

        # Inputs frame
        self.frame3 = Tkinter.Frame(self.master)

        user_label = Tkinter.Label(self.frame3, text="Set Computer Name Here:")
        user_label.pack()
        self.entry_computer_name = Tkinter.Entry(self.frame3,
                                                 background='white',
                                                 textvariable=self.input_computer_name,
                                                 width=30)
        self.entry_computer_name.pack(pady=(0, 20))

        self.frame3.pack(padx=40, pady=5)

        # Buttons
        self.frame5 = Tkinter.Frame(self.master)
        submit = Tkinter.Button(self.frame5, text='Rename', height=1, width=8, default='active', command=self.submit)
        submit.pack(side='right')
        cancel = Tkinter.Button(self.frame5, text='Cancel', height=1, width=8, command=self.cancel)
        cancel.pack(side='right')
        self.frame5.pack(padx=40, pady=(5, 30))

        # Add GUI padding

    def cancel(self):
        """Exit the GUI"""
        print('User has closed the app')
        self.master.destroy()

    def submit(self):

        i_computer = ''.join(self.input_computer_name.get().split())
        newName = "{}".format(i_computer)
        print "newName: {}".format(newName)

        # Rename the Hostname
        cmd = [scutil, '--set', 'HostName', newName]
        rename = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)
        (out, err) = rename.communicate()

        if rename.returncode == 0:
            print "Set hostname to {}".format(newName)
        else:
            print "Rename failed!"
            sys.exit(1)

        # Rename the LocalHostname
        cmd = [scutil, '--set', 'LocalHostName', newName]
        rename = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)
        (out, err) = rename.communicate()

        if rename.returncode == 0:
            print "Set localHostName to {}".format(newName)
        else:
            print "Rename failed!"
            sys.exit(1)

        # Rename the ComputerName
        cmd = [scutil, '--set', 'ComputerName', newName]
        rename = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)
        (out, err) = rename.communicate()

        if rename.returncode == 0:
            print "Set Computer Name to {}".format(newName)
        else:
            print "Rename failed!"
            sys.exit(1)

        # Submit new inventory
        cmd = [JAMF, 'recon']
        inventory = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)
        (out, err) = inventory.communicate()
        if inventory.returncode == 0:
            print "Submitted inventory to JSS"
        else:
            print "Inventory update failed!"
            sys.exit(1)
        print('Computer Name has been renamed')

        self.master.destroy()


def main():
    # Prevent the Python app icon from appearing in the Dock
    info = AppKit.NSBundle.mainBundle().infoDictionary()
    info['CFBundleIconFile'] = u'PythonApplet.icns'
    info['LSUIElement'] = True

    root = Tkinter.Tk()
    app = App(root)
    # Have the GUI appear on top of all other windows
    AppKit.NSApplication.sharedApplication().activateIgnoringOtherApps_(True)
    rdata = app.master.mainloop()

    sys.exit(0)

if __name__ == '__main__':
    main()