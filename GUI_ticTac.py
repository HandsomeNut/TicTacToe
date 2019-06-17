import copy
import tkinter as tk
from random import choice
from tkinter import messagebox as msg, CENTER, HORIZONTAL

import pygame
from PIL import ImageTk, Image


class Move:
    index = []
    score = 0


class MainGame:
    # # # Initialisierung der Klassenvariablen

    # # GUI-Variablen
    path = ["Data/Tac.png", "Data/Tic.png", "Data/bot.png", "Data/man.png"]
    stroke = ["Data/stroke1.wav", "Data/stroke2.wav", "Data/stroke3.wav"]
    winSound = ["Data/win.wav"]
    bigPics = []
    smallPics = []
    tokenSelector = None

    # # Spiellogikvariablen
    tokens = []  # Pos 0 Player 1 Token; Pos 1 Player 2 Token
    turnPlayer = 0  # 0 => Spieler 1 am Zug, 1 => Spieler 2 am Zug
    symbolSet = [[0, 0]]
    symbolPos = [[50, 50], [50, 150], [50, 250], [150, 50], [150, 150], [150, 250], [250, 50], [250, 150], [250, 250]]
    playBoard = [[" " for i in range(3)] for i in range(3)]
    fc = 0
    aiMove = ()

    maxDepth = 28000

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
        for fig in range(4):
            fileData = Image.open(self.path[fig])
            # Anpassen der Bildgröße auf 95x95
            fileData = fileData.resize((35, 35), Image.ANTIALIAS)
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
        self.turnPlayer = 0
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

    # Überprüfen ob gewonnen
    def winCheck(self):
        if self.threeInRow(self.playBoard):
            self.winMessage()
        elif self.gameDraw(self.playBoard):
            if msg.askyesno(" Unentschieden", "Keiner hat gewonnen!\n Noch eine Runde?"):
                self._new()
            else:
                self._quit()

    # Gewinnbedingen erfüllt?
    def threeInRow(self, board):

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
    def gameDraw(self, board):
        for col in range(len(board)):
            for row in range(len(board)):
                if self.playBoard[col][row] == " ":
                    return False
        return True

    def winMessage(self):
        self.turnMade()
        self.playSound(self.winSound)

        if self.turnPlayer == 0:
            if msg.askyesno(" GEWONNEN! :)", "Du hast hat das Spiel gewonnen!\n Noch eine Runde?"):
                self._new()
            else:
                self._quit()
        else:
            if msg.askyesno(" Leider Verloren!!! ", "Leider hast du das Spiel verloren!\n Noch eine Runde?"):
                self._new()
            else:
                self._quit()

    # Existiert der Token auf dem gewählten Feld bereits
    def tokenExists(self, bildCoords):
        for i in range(len(self.symbolSet)):
            if bildCoords == self.gameField.coords(self.symbolSet[i]):
                msg.showwarning(" Feld bereits gewählt ", " Dieses Feld ist bereits ausgewählt ")
                return True

    def playSound(self, sound):
        pygame.mixer.music.load(choice(sound))
        pygame.mixer.music.play()

    # Token wird auf Canvas nach Koordinaten oder AI Kalkulation gezeichnet. Zug weitergegeben.
    def drawToken(self, event):

        # Kontrolle Linke Spalte
        if (self.turnPlayer == 0 and event.x < 100 and event.y < 100 and not self.tokenExists(self.symbolPos[0])) \
                or (self.turnPlayer == 1 and self.aiMove == (0, 0)):
            self.symbolSet.append(
                self.gameField.create_image(50, 50, anchor=CENTER, image=self.bigPics[self.tokens[self.turnPlayer][1]]))
            self.playBoard[0][0] = self.tokens[self.turnPlayer][0]
            self.playSound(self.stroke)
            self.turnMade()

        elif (self.turnPlayer == 0 and event.x < 100 < event.y < 200 and not self.tokenExists(self.symbolPos[1])) \
                or (self.turnPlayer == 1 and self.aiMove == (1, 0)):
            self.symbolSet.append(
                self.gameField.create_image(50, 150, anchor=CENTER,
                                            image=self.bigPics[self.tokens[self.turnPlayer][1]]))
            self.playBoard[1][0] = self.tokens[self.turnPlayer][0]
            self.playSound(self.stroke)
            self.turnMade()

        elif (self.turnPlayer == 0 and event.x < 100 and event.y > 200 and not self.tokenExists(self.symbolPos[2])) \
                or (self.turnPlayer == 1 and self.aiMove == (2, 0)):
            self.symbolSet.append(
                self.gameField.create_image(50, 250, anchor=CENTER,
                                            image=self.bigPics[self.tokens[self.turnPlayer][1]]))
            self.playBoard[2][0] = self.tokens[self.turnPlayer][0]
            self.playSound(self.stroke)
            self.turnMade()

        # Kontrolle mittlere Spalte
        elif (self.turnPlayer == 0 and event.y < 100 < event.x < 200 and not self.tokenExists(self.symbolPos[3])) \
                or (self.turnPlayer == 1 and self.aiMove == (0, 1)):
            self.symbolSet.append(
                self.gameField.create_image(150, 50, anchor=CENTER,
                                            image=self.bigPics[self.tokens[self.turnPlayer][1]]))
            self.playBoard[0][1] = self.tokens[self.turnPlayer][0]
            self.playSound(self.stroke)
            self.turnMade()

        elif (self.turnPlayer == 0 and 100 < event.x < 200 and 100 < event.y < 200 and not self.tokenExists(
                self.symbolPos[4])) \
                or (self.turnPlayer == 1 and self.aiMove == (1, 1)):
            self.symbolSet.append(
                self.gameField.create_image(150, 150, anchor=CENTER,
                                            image=self.bigPics[self.tokens[self.turnPlayer][1]]))
            self.playBoard[1][1] = self.tokens[self.turnPlayer][0]
            self.playSound(self.stroke)
            self.turnMade()

        elif (self.turnPlayer == 0 and event.x > 100 and event.x < 200 < event.y and not self.tokenExists(
                self.symbolPos[5])) \
                or (self.turnPlayer == 1 and self.aiMove == (2, 1)):
            self.symbolSet.append(
                self.gameField.create_image(150, 250, anchor=CENTER,
                                            image=self.bigPics[self.tokens[self.turnPlayer][1]]))
            self.playBoard[2][1] = self.tokens[self.turnPlayer][0]
            self.playSound(self.stroke)
            self.turnMade()

        # Kontrolle rechte Spalte
        elif (self.turnPlayer == 0 and event.x > 200 and event.y < 100 and not self.tokenExists(self.symbolPos[6])) \
                or (self.turnPlayer == 1 and self.aiMove == (0, 2)):
            self.symbolSet.append(
                self.gameField.create_image(250, 50, anchor=CENTER,
                                            image=self.bigPics[self.tokens[self.turnPlayer][1]]))
            self.playBoard[0][2] = self.tokens[self.turnPlayer][0]
            self.playSound(self.stroke)
            self.turnMade()

        elif (self.turnPlayer == 0 and event.x > 200 > event.y and event.y > 100 and not self.tokenExists(
                self.symbolPos[7])) \
                or (self.turnPlayer == 1 and self.aiMove == (1, 2)):
            self.symbolSet.append(
                self.gameField.create_image(250, 150, anchor=CENTER,
                                            image=self.bigPics[self.tokens[self.turnPlayer][1]]))
            self.playBoard[1][2] = self.tokens[self.turnPlayer][0]
            self.playSound(self.stroke)
            self.turnMade()

        elif (self.turnPlayer == 0 and event.x > 200 and event.y > 200 and not self.tokenExists(self.symbolPos[8])) \
                or (self.turnPlayer == 1 and self.aiMove == (2, 2)):
            self.symbolSet.append(
                self.gameField.create_image(250, 250, anchor=CENTER,
                                            image=self.bigPics[self.tokens[self.turnPlayer][1]]))
            self.playBoard[2][2] = self.tokens[self.turnPlayer][0]
            self.playSound(self.stroke)
            self.turnMade()

    # Token wird auf Spielfeld gesetzt und Zug weitergegeben
    def player(self, event):

        #### Player turn
        if self.turnPlayer == 0:

            self.drawToken(event)

            # Debug Printout Spielarray
            for i in range(len(self.symbolSet)):
                print(self.gameField.coords(self.symbolSet[i]))

            for token in self.playBoard:
                print(token)
            print(self.turnPlayer)

            print("clicked at", event.x, event.y)

            # # Player WinCheck
            self.winCheck()

        self.kiMove(event)

    def kiMove(self, event):
        #### AI Turn
        if self.turnPlayer == 1:
            msg.showinfo(" KI Zug! ", " Die KI macht ihren Zug! ")
            self.curDepth = -1
            player = 1
            self.aiMove = self.minimax(player, self.playBoard).index
            print(self.aiMove)
            self.drawToken(event)

            # # AI Wincheck
            self.winCheck()

    # Setting up next Turn
    def turnMade(self):
        if self.turnPlayer == 0:
            self.turnPlayer += 1
        else:
            self.turnPlayer = 0

    def _nextplayer(self, player):
        if player == 1:
            player = 0
        else:
            player = 1

        return player

    # Funktion kalkuliert den besten Zug für die KI
    def minimax(self, player, board):

        # Grenze für die Rekursionstiefe
        self.curDepth += 1
        print(self.curDepth)
        if self.curDepth > self.maxDepth:
            if player == 0:
                move = Move()
                move.score = -10000
                return move
            elif player == 1:
                move = Move()
                move.score = 10000
                return move

        emptyField = []

        # Checking for empty fields
        for y in range(len(board)):
            for x in range(len(board)):
                if board[y][x] == " ":
                    emptyField.append((y, x))

        move = Move()
        # Checking for terminal states
        if self.threeInRow(board) and self._nextplayer(player) == 1:
            move.score = 10
            return move
        elif self.threeInRow(board) and self._nextplayer(player) == 0:
            move.score = -10
            return move
        elif len(emptyField) == 0:
            move.score = 0
            return move

        moves = []

        # plotting the next turn
        for field in emptyField:
            move = Move()
            fieldNew = copy.deepcopy(board)
            move.index = field
            fieldNew[field[0]][field[1]] = self.tokens[player][0]
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

    # KI starts the Game
    def _kiStart(self):
        self.turnPlayer = 1
        self._start()
        self.kiMove(event=1)

    def _start(self):
        self.tokenSelector.destroy()
        self.startPlay.grid_forget()
        if self.p1token.get() == 0:
            self.tokens.append(("X", 0))
            self.tokens.append(("O", 1))
            print(self.tokens)

        else:
            self.tokens.append(("O", 1))
            self.tokens.append(("X", 0))
        self.maxDepth = self.difSet.get()

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

        self.gameField.bind("<Button-1>", self.player)

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

            # Frame für Radiobuttons und Labels
            selectorFrame = tk.LabelFrame(self.tokenSelector, text=" Einstellungen ", borderwidth=0)
            selectorFrame.grid(column=0, row=0)

            nameToken = ["Tic", "Tac"]

            labelP1 = tk.Label(selectorFrame, text=" Spieler 1 ")
            labelP1.grid(column=0, row=0)

            # Spielsteinwahl Spieler 1
            self.p1token = tk.IntVar()
            self.p1token.set(0)
            for col in range(2):
                p1select = tk.Radiobutton(selectorFrame, text=nameToken[col], image=self.smallPics[col],
                                          variable=self.p1token, value=col, compound="right", command=self._radCallP1)
                p1select.grid(column=col, row=1)

            labelP2 = tk.Label(selectorFrame, text=" Spieler 2 (Bot) ")
            labelP2.grid(column=0, row=2)

            # Spielsteinwahl Spieler 2
            self.p2token = tk.IntVar()
            self.p2token.set(1)
            for col in range(2):
                p2select = tk.Radiobutton(selectorFrame, text=nameToken[col], image=self.smallPics[col],
                                          variable=self.p2token, value=col, compound="right", command=self._radCallP2)
                p2select.grid(column=col, row=3)

            # KI Intelligenz Slider
            self.difSet = tk.IntVar()
            self.difSet.set(1)
            difficulty = tk.Scale(self.tokenSelector, label=" Schwierigkeitsgrad ", variable=self.difSet, from_=1, to=30000, orient=HORIZONTAL,
                                       length=150, resolution=100, tickinterval=30000, showvalue = 0)
            difficulty.grid(column=0, row=2, padx=8, pady=8)

            tk.Button(self.tokenSelector, text=" Ich fange an ", image=self.smallPics[3], compound="left",
                      width=150, command=self._start).grid(column=0, row=4, padx=4, pady=4)
            tk.Button(self.tokenSelector, text=" Die KI fängt an " , image=self.smallPics[2], compound="left",
                      width=150, command=self._kiStart).grid(column=0, row=5, padx=4, pady=4)


# Instanz MainGame wird erstellt und Spiel gestartet
game = MainGame()

game.root.mainloop()
