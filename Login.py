import tkinter as tk
from tkinter import *
import mainMenu
import sqlite3
from database import *

#Page set up
LoginWin = Tk()
LoginWin.title("Home Page")
LoginWin.attributes('-fullscreen',True)
LoginWin.configure(bg='pink')



def validate(username,password):
    print("validate")
    print(username)
    conn = sqlite3.connect("carpooldb.db")
    curs = conn.cursor()
    curs.execute("SELECT Password FROM Users WHERE Username =?", (username,))
    rows = curs.fetchone()
    print(rows)
    if rows is not None:
        print("he")
        for r in rows:
            if r == password:
                LoginWin.destroy()
                mainMenu.open(username)
                print(username)

            else:
                tkWindowV = Tk()
                tkWindowV.geometry('400x150')
                tkWindowV.title('Invalid')
                ValidLabel = Label(tkWindowV, text="Login unsuccesful").grid(row=0, column=0)
    else:
        tkWindowV = Tk()
        tkWindowV.geometry('400x150')
        tkWindowV.title('Invalid')
        ValidLabel = Label(tkWindowV, text="Login unsuccesful").grid(row=0, column=0)






def submit_login():
    usernameG = username.get()
    print(usernameG)
    passwordG = password.get()
    validate(usernameG,passwordG)

def exitpage():
    LoginWin.destroy()
    return

def GoHome():
    LoginWin.destroy()
    import Homepage



usernameLabel = Label(LoginWin, text ="Username:",bg='pink',fg='#52290A',font=('Arial',11)).place(x=500,y=200)
username = StringVar()
print(username.get())
usernameEntry = Entry(LoginWin, textvariable= username)
usernameEntry.place(x=600,y=200)

passwordLabel = Label(LoginWin, text="Password:",bg='pink',fg='#52290A',font=('Arial',11)).place(x=500,y=250)
password = StringVar()
passwordEntry = Entry(LoginWin, textvariable = password,show='*')
passwordEntry.place(x=600,y=250)

submit = Button(LoginWin,text="Submit",width=8,height=2,bg="beige",command= submit_login).place(x=500,y=350)
Exitbutton= Button(LoginWin, text="Exit",width=8,height=2,bg="beige",command=exitpage).place(x=50,y=625)
HomeButton = Button(LoginWin, text="HomePage",width=8,height=2, bg="beige", command=GoHome).place(x=150, y=625)
LoginWin.mainloop()