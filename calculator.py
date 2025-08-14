from tkinter import *

from click import command

window = Tk()
window.geometry("600x600")
window.maxsize(600,600)
window.minsize(600,600)
window.title("instagram profile downloader")

#label
label = Label(window, text="", fg="black", bg="white")
# label1 = Label(window, text="+", fg="black", bg="white")
label.place(x=238, y=6, width=124, height=20)
# label1.place(x=290, y=68)

#button
def add():
    x = int(input.get())
    y = int(input2.get())
    result = x + y
    label.config(text=str(result))

def sub():
    x = int(input.get())
    y = int(input2.get())
    result = x - y
    label.config(text=str(result))

def mul():
    x = int(input.get())
    y = int(input2.get())
    result = x * y
    label.config(text=str(result))

def div():
    x = int(input.get())
    y = int(input2.get())
    if y != 0:
        result = x / y
        label.config(text=str(result))
    else:
        label.config(text="Error: Division by zero")


def one():
    input.insert(0, "1")

def two():
    input.insert(0, "2")

def three():
    input.insert(0, "3")

def four():
    input.insert(0, "4")

def five():
    input.insert(0, "5")

def six():
    input.insert(0, "6")

def seven():
    input.insert(0, "7")

def eight():
    input.insert(0, "8")

def nine():
    input.insert(0, "9")

def zero():
    input.insert(0, "0")
#
# def mos():
#     input1.insert(0, "+")
#
# def man():
#     input1.insert(0, "-")
#
# def zar():
#     input1.insert(0, "*")
#
# def tag():
#     input1.insert(0, "/")
#
# def mosa():
#     input.insert(0, "=")



button_add = Button(window, text="+", fg="red", bg="yellow", command=add)
button_mul = Button(window, text="-", fg="red", bg="yellow", command=sub)
button_sub = Button(window, text="*", fg="red", bg="yellow", command=mul)
button_div = Button(window, text="/", fg="red", bg="yellow", command=div)
button_add.place(x=308, y=80)
button_sub.place(x=340, y=80)
button_mul.place(x=276, y=80)
button_div.place(x=244, y=80)




button1 = Button(window, text="1", fg="red", bg="white", command=one)
button2 = Button(window, text="2", fg="red", bg="white", command=two)
button3 = Button(window, text="3", fg="red", bg="white", command=three)
button4 = Button(window, text="4", fg="red", bg="white", command=four)
button5 = Button(window, text="5", fg="red", bg="white", command=five)
button6 = Button(window, text="6", fg="red", bg="white", command=six)
button7 = Button(window, text="7", fg="red", bg="white", command=seven)
button8 = Button(window, text="8", fg="red", bg="white", command=eight)
button9 = Button(window, text="9", fg="red", bg="white", command=nine)
button0 = Button(window, text="0", fg="red", bg="white", command=zero)
# button_m = Button(window, text="+", fg="red", bg="white", command=mos)
# button_ma = Button(window, text="-", fg="red", bg="white", command=man)
# button_z = Button(window, text="*", fg="red", bg="white", command=zar)
# button_t = Button(window, text="/", fg="red", bg="white", command=tag)
# button_mosa = Button(window, text="=", fg="red", bg="white", command=mosa)
button1.place(x=260, y=140)
button2.place(x=290, y=140)
button3.place(x=320, y=140)
button4.place(x=260, y=170)
button5.place(x=290, y=170)
button6.place(x=320, y=170)
button7.place(x=260, y=200)
button8.place(x=290, y=200)
button9.place(x=320, y=200)
button0.place(x=290, y=230)
# button_m.place(x=318, y=230)
# button_ma.place(x=345, y=200)
# button_z.place(x=345, y=170)
# button_t.place(x=345, y=140)
# button_mosa.place(x=345, y=230, width=50)



#inputs


input = Entry(window)
# input1 = Entry(window)
input2 = Entry(window)
input.place(x=238, y=34)
# input1.place(x=287, y=69, width=15, height=15)
input2.place(x=238,y=58)










window.mainloop()