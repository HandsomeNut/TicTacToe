import tkinter as tk
from tkinter import messagebox as msg, CENTER
from PIL import ImageTk, Image
from random import choice
import pygame
import copy

class Move:

    index = []
    score = 0


class MainGame:

    # # # Initialisierung der Klassenvariablen

    # # GUI-Variablen
    path = ["Data/Tac.png", "Data/Tic.png"]
    stroke = ["Data/stroke1.wav", "Data/stroke2.wav", "Data/stroke3.wav"]
    winSound = ["Data/win.wav"]
    bigPics = []
    smallPics = []
    tokenSelector = None

    # # Spiellogikvariablen
    tokens = []
    turnPlayer = 0 # 0 => Spieler 1 am Zug, 1 => Spieler 2 am Zug
    symbolSet = [[0, 0]]
    symbolPos = [[50, 50], [50, 150], [50, 250], [150, 50], [150, 150], [150, 250], [250, 50], [250, 150], [250, 250]]
    playBoard = [[" " for i in range(3)] for i in range(3)]
    fc = 0

    # Sound Initialisierung
    pygame.mixer.init()

    # Bilder werden aus Data Verzeichnis importiert
    def pictures(self):
        # Große Bilder
        for fig in range(2):
            fileData = Image.open(self.path[fig])
            # Anpassen der Bildgröße auf 95x95
            fileData = fileData.resize((95, 95), Image.ANTIALIAS)
            # Umwandeln des Bildes in anzeigefähiges PhotoImage
            fileData = ImageTk.PhotoImage(fileData)

            self.bigPics.append(fileData)

        # Kleine Bilder
        for fig in range(2):
            fileData = Image.open(self.path[fig])
            # Anpassen der Bildgröße auf 95x95
            fileData = fileData.resize((25, 25), Image.ANTIALIAS)
            # Umwandeln des Bildes in anzeigefähiges PhotoImage
            fileData = ImageTk.PhotoImage(fileData)

            self.smallPics.append(fileData)

    # Neues Spiel beginnen
    def _new(self):
        self.gameField.grid_forget()
        self.canvasFrame.grid_forget()
        self.createGameField()
        self.symbolSet = [[0, 0]]
        self.playBoard = [[" " for i in range(3)] for i in range(3)]
        self.tokenSelector = None
        self.tokens = []
        self.newGame()

    # Spiel beenden
    def _quit(self):
        self.root.quit()
        self.root.destroy()
        exit()

    # # Spiellogik

    # Sind drei Steine in einer Reihe?
    def fieldsTheSame(self, startY, startX, playBoard, dx, dy):
        firstField = playBoard[startY][startX]
        if firstField == " ":
            return False
        for i in range(3):
            y = startY + i * dx
            x = startX + i * dy
            if playBoard[y][x] != firstField:
                return False

        return True

    # Gewinnbedingen erfüllt?
    def winCheck(self, board):



        # Reihe wird überprüft
        for y in range(len(board)):
            if self.fieldsTheSame(y, 0, board, 0, 1):
                return True

        # Spalte wird überprüft
        for x in range(len(board)):
            if self.fieldsTheSame(0, x, board, 1, 0):
                return True

        # Check diagonal
        if self.fieldsTheSame(0, 0, board, 1, 1):
            return True

        if self.fieldsTheSame(2, 0, board, -1, 1):
            return True

        return False

    # Ist das Spiel unentschieden?
    def draw(self, board):
        for col in range(len(board)):
            for row in range(len(board)):
                if self.playBoard[col][row] == " ":
                    return False
        return True

    def winMessage(self):
        self.turnMade()
        player = "Spieler " + str(self.turnPlayer + 1)
        self.playSound(self.winSound)
        if msg.askyesno(" GEWONNEN!", player + " hat das Spiel gewonnen!\n Noch eine Runde?"):
            self._new()
        else:
            self._quit()

    def tokenExists(self, bildCoords):
        for i in range(len(self.symbolSet)):
            if bildCoords == self.gameField.coords(self.symbolSet[i]):
                msg.showwarning(" Feld bereits gewählt ", " Dieses Feld ist bereits ausgewählt ")
                return True

    def playSound(self, sound):
        pygame.mixer.music.load(choice(sound))
        pygame.mixer.music.play()

    # Token wird auf Spielfeld gesetzt und Zug weitergegeben
    def makeMove(self, event):

        print("clicked at", event.x, event.y)

        # Kontrolle Linke Spalte
        if event.x < 100 and event.y < 100 and not self.tokenExists(self.symbolPos[0]):
            self.symbolSet.append(self.gameField.create_image(50, 50, anchor=CENTER, image=self.bigPics[self.tokens[self.turnPlayer]]))
            self.playBoard[0][0] = self.tokens[self.turnPlayer]
            self.playSound(self.stroke)
            self.turnMade()

        elif event.x < 100 < event.y < 200 and not self.tokenExists(self.symbolPos[1]):
            self.symbolSet.append(self.gameField.create_image(50, 150, anchor=CENTER, image=self.bigPics[self.tokens[self.turnPlayer]]))
            self.playBoard[1][0] = self.tokens[self.turnPlayer]
            self.playSound(self.stroke)
            self.turnMade()

        elif event.x < 100 and event.y > 200 and not self.tokenExists(self.symbolPos[2]):
            self.symbolSet.append(self.gameField.create_image(50, 250, anchor=CENTER, image=self.bigPics[self.tokens[self.turnPlayer]]))
            self.playBoard[2][0] = self.tokens[self.turnPlayer]
            self.playSound(self.stroke)
            self.turnMade()

        # Kontrolle mittlere Spalte
        elif event.y < 100 < event.x < 200 and not self.tokenExists(self.symbolPos[3]):
            self.symbolSet.append(self.gameField.create_image(150, 50, anchor=CENTER, image=self.bigPics[self.tokens[self.turnPlayer]]))
            self.playBoard[0][1] = self.tokens[self.turnPlayer]
            self.playSound(self.stroke)
            self.turnMade()

        elif 100 < event.x < 200 and 100 < event.y < 200 and not self.tokenExists(self.symbolPos[4]):
            self.symbolSet.append(self.gameField.create_image(150, 150, anchor=CENTER, image=self.bigPics[self.tokens[self.turnPlayer]]))
            self.playBoard[1][1] = self.tokens[self.turnPlayer]
            self.playSound(self.stroke)
            self.turnMade()

        elif event.x > 100 and event.x < 200 < event.y and not self.tokenExists(self.symbolPos[5]):
            self.symbolSet.append(self.gameField.create_image(150, 250, anchor=CENTER, image=self.bigPics[self.tokens[self.turnPlayer]]))
            self.playBoard[2][1] = self.tokens[self.turnPlayer]
            self.playSound(self.stroke)
            self.turnMade()

        # Kontrolle rechte Spalte
        elif event.x > 200 and event.y < 100 and not self.tokenExists(self.symbolPos[6]):
            self.symbolSet.append(self.gameField.create_image(250, 50, anchor=CENTER, image=self.bigPics[self.tokens[self.turnPlayer]]))
            self.playBoard[0][2] = self.tokens[self.turnPlayer]
            self.playSound(self.stroke)
            self.turnMade()

        elif event.x > 200 > event.y and event.y > 100 and not self.tokenExists(self.symbolPos[7]):
            self.symbolSet.append(self.gameField.create_image(250, 150, anchor=CENTER, image=self.bigPics[self.tokens[self.turnPlayer]]))
            self.playBoard[1][2] = self.tokens[self.turnPlayer]
            self.playSound(self.stroke)
            self.turnMade()

        elif event.x > 200 and event.y > 200 and not self.tokenExists(self.symbolPos[8]):
            self.symbolSet.append(self.gameField.create_image(250, 250, anchor=CENTER, image=self.bigPics[self.tokens[self.turnPlayer]]))
            self.playBoard[2][2] = self.tokens[self.turnPlayer]
            self.playSound(self.stroke)
            self.turnMade()

        for i in range(len(self.symbolSet)):
            print(self.gameField.coords(self.symbolSet[i]))



        # # Player WinCheck
        if self.winCheck(self.playBoard):
            self.winMessage()
        elif self.draw(self.playBoard):
            if msg.askyesno(" Unentschieden", "Keiner hat gewonnen!\n Noch eine Runde?"):
                self._new()
            else:
                self._quit()

        # AI Turn
        if self.turnPlayer == 1:
            board = copy.deepcopy(self.playBoard)
            player = 1
            aiMove = self.minimax(player, board).index

            # AÍ Drawphase
            if aiMove == (0,0):
                self.symbolSet.append(self.gameField.create_image(50, 50, anchor=CENTER,
                                                                  image=self.bigPics[self.tokens[self.turnPlayer]]))
                self.playBoard[0][0] = self.tokens[self.turnPlayer]
                self.playSound(self.stroke)
                self.turnMade()
            elif aiMove == (1,0):
                self.symbolSet.append(self.gameField.create_image(50, 150, anchor=CENTER,
                                                                  image=self.bigPics[self.tokens[self.turnPlayer]]))
                self.playBoard[1][0] = self.tokens[self.turnPlayer]
                self.playSound(self.stroke)
                self.turnMade()

            elif aiMove == (2,0):
                self.symbolSet.append(self.gameField.create_image(50, 250, anchor=CENTER,
                                                                  image=self.bigPics[self.tokens[self.turnPlayer]]))
                self.playBoard[2][0] = self.tokens[self.turnPlayer]
                self.playSound(self.stroke)
                self.turnMade()

                # Kontrolle mittlere Spalte
            elif aiMove == (0,1):
                self.symbolSet.append(self.gameField.create_image(150, 50, anchor=CENTER,
                                                                  image=self.bigPics[self.tokens[self.turnPlayer]]))
                self.playBoard[0][1] = self.tokens[self.turnPlayer]
                self.playSound(self.stroke)
                self.turnMade()

            elif aiMove == (1,1):
                self.symbolSet.append(self.gameField.create_image(150, 150, anchor=CENTER,
                                                                  image=self.bigPics[self.tokens[self.turnPlayer]]))
                self.playBoard[1][1] = self.tokens[self.turnPlayer]
                self.playSound(self.stroke)
                self.turnMade()

            elif aiMove == (1,2):
                self.symbolSet.append(self.gameField.create_image(150, 250, anchor=CENTER,
                                                                  image=self.bigPics[self.tokens[self.turnPlayer]]))
                self.playBoard[2][1] = self.tokens[self.turnPlayer]
                self.playSound(self.stroke)
                self.turnMade()

                # Kontrolle rechte Spalte
            elif aiMove == (2,0):
                self.symbolSet.append(self.gameField.create_image(250, 50, anchor=CENTER,
                                                                  image=self.bigPics[self.tokens[self.turnPlayer]]))
                self.playBoard[0][2] = self.tokens[self.turnPlayer]
                self.playSound(self.stroke)
                self.turnMade()

            elif aiMove == (2,1):
                self.symbolSet.append(self.gameField.create_image(250, 150, anchor=CENTER,
                                                                  image=self.bigPics[self.tokens[self.turnPlayer]]))
                self.playBoard[1][2] = self.tokens[self.turnPlayer]
                self.playSound(self.stroke)
                self.turnMade()

            elif aiMove == (2,2):
                self.symbolSet.append(self.gameField.create_image(250, 250, anchor=CENTER,
                                                                  image=self.bigPics[self.tokens[self.turnPlayer]]))
                self.playBoard[2][2] = self.tokens[self.turnPlayer]
                self.playSound(self.stroke)
                self.turnMade()


            # AI Wincheck
            if self.winCheck(self.playBoard):
                self.winMessage()
            elif self.draw(self.playBoard):
                if msg.askyesno(" Unentschieden", "Keiner hat gewonnen!\n Noch eine Runde?"):
                    self._new()
                else:
                    self._quit()


    def turnMade(self):
        if self.turnPlayer == 0:
            self.turnPlayer += 1
        else:
            self.turnPlayer = 0

    def _nextplayer(self, player):
        if player == 0:
            player += 1
        else:
            player = 0

        return player



    def minimax(self, player, board):

        print(board)
        emptyField = []

        # Checking for empty fields
        for y in range(len(board)):
            for x in range(len(board)):
                if board[y][x] == " ":
                    emptyField.append((y, x))

        move = Move()
        # Checking for terminal states
        if self.winCheck(board) and self._nextplayer(player) == 1:
            move.score = 10
            return move
        elif self.winCheck(board) and self._nextplayer(player) == 0:
            move.score = -10
            return move
        elif len(emptyField)== 0:
            move.score= 0
            return move

        moves = []

        # plotting the next turn
        for field in emptyField:
            move = Move()
            fieldNew = copy.deepcopy(board)
            move.index = field
            fieldNew[field[0]][field[1]] = player
            result = self.minimax(self._nextplayer(player), fieldNew)
            move.score = result.score
            moves.append(move)

        # Finding best Move by Score
        bestMove = 0
        if player == 1:
            bestScore = -10000
            for index in range(0, len(moves)):
                if moves[index].score > bestScore:
                    bestScore = moves[index].score
                    bestMove = index

        if player == 0:
            bestScore = 10000
            for index in range(0, len(moves)):
                if moves[index].score < bestScore:
                    bestScore = moves[index].score
                    bestMove = index

        return moves[bestMove]



    # newGame Kindfenster Funktionen
    def _on_closing(self):
        pass


    def _radCallP1(self):
        if self.p1token.get() == 0:
            self.p2token.set(1)
        else:
            self.p2token.set(0)

    def _radCallP2(self):
        if self.p2token.get() == 0:
            self.p1token.set(1)
        else:
            self.p1token.set(0)

    def _start(self):
        self.tokenSelector.destroy()
        self.startPlay.grid_forget()
        self.tokens.append(self.p1token.get())
        self.tokens.append(self.p2token.get())

    # Init Hauptfenster
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(" Tic Tac Toe O X ")
        self.root.resizable(False, False)
        img = tk.PhotoImage(file="Data/TicTacToe.png")
        self.root.tk.call("wm", "iconphoto", self.root._w, img)
        self.pictures()
        self.createGameField()
        self.mainMenu()

    # Hauptfenster
    def createGameField(self):
        # Erstellen des Canvas und des Frames
        self.canvasFrame = tk.LabelFrame(self.root, text=" Spielfeld ")
        self.canvasFrame.grid(column=0, row=0)
        self.gameField = tk.Canvas(self.canvasFrame, width=300, height=300, bg="white")
        self.gameField.grid(column=0, row=0)

        # Button für zum Spielbeginn erstellen
        self.startPlay = tk.Button(self.root, width=36, height=18, text=" SPIELEN ", command=self.newGame)
        self.startPlay.grid(column=0, row=0)

        # Spielfeld zeichnen
        self.gameField.create_line(0, 100, 300, 100, width=3)
        self.gameField.create_line(0, 200, 300, 200, width=3)
        self.gameField.create_line(100, 0, 100, 300, width=3)
        self.gameField.create_line(200, 0, 200, 300, width=3)

        self.gameField.bind("<Button-1>", self.makeMove)

    def mainMenu(self):
        menuBar = tk.Menu(self.root)
        self.root.config(menu=menuBar)

        gameMenu = tk.Menu(menuBar, tearoff=0)

        menuBar.add_cascade(label="Spiel", menu=gameMenu)
        gameMenu.add_command(label=" Neues Spiel ", command=self._new)
        gameMenu.add_command(label=" Spiel beenden", command=self._quit)


    # Kindfenster für ein neues Spiel
    def newGame(self):


        if self.tokenSelector is None:
            self.tokenSelector = tk.Toplevel()
            self.tokenSelector.title(' Neues Spiel ')
            self.tokenSelector.resizable(False, False)
            self.tokenSelector.protocol("WM_DELETE_WINDOW", self._on_closing)

            nameToken = ["Tic", "Tac"]

            labelP1 = tk.Label(self.tokenSelector, text=" Spieler 1 ")
            labelP1.grid(column=0, row=0)

            # Spielsteinwahl Spieler 1
            self.p1token = tk.IntVar()
            self.p1token.set(0)
            for col in range(2):
                p1select = tk.Radiobutton(self.tokenSelector, text=nameToken[col], image=self.smallPics[col],
                                          variable=self.p1token, value=col, compound="right", command=self._radCallP1)
                p1select.grid(column=col, row=1)


            labelP2 = tk.Label(self.tokenSelector, text=" Spieler 2 (Bot) ")
            labelP2.grid(column=0, row=2)

            # Spielsteinwahl Spieler 2
            self.p2token = tk.IntVar()
            self.p2token.set(1)
            for col in range(2):
                p2select = tk.Radiobutton(self.tokenSelector, text=nameToken[col], image=self.smallPics[col],
                                          variable=self.p2token, value=col, compound="right", command=self._radCallP2)
                p2select.grid(column=col, row=3)

            tk.Button(self.tokenSelector, text= " Spiel beginnen ", command=self._start).grid(column=0, row=4)


# Instanz MainGame wird erstellt und Spiel gestartet
game = MainGame()

game.root.mainloop()
