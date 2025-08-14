from tkinter import *
import instaloader
import urllib
from urllib.request import urlopen
from PIL import Image, ImageTk
import io
from calculator import label

def get_image():
    L = instaloader.Instaloader()
    profile = instaloader.Profile.from_username(L.context, f"{username.get()}")
    a = urlopen(profile.get_profile_pic_url())
    data = a.read()
    a.close()
    image = Image.open(io.BytesIO(data))
    pic = ImageTk.PhotoImage(image)
    label.configure(image=pic)
    label.image = pic
    label.pack()



window = Tk()
window.geometry("600x600")
window.maxsize(800,800)
window.minsize(200,200)
window.title("instagram profile downloader")

#label
Label(window, text="enter your instagram username").pack()





button = Button(window, text="stat download", fg="red", bg="yellow")
button.place(x=270,y=50)
button.configure(command=get_image)




username = Entry(window, width=50)
username.pack()



window.mainloop()