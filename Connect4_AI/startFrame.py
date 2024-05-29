import tkinter as tk
from tkinter.font import Font
from gameFrames import GameFrame
from mybutton import ButtonStyle, MyButton


class StartFrame(tk.Frame):
    title: tk.Label
    startButton: MyButton
    gridFrame: tk.Frame
    pruningButton: MyButton
    pruningLabel: tk.Label
    pruning: bool
    inputBox: tk.Entry
    depthLabel: tk.Label
    font: Font
    onStyle: ButtonStyle
    offStyle: ButtonStyle

    def __init__(
        self, master, foreground: str = "#DDEBE6", background: str = "#5f9ea0"
    ):
        super().__init__(master=master, background=background, padx=10, pady=10)

        self.font = Font(family="Yu Gothic UI Semibold", size=25, weight="bold")
        self.pruning = True

        titleFont = self.font.copy()
        titleFont.config(size=40, weight="bold")

        valdiation = self.register(self.validateInput)

        self.onStyle = {"buttonColor": "#fc7e68", "shadowColor": "#DD6350"}
        self.offStyle = {"buttonColor": "#5f9ea0", "shadowColor": "#3F7E80"}

        self.title = tk.Label(
            self,
            text="Connect 4",
            background=background,
            foreground=foreground,
            font=titleFont,
        )

        self.gridFrame = tk.Frame(self, background=foreground, padx=5, pady=5)
        self.gridFrame.rowconfigure([0, 1, 2], weight=1)
        self.gridFrame.columnconfigure([0, 1], weight=1)

        self.pruningLabel = tk.Label(
            self.gridFrame,
            foreground=background,
            background=foreground,
            text="alpha-beta pruning",
            font=self.font,
        )

        self.depthLabel = tk.Label(
            self.gridFrame,
            foreground=background,
            background=foreground,
            text="depth of the tree",
            font=self.font,
        )

        self.pruningButton = MyButton(
            self.gridFrame,
            buttonColor="#fc7e68",
            textColor="white",
            txt="ON",
            shadowLength=5,
            shadowColor="#DD6350",
            cornerRadius=20,
            width=100,
            height=0,
            font=self.font,
            padx=5,
            pady=5,
            command=self.clickPruning,
        )

        self.inputBox = tk.Entry(
            self.gridFrame,
            background="white",
            font=self.font,
            foreground=background,
            width=2,
            justify="center",
            relief="flat",
            highlightbackground=foreground,
            highlightcolor=background,
            highlightthickness=2,
            validate="key",
            validatecommand=(valdiation, "%P"),
        )

        self.startButton = MyButton(
            self.gridFrame,
            buttonColor=background,
            textColor=foreground,
            shadowColor="#3F7E80",
            shadowLength=7,
            txt="start the game",
            cornerRadius=70,
            height=70,
            width=70,
            font=self.font,
            padx=20,
            pady=10,
            command=self.startGame,
        )

        self.title.pack(pady=5, anchor="center", expand=True)

        self.pruningLabel.grid(row=0, column=0, sticky="w", pady=5)
        self.depthLabel.grid(row=1, column=0, sticky="w", pady=5)
        self.pruningButton.grid(row=0, column=1, sticky="w", pady=5, padx=5)
        self.inputBox.grid(row=1, column=1, sticky="NSWE", pady=5, padx=5)
        self.startButton.grid(row=2, column=0, columnspan=2, pady=10)

        self.gridFrame.pack(anchor="center", expand=True)

    def clickPruning(self):
        if self.pruning:
            self.pruningButton.applyStyle(self.offStyle)
            self.pruningButton.setText("OFF")
            self.pruning = False
        else:
            self.pruningButton.applyStyle(self.onStyle)
            self.pruningButton.setText("ON")
            self.pruning = True

    def validateInput(self, newText: str):
        if newText.isdigit():
            self.inputBox.config(background="white")
            return True
        if newText == "":
            return True
        return False

    def startGame(self):
        text = self.inputBox.get()
        if not text.isdigit():
            self.inputBox.config(background="#FF7F7F")
        elif int(text) == 0:
            self.inputBox.config(background="#FF7F7F")
        else:
            tmpFrame = tk.Frame(self.master, background="#DDEBE6")
            GameFrame(
                tmpFrame,
                previousFrame=self,
                withPruning=self.pruning,
                maxDepth=int(text),
            ).pack(anchor="center", expand=False, side="left")
            self.pack_forget()
            tmpFrame.pack(anchor="center", expand=False)


x = tk.Tk()
x.title("AI assignment 2")
x.config(background="#DDEBE6")
StartFrame(x).pack(anchor="center", expand=True, fill="both")
x.update()
x.minsize(450, 793)
x.mainloop()
