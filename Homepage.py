from tkinter import *


#Main homepage set up
Homepage = Tk()
Homepage.title("Home Page")
Homepage.attributes('-fullscreen',True)
Homepage.configure(bg='beige')


#Functions
def OpenSignup():
    Homepage.destroy()
    import SignUp



def OpenLogin():
    Homepage.destroy()
    import Login



def exitpage():
    Homepage.destroy()

Label(Homepage,text="LiftLink", font=('Arial',35),bg="beige").place(x = 550,y= 50)
#Buttons on the homePage
SignUpButton = Button(Homepage,width = 10,height= 5,text="Sign Up", font=('Arial',35),bg="pink",command=OpenSignup).place(x=300,y=200)
LoginButton = Button(Homepage,width = 10,height= 5, text = "Login",font=('Arial',35),bg="pink",command=OpenLogin).place(x=700, y=200)
Exitbutton= Button(Homepage,width= 8,height=2, text="Exit",bg="pink",command=exitpage).place(x=50, y=625)


Homepage.mainloop()