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
tokenWin = None

symbolSet = [[0, 0]]
symbolPos = [[50, 50], [50, 150], [50, 250], [150, 50], [150, 150], [150, 250], [250, 50], [250, 150], [250, 250]]
playBoard = [i+1 for i in range(9)]
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


def anih1():
    tokenWin.destroy()
    button1.grid_forget()
    radVar.set(0)


def anih2():
    tokenWin.destroy()
    button1.grid_forget()
    radVar.set(1)


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
    global tokenWin, on_closing, anih1, anih2

    if tokenWin is None:
        tokenWin = Toplevel()
        tokenWin.title(' Spielstein ')
        tokenWin.resizable(False, False)
        tokenWin.protocol("WM_DELETE_WINDOW", on_closing)
        message = " Wähle deinen Spielstein! "
        Label(tokenWin, text=message).pack()
        Button(tokenWin, text='Tic', image=kleineBilder[0], compound="right", command=anih1).pack(side=LEFT)
        Button(tokenWin, text='Tac', image=kleineBilder[1], compound="right", command=anih2).pack(side=LEFT)


def makeMove(event):
    global playSound, bildDa

    spielStein = radVar.get()

    print("clicked at", event.x, event.y)

    # Kontrolle Linke Spalte
    if event.x < 100 and event.y < 100 and not bildDa(symbolPos[0]):
        symbolSet.append(w.create_image(50, 50, anchor=CENTER, image=großeBilder[spielStein]))
        playBoard[0] = spielStein
        playSound()

    elif event.x < 100 < event.y < 200 and not bildDa(symbolPos[1]):
        symbolSet.append(w.create_image(50, 150, anchor=CENTER, image=großeBilder[spielStein]))
        playBoard[1] = spielStein
        playSound()

    elif event.x < 100 and event.y > 200 and not bildDa(symbolPos[2]):
        symbolSet.append(w.create_image(50, 250, anchor=CENTER, image=großeBilder[spielStein]))
        playBoard[2] = spielStein
        playSound()

    # Kontrolle mittlere Spalte
    elif event.y < 100 < event.x < 200 and not bildDa(symbolPos[3]):
        symbolSet.append(w.create_image(150, 50, anchor=CENTER, image=großeBilder[spielStein]))
        playBoard[3] = spielStein
        playSound()

    elif 100 < event.x < 200 and 100 < event.y < 200 and not bildDa(symbolPos[4]):
        symbolSet.append(w.create_image(150, 150, anchor=CENTER, image=großeBilder[spielStein]))
        playBoard[4] = spielStein
        playSound()

    elif event.x > 100 and event.x < 200 < event.y and not bildDa(symbolPos[5]):
        symbolSet.append(w.create_image(150, 250, anchor=CENTER, image=großeBilder[spielStein]))
        playBoard[5] = spielStein
        playSound()

    # Kontrolle rechte Spalte
    elif event.x > 200 and event.y < 100 and not bildDa(symbolPos[6]):
        symbolSet.append(w.create_image(250, 50, anchor=CENTER, image=großeBilder[spielStein]))
        playBoard[6] = spielStein
        playSound()

    elif event.x > 200 > event.y and event.y > 100 and not bildDa(symbolPos[7]):
        symbolSet.append(w.create_image(250, 150, anchor=CENTER, image=großeBilder[spielStein]))
        playBoard[7] = spielStein
        playSound()

    elif event.x > 200 and event.y > 200 and not bildDa(symbolPos[8]):
        symbolSet.append(w.create_image(250, 250, anchor=CENTER, image=großeBilder[spielStein]))
        playBoard[8] = spielStein
        playSound()

    for i in range(len(symbolSet)):
        print(w.coords(symbolSet[i]))

    for token in playBoard:
        print(token)

    # # WinCheck
    # test = True
    #
    # for check in range(0,2):
    #     if playBoard[check] == playBoard[check + 1]:
    #         test = False
    #     else:
    #         test = True
    #         break
    #
    # for check in range(3, 5):
    #     if playBoard[check] == playBoard[check + 1]:
    #         test = False
    #     else:
    #         test = True
    #         break
    #
    # for check in range(6, 8):
    #     if playBoard[check] == playBoard[check + 1]:
    #         test = False
    #     else:
    #         test = True
    #         break
    #
    # for check in range(0, 4, 4):
    #     if playBoard[check] == playBoard[check + 4]:
    #         test = False
    #     else:
    #         test = True
    #         break
    #
    # for check in range(2, 4, 2):
    #     if playBoard[check] == playBoard[check + 2]:
    #         test = False
    #     else:
    #         test = True
    #         break
    #
    # if test:
    #     msg.showinfo(" GEWONNEN ", " Du hast gewonnen!!! ")

def _new():
    global symbolSet, tokenWin, button1, playBoard

    w.delete("all")
    w.create_line(0, 100, 300, 100, width=3)
    w.create_line(0, 200, 300, 200, width=3)
    w.create_line(100, 0, 100, 300, width=3)
    w.create_line(200, 0, 200, 300, width=3)
    symbolSet = [[0, 0]]
    button1 = Button(root, width=34, height=17, text=" SPIELEN ", command=messageWindow)
    button1.grid(column=0, row=0)
    tokenWin = None
    playBoard = [i + 1 for i in range(9)]


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
