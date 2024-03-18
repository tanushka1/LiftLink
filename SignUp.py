import tkinter as tk
from tkinter import *
from database import *
import mainMenu



print("running signup")
SignupWin = Tk()
SignupWin.title("Home Page")
SignupWin.attributes('-fullscreen', True)
SignupWin.configure(bg='pink')



def setCar():

    if (yesCar.get() == 1):
        return True
    else:
        return False

def passwordIncorrect():
    incorrect = Label(SignupWin,text="Passwords did not match please retry").place(x=800,y=500)
    password.set("")
    passwordre.set("")



def submit_login():

    username = usernameL.get()
    #global usernametoGive = username
    passwordFinal = password.get()
    passwordRes = passwordre.get()
    firstname = fname.get()
    lastname = lname.get()
    addressOne = addresslineo.get()
    addressTwo = addresslinet.get()
    cityTown = city.get()
    postCode = postcode.get()
    print(setCar())
    if setCar() == True:
        carBool = True
        print("hello")
    else:
        carBool = False

    if passwordFinal==passwordRes:
        add_user(str(username),str(passwordFinal),str(firstname),str(lastname),str(addressOne),str(addressTwo),str(cityTown),str(postCode),carBool)
        mainMenu.open(username)
        SignupWin.destroy()
    else:
        passwordIncorrect()


def exitpage():
    SignupWin.destroy()


def GoHome():
    SignupWin.destroy()
    import Homepage


# Sign up labels
# Email
usernameLabel = Label(SignupWin, text="Username:",bg='pink',fg='#52290A',font=('Arial',11)).place(x=500, y=50)
usernameL = StringVar()
usernameEntry = Entry(SignupWin, textvariable=usernameL)
usernameEntry.place(x=700, y=50)

# Password
passwordLabel = Label(SignupWin, text="Password:",bg='pink',fg='#52290A',font=('Arial',11)).place(x=500, y=100)
password = StringVar()
passwordEntry = Entry(SignupWin, textvariable=password,show='*')
passwordEntry.place(x=700, y=100)

# Password re-confirmation
passwordreLabel = Label(SignupWin, text="Confirm password:",bg='pink',fg='#52290A',font=('Arial',11)).place(x=500, y=150)
passwordre = StringVar()
passwordreEntry = Entry(SignupWin, textvariable=passwordre,show='*')
passwordreEntry.place(x=700, y=150)

# FirstName
fnameLabel = Label(SignupWin, text="First Name:",bg='pink',fg='#52290A',font=('Arial',11)).place(x=500, y=200)
fname = StringVar()
fnameLabelEntry = Entry(SignupWin, textvariable=fname)
fnameLabelEntry.place(x=700, y=200)

# lastname
lnameLabel = Label(SignupWin, text="Last Name:",bg='pink',fg='#52290A',font=('Arial',11)).place(x=500, y=250)
lname = StringVar()
lnameLabelEntry = Entry(SignupWin, textvariable=lname)
lnameLabelEntry.place(x=700, y=250)

# address
addresslineoLabel = Label(SignupWin, text="Address Line 1:",bg='pink',fg='#52290A',font=('Arial',11)).place(x=500, y=300)
addresslineo = StringVar()
addresslineoEntry = Entry(SignupWin, textvariable=addresslineo)
addresslineoEntry.place(x=700, y=300)

addresslinetLabel = Label(SignupWin, text="Address Line 2:",bg='pink',fg='#52290A',font=('Arial',11)).place(x=500, y=350)
addresslinet = StringVar()
addresslinetEntry = Entry(SignupWin, textvariable=addresslinet)
addresslinetEntry.place(x=700, y=350)

citylabel = Label(SignupWin, text="City/Town:",bg='pink',fg='#52290A',font=('Arial',11)).place(x=500, y=400)
city = StringVar()
cityEntry = Entry(SignupWin, textvariable=city)
cityEntry.place(x=700, y=400)

postcodeLabel = Label(SignupWin, text="Postcode:",bg='pink',fg='#52290A',font=('Arial',11)).place(x=500, y=450)
postcode = StringVar()
postcodeEntry = Entry(SignupWin, textvariable=postcode)
postcodeEntry.place(x=700, y=450)

# car
yesCar = tk.IntVar()
carCheck = tk.Checkbutton(SignupWin, text='I have a car',bg='pink',fg='#52290A',font=('Arial',11), variable=yesCar, onvalue=1, offvalue=0,
                          command=setCar).place(x=500, y=500)

# buttons
SubmitButton = Button(SignupWin,width=8,height=2, text="Submit", bg="beige", command=submit_login).place(x=500, y=550)
Exitbutton= Button(SignupWin,width=8,height=2, text="Exit",bg="beige",command=exitpage).place(x=50,y=625)
HomeButton = Button(SignupWin,width=8,height=2, text="Homepage",bg="beige",command=GoHome).place(x=150,y=625)

SignupWin.mainloop()


