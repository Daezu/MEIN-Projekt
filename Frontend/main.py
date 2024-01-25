from tkinter import *
from tkinter.ttk import *

from datetime import datetime
import time, json, os

from CustomWidgets import *

from API_Wrapper import User, Symptom, Medicine, Diagnosis



class DiagnosisGUI(Toplevel):
    
    def __init__(self, appTitle: str, user: User, *args, **kwargs):
        super().__init__(*args, **kwargs)
        super().geometry("500x400")
        super().resizable(False, False)
        
        super().protocol("WM_DELETE_WINDOW", self.onClose)

        self.user = user

        self.appTitle = appTitle
        super().title(self.appTitle)

        self.createFrame = Frame(master = self)

        self.onCloseFunction = lambda: None
        
        self.onCreateFunction = lambda symptom: None

        self.symptom = None

        self.createGUI()

        
    def createGUI(self):
        self.title(self.appTitle + " - Diagnose bekommen")
        self.createFrame.place(relx = 0.5, rely = 0.5, anchor = "c", relwidth = 0.9, relheight = 0.9)
        
        self.fromInput = Input(master = self.createFrame, title = "Von", layout = Layout.HORIZONTAL, scheme = True, padx = 20)
        self.fromInput.place(relx = 0.5, rely = 0.3, relwidth = 1, height = 40, anchor = "c")
        self.fromInput.getEntry().setMaxLenght(100)
        self.fromInput.getEntry().insert(0, "12.01.2024")

        self.untilInput = Input(master = self.createFrame, title = "Bis", layout = Layout.HORIZONTAL, scheme = True, padx = 20)
        self.untilInput.place(relx = 0.5, rely = 0.4, relwidth = 1, height = 40, anchor = "c")
        self.untilInput.getEntry().setMaxLenght(100)
        self.untilInput.getEntry().insert(0, "26.01.2024")

        submitButton = Button(master = self.createFrame, text = "Diagnose erstellen", command = self.create)
        submitButton.place(relx = 0.5, rely = 0.7, relwidth = 0.5, height = 30, anchor = "c")
        
        self.feedbackLabel = Label(master = self.createFrame, wraplength = 500 * 0.9, anchor = "c")
        self.feedbackLabel.place(relx = 0.5, rely = 0.8, relwidth = 1, height = 80, anchor = "n")


    # Create
    def create(self):
        fromDate = int(time.mktime(datetime.strptime(self.fromInput.get(), "%d.%m.%Y").timetuple()))
        untilDate = int(time.mktime(datetime.strptime(self.untilInput.get(), "%d.%m.%Y").timetuple()))
        diagnosis = self.user.diagnose(self.fromInput.get(), self.untilInput.get())
        self.setFeedbackText('Diagnose: \n' + diagnosis.description)
        self.onCreate(diagnosis)
    def onCreate(self, diagnosis: Diagnosis):
        self.onCreateFunction(diagnosis)
    def setOnCreateFunction(self, function: callable):
        self.onCreateFunction = function


    # Feedback
    def setFeedbackText(self, text: str):
        self.feedbackLabel.config(text = text)

    # Apptitle
    def setAppTitle(self, appTitle: str):
        self.appTitle = appTitle
    def getAppTitle(self) -> str:
        return self.appTitle
    
    # OnClose
    def onClose(self):
        self.onCloseFunction()
        super().destroy()
    def setOnCloseFunction(self, function: callable):
        self.onCloseFunction = function














class SymptomCreationGUI(Toplevel):
    
    def __init__(self, appTitle: str, user: User, *args, **kwargs):
        super().__init__(*args, **kwargs)
        super().geometry("500x400")
        super().resizable(False, False)
        
        super().protocol("WM_DELETE_WINDOW", self.onClose)

        self.user = user

        self.appTitle = appTitle
        super().title(self.appTitle)

        self.createFrame = Frame(master = self)

        self.onCloseFunction = lambda: None
        
        self.onCreateFunction = lambda symptom: None

        self.symptom = None

        self.createGUI()

    def getName(self) -> str:
        return self.nameInput.get()
        
    def createGUI(self):
        self.title(self.appTitle + " - Symptom erstellen")
        self.createFrame.place(relx = 0.5, rely = 0.5, anchor = "c", relwidth = 0.9, relheight = 0.9)
        
        self.nameInput = Input(master = self.createFrame, title = "Name", layout = Layout.HORIZONTAL, scheme = True, padx = 20)
        self.nameInput.place(relx = 0.5, rely = 0.3, relwidth = 1, height = 40, anchor = "c")
        self.nameInput.getEntry().setMaxLenght(100)
        self.nameInput.getEntry().insert(0, "Symptom1")

        self.severityInput = Input(master = self.createFrame, title = "Stärke", layout = Layout.HORIZONTAL, scheme = True, padx = 20)
        self.severityInput.place(relx = 0.5, rely = 0.4, relwidth = 1, height = 40, anchor = "c")
        self.severityInput.getEntry().setMaxLenght(100)
        self.severityInput.getEntry().insert(0, "1/10")

        self.firstOccurrenceInput = Input(master = self.createFrame, title = "Erstes Auftreten", layout = Layout.HORIZONTAL, scheme = True, padx = 20)
        self.firstOccurrenceInput.place(relx = 0.5, rely = 0.5, relwidth = 1, height = 40, anchor = "c")
        self.firstOccurrenceInput.getEntry().setMaxLenght(100)
        self.firstOccurrenceInput.getEntry().insert(0, "26.01.2024")

        self.lastOccurrenceInput = Input(master = self.createFrame, title = "Letztes Auftreten", layout = Layout.HORIZONTAL, scheme = True, padx = 20)
        self.lastOccurrenceInput.place(relx = 0.5, rely = 0.6, relwidth = 1, height = 40, anchor = "c")
        self.lastOccurrenceInput.getEntry().setMaxLenght(100)
        self.lastOccurrenceInput.getEntry().insert(0, "26.01.2024")

        submitButton = Button(master = self.createFrame, text = "Symptom erstellen", command = self.create)
        submitButton.place(relx = 0.5, rely = 0.7, relwidth = 0.5, height = 30, anchor = "c")
        
        self.feedbackLabel = Label(master = self.createFrame, wraplength = 500 * 0.9, anchor = "c")
        self.feedbackLabel.place(relx = 0.5, rely = 0.8, relwidth = 1, height = 80, anchor = "n")


    # Create
    def create(self):
        name = self.getName()
        if name == "":
            self.setFeedbackText("Bitte gib einen Namen an!")
            return
        first_occurrence = int(time.mktime(datetime.strptime(self.firstOccurrenceInput.get(), "%d.%m.%Y").timetuple()))
        last_occurrence = int(time.mktime(datetime.strptime(self.lastOccurrenceInput.get(), "%d.%m.%Y").timetuple()))
        symptom = self.user.createSymptom(name = name, severity = self.severityInput.get(), 
                                        first_occurrence = first_occurrence, 
                                        last_occurrence = last_occurrence)
        self.setFeedbackText('Du hast das Symptom "' + name + '" erstellt.')
        self.onCreate(symptom)
    def onCreate(self, symptom: Symptom):
        self.onCreateFunction(symptom)
    def setOnCreateFunction(self, function: callable):
        self.onCreateFunction = function


    # Feedback
    def setFeedbackText(self, text: str):
        self.feedbackLabel.config(text = text)

    # Apptitle
    def setAppTitle(self, appTitle: str):
        self.appTitle = appTitle
    def getAppTitle(self) -> str:
        return self.appTitle
    
    # OnClose
    def onClose(self):
        self.onCloseFunction()
        super().destroy()
    def setOnCloseFunction(self, function: callable):
        self.onCloseFunction = function

class MedicineCreationGUI(Toplevel):
    
    def __init__(self, appTitle: str, user: User, *args, **kwargs):
        super().__init__(*args, **kwargs)
        super().geometry("500x400")
        super().resizable(False, False)
        
        super().protocol("WM_DELETE_WINDOW", self.onClose)

        self.user = user

        self.appTitle = appTitle
        super().title(self.appTitle)

        self.createFrame = Frame(master = self)

        self.onCloseFunction = lambda: None
        
        self.onCreateFunction = lambda symptom: None

        self.symptom = None

        self.createGUI()

    def getName(self) -> str:
        return self.nameInput.get()
        
    def createGUI(self):
        self.title(self.appTitle + " - Medikament erstellen")
        self.createFrame.place(relx = 0.5, rely = 0.5, anchor = "c", relwidth = 0.9, relheight = 0.9)
        
        self.nameInput = Input(master = self.createFrame, title = "Name", layout = Layout.HORIZONTAL, scheme = True, padx = 20)
        self.nameInput.place(relx = 0.5, rely = 0.3, relwidth = 1, height = 40, anchor = "c")
        self.nameInput.getEntry().setMaxLenght(100)
        self.nameInput.getEntry().insert(0, "Medicine1")

        self.doseInput = Input(master = self.createFrame, title = "Dosis", layout = Layout.HORIZONTAL, scheme = True, padx = 20)
        self.doseInput.place(relx = 0.5, rely = 0.4, relwidth = 1, height = 40, anchor = "c")
        self.doseInput.getEntry().setMaxLenght(100)
        self.doseInput.getEntry().insert(0, "3/tag")

        self.firstIntakeInput = Input(master = self.createFrame, title = "Erste Einnahme", layout = Layout.HORIZONTAL, scheme = True, padx = 20)
        self.firstIntakeInput.place(relx = 0.5, rely = 0.5, relwidth = 1, height = 40, anchor = "c")
        self.firstIntakeInput.getEntry().setMaxLenght(100)
        self.firstIntakeInput.getEntry().insert(0, "26.01.2024")

        self.lastIntakeInput = Input(master = self.createFrame, title = "Letzte Einnahme", layout = Layout.HORIZONTAL, scheme = True, padx = 20)
        self.lastIntakeInput.place(relx = 0.5, rely = 0.6, relwidth = 1, height = 40, anchor = "c")
        self.lastIntakeInput.getEntry().setMaxLenght(100)
        self.lastIntakeInput.getEntry().insert(0, "26.01.2024")

        submitButton = Button(master = self.createFrame, text = "Medikament erstellen", command = self.create)
        submitButton.place(relx = 0.5, rely = 0.7, relwidth = 0.5, height = 30, anchor = "c")
        
        self.feedbackLabel = Label(master = self.createFrame, wraplength = 500 * 0.9, anchor = "c")
        self.feedbackLabel.place(relx = 0.5, rely = 0.8, relwidth = 1, height = 80, anchor = "n")


    # Create
    def create(self):
        name = self.getName()
        if name == "":
            self.setFeedbackText("Bitte gib einen Namen an!")
            return
        first_intake = int(time.mktime(datetime.strptime(self.firstIntakeInput.get(), "%d.%m.%Y").timetuple()))
        last_intake = int(time.mktime(datetime.strptime(self.lastIntakeInput.get(), "%d.%m.%Y").timetuple()))
        medicine = self.user.createMedicine(name = name, dose = self.doseInput.get(), 
                                        first_intake = first_intake, 
                                        last_intake = last_intake)
        self.setFeedbackText('Du hast das Medikament "' + name + '" erstellt.')
        self.onCreate(medicine)
    def onCreate(self, medicine: Medicine):
        self.onCreateFunction(medicine)
    def setOnCreateFunction(self, function: callable):
        self.onCreateFunction = function


    # Feedback
    def setFeedbackText(self, text: str):
        self.feedbackLabel.config(text = text)

    # Apptitle
    def setAppTitle(self, appTitle: str):
        self.appTitle = appTitle
    def getAppTitle(self) -> str:
        return self.appTitle
    
    # OnClose
    def onClose(self):
        self.onCloseFunction()
        super().destroy()
    def setOnCloseFunction(self, function: callable):
        self.onCloseFunction = function


"""
class TopicModificationGUI(Toplevel):
    
    def __init__(self, appTitle: str, user: User, topic: Topic, *args, **kwargs):
        super().__init__(*args, **kwargs)
        super().geometry("500x400")
        super().resizable(False, False)
        
        super().protocol("WM_DELETE_WINDOW", self.onClose)

        self.user = user

        self.appTitle = appTitle
        super().title(self.appTitle)

        self.onCloseFunction = lambda: None
        
        self.modificationFrame = Frame(master = self)

        self.onModificationFunction = lambda topic: None

        self.createGUI(topic = topic)

    def getTitle(self) -> str:
        return self.titleInput.get()
        
    def createGUI(self, topic: Topic):
        self.topic = topic
        self.modificationFrame.destroy()
        self.modificationFrame = Frame(master = self)
        self.modificationFrame.place(relx = 0.5, rely = 0.5, anchor = "c", relwidth = 0.9, relheight = 0.9)
        
        self.topicList = [Topic(topicUUID) for topicUUID in self.user.getTopicUUIDs()]
        self.topicTitleList = [topicListItem.getTitle() for topicListItem in self.topicList]

        self.topicSelectionVar = StringVar()
        self.topicSelection = LabeledWidget(master = self.modificationFrame, type = OptionMenu, title = "Wähle ein Thema", 
                                            customWidgetParmList = (self.topicSelectionVar, "", *self.topicTitleList), 
                                            customWidgetParmDict = {"command": lambda event: (self.titleInput.getEntry().delete(0, END), self.titleInput.getEntry().insert(0, self.getSelectedTopic().getTitle()))},
                                            layout = Layout.HORIZONTAL, scheme = True, padx = 20)
        self.topicSelection.place(relx = 0.5, rely = 0.2, relwidth = 1, height = 40, anchor = "c")
        self.topicSelectionVar.set(self.topic.getTitle())
        self.title(self.appTitle + " - " + self.getSelectedTopic().getTitle() + " bearbeiten")

        self.titleInput = Input(master = self.modificationFrame, title = "Titel", layout = Layout.HORIZONTAL, scheme = True, padx = 20)
        self.titleInput.place(relx = 0.5, rely = 0.4, relwidth = 1, height = 40, anchor = "c")
        self.titleInput.getEntry().setMaxLenght(100)
        self.titleInput.getEntry().insert(0, self.getSelectedTopic().getTitle())

        submitButton = Button(master = self.modificationFrame, text = "Änderung übernehmen", command = lambda: (setattr(self, "topic", self.getSelectedTopic()), self.modify()))
        submitButton.place(relx = 0.5, rely = 0.5, relwidth = 0.5, height = 30, anchor = "c")
        
        self.feedbackLabel = Label(master = self.modificationFrame, wraplength = 500 * 0.9, anchor = "c")
        self.feedbackLabel.place(relx = 0.5, rely = 0.6, relwidth = 1, height = 80, anchor = "n")

    def setSelectedTopic(self, topic):
        self.titleInput.getEntry().delete(0, END)
        self.titleInput.getEntry().insert(0, topic.getTitle())
        self.topicSelectionVar.set(topic.getTitle())

    def getSelectedTopic(self):
        return self.topicList[self.topicTitleList.index(self.topicSelectionVar.get())]

    # modify
    def modify(self):
        title = self.getTitle()
        if title == "":
            self.setFeedbackText("Bitte gib einen Titel an!")
            return
        oldTitle = self.topic.getTitle()
        if title == oldTitle:
            self.setFeedbackText("Du hast noch keinen Wert geändert.")
            return
        self.topic.setTitle(title)
        self.setFeedbackText('Du hast den Titel von "' + oldTitle + '" zu "' + title + '" geändert.')
        self.onModification(self.topic)
    def onModification(self, topic: Topic):
        self.onModificationFunction(topic)
    def setOnModificationFunction(self, function: callable):
        self.onModificationFunction = function


    # Feedback
    def setFeedbackText(self, text: str):
        self.feedbackLabel.config(text = text)

    # Apptitle
    def setAppTitle(self, appTitle: str):
        self.appTitle = appTitle
        self.title(self.appTitle + " - " + self.getSelectedTopic.getTitle() + " bearbeiten")
    def getAppTitle(self) -> str:
        return self.appTitle
    
    # OnClose
    def onClose(self):
        self.onCloseFunction()
        super().destroy()
    def setOnCloseFunction(self, function: callable):
        self.onCloseFunction = function



"""



class AccountGUI(Toplevel):
    
    def __init__(self, appTitle: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        super().geometry("500x400")
        super().resizable(False, False)

        self.onCloseFunction = lambda: None
        super().protocol("WM_DELETE_WINDOW", self.onClose)
        self.onLoginFunction = lambda: None
        self.onRegisterFunction = lambda: None

        self.appTitle = appTitle
        
        self.dataWidgets = {}

        self.loginFrame = Frame(master = self)
        self.registerFrame = Frame(master = self)

        self.setLoginGUI()
        
    def setLoginGUI(self):
        self.registerFrame.place_forget()
        super().title(self.appTitle + " - Anmeldung")
        self.loginFrame.place(relx = 0.5, rely = 0.5, anchor = "c", relwidth = 0.9, relheight = 0.9)
        
        self.dataWidgets = {}
        inputTitles = (("email", "Email"), ("password", "Passwort"))
        for i in range(len(inputTitles)):
            input = Input(master = self.loginFrame, title = inputTitles[i][1], layout = Layout.HORIZONTAL, scheme = True, padx = 20)
            input.place(relx = 0.5, rely = 0.2 + 0.2 * i, relwidth = 1, height = 40, anchor = "c")
            input.getEntry().setMaxLenght(100)
            self.dataWidgets.update({inputTitles[i][0]: input})

        self.dataWidgets.get("password").getEntry().config(show = "*")

        submitButton = Button(master = self.loginFrame, text = "Anmelden", command = self.onLogin)
        submitButton.place(relx = 0.5, rely = 0.5, relwidth = 0.5, height = 30, anchor = "c")
        
        self.feedbackLabel = Label(master = self.loginFrame, wraplength = 500 * 0.9, anchor = "c")
        self.feedbackLabel.place(relx = 0.5, rely = 0.6, relwidth = 1, height = 80, anchor = "n")

        registerFrame = Frame(master = self.loginFrame)
        registerFrame.place(relx = 0.5, rely = 0.85, relwidth = 1, anchor = "c")
        registerLabel = Label(master = registerFrame, text = "Du hast noch keinen Account?", anchor = "c")
        registerLabel.pack(expand = True)
        registerHyperlinkLabel = HyperlinkLabel(master = registerFrame, text = "Jetzt Registrieren!", anchor = "c")
        registerHyperlinkLabel.addOnClickFunction(lambda: self.setRegisterGUI())
        registerHyperlinkLabel.pack(expand = True)

    def setRegisterGUI(self):
        self.loginFrame.place_forget()
        super().title(self.appTitle + " - Registrierung")
        self.registerFrame.place(relx = 0.5, rely = 0.5, anchor = "c", relwidth = 0.9, relheight = 0.9)

        self.dataWidgets = {}
        inputTitles = (("name", "Benutzername"), ("email", "Email"), ("password", "Passwort"))
        for i in range(len(inputTitles)):
            input = Input(master = self.registerFrame, title = inputTitles[i][1], layout = Layout.HORIZONTAL, scheme = True, padx = 20)
            input.place(relx = 0.5, rely = 0.1 + 0.1 * i, relwidth = 1, height = 30, anchor = "c")
            input.getEntry().setMaxLenght(100)
            input.getEntry().config(background = "red")
            self.dataWidgets.update({inputTitles[i][0]: input})
        
        self.dataWidgets.get("password").getEntry().config(show = "*")

        submitButton = Button(master = self.registerFrame, text = "Registrieren", command = self.onRegister)
        submitButton.place(relx = 0.5, rely = 0.5, relwidth = 0.5, height = 30, anchor = "c")

        self.feedbackLabel = Label(master = self.registerFrame, wraplength = 500 * 0.9, anchor = "c")
        self.feedbackLabel.place(relx = 0.5, rely = 0.6, relwidth = 1, height = 80, anchor = "n")

        loginFrame = Frame(master = self.registerFrame)
        loginFrame.place(relx = 0.5, rely = 0.85, relwidth = 1, anchor = "c")
        loginLabel = Label(master = loginFrame, text = "Du hast schon einen Account?", anchor = "c")
        loginLabel.pack(expand = True)
        loginHyperlinkLabel = HyperlinkLabel(master = loginFrame, text = "Jetzt Anmelden!", anchor = "c")
        loginHyperlinkLabel.addOnClickFunction(lambda: self.setLoginGUI())
        loginHyperlinkLabel.pack(expand = True)

    # Data
    def getData(self) -> dict[str, str]:
        data = {}
        for key in self.dataWidgets.keys():
            try:
                if self.dataWidgets.get(key).get() == "":
                    continue
                data.update({key.lower(): self.dataWidgets.get(key).get()})
            except:
                continue
        return data

    # OnLogin
    def onLogin(self):
        self.onLoginFunction(self.dataWidgets)
    def setOnLoginFunction(self, function: callable):
        self.onLoginFunction = function
        
    # OnRegister
    def onRegister(self):
        self.onRegisterFunction(self.dataWidgets)
    def setOnRegisterFunction(self, function: callable):
        self.onRegisterFunction = function

    # Feedback
    def setFeedbackText(self, text: str):
        self.feedbackLabel.config(text = text)

    # Apptitle
    def setAppTitle(self, appTitle: str):
        self.appTitle = appTitle
    def getAppTitle(self) -> str:
        return self.appTitle
    
    # OnClose
    def onClose(self):
        self.onCloseFunction()
        super().destroy()
    def destroy(self):
        self.onClose()
    def setOnCloseFunction(self, function: callable):
        self.onCloseFunction = function

        


        
class Pane(Frame):
    
    def __init__(self, title: str, info: dict[str, str], id: str = None, scheme: bool = False, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title = title
        self.info = info
        self.scheme = scheme

        self.id = str(id)
        self.style = Style()
        self.styleName = self.title.lower() + "." + self.id + ".pane.TFrame"
        self.config(style = self.styleName)

        self.onDestroyFunction = lambda: None

        self.create()

    def bind(self, *args, **kwargs):
        super().bind(*args, **kwargs)
        self.titleLabel.bind(*args, **kwargs)
        self.infoFrame.bind(*args, **kwargs)
        for infoLabel in self.infoLabels.values():
            infoLabel.bind(*args, **kwargs)

    def create(self):
        
        self.titleLabel = Label(master = self, text = self.title, anchor = "c", font = (None, 15, "bold"))
        self.titleLabel.place(relx = 0.5, rely = 0.5, relwidth = 1, height = 40, anchor = "c")

        self.infoFrame = Frame(master = self, style = self.styleName)
        self.infoFrame.place(relx = 0.5, rely = 0.7, relwidth = 1, relheight = 0.3, anchor = "n")

        self.infoFrame.grid_columnconfigure(0, weight = 1)
        self.infoLabels = {}
        for i in range(len(self.info)):
            self.infoFrame.grid_rowconfigure(i, weight = 1)
            key = list(self.info.keys())[i]
            infoLabel = LabeledWidget(master = self.infoFrame, id = self.id, title = key, type = Label, scheme = self.scheme, padx = (5, 5))
            infoLabel.getCustomWidget().config(text = self.info.get(key))
            infoLabel.grid(row = i, column = 0, sticky = "nesw")
            self.infoLabels.update({key: infoLabel})


    def getTitleLabel(self) -> Label:
        return self.titleLabel

    def setBackground(self, background: str):
        self.style.configure(self.styleName, background = background)
        self.titleLabel.config(background = background)
        for label in self.infoLabels.values():
            label.setBackground(background = background)


    # Info
    def setInfo(self, info: dict[str, str]):
        self.info = info
    def updateInfo(self, key: str, value: str):
        self.info.update({key: value})

    # On Destroy
    def destroy(self):
        self.onDestroyFunction()
        super().destroy()
    def setOnDestroyFunction(self, function: callable):
        self.onDestroyFunction = function

    











class DiaryGUI:

    def __init__(self):
        self.root = Tk()
        self.root.geometry("1020x700")
        self.root.minsize(1020, 700)
        self.appTitle = "Medical Diary"
        self.version = "1.0"
        self.root.title(self.appTitle)
        
        self.style = Style()
        self.style.theme_use("vista")

        self.externalGUI = None
        self.helpGUI = None
        self.accountGUI = None

        self.listFrame = None
        
        self.filePath = os.getcwd() +  "\\diary\\"
        if not os.path.exists(self.filePath):
            try:
                os.makedirs(self.filePath)
                open(self.filePath + "user.json", "x")
            except:
                None
        self.user = None
        try:
            with open(self.filePath + "user.json", "r") as userFile:
                jsonUser = json.load(userFile)
                email = jsonUser.get("email")
                password = jsonUser.get("password")
            self.user = User.login(email = email, password = password)
        except:
            None
        
        if self.user == None:
            self.setLoginGUI()
            self.root.mainloop()
            return

        self.create()

        self.root.mainloop()


    def create(self):

        # Menubar
        self.menubar = Menu(self.root)
        self.root.config(menu = self.menubar)
        self.helpMenu = Menu(self.menubar, tearoff = False)
        self.menubar.add_cascade(label = "Hilfe", menu = self.helpMenu)
        self.helpMenu.add_command(label = "Über " + self.appTitle, command = self.openHelpGUI)
        self.helpMenu.add_separator()
        self.helpMenu.add_command(label = "Benutzer wechseln", command = self.openAccountGUI)

        self.blend(False)

        self.optionsFrame = Frame(master = self.root)
        self.optionsFrame.place(relx = 0.5, y = 0, relwidth = 1, height = 50, anchor = "n")
        
        self.infoFrame = Frame(master = self.root)
        self.infoFrame.place(relx = 0.5, y = 50, relwidth = 1, height = 50, anchor = "n")

        # Creation Buttone
        self.createSymptomButton = Button(master = self.optionsFrame, text = "Symptom erstellen", command = self.openSymptomCreationGUI)
        self.createSymptomButton.place(relx = 0.2, rely = 0.5, height = 30, relwidth = 0.25, anchor = "c")

        self.createMedicineButton = Button(master = self.optionsFrame, text = "Medikament erstellen", command = self.openMedicineCreationGUI)
        self.createMedicineButton.place(relx = 0.5, rely = 0.5, height = 30, relwidth = 0.25, anchor = "c")

        self.diagnoseButton = Button(master = self.optionsFrame, text = "Diagnose bekommen", command = self.openDiagnosisGUI)
        self.diagnoseButton.place(relx = 0.8, rely = 0.5, height = 30, relwidth = 0.25, anchor = "c")


        self.setListGUI()


    def setListGUI(self):

        if not self.listFrame == None:
            self.listFrame.destroy()
        self.listFrame = Frame(master = self.root)
        self.listFrame.pack(pady = (100, 0), side = "top", fill = "both", expand = True)

        self.root.config(cursor = "wait")
        
        width = self.listFrame.winfo_width()
        height = self.listFrame.winfo_height()

        def stripDate(date: datetime):
            return str(date.day) + "." + str(date.month) + "." + str(date.year)

        # Symptoms
        symptomsVeiwFrame = Frame(master = self.listFrame)
        symptomsVeiwFrame.place(relx = 0.5, rely = 0.25, relwidth = 1, relheight = 0.5, anchor = "c")

        symptomsVeiw = Treeview(master = symptomsVeiwFrame, columns = ("severity", "first_occurrence", "last_occurrence"))
        symptomsVeiw.column("#0", anchor = "e")
        symptomsVeiw.column("severity", anchor = "e")
        symptomsVeiw.column("first_occurrence", anchor = "e")
        symptomsVeiw.column("last_occurrence", anchor = "e")

        symptomsVeiw.heading("#0", text = "Name")
        symptomsVeiw.heading("severity", text = "Stärke")
        symptomsVeiw.heading("first_occurrence", text = "Erstes Auftreten")
        symptomsVeiw.heading("last_occurrence", text = "Letztes Auftreten")

        for s in self.user.getSymptoms():
            symptomsVeiw.insert("", 0, text = s.getName(), values = (s.getSeverity(), stripDate(s.getFirstOccurrence()), stripDate(s.getLastOccurrence())))
        
        symptomsvsb = Scrollbar(symptomsVeiwFrame, orient="vertical", command = symptomsVeiw.yview)
        symptomsvsb.pack(side = "right", fill = "y")

        symptomsVeiw.configure(yscrollcommand=symptomsvsb.set)
        symptomsVeiw.pack(side = "left", fill = "both", expand = True)

        # Medicines
        medicinesVeiwFrame = Frame(master = self.listFrame)
        medicinesVeiwFrame.place(relx = 0.5, rely = 0.75, relwidth = 1, relheight = 0.5, anchor = "c")

        medicinesVeiw = Treeview(master = medicinesVeiwFrame, columns = ("dose", "first_intake", "last_intake"))
        medicinesVeiw.column("#0", anchor = "e")
        medicinesVeiw.column("dose", anchor = "e")
        medicinesVeiw.column("first_intake", anchor = "e")
        medicinesVeiw.column("last_intake", anchor = "e")

        medicinesVeiw.heading("#0", text = "Name")
        medicinesVeiw.heading("dose", text = "Dosis")
        medicinesVeiw.heading("first_intake", text = "Erste Einnahme")
        medicinesVeiw.heading("last_intake", text = "Letzte Einnahme")

        for s in self.user.getMedincines():
            medicinesVeiw.insert("", 0, text = s.getName(), values = (s.getDose(), stripDate(s.getFirstIntake()), stripDate(s.getLastIntake())))
            

        medicinesvsb = Scrollbar(medicinesVeiwFrame, orient="vertical", command = medicinesVeiw.yview)
        medicinesvsb.pack(side = "right", fill = "y")

        medicinesVeiw.configure(yscrollcommand=medicinesvsb.set)
        medicinesVeiw.pack(side = "left", fill = "both", expand = True)

        # Stuff
        self.root.config(cursor = "")



    # Help GUI
    def openHelpGUI(self):

        if self.helpGUI == None:
            self.helpGUI = Toplevel()
            self.helpGUI.geometry("300x200")
            self.helpGUI.resizable(False, False)
            self.helpGUI.title("Über " + self.appTitle)
            self.helpGUI.protocol("WM_DELETE_WINDOW", lambda: (self.helpGUI.destroy(), setattr(self, "helpGUI", None)))
            helpFrame = Frame(master = self.helpGUI)
            helpFrame.place(relx = 0.5, rely = 0.5, relwidth = 0.9, relheight = 0.9, anchor = "c")
            Label(master = helpFrame, text = self.appTitle, font = (None, 20), anchor = "n").place(relx = 0.5, rely = 0, relwidth = 1, relheight = 0.2, anchor = "n")
            Label(master = helpFrame, text = "Version " + self.version, font = (None, 20), anchor = "n").place(relx = 0.5, rely = 0.2, relwidth = 1, relheight = 0.2, anchor = "n")
            contactLabel = LabeledWidget(master = helpFrame, title = "Kontakt")
            contactLabel.getCustomWidget().config(font = (None, 15), text = "niklas.boeer@stud.th-bingen.de", anchor = "c")
            contactLabel.getTitleLabel().config(anchor = "c")
            contactLabel.place(relx = 0.5, rely = 0.45, relwidth = 1, relheight = 0.2, anchor = "n")
        else:
            self.helpGUI.bell()
        self.helpGUI.focus_force()

    
    # Symptom GUI
    def openSymptomCreationGUI(self):
        if self.externalGUI == None:
            self.externalGUI = SymptomCreationGUI(user = self.user, appTitle = self.appTitle)
            def onClose():
                setattr(self, "externalGUI", None)
                self.setListGUI()
            self.externalGUI.setOnCloseFunction(onClose)
        else:
            self.externalGUI.bell()
        self.externalGUI.focus_force()
    
    
    # Medicine GUI
    def openMedicineCreationGUI(self):
        if self.externalGUI == None:
            self.externalGUI = MedicineCreationGUI(user = self.user, appTitle = self.appTitle)
            def onClose():
                setattr(self, "externalGUI", None)
                self.setListGUI()
            self.externalGUI.setOnCloseFunction(onClose)
        else:
            self.externalGUI.bell()
        self.externalGUI.focus_force()
    
    # Diagnosis GUI
    def openDiagnosisGUI(self):
        if self.externalGUI == None:
            self.externalGUI = DiagnosisGUI(user = self.user, appTitle = self.appTitle)
            self.externalGUI.setOnCloseFunction(lambda: setattr(self, "externalGUI", None))
        else:
            self.externalGUI.bell()
        self.externalGUI.focus_force()


        



    # Verdecken
    def blend(self, blend: bool):
        if blend:
            self.blendFrame = Frame(master = self.root)
            self.blendFrame.place(x = 0, y = 0, relwidth = 1, relheight = 1)
        else:
            try:
                self.blendFrame.destroy()
            except:
                None










    # Anmeldescreen
    def setLoginGUI(self):
        self.blend(True)

        loginFrame = Frame(master = self.blendFrame)
        loginFrame.place(relx = 0.5, rely = 0.5, anchor = "c")

        loginLabel = Label(master = loginFrame, text = "Bitte melde dich an, um zu beginnen!")
        loginLabel.pack()

        loginButton = Button(master = loginFrame, text = "Anmelden", command = self.openAccountGUI)
        loginButton.pack()


    # Account Registrierung / Anmeldung
    def register(self, dataInputs: dict):
        
        valid = True
        for input in dataInputs.values():
            input.setValid(not input.get() == "")
            valid = valid and not input.get() == ""

        if not valid:
            return

        name = dataInputs.get("name").get()
        email = dataInputs.get("email").get()
        password = dataInputs.get("password").get()
        
        self.accountGUI.config(cursor = "wait")
        self.accountGUI.update()
        try:
            self.user = User.register(name, email, password)
            with open(self.filePath + "user.json", "w") as userFile:
                userFile.write(json.dumps({"email": email, "password": password}))
        except:
            raise
            self.accountGUI.setFeedbackText("Fehler bei der Registrierung!")
            return
        finally:    
            self.accountGUI.config(cursor = "")

        self.accountGUI.destroy()
        self.create()

    def login(self, dataInputs):
        valid = True
        for input in dataInputs.values():
            input.setValid(not input.get() == "")
            valid = valid and not input.get() == ""

        if not valid:
            return

        email = dataInputs.get("email").get()
        password = dataInputs.get("password").get()

        self.accountGUI.config(cursor = "wait")
        self.accountGUI.update()
        try:
            self.user = User.login(email, password)
            if self.user == None:
                self.accountGUI.setFeedbackText("Falsche Email oder Passwort!")
                return
            with open(self.filePath + "user.json", "w") as userFile:
                userFile.write(json.dumps({"email": email, "password": password}))
        except:
            raise
            self.accountGUI.setFeedbackText("Fehler bei der Anmeldung!")
            return
        finally:
            self.accountGUI.config(cursor = "")


        self.accountGUI.destroy()
        self.create()

    def openAccountGUI(self):
        if self.accountGUI == None:
            self.accountGUI = AccountGUI(appTitle = self.appTitle)
            self.accountGUI.setOnCloseFunction(lambda: setattr(self, "accountGUI", None))
            self.accountGUI.setOnLoginFunction(lambda dataInputs: self.login(dataInputs))
            self.accountGUI.setOnRegisterFunction(lambda dataInputs: self.register(dataInputs))
        else:
            self.accountGUI.bell()
        self.accountGUI.focus_force()
     
        

if __name__ == "__main__":
    DiaryGUI()
















