import sys
import tkinter as tk
from tkinter import *

from database import *





def open(username):
    print("running main")
    print(username)
    MainmenuWin = Tk()
    MainmenuWin.title("Home Page")
    MainmenuWin.attributes('-fullscreen', True)
    MainmenuWin.configure(bg='pink')
    curr_user = username
    title = "Links near " + username
    titleLabel = Label(MainmenuWin, text=title,bg='pink',fg="#52290A",font=('Arial',33)).place(x = 100, y = 50)
    namesListoutputNeighbours = outputNeighbours(username)
    print(namesListoutputNeighbours)
    if namesListoutputNeighbours == []:
        Label(MainmenuWin, text="No links found near you",bg='pink',fg="#52290A",font=('Arial',25)).place(x =100,y=150)
    else:
        for i in range(len(namesListoutputNeighbours)):
            xcoord = 100
            ycoord = 100
            textToShow = " ".join(namesListoutputNeighbours[i])
            print(textToShow)
            Label(MainmenuWin, text=textToShow,bg='pink',fg="#52290A",font=('Arial',25)).place(x = 100 , y = (ycoord * i)+150)

    def exit():
        MainmenuWin.destroy()

    def GoHome():
        MainmenuWin.destroy()
        import Homepage



    canvas = tk.Canvas(MainmenuWin, width=500, height=800, bg="beige").place(x = 900,y = 0)
    ExitButton =Button(MainmenuWin,width=8, height= 2, text="Exit", bg="beige", command=exit).place(x=50, y=625)
    Homebutton =Button(MainmenuWin,width=8, height= 2,text="HomePage", bg="beige", command=GoHome).place(x=150, y=625)




    MainmenuWin.mainloop()




def outputNeighbours(usr):
    neighbours = getNeighbourIDs(usr)  # maybe adjust this to make sure it doesnt return tuples list
    namesOfneighbours = []
    for neighbour in neighbours:
        namesOfneighbours.append(getPersonInfo(neighbour[0])[0])

    return namesOfneighbours






