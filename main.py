#import os
from distutils.dir_util import copy_tree
from datetime import datetime
import schedule
import time
import _thread
import sys
import os
import tkinter as tk
    

TARGET = r'D:\\SteamLibrary\\steamapps\\common\\State of Decay YOSE\\USER\\76561198828850182'
BACKUP  = r'C:\\Users\\artemis\\Documents\\sod'

def get_timestamp():
    return datetime.timestamp(datetime.now())

def copy_files():
    print("backup taken at " + str(datetime.fromtimestamp(get_timestamp())) + "\n")
    copy_tree(TARGET, BACKUP + r'\\' + str(get_timestamp()) )

def start_backup():
    print("backup thread is running ...")
    schedule.every(10).minutes.do(copy_files)
    while True:
        schedule.run_pending()
        time.sleep(10)

def restore_files(version):
    print("restoring version " + str(version))
    copy_tree(BACKUP + r'\\' + str(version), TARGET)

if __name__ == '__main__':


    def set_options():
        global OptionList
        OptionList = next(os.walk(BACKUP))[1]
        for i, item in enumerate(OptionList):
            OptionList[i] = str(datetime.fromtimestamp(float(item)))
        if len(OptionList) == 0:
            OptionList = ['no backups available']

    def refresh_options():
        variable.set('')
        opt['menu'].delete(0, 'end')
        NewOptionList = next(os.walk(BACKUP))[1]
        for i, item in enumerate(NewOptionList):
            NewOptionList[i] = str(datetime.fromtimestamp(float(item)))
        if len(OptionList) == 0:
            NewOptionList = ['no backups available']
        for choice in NewOptionList:
            opt['menu'].add_command(label=choice, command=tk._setit(variable, choice))    

    set_options()

    app = tk.Tk()

    app.geometry('500x500')
    app.iconbitmap('sod1.ico')
    app.winfo_toplevel().title("State of Decay:  Backup Manager")

    variable = tk.StringVar(app)
    variable.set(OptionList[0])

    backUpFlag = 0
    def backUpStartCallback(*args):
        global backUpFlag
        if backUpFlag == 0:
            backUpFlag = 1
            backupStatusLabel.configure(text="Backup process has started ")
            _thread.start_new_thread( start_backup, () )

    B = tk.Button(app, text ="Start Backup", command=backUpStartCallback)
    B.pack()

    backupStatusLabel = tk.Label(text="", font=('Helvetica', 12), fg='red')
    backupStatusLabel.pack(side="top")




    B2 = tk.Button(app, text ="Refresh List", command=refresh_options)
    B2.pack()

    opt = tk.OptionMenu(app, variable, *OptionList)
    opt.config(width=90, font=('Helvetica', 12))
    opt.pack(side="top")


    labelTest = tk.Label(text="", font=('Helvetica', 12), fg='red')
    labelTest.pack(side="top")

    def callback(*args):
        labelTest.configure(text="The selected item is {}".format(variable.get()))

    def RestoreCallback():
        print(variable.get())
        version =datetime.timestamp(datetime.strptime(variable.get(),'%Y-%m-%d %H:%M:%S.%f')) 
        restore_files(version)

    B1 = tk.Button(app, text ="Restore Selected Backup", command=RestoreCallback)
    B1.pack()

    backupStatusLabel = tk.Label(text="", font=('Helvetica', 12), fg='red')
    backupStatusLabel.pack(side="top")

    variable.trace("w", callback)

    app.mainloop()