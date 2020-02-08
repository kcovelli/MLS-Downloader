import os, urllib, re
from urllib.request import urlopen, urlretrieve
from tkinter import *

class App:

    def __init__(self, master):

        # MLS number regex
        self.p = "\A[CEWXcewx][0-9]{7}\Z"
        
        frame = Frame(master)
        frame.pack()

        self.button = Button(
            frame, text="QUIT", fg="red", command=frame.quit
            )
        self.button.pack(side=LEFT)

        self.dl = Button(frame, text="Download Images", command=self.start_dl)
        self.dl.pack(side=LEFT)

        self.e = Entry(master)
        self.e.pack()

        self.e.delete(0, END)
        self.e.insert(0, "")

    def start_dl(self):
        self.MLS = self.e.get()
        if not os.path.exists(self.MLS):
            os.mkdir(self.MLS)
        for i in range(1, 21):
            if self.get_image(img_url, i) == -1:
                break


    def get_image(self, url, i):
        dl_url = "http://trebphotos.stratusdata.com/Live/Default.ashx?type=ListingPhoto&entityName=Listing&entityID=" + self.MLS + "&index=" + str(i)
        filename= str(i) + ".jpg"
        fullfilename = os.path.join(self.MLS, filename)

        try:
            urlretrieve(dl_url, fullfilename)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                if i == 1:
                    print("MLS listing not found. Stopping...")
                else:
                    print("Image " + str(i) + " not found. Stopping...")
            else:
                print("Error reaching Stratus, exiting...")
            return -1
        
        print('image ' + str(i) + ' downloaded')
        return 0

root = Tk()

app = App(root)

root.mainloop()
root.destroy()
