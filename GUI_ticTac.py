import copy
import tkinter as tk
from random import choice
from threading import Thread
from tkinter import messagebox as msg, ttk, CENTER, HORIZONTAL, INSERT, WORD, DISABLED

import pygame
from PIL import ImageTk, Image

# Move class to store index and score for minimax
class Move:
    index = []
    score = 0


class MainGame:
# # # Initialising important variables

    # # GUI-variables
    path = ["Data/Tac.png", "Data/Tic.png", "Data/bot.png", "Data/man.png"]
    stroke = ["Data/stroke1.wav", "Data/stroke2.wav", "Data/stroke3.wav"]
    winSound = ["Data/win.wav"]
    bigPics = []
    smallPics = []

    # Child window control variables
    gameSetup = None
    gameRules = None

    # # Game logic variables
    tokens = []  # Pos 0 Player 1 Token; Pos 1 Player 2 Token
    turnPlayer = 0  # 0 => Spieler 1 am Zug, 1 => Spieler 2 am Zug
    symbolSet = [[0, 0]]
    symbolPos = [[50, 50], [50, 150], [50, 250], [150, 50], [150, 150], [150, 250], [250, 50], [250, 150], [250, 250]]
    playBoard = [[" " for i in range(3)] for i in range(3)]
    fc = 0
    aiMove = ()

    curDepth = -1
    maxDepth = 30000

    # Sound Initialisierung
    pygame.mixer.init()

# Init Game
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(" Tic Tac Toe O X ")
        self.root.resizable(False, False)
        img = tk.PhotoImage(file="Data/TicTacToe.png")
        self.root.tk.call("wm", "iconphoto", self.root._w, img)
        self.pictures()
        self.createGameField()
        self.mainMenu()
        self.startMini()
        self.gameLoad()

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


# # Game logic

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
            if msg.askyesno(" GEWONNEN! :)", "Du hast hat das Spiel gewonnen!\nNoch eine Runde?"):
                self._new()
            else:
                self._quit()
        else:
            if msg.askyesno(" Leider Verloren!!! ", "Leider hast du das Spiel verloren!\nNoch eine Runde?"):
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


    # Start a new game
    def _new(self):
        self.gameField.grid_forget()
        self.canvasFrame.grid_forget()
        self.createGameField()
        self.load.grid_forget()
        self.loading.grid_forget()
        self.symbolSet = [[0, 0]]
        self.playBoard = [[" " for i in range(3)] for i in range(3)]
        self.gameSetup = None
        self.tokens = []
        self.turnPlayer = 0
        self.setupWin()

    # Quit game, used in gameMenu and winMessages
    def _quit(self):
        self.root.quit()
        self.root.destroy()
        exit()

    def _about(self):
        msg.showinfo(" Über TicTacToe ", " Version: 1.0.0 190622 \nCreat0r: MadocMcGee")


# Minimax Pre-Load

    # setting up initMinimax as new Thread
    def startMini(self):
        self.run_load = Thread(target=self.initMinimax)
        self.run_load.setDaemon(True)
        self.run_load.start()
        print(self.run_load)

    # Starting Minimax during Init
    def initMinimax(self, player=1, board=[[" " for i in range(3)] for i in range(3)]):
        self.tokens = [("X", 0), ("O", 1)]
        self.minimax(player, board)

    # Updating Loading bar value
    def _progress(self, curValue):
        self.load["value"] = curValue

    # Updating Progressbar according to initMinimax
    def gameLoad(self):
        while self.curDepth < self.maxDepth + 15:
            curValue = self.curDepth
            self.load.after(10, self._progress(curValue))
            self.load.update()
        self.load.grid_forget()
        self.loading.grid_forget()

# Game window creation

    # Main gaming window
    def createGameField(self):
        # Erstellen des Canvas und des Frames
        self.canvasFrame = tk.LabelFrame(self.root, text=" Spielfeld ")
        self.canvasFrame.grid(column=0, row=0)
        self.gameField = tk.Canvas(self.canvasFrame, width=300, height=300, bg="white")
        self.gameField.grid(column=0, row=0)

        # Button für zum Spielbeginn erstellen
        self.startPlay = tk.Button(self.root, width=36, height=18, text=" SPIELEN ", command=self.setupWin)
        self.startPlay.grid(column=0, row=0)

        # LoadingBar
        self.load = ttk.Progressbar(self.root, length=240, mode="determinate")
        self.load.grid(column=0, row=0)
        self.load["maximum"] = 30000
        self.loading = tk.Label(self.root, text=" Lade Spiel... ")
        self.loading.grid(column=0, row=1)

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
        helpMenu = tk.Menu(menuBar, tearoff=0)

        menuBar.add_cascade(label="Spiel", menu=gameMenu)
        gameMenu.add_command(label=" Neues Spiel ", command=self._new)
        gameMenu.add_command(label=" Spiel beenden", command=self._quit)

        menuBar.add_cascade(label="Hilfe", menu=helpMenu)
        helpMenu.add_command(label=" Spielregel ", command=self.rulesWin)
        helpMenu.add_command(label=" Über ", command=self._about)


# game setup child window functions

    # prevents gamesetup win from closing
    def _on_closing(self):
        pass

    # Player 1 token selection Radiobuttons
    def _radCallP1(self):
        if self.p1token.get() == 0:
            self.p2token.set(1)
        else:
            self.p2token.set(0)

    # Player 2 token selection Radiobuttons
    def _radCallP2(self):
        if self.p2token.get() == 0:
            self.p1token.set(1)
        else:
            self.p1token.set(0)

    # KI starts the Game
    def _kiStart(self):
        self.turnPlayer = 1
        self._tokenStart()
        self.kiMove(event=1)

    # Setting up the tokens for game start
    def _tokenStart(self):
        self.gameSetup.destroy()
        self.startPlay.grid_forget()
        if self.p1token.get() == 0:
            self.tokens.append(("X", 0))
            self.tokens.append(("O", 1))
            print(self.tokens)

        else:
            self.tokens.append(("O", 1))
            self.tokens.append(("X", 0))
        self.maxDepth = self.difSet.get()


    # Game Setup Child window
    def setupWin(self):

        if self.gameSetup is None:
            self.gameSetup = tk.Toplevel()
            self.gameSetup.title(' Neues Spiel ')
            self.gameSetup.resizable(False, False)
            self.gameSetup.protocol("WM_DELETE_WINDOW", self._on_closing)

            # Frame for Player token selection
            selectorFrame = tk.LabelFrame(self.gameSetup, text=" Einstellungen ", borderwidth=0)
            selectorFrame.grid(column=0, row=0)

            nameToken = ["Tic", "Tac"]

            labelP1 = tk.Label(selectorFrame, text=" Spieler 1 ")
            labelP1.grid(column=0, row=0)

            # Token selection for Player 1
            self.p1token = tk.IntVar()
            self.p1token.set(0)
            for col in range(2):
                p1select = tk.Radiobutton(selectorFrame, text=nameToken[col], image=self.smallPics[col],
                                          variable=self.p1token, value=col, compound="right", command=self._radCallP1)
                p1select.grid(column=col, row=1)

            labelP2 = tk.Label(selectorFrame, text=" Spieler 2 (Bot) ")
            labelP2.grid(column=0, row=2)

            # Token selection Player 2
            self.p2token = tk.IntVar()
            self.p2token.set(1)
            for col in range(2):
                p2select = tk.Radiobutton(selectorFrame, text=nameToken[col], image=self.smallPics[col],
                                          variable=self.p2token, value=col, compound="right", command=self._radCallP2)
                p2select.grid(column=col, row=3)

            # AI difficulty slider
            self.difSet = tk.IntVar()
            self.difSet.set(1)
            difficulty = tk.Scale(self.gameSetup, label=" Schwierigkeitsgrad ", variable=self.difSet, from_=1,
                                  to=30000, orient=HORIZONTAL,
                                  length=150, resolution=100, tickinterval=30000, showvalue=0)
            difficulty.grid(column=0, row=2, padx=8, pady=8)

            tk.Button(self.gameSetup, text=" Ich fange an ", image=self.smallPics[3], compound="left",
                      width=150, command=self._tokenStart).grid(column=0, row=4, padx=4, pady=4)
            tk.Button(self.gameSetup, text=" Die KI fängt an ", image=self.smallPics[2], compound="left",
                      width=150, command=self._kiStart).grid(column=0, row=5, padx=4, pady=4)

    # Rules window closing Button
    def _rulesClose(self):
        self.gameRules.destroy()
        self.gameRules = None

    # Rules child window
    def rulesWin(self):
        if self.gameRules is None:
            self.gameRules = tk.Toplevel()
            self.gameRules.title(" Regeln TicTacToe ")
            self.gameRules.resizable(False, False)
            self.gameRules.protocol("WM_DELETE_WINDOW", self._on_closing)

            rules = tk.Text(self.gameRules, wrap=WORD, height= 15, width=35, font="Arial", spacing1=1)
            rules.grid(column=0, row=0)

            with open("Data/rules.txt", "r") as f:
                rules.insert(INSERT, f.read())
            rules.config(state=DISABLED)

            close = tk.Button(self.gameRules, text="Schließen", command=self._rulesClose)
            close.grid(column=0, row=1)

# Instanz MainGame wird erstellt und Spiel gestartet
game = MainGame()

# New thread for initMinimax
run_load = Thread(target=game.initMinimax)

game.root.mainloop()
