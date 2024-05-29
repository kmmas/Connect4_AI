import time
import tkinter as tk
from tkinter.font import Font
from Prouning import minMaxWithProuning
from State import State
from heuristic import eval_score_four_consecutive
from methods import minMax
from mybutton import MyButton
from constant import *


class Connect4(tk.Canvas):
    def __init__(
        self,
        master,
        rowSize: int = 7,
        columnSize: int = 6,
        holeSize: int = 50,
        padx: int = 10,
        pady: int = 10,
        background: str = "blue",
        emptyHole: str = "white",
        player1: str = "red",
        player2: str = "yellow",
    ):
        super().__init__(
            master=master,
            background=background,
            highlightthickness=0,
            bd=0,
            width=((rowSize * holeSize) + (rowSize + 1) * padx),
            height=((columnSize * holeSize) + (columnSize + 1) * pady),
        )

        self.drawnState = []
        self.player1 = player1
        self.player2 = player2

        for i in range(rowSize):
            self.drawnState.append([])
            for j in range(columnSize):
                tmp = self.create_oval(
                    padx * (i + 1) + i * holeSize,
                    pady * (j + 1) + j * holeSize,
                    padx * (i + 1) + (i + 1) * holeSize,
                    pady * (j + 1) + (j + 1) * holeSize,
                    fill=emptyHole,
                    width=0,
                )
                self.drawnState[i].append(tmp)

    def makeAction(self, row: int, column: int, isPlayer1: bool):
        color = self.player1 if isPlayer1 else self.player2
        self.itemconfig(self.drawnState[column][row], fill=color)


class drawnState(tk.Frame):
    def __init__(
        self,
        master,
        state: State,
        active: bool = False,
        isMin: bool = True,
        background: str = "green",
        gameBackground: str = "blue",
        emptyHole: str = "white",
        player1: str = "red",
        player2: str = "yellow",
        border: str = "black",
    ):
        super().__init__(master, padx=5, pady=5, background=background)
        self.state = state
        self.isMin = isMin
        self.background = background
        self.gameBackground = gameBackground
        self.player1 = player1
        self.player2 = player2
        self.emptyHole = emptyHole
        self.border = border
        self.connect4 = Connect4(
            self,
            holeSize=10,
            padx=2,
            pady=2,
            background=gameBackground,
            emptyHole=emptyHole,
            player1=player1,
            player2=player2,
        )
        for i in range(self.state.rows):
            for j in range(self.state.cols):
                if self.state.state_board[i][j] == PLAYER:
                    self.connect4.makeAction(i, j, True)
                elif self.state.state_board[i][j] == AI:
                    self.connect4.makeAction(i, j, False)
        self.connect4.pack(anchor="center", expand=True)
        txt = "trimmed" if state.trimmed else str(state.value)
        tk.Label(self, text=txt, background=background).pack()
        if len(state.children) > 0:
            turn = "MIN" if isMin else "MAX"
            tk.Label(
                self,
                text=turn,
                foreground=(player2 if isMin else player1),
                background=background,
            ).pack()
        if active:
            self.connect4.bind("<Button-1>", self.onClick)

    def onClick(self, event):
        prev = self.master
        prev.pack_forget()
        tmp = TreeFrame(
            master=prev.master,
            state=self.state,
            previousFrame=prev,
            isMin=self.isMin,
            background=self.background,
            border=self.border,
            player1=self.player1,
            player2=self.player2,
            gameBackground=self.gameBackground,
            emptyHole=self.emptyHole,
        )
        tmp.pack(anchor="center")


class TreeFrame(tk.Frame):
    def __init__(
        self,
        master,
        state: State,
        previousFrame: tk.Frame = None,
        isMin: bool = True,
        background: str = "green",
        gameBackground: str = "blue",
        emptyHole: str = "white",
        player1: str = "red",
        player2: str = "yellow",
        border: str = "black",
    ):
        super().__init__(master=master, background=border)

        length = len(state.children)
        self.rowconfigure([0, 1], weight=1)
        self.columnconfigure(list(range(max(1, length))), weight=1)
        origin = drawnState(
            self,
            state=state,
            isMin=isMin,
            background=background,
            gameBackground=gameBackground,
            emptyHole=emptyHole,
            player1=player1,
            player2=player2,
            border=border,
        )
        origin.grid(
            row=0, column=0, columnspan=max(1, length), sticky="NSEW", padx=2, pady=2
        )

        if length > 0:
            i = 0
            for child in state.children:
                drawnState(
                    self,
                    state=child,
                    active=True,
                    isMin=(not isMin),
                    background=background,
                    gameBackground=gameBackground,
                    emptyHole=emptyHole,
                    player1=player1,
                    player2=player2,
                    border=border,
                ).grid(
                    row=1,
                    column=i,
                    sticky="NSEW",
                    padx=2,
                    pady=2,
                )
                i += 1
        self.previousFrame = previousFrame
        if self.previousFrame is not None:
            origin.connect4.bind("<Button-1>", self.goBack)

    def goBack(self, event):
        if self.previousFrame is not None:
            self.destroy()
            self.previousFrame.pack(anchor="center")
            self.master.update()


class GameFrame(tk.Frame):
    connect4: Connect4
    buttons: list[MyButton]
    buttonsFrame: tk.Frame
    holeSize: int
    padx: int
    pady: int
    topEffect: tk.Canvas
    player1: str
    scoreFrame: tk.Frame
    font: Font
    backButton: MyButton
    treeButton: MyButton
    previousFrame: tk.Frame
    state: State
    messageBox: tk.Label
    topFrame: tk.Frame

    def __init__(
        self,
        master,
        previousFrame: tk.Frame = None,
        background: str = "#DDEBE6",
        outerPadx: int = 10,
        outerPady: int = 10,
        rowSize: int = 7,
        columnSize: int = 6,
        holeSize: int = 50,
        padx: int = 10,
        pady: int = 10,
        emptyHole: str = "#DDEBE6",
        player1: str = "#fc7e68",
        player2: str = "#254689",
        gameBackground: str = "#5f9ea0",
        withPruning: bool = False,
        maxDepth: int = 3,
    ):
        super().__init__(
            master=master,
            background=background,
            padx=outerPadx,
            pady=outerPady,
        )
        self.previousFrame = previousFrame
        self.holeSize = holeSize
        self.padx = padx
        self.pady = pady
        self.player1 = player1
        self.player2 = player2
        self.emptyHole = emptyHole
        self.background = background
        self.gameBackground = gameBackground

        self.font = Font(family="Yu Gothic UI Semibold", size=20, weight="bold")
        self.previousState = None
        self.treeIsOpen = False
        self.tree = None
        self.state = State(
            [
                ["-", "-", "-", "-", "-", "-", "-"],
                ["-", "-", "-", "-", "-", "-", "-"],
                ["-", "-", "-", "-", "-", "-", "-"],
                ["-", "-", "-", "-", "-", "-", "-"],
                ["-", "-", "-", "-", "-", "-", "-"],
                ["-", "-", "-", "-", "-", "-", "-"],
            ]
        )
        self.withPruning = withPruning
        self.maxDepth = maxDepth

        self.connect4 = Connect4(
            master=self,
            rowSize=rowSize,
            columnSize=columnSize,
            holeSize=holeSize,
            padx=padx,
            pady=pady,
            emptyHole=emptyHole,
            player1=player1,
            player2=player2,
            background=gameBackground,
        )

        self.topEffect = tk.Canvas(
            self,
            background=background,
            width=self.connect4["width"],
            height=holeSize + pady,
            highlightthickness=0,
            bd=0,
        )

        self.scoreFrame = tk.Frame(self, background=background)

        self.playerLabel = tk.Label(
            self.scoreFrame,
            background=background,
            text="Player score: 0",
            foreground=gameBackground,
            font=self.font,
        )

        self.computerLabel = tk.Label(
            self.scoreFrame,
            background=background,
            text="Computer score: 0",
            foreground=gameBackground,
            font=self.font,
        )
        self.topFrame = tk.Frame(self, background=background)
        self.backButton = MyButton(
            self.topFrame,
            font=self.font,
            txt="\u276E",
            buttonColor=gameBackground,
            textColor=background,
            width=60,
            height=60,
            cornerRadius=20,
            hover=True,
            command=self.goBack,
            enterCommand=lambda: self.backButton.setText("\u276E go back"),
            leaveCommand=lambda: self.backButton.setText("\u276E"),
            padx=10,
            pady=10,
        )

        self.treeButton = MyButton(
            self.topFrame,
            font=self.font,
            txt="show tree",
            buttonColor=gameBackground,
            textColor=background,
            width=60,
            height=60,
            cornerRadius=20,
            hover=True,
            command=self.showTree,
            padx=10,
            pady=10,
        )

        self.messageBox = tk.Label(
            self,
            background=background,
            text="AI is thinking...",
            foreground=gameBackground,
            font=self.font,
        )

        valdiation = self.register(self.validateInput)

        self.gridFrame = tk.Frame(self, background=background, padx=5, pady=5)
        self.gridFrame.rowconfigure([0, 1, 2], weight=1)
        self.gridFrame.columnconfigure([0, 1], weight=1)

        self.buttonsFrame = tk.Frame(
            self.gridFrame, background=background, padx=padx // 2
        )
        self.buttons = []

        for i in range(rowSize):
            tmp = MyButton(
                self.buttonsFrame,
                width=holeSize,
                height=holeSize,
                txt=str(i),
                font=self.font,
                buttonColor=background,
                hover=True,
                enterCommand=lambda col=i: self.hover(col),
                leaveCommand=self.leave,
                command=lambda col=i: self.action(col),
                hoverStyle={"textColor": player1},
            )
            tmp.pack(padx=padx // 2, anchor="center", side="left")
            self.buttons.append(tmp)

        self.pruningLabel = tk.Label(
            self.gridFrame,
            foreground=gameBackground,
            background=background,
            text="alpha-beta pruning",
            font=self.font,
        )

        self.depthLabel = tk.Label(
            self.gridFrame,
            foreground=gameBackground,
            background=background,
            text="depth of the tree",
            font=self.font,
        )

        self.onStyle = {"buttonColor": "#fc7e68", "shadowColor": "#DD6350"}
        self.offStyle = {"buttonColor": "#5f9ea0", "shadowColor": "#3F7E80"}
        style = self.onStyle if self.withPruning else self.offStyle
        self.pruningButton = MyButton(
            self.gridFrame,
            textColor="white",
            txt="ON" if self.withPruning else "OFF",
            shadowLength=5,
            cornerRadius=20,
            width=100,
            height=0,
            font=self.font,
            padx=5,
            pady=5,
            command=self.clickPruning,
            **style,
        )

        self.inputBox = tk.Entry(
            self.gridFrame,
            background="white",
            font=self.font,
            foreground=gameBackground,
            width=2,
            justify="center",
            relief="flat",
            highlightbackground=background,
            highlightcolor=gameBackground,
            highlightthickness=2,
            validate="key",
            validatecommand=(valdiation, "%P"),
        )
        self.inputBox.insert(0, str(self.maxDepth))
        self.inputBox.bind("<Return>", self.saveDepth)
        self.backButton.pack(side="left")
        self.treeButton.pack(side="right")
        self.topFrame.pack(fill="both")
        self.playerLabel.pack(anchor="w")
        self.computerLabel.pack(anchor="w")
        self.scoreFrame.pack(anchor="w", pady=10)
        self.topEffect.pack()
        self.connect4.pack()
        self.buttonsFrame.grid(row=0, column=0, columnspan=2)
        self.pruningLabel.grid(row=1, column=0, sticky="w", pady=2)
        self.depthLabel.grid(row=2, column=0, sticky="w", pady=2)
        self.pruningButton.grid(row=1, column=1, sticky="NSEW", pady=2)
        self.inputBox.grid(row=2, column=1, sticky="NSEW", pady=2)
        self.gridFrame.pack()

    def showTree(self):
        if self.treeIsOpen:
            self.tree.destroy()
            self.treeIsOpen = False
            self.treeButton.setText("show tree")
        elif self.previousState is not None:
            self.tree = tk.Frame(self.master, background=self.background)
            TreeFrame(
                self.tree,
                self.previousState,
                background=self.background,
                gameBackground=self.gameBackground,
                emptyHole=self.emptyHole,
                player1=self.player1,
                player2=self.player2,
                border=self.background,
            ).pack(anchor="center")
            self.tree.pack(side="left", anchor="center")
            self.treeIsOpen = True
            self.treeButton.setText("hide tree")

    def clickPruning(self):
        if self.withPruning:
            self.pruningButton.applyStyle(self.offStyle)
            self.pruningButton.setText("OFF")
            self.withPruning = False
        else:
            self.pruningButton.applyStyle(self.onStyle)
            self.pruningButton.setText("ON")
            self.withPruning = True

    def saveDepth(self, event):
        text = self.inputBox.get()
        if len(text) == 0:
            self.inputBox.insert(0, str(self.maxDepth))
        elif int(text) == 0:
            self.inputBox.delete(0, "end")
            self.inputBox.insert(0, str(self.maxDepth))
        else:
            self.maxDepth = int(text)
        self.master.focus_set()

    def displayDepth(self):
        self.inputBox.delete(0, "end")
        self.inputBox.insert(0, str(self.maxDepth))

    def validateInput(self, newText: str):
        if newText.isdigit():
            self.inputBox.config(background="white")
            return True
        if newText == "":
            return True
        return False

    def action(self, column):
        self.displayDepth()
        self.master.focus_set()
        row = self.state.addToColumn(column, PLAYER)
        if row < 0:
            print("error")
        else:
            self.connect4.makeAction(row, column, True)
            self.pack_propagate(False)
            self.gridFrame.pack_forget()
            self.messageBox.pack()
            self.update()
            if not self.state.isTerminalState():
                self.aiTurn()
            else:
                print("finished")
                self.announceWinner()

    def updateScore(self):
        player = eval_score_four_consecutive(self.state.state_board, PLAYER)
        computer = eval_score_four_consecutive(self.state.state_board, AI)
        self.playerLabel.config(text="Player score: " + str(player))
        self.computerLabel.config(text="Computer score: " + str(computer))

    def announceWinner(self):
        self.gridFrame.destroy()
        player = eval_score_four_consecutive(self.state.state_board, PLAYER)
        computer = eval_score_four_consecutive(self.state.state_board, AI)
        if player > computer:
            self.messageBox.configure(text="winner is player")
            self.messageBox.pack()
        elif player < computer:
            self.messageBox.configure(text="winner is computer")
            self.messageBox.pack()
        else:
            self.messageBox.configure(text="it is a tie")
            self.messageBox.pack()

    def aiTurn(self):
        self.previousState = self.state
        if self.withPruning:
            method = minMaxWithProuning
            print("starting with pruning, maxDepth = " + str(self.maxDepth))
        else:
            method = minMax
            print("starting without pruning, maxDepth = " + str(self.maxDepth))

        start = time.time()
        tmp = method(self.state, self.maxDepth, AI)
        end = time.time()
        print(f"time taken = {end -start}")
        print(f"expanded nodes = {tmp[2]}")
        self.state = tmp[1]
        row, col = self.state.generatingAction
        self.connect4.makeAction(row, col, False)
        self.updateScore()
        if not self.state.isTerminalState():
            self.pack_propagate(True)
            self.messageBox.pack_forget()
            self.gridFrame.pack()
        else:
            print("finished")
            self.announceWinner()

    def hover(self, i):
        startx = self.padx * (i + 1) + i * self.holeSize
        self.save = self.topEffect.create_oval(
            startx,
            0,
            startx + self.holeSize,
            self.holeSize,
            width=0,
            fill=self.player1,
            tags="toDelete",
        )

    def leave(self):
        for i in self.topEffect.find_withtag("toDelete"):
            self.topEffect.delete(i)

    def disable(self):
        for button in self.buttons:
            button.disable()

    def enable(self):
        for button in self.buttons:
            button.enable()

    def goBack(self):
        if self.previousFrame is not None:
            self.master.destroy()
            self.previousFrame.pack(fill="both", expand=True, anchor="center")


if __name__ == "__main__":
    x = tk.Tk()
    x.title("AI assignment 2")
    x.config(background="#DDEBE6")
    y = tk.Frame(x, background="#DDEBE6")
    y.pack(anchor="center")
    GameFrame(y).pack(anchor="center", expand=False, side="left")
    x.update()
    x.minsize(width=x.winfo_width(), height=x.winfo_height())
    print(x.winfo_width(), x.winfo_height())
    x.mainloop()
