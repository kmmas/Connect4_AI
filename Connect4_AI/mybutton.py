import tkinter as tk
from tkinter import font
from typing import Literal, TypedDict, Callable


class Borders(TypedDict):
    top: int
    bottom: int
    left: int
    right: int


class ButtonStyle(TypedDict):
    shape: Literal["rect", "circle"]
    width: int
    height: int
    cornerRadius: int
    shadowLength: int
    shadowHasBorder: bool
    borders: Borders | None
    buttonColor: str
    textColor: str
    buttonBorderColor: str
    shadowColor: str
    shadowBorderColor: str
    font: font.Font
    padx: int
    pady: int
    justify: Literal["center", "left", "right"]
    resize: Literal["scale", "redraw"]


class MyButton(tk.Canvas):
    def __init__(
        self,
        master,
        shape: Literal["rect", "circle"] = "rect",
        width: int = 100,
        height: int = 100,
        cornerRadius: int = 0,
        shadowLength: int = 0,
        shadowHasBorder: bool = True,
        borders: Borders = {},
        buttonColor: str = "#e7e3db",
        textColor: str = "black",
        buttonBorderColor: str = "black",
        shadowColor: str = "black",
        shadowBorderColor: str = "black",
        txt: str = "",
        font: font.Font = (None, 10),
        padx: int = 0,
        pady: int = 0,
        justify: Literal["center", "left", "right"] = "center",
        resize: Literal["scale", "redraw"] = "redraw",
        command: Callable[[], None] = None,
        hover: bool = False,
        hoverStyle: ButtonStyle = None,
        enterCommand: Callable[[], None] = None,
        leaveCommand: Callable[[], None] = None,
        disabledStyle: ButtonStyle = {},
    ):
        super().__init__(master=master, width=width, height=height)
        self.config(highlightthickness=0, bd=0, bg=self.master["bg"])
        self.shape = shape
        self.defaultWidth = width
        self.defaultHeight = height
        self.width = width
        self.height = height
        self.cornerRadius = cornerRadius
        self.shadowLength = shadowLength
        self.shadowHasBorder = shadowHasBorder
        self.borders: Borders = {"top": 0, "bottom": 0, "left": 0, "right": 0} | borders
        self.buttonColor = buttonColor
        self.textColor = textColor
        self.buttonBorderColor = buttonBorderColor
        self.shadowColor = shadowColor
        self.shadowBorderColor = shadowBorderColor
        self.txt = txt
        self.font = font
        self.padx = padx
        self.pady = pady
        self.justify = justify
        self.resizeMode = resize
        self.command = command
        self.hover = hover
        self.hoverStyle = hoverStyle
        self.enterCommand = enterCommand
        self.leaveCommand = leaveCommand
        self.disabled = False
        self.disabledStyle: ButtonStyle = {
            "buttonColor": "#e5e5e5",
            "textColor": "#aeaeae",
            "shadowLength": 0,
        } | disabledStyle
        self.currentHover = False
        self.hovering = False
        self.calculateDimensions()
        self.drawShadowBorders()
        self.drawShadow()
        self.drawButtonBorders()
        self.drawButton()
        self.drawText()
        self.tag_bind("button", "<Button-1>", self.onClick)
        self.tag_bind("button", "<ButtonRelease-1>", self.onRelease)
        self.tag_bind("button", "<Enter>", self.onEnter)
        self.tag_bind("button", "<Leave>", self.onLeave)
        self.bind("<Configure>", self.resize)
        self.bind("<Unmap>", self.onUnmap)

    def onUnmap(self, event):
        if self.hovering:
            self.leaveCommand()

    def onClick(self, event: tk.Event):
        if self.disabled:
            return
        self.move("button", 0, self.shadowLength)

    def onRelease(self, event: tk.Event):
        if self.disabled:
            return
        self.move("button", 0, -self.shadowLength)
        if self.command is not None:
            self.command()

    def onEnter(self, event: tk.Event):
        if self.hover and not self.disabled:
            self.hovering = True
            if self.hoverStyle is not None:
                self.savedStyle = self.getStyle()
                self.applyStyle(self.hoverStyle)
                self.currentHover = True
            if self.enterCommand is not None:
                self.enterCommand()

    def onLeave(self, event: tk.Event):
        if self.hover and not self.disabled:
            self.hovering = False
            if self.hoverStyle is not None:
                self.applyStyle(self.savedStyle)
                self.currentHover = False
            if self.leaveCommand is not None:
                self.leaveCommand()

    def calculateDimensions(self):
        currentFont = font.Font(font=self.font)
        txtlines = self.txt.split("\n")
        txtwidth = max([currentFont.measure(i) for i in txtlines])
        txtheight = currentFont.metrics("linespace") * len(txtlines)
        width = max(
            (self.borders["right"] + self.borders["right"] + txtwidth + 2 * self.padx),
            self.defaultWidth,
        )
        height = max(
            (
                self.borders["top"]
                + self.borders["bottom"]
                + txtheight
                + self.shadowLength
                + 2 * self.pady
            ),
            self.defaultHeight,
        )
        self.config(width=width, height=height)

    def drawShadowBorders(self, update=False):
        if not update:
            self.shadowBorder = self.createShape(
                0,
                self.shadowLength,
                self.width,
                self.height,
                fill=self.shadowBorderColor,
            )
        else:
            self.updateShape(
                self.shadowBorder,
                0,
                self.shadowLength,
                self.width,
                self.height,
            )

    def drawShadow(self, update=False):
        if not self.shadowHasBorder:
            borders: Borders = {"top": 0, "bottom": 0, "left": 0, "right": 0}
        else:
            borders = self.borders
        if not update:
            self.shadow = self.createShape(
                borders["left"],
                borders["top"] + self.shadowLength,
                self.width - borders["right"],
                self.height - borders["bottom"],
                fill=self.shadowColor,
            )
        else:
            self.updateShape(
                self.shadow,
                borders["left"],
                borders["top"] + self.shadowLength,
                self.width - borders["right"],
                self.height - borders["bottom"],
            )

    def drawButtonBorders(self, update=False):
        if not update:
            self.buttonBorder = self.createShape(
                0,
                0,
                self.width,
                self.height - self.shadowLength,
                fill=self.buttonBorderColor,
                tags="button",
            )
        else:
            self.updateShape(
                self.buttonBorder,
                0,
                0,
                self.width,
                self.height - self.shadowLength,
            )

    def drawButton(self, update=False):
        if not update:
            self.button = self.createShape(
                self.borders["left"],
                self.borders["top"],
                self.width - self.borders["right"],
                self.height - self.borders["bottom"] - self.shadowLength,
                fill=self.buttonColor,
                tags="button",
            )
        else:
            self.updateShape(
                self.button,
                self.borders["left"],
                self.borders["top"],
                self.width - self.borders["right"],
                self.height - self.borders["bottom"] - self.shadowLength,
            )

    def drawText(self, update=False):
        x = (self.borders["left"] + self.width - self.borders["right"]) / 2
        y = (
            self.borders["top"]
            + self.height
            - self.borders["bottom"]
            - self.shadowLength
        ) / 2
        if not update:
            self.text = self.create_text(
                x,
                y,
                text=self.txt,
                fill=self.textColor,
                anchor="center",
                tags="button",
                font=self.font,
                justify=self.justify,
            )
        else:
            self.coords(self.text, x, y)

    def setText(self, txt):
        self.txt = txt
        self.itemconfig(self.text, text=txt)
        self.calculateDimensions()

    def getPoints(self, x1, y1, x2, y2, radius):
        return [
            x1 + radius,
            y1,
            x1 + radius,
            y1,
            x2 - radius,
            y1,
            x2 - radius,
            y1,
            x2,
            y1,
            x2,
            y1 + radius,
            x2,
            y1 + radius,
            x2,
            y2 - radius,
            x2,
            y2 - radius,
            x2,
            y2,
            x2 - radius,
            y2,
            x2 - radius,
            y2,
            x1 + radius,
            y2,
            x1 + radius,
            y2,
            x1,
            y2,
            x1,
            y2 - radius,
            x1,
            y2 - radius,
            x1,
            y1 + radius,
            x1,
            y1 + radius,
            x1,
            y1,
        ]

    def create_round_rectangle(self, x1, y1, x2, y2, radius, **kwargs):
        points = self.getPoints(x1, y1, x2, y2, radius)
        return self.create_polygon(points, **kwargs, smooth=True)

    def createShape(self, x0, y0, x1, y1, fill, **kwargs):
        if self.shape == "rect":
            return self.create_round_rectangle(
                x0,
                y0,
                x1,
                y1,
                self.cornerRadius,
                fill=fill,
                outline="",
                width=0,
                **kwargs
            )
        if self.shape == "circle":
            return self.create_oval(
                x0, y0, x1, y1, fill=fill, outline="", width=0, **kwargs
            )

    def updateShape(self, tagOrId, x0, y0, x1, y1):
        if self.shape == "rect":
            self.coords(tagOrId, self.getPoints(x0, y0, x1, y1, self.cornerRadius))
        if self.shape == "circle":
            self.coords(tagOrId, x0, y0, x1, y1)

    def resize(self, event: tk.Event):
        if self.resizeMode == "scale":
            xscale = float(event.width) / self.width
            yscale = float(event.height) / self.height
            self.shadowLength *= yscale
            self.width = event.width
            self.height = event.height
            self.scale("all", 0, 0, xscale, yscale)

        if self.resizeMode == "redraw":
            self.width = event.width
            self.height = event.height
            self.updateDrawing()

    def updateDrawing(self):
        self.drawShadowBorders(update=1)
        self.drawShadow(update=1)
        self.drawButtonBorders(update=1)
        self.drawButton(update=1)
        self.drawText(update=1)

    def applyStyle(self, style: ButtonStyle):
        updateNeeded = False
        if "width" in style:
            self.defaultWidth = style["width"]
            self.calculateDimensions()

        if "height" in style:
            self.defaultHeight = style["height"]
            self.calculateDimensions()

        if "cornerRadius" in style:
            updateNeeded = True if self.shape == "rect" else False
            self.cornerRadius = style["cornerRadius"]

        if "shadowLength" in style:
            updateNeeded = True
            self.shadowLength = style["shadowLength"]

        if "shadowHasBorder" in style:
            updateNeeded = True
            self.shadowHasBorder = style["shadowHasBorder"]

        if "borders" in style:
            updateNeeded = True
            self.borders = style["borders"]

        if "buttonColor" in style:
            self.buttonColor = style["buttonColor"]
            self.itemconfig(self.button, fill=self.buttonColor)

        if "textColor" in style:
            self.textColor = style["textColor"]
            self.itemconfig(self.text, fill=self.textColor)

        if "buttonBorderColor" in style:
            self.buttonBorderColor = style["buttonBorderColor"]
            self.itemconfig(self.buttonBorder, fill=self.buttonBorderColor)

        if "shadowColor" in style:
            self.shadowColor = style["shadowColor"]
            self.itemconfig(self.shadow, fill=self.shadowColor)

        if "shadowBorderColor" in style:
            self.shadowBorderColor = style["shadowBorderColor"]
            self.itemconfig(self.shadowBorder, fill=self.shadowBorderColor)

        if "font" in style:
            self.font = style["font"]
            self.itemconfig(self.text, font=self.font)
            self.calculateDimensions()

        if "padx" in style:
            self.padx = style["padx"]
            self.calculateDimensions()

        if "pady" in style:
            self.pady = style["pady"]
            self.calculateDimensions()

        if "justify" in style:
            self.justify = style["justify"]
            self.itemconfig(self.text, justify=self.justify)

        if updateNeeded:
            self.updateDrawing()

    def getStyle(self):
        currentStyle: ButtonStyle = {
            "shape": self.shape,
            "width": self.defaultWidth,
            "height": self.defaultHeight,
            "cornerRadius": self.cornerRadius,
            "shadowLength": self.shadowLength,
            "shadowHasBorder": self.shadowHasBorder,
            "borders": self.borders,
            "buttonColor": self.buttonColor,
            "textColor": self.textColor,
            "buttonBorderColor": self.buttonBorderColor,
            "shadowColor": self.shadowColor,
            "shadowBorderColor": self.shadowBorderColor,
            "font": self.font,
            "padx": self.padx,
            "pady": self.pady,
            "justify": self.justify,
            "resize": self.resizeMode,
        }
        return currentStyle

    def disable(self):
        if self.disabled:
            return
        if not self.currentHover:
            self.savedStyle = self.getStyle()
        self.applyStyle(self.disabledStyle)
        self.disabled = True

    def enable(self):
        if not self.disabled:
            return
        self.applyStyle(self.savedStyle)
        self.disabled = False
