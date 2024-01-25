from tkinter import *
from tkinter.ttk import *
from enum import Enum

class Color(Enum):
    def __str__(self):
        return self.value

    DEFAULT = "SystemButtonFace"

    RED = "#dc3546"
    GREEN = "#28a745"
    LIGHTBLUE = "#9fc3fc"

class Layout(Enum):
    VERTICAL = "vertical"
    HORIZONTAL = "horizontal"

# Entry mit extrafunktionen
class ExtendedEntry(Entry):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.maxLenght = None

        self.textVar = StringVar()
        super().config(textvar = self.textVar)

        self.validate = "all"
        self.updateValidation()
        self.onValidChangeFunctions = []
        self.onInvalidChangeFunctions = []

        self.onChangeFunctions = []
        self.onChange = self.textVar.trace_variable("w", lambda name, mode, cbname: None)

        super().config(validatecommand = (super().register(self.check), "%d", "%i", "%P", "%s", "%S", "%v", "%V", "%W"))

    def checkValid(self, reason, i, newValue, s, change, v, event, W) -> bool:
        if reason == "1":
            if len(newValue) > self.maxLenght:
                return False

        return True

    def check(self, reason, i, newValue, s, change, v, event, W) -> bool:
        valid = self.checkValid(reason, i, newValue, s, change, v, event, W)
        try:
            valid = self.onValidateFunction(reason, i, newValue, s, change, v, event, W)
        except:
            None
        if valid:
            super().after_idle(lambda: self.onValidChange())
        else:
            super().after_idle(lambda: self.onInvalidChange())
        return valid

    def onValidChange(self):
        for cmd in self.onValidChangeFunctions:
            cmd()
    def onInvalidChange(self):
        for cmd in self.onInvalidChangeFunctions:
            cmd()

    def setValidateFunction(self, validateFunction: callable, validate: str = "all"):
        self.validate = validate
        self.validateFunction = validateFunction
    def updateValidation(self):
        super().after_idle(lambda: self.config(validate = self.validate))

    def addOnValidChangeFunction(self, function: callable):
        self.onValidChangeFunctions.append(function)
    def removeOnValidChangeFunction(self, function: callable):
        self.onValidChangeFunctions.remove(function)
    def addOnInvalidChangeFunction(self, function: callable):
        self.onInvalidChangeFunctions.append(function)
    def removeOnInvalidChangeFunction(self, function: callable):
        self.onInvalidChangeFunctions.remove(function)


    def onChange(self, name, mode, cbname):
        for f in self.onChangeFunctions.values():
            f()
    def setTextVar(self, value):
        self.textVar = value
        super().config(textvar = self.textVar)
        self.onChange = self.textVar.trace("w", self.onChange)
    def updateOnChange(self):
        self.textVar.trace_vdelete("w", self.onChange)
        self.onChange = self.textVar.trace("w", self.onChange)
    def addOnChange(self, name: str, function):
        self.onChangeFunctions[name] = function
        self.updateOnChange()
    def removeOnChange(self, name):
        self.onChangeFunctions.pop(name)
        self.updateOnChange()

    def setMaxLenght(self, maxLenght: int):
        self.maxLenght = maxLenght
    def getMaxLenght(self) -> int:
        return self.maxLenght

    def setText(self, text: str):
        self.textVar.set(text)
    def getTextVar(self) -> StringVar:
        return self.textVar



class ExtendedText(Text):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.maxLenght = None
        self.nextChange = True

        super().bind("<Key>", lambda event: self.onChange())
        super().bind("<KeyRelease>", lambda event: self.onValidation())
        

    def validate(self):
        if len(self.get("1.0", END)) > self.maxLenght:
            return False
        return True

    def onValidation(self):
        self.nextChange = self.validate()
    
    def onChange(self):
        if self.nextChange:
            return
        text = self.get("1.0", END)
        self.after_idle(lambda: self.delete("1.0", END))
        self.after_idle(lambda: self.insert(END, text[:-1]))
        

    def setMaxLenght(self, maxLenght: int):
        self.maxLenght = maxLenght
    def getMaxLenght(self) -> int:
        return self.maxLenght

class ScrolledEntry(Frame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.entry = ExtendedText(master = self, wrap = "none", font = ("arial", 11))

        self.xScrollbar = Scrollbar(self, orient = "horizontal", command = self.entry.xview)
        self.yScrollbar = Scrollbar(self, orient = "vertical", command = self.entry.yview)
        
        self.xScrollbar.pack(side = "bottom", fill = "x")
        self.yScrollbar.pack(side = "right", fill = "y")

        self.entry.config(xscrollcommand = self.xScrollbar.set, yscrollcommand = self.yScrollbar.set)
        self.entry.pack(fill = "both", expand = True)

    def get(self) -> str:
        return self.entry.get("1.0", END)

    def getEntry(self) -> ExtendedEntry:
        return self.entry







class LabeledWidget(Frame):

    def __init__(self, title: str = "LabeledWidget", sameSize: bool = True, id: str = None, type: Widget = Label, customWidgetParmList: list[object] = (), customWidgetParmDict: dict[str, object] = {}, layout: Layout = Layout.HORIZONTAL, scheme: bool = False, padx: list[int] = (0, 0), pady: list[int] = (0, 0), *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.title = title

        self.type = type

        self.id = str(id)
        self.style = Style()
        self.styleName = self.title.lower() + "." + self.id + ".labeledwidget.TFrame"
        self.config(style = self.styleName)

        # Anordnung von Label und Entry
        # vertikal: Label oben, CustomWidget unten
        # horizontal: Label links, CustomWidget rechts
        self.layout = layout

        self.padx = padx
        self.pady = pady

        self.scheme = scheme

        self.customWidgetParmList = customWidgetParmList
        self.customWidgetParmDict = customWidgetParmDict

        self.sameSize = sameSize

        self.create()

    def destroy(self):
        self.setBackground(Color.DEFAULT)
        super().destroy()

    def bind(self, *args, **kwargs):
        super().bind(*args, **kwargs)
        self.titleLabel.bind(*args, **kwargs)
        self.customWidget.bind(*args, **kwargs)

    def create(self):

        self.titleLabel = Label(master = self, text = self.title + ":")
        self.customWidget = self.type(self, *self.customWidgetParmList, **self.customWidgetParmDict)

        if self.sameSize:
            self.grid_rowconfigure(0, weight = 1)
            self.grid_rowconfigure(1, weight = int(self.layout == Layout.VERTICAL))
        
            if self.scheme:
                self.grid_columnconfigure(0, weight = int(self.layout == Layout.VERTICAL), uniform = "scheme")
                self.grid_columnconfigure(1, weight = int(self.layout == Layout.HORIZONTAL), uniform = "scheme")
            else:
                self.grid_columnconfigure(0, weight = int(self.layout == Layout.VERTICAL))
                self.grid_columnconfigure(1, weight = int(self.layout == Layout.HORIZONTAL))
        
            self.titleLabel.grid(row = 0, column = 0, sticky = "w", padx = self.padx, pady = self.pady)
            self.customWidget.grid(row = int(self.layout == Layout.VERTICAL), column = int(self.layout == Layout.HORIZONTAL), sticky = "ew", padx = self.padx, pady = self.pady)
        else:
            if self.layout == Layout.HORIZONTAL:
                self.titleLabel.pack(side = "left", fill = "y")
            else:
                self.titleLabel.pack(side = "top", fill = "x")
            self.customWidget.pack(fill = "both", expand = True)

    def getTitleLabel(self) -> Label:
        return self.titleLabel
    def getCustomWidget(self) -> Widget:
        return self.customWidget


    def getTitle(self) -> str:
        return self.title
    def setTitle(self, title: str):
        self.title = title
        self.styleName = self.title.lower() + "." + self.id + ".labeledwidget.TFrame"
        self.config(style = self.styleName)

    def updateGrid(self):
        self.titleLabel.grid_forget()
        self.customWidget.grid_forget()
        self.titleLabel.grid(row = 0, column = 0, sticky = "w", padx = self.padx, pady = self.pady)
        self.customWidget.grid(row = int(self.layout == Layout.VERTICAL), column = int(self.layout == Layout.HORIZONTAL), sticky = "ew", padx = self.padx, pady = self.pady)

    def setPadX(self, padx: int):
        self.padx = padx
        self.updateGrid()
    def getPadX(self) -> int:
        return self.padx
    def setPadY(self, pady: int):
        self.pady = pady
        self.updateGrid()
    def getPadY(self) -> int:
        return self.pady

    def getStyle(self) -> Style:
        return self.style


    def setValid(self, value):
        if value:
            self.setBackground(Color.DEFAULT)
        else:
            self.setBackground(Color.RED)


    def setBackground(self, background: str):
        self.style.configure(self.styleName, background = background)
        self.titleLabel.config(background = background)
        try:
            self.customWidget.config(background = background)
        except:
            None

    def setFont(self, font):
        self.titleLabel.config(font = font)
        self.customWidget.config(font = font)




class Input(LabeledWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(type = ExtendedEntry, *args, **kwargs)

    def getEntry(self) -> ExtendedEntry:
        return self.getCustomWidget()
    def get(self) -> str:
        return self.getCustomWidget().get()


class HyperlinkLabel(Label):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        super().config(foreground = "blue", cursor = "hand2", font = (None, 10, "underline"))
        self.onClickFunctions = []
        super().bind("<Button-1>", lambda event: self.onClick())

    def onClick(self):
        for cmd in self.onClickFunctions:
            cmd()

    def addOnClickFunction(self, function: callable):
        self.onClickFunctions.append(function)
    def removeOnClickFunction(self, function: callable):
        self.onClickFunctions.remove(function)

