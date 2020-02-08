from tkinter import filedialog, messagebox
from tkinter import Button, StringVar, Entry, Label, N, S, E, W, Tk, HORIZONTAL, mainloop, messagebox
from tkinter.ttk import Progressbar
import os
from urllib.request import urlopen, urlretrieve
import urllib.error

def browse():
    # Allow user to select a directory and store it in global var
    # called folder_path
    global folder_path
    global pb
    global root

    pb['value']=0
    root.update_idletasks()
    
    filename = filedialog.askdirectory()
    folder_path.set(filename)
    

def download(event=None):
    global MLS
    global folder_path
    global pb
    global root

    pb['value']=0
    
    if folder_path.get() == "" or folder_path.get() == None:
        messagebox.showinfo("Error", "Choose a download folder")
    elif MLS.get() == "" or MLS.get() == None:
        messagebox.showinfo("Error", "Enter a MLS number")
    else:
        if not os.path.exists(folder_path.get()):
            os.mkdir(folder_path.get())
        img_url = "http://trebphotos.stratusdata.com/Live/Default.ashx?type=ListingPhoto&entityName=Listing&entityID=" + MLS.get() + "&index="
        for i in range(1, 21):
            r = get_image(img_url, i)
            if r == -1:
                pb['value']=100
                break
            elif r == -2:
                pb['value']=0
                break
            else:
                pb['value']=int((i/20)*100)
                root.update_idletasks()
        
        
def get_image(url, i):
    global folder_path
    
    dl_url = url + str(i)
    filename= str(i) + ".jpg"
    fullfilename = os.path.join(folder_path.get(), filename)

    try:
        urlretrieve(dl_url, fullfilename)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            if i == 1:
                messagebox.showinfo("Error", "Listing not found");
                return -2 # mls number wrong
            return -1 # no more pictures
        else:
            messagebox.showinfo("Error", "Error reaching Stratus");
            return -2 # some other error
    return 0


root = Tk()
root.resizable(False, False)
root.title("MLS DL")
root.bind('<Return>', download)

mls_lbl = Label(master=root, text="MLS Number: ")
mls_lbl.grid(row=0, column=1, padx=3, sticky=E)

MLS = StringVar()
mls_e = Entry(master=root, textvariable=MLS)
mls_e.grid(row=0, column=2, padx=3, pady=(5,3), sticky=E+W)

info_lbl = Label(master=root, text="Download Folder: ")
info_lbl.grid(row=1, column=1, padx=3, pady=(0,3), sticky=E)
              
folder_path = StringVar()
path_lbl = Label(master=root,textvariable=folder_path)
path_lbl.grid(row=1, column=2, padx=(0,5))

browse_b= Button(text="Choose Folder", command=browse)
browse_b.grid(row=2, column=1,padx=(5,1), sticky=E+W)

download_b= Button(text="Download", command=download)
download_b.grid(row=2, column=2, padx=(2,5), sticky=E+W)

pb = Progressbar(root, orient=HORIZONTAL, mode='determinate')
pb.grid(row=3, column=1, pady=(3,5), padx=5, columnspan=3, sticky=E+W)
mainloop()
