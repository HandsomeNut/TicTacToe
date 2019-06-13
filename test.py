from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox as msg
from random import choice
import pygame

root = Tk()
root.title(" Tic Tac Toe X O ")
root.resizable(False, False)
img = PhotoImage(file="Data/TicTacToe.png")
root.tk.call("wm", "iconphoto", root._w, img)

tokenSelector = None
symbolSet = [[0, 0]]
symbolPos = [[50, 50], [50, 150], [50, 250], [150, 50], [150, 150], [150, 250], [250, 50], [250, 150], [250, 250]]
playBoard = [[" " for i in range(3)] for i in range(3)]
path = ["Data/Tac.png", "Data/Tic.png"]
großeBilder = []
kleineBilder = []
pygame.mixer.init()
radVar = IntVar()
radVar.set(0)


# Große Bilder
for fig in range(2):
    fileData = Image.open(path[fig])
    # Anpassen der Bildgröße auf 95x95
    fileData = fileData.resize((95, 95), Image.ANTIALIAS)
    # Umwandeln des Bildes in anzeigefähiges PhotoImage
    fileData = ImageTk.PhotoImage(fileData)

    großeBilder.append(fileData)

# Kleine Bilder
for fig in range(2):
    fileData = Image.open(path[fig])
    # Anpassen der Bildgröße auf 95x95
    fileData = fileData.resize((25, 25), Image.ANTIALIAS)
    # Umwandeln des Bildes in anzeigefähiges PhotoImage
    fileData = ImageTk.PhotoImage(fileData)

    kleineBilder.append(fileData)



def on_closing():
    pass


def tic():
    tokenSelector.destroy()
    button1.grid_forget()
    radVar.set(0)


def tac():
    tokenSelector.destroy()
    button1.grid_forget()
    radVar.set(1)

def alleFelderBesetzt(startY, startX, playBoard, dx, dy):
    firstField = playBoard[startY][startX]
    if firstField == " ":
        return False
    for i in range(3):
        y = startY + i * dx
        x = startX + i * dy
        if playBoard[y][x] != firstField:
            return False

    return True


def winCheck(playBoard):
    # Check rows
    for y in range(len(playBoard)):
        if alleFelderBesetzt(y, 0, playBoard, 0, 1):
            msg.showinfo(" GEWONNEN!", " Du hast das Spiel gewonnen! ")

    # Check column
    for x in range(len(playBoard)):
        if alleFelderBesetzt(0, x, playBoard, 1, 0):
            msg.showinfo(" GEWONNEN!", " Du hast das Spiel gewonnen! ")

    # Check diagonal
    if alleFelderBesetzt(0, 0, playBoard, 1, 1):
        msg.showinfo(" GEWONNEN!", " Du hast das Spiel gewonnen! ")

    if alleFelderBesetzt(2, 0, playBoard, -1, 1):
        msg.showinfo(" GEWONNEN!", " Du hast das Spiel gewonnen! ")



def bildDa(bildCoords):
    for i in range(len(symbolSet)):
        if bildCoords == w.coords(symbolSet[i]):
            msg.showwarning(" Feld bereits gewählt ", " Dieses Feld ist bereits ausgewählt ")
            return True

def playSound():
    foo = ["Data/stroke1.wav", "Data/stroke2.wav", "Data/stroke3.wav"]
    pygame.mixer.music.load(choice(foo))
    pygame.mixer.music.play()

def messageWindow():
    global tokenSelector

    if tokenSelector is None:
        tokenSelector = Toplevel()
        tokenSelector.title(' Spielstein ')
        tokenSelector.resizable(False, False)
        tokenSelector.protocol("WM_DELETE_WINDOW", on_closing)
        message = " Wähle deinen Spielstein! "
        Label(tokenSelector, text=message).pack()
        Button(tokenSelector, text='Tic', image=kleineBilder[0], compound="right", command=tic).pack(side=LEFT)
        Button(tokenSelector, text='Tac', image=kleineBilder[1], compound="right", command=tac).pack(side=LEFT)


def makeMove(event):

    spielStein = radVar.get()

    print("clicked at", event.x, event.y)

    # Kontrolle Linke Spalte
    if event.x < 100 and event.y < 100 and not bildDa(symbolPos[0]):
        symbolSet.append(w.create_image(50, 50, anchor=CENTER, image=großeBilder[spielStein]))
        playBoard[0][0] = spielStein
        playSound()

    elif event.x < 100 < event.y < 200 and not bildDa(symbolPos[1]):
        symbolSet.append(w.create_image(50, 150, anchor=CENTER, image=großeBilder[spielStein]))
        playBoard[1][0] = spielStein
        playSound()

    elif event.x < 100 and event.y > 200 and not bildDa(symbolPos[2]):
        symbolSet.append(w.create_image(50, 250, anchor=CENTER, image=großeBilder[spielStein]))
        playBoard[2][0] = spielStein
        playSound()

    # Kontrolle mittlere Spalte
    elif event.y < 100 < event.x < 200 and not bildDa(symbolPos[3]):
        symbolSet.append(w.create_image(150, 50, anchor=CENTER, image=großeBilder[spielStein]))
        playBoard[0][1] = spielStein
        playSound()

    elif 100 < event.x < 200 and 100 < event.y < 200 and not bildDa(symbolPos[4]):
        symbolSet.append(w.create_image(150, 150, anchor=CENTER, image=großeBilder[spielStein]))
        playBoard[1][1] = spielStein
        playSound()

    elif event.x > 100 and event.x < 200 < event.y and not bildDa(symbolPos[5]):
        symbolSet.append(w.create_image(150, 250, anchor=CENTER, image=großeBilder[spielStein]))
        playBoard[2][1] = spielStein
        playSound()

    # Kontrolle rechte Spalte
    elif event.x > 200 and event.y < 100 and not bildDa(symbolPos[6]):
        symbolSet.append(w.create_image(250, 50, anchor=CENTER, image=großeBilder[spielStein]))
        playBoard[0][2] = spielStein
        playSound()

    elif event.x > 200 > event.y and event.y > 100 and not bildDa(symbolPos[7]):
        symbolSet.append(w.create_image(250, 150, anchor=CENTER, image=großeBilder[spielStein]))
        playBoard[1][2] = spielStein
        playSound()

    elif event.x > 200 and event.y > 200 and not bildDa(symbolPos[8]):
        symbolSet.append(w.create_image(250, 250, anchor=CENTER, image=großeBilder[spielStein]))
        playBoard[2][2] = spielStein
        playSound()

    for i in range(len(symbolSet)):
        print(w.coords(symbolSet[i]))

    for token in playBoard:
        print(token)

    # # WinCheck
    winCheck(playBoard)


def _new():
    global symbolSet, tokenSelector, button1, playBoard

    w.delete("all")
    w.create_line(0, 100, 300, 100, width=3)
    w.create_line(0, 200, 300, 200, width=3)
    w.create_line(100, 0, 100, 300, width=3)
    w.create_line(200, 0, 200, 300, width=3)
    symbolSet = [[0, 0]]
    button1 = Button(root, width=34, height=17, text=" SPIELEN ", command=messageWindow)
    button1.grid(column=0, row=0)
    tokenSelector = None
    playBoard = [[" " for i in range(3)] for i in range(3)]


frameSet1 = LabelFrame(root, text=" Spielfeld ").grid(column=0, row=0)
w = Canvas(frameSet1, width=300, height=300, bg="white")
w.grid(column=0, row=0)
button1 = Button(root, width=34, height=17, text=" SPIELEN ", command=messageWindow)
button1.grid(column=0, row=0)

w.create_line(0, 100, 300, 100, width=3)
w.create_line(0, 200, 300, 200, width=3)
w.create_line(100, 0, 100, 300, width=3)
w.create_line(200, 0, 200, 300, width=3)

w.bind("<Button-1>", makeMove)

menuBar = Menu(root)
root.config(menu=menuBar)

fileMenu = Menu(menuBar, tearoff=0)

menuBar.add_cascade(label="Datei", menu=fileMenu)
fileMenu.add_command(label=" Neu ", command=_new)

root.mainloop()
