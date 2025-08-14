from tkinter import *


window = Tk()
window.geometry("600x600")
window.maxsize(600,600)
window.minsize(600,600)
window.title("filling")


Email = Label(window, text="Email:", fg="black")
password = Label(window, text="Password:", fg="black")
Email.place(x=100, y=100)
password.place(x=100, y=140)



next = Button(window, text="Next", command=window.quit)
next.place(x=320, y=200)


input = Entry(window)
input1 = Entry(window)
input.place(x=180, y=100)
input1.place(x=180, y=140)




window.mainloop()