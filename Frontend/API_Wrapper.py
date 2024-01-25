from requests import post, patch, get
import json
from datetime import datetime

from calendar import monthrange


BASE_URL: str = "http://127.0.0.1:8080"


def convertToDatetime(timestring) -> datetime:
    return datetime.strptime(timestring.split(".")[0].replace("Z", ""), "%Y-%m-%dT%H:%M:%S")

class User:
    
    @classmethod
    def register(cls, name: str, email: str, password: str) -> 'User':
        data = {"name": name.strip(), "email": email.strip(), "password": password.strip()}
        response = post(BASE_URL + "/user", json = data)
        responseData = response.json()
        return cls(responseData.get("userid"), responseData.get("name"), responseData.get("email"))
        
    @classmethod
    def login(cls, email: str, password: str) -> 'User':
        response = get(BASE_URL + "/user/search?email=" + email.strip())
        responseData = dict(json.loads(response.text)[0])
        responseData = response.json()[0]
        if responseData == None:
            return None
        if not password.strip() == responseData.get("password"):
            return None
        return cls(responseData.get("userid"), responseData.get("name"), responseData.get("email"))


    def __init__(self, id: str, name: str, email: str):
        self.id = id

        self.name = name
        self.email = email

        self.reloadAll()

    def reloadAll(self):
        self.medicines = Medicine.findByUserId(self.id)
        self.symptoms = Symptom.findByUserId(self.id)

    def getMedincines(self) -> list['Medicine']:
        return self.medicines

    def getSymptoms(self) -> list['Symptom']:
        return self.symptoms

    def createMedicine(self, name, dose, first_intake, last_intake):
        m = Medicine.create(self.id, name, dose, first_intake, last_intake)
        self.medicines.append(m)
        return m
    def createSymptom(self, name, severity, first_occurrence, last_occurrence):
        s = Symptom.create(self.id, name, severity, first_occurrence, last_occurrence)
        self.symptoms.append(s)
        return s
    
    def getMedicinesAt(self, day, month, year):
        l = []
        for m in self.medicines:
            date = m.getTimestamp()
            if day == date.date().day and month == date.date().month and year == date.date().year:
                l.append(m)
        return l
    def getSymptomsAt(self, day, month, year):
        l = []
        for s in self.symptoms:
            date = s.getTimestamp()
            if day == date.date().day and month == date.date().month and year == date.date().year:
                l.append(s)
        return l

    def diagnose(self, fromDate, untilDate):
        symptomsCount = 0
        fromDay = int(fromDate.split(".")[0])
        fromMonth = int(fromDate.split(".")[1])
        fromYear = int(fromDate.split(".")[2])
        untilDay = int(untilDate.split(".")[0])
        untilMonth = int(untilDate.split(".")[1])
        untilYear = int(untilDate.split(".")[2])
        first = True
        while fromYear < untilYear:
            for month in range(1, 13):
                if first:
                    for day in range(fromDay, monthrange(fromYear, month)[1] + 1):
                        symptomsCount += len(self.getSymptomsAt(day, month, fromYear))
                    first = False
                else:
                    for day in range(1, monthrange(fromYear, month)[1] + 1):
                        symptomsCount += len(self.getSymptomsAt(day, month, fromYear))
            fromYear += 1
        fromYear -= 1
        
        while fromMonth < untilMonth:
            for day in range(1, monthrange(untilYear, fromMonth)[1] + 1):
                symptomsCount += len(self.getSymptomsAt(day, fromMonth, untilYear))
            fromMonth += 1
        fromMonth -= 1

        while fromDay <= untilDay and fromDay <= monthrange(untilYear, untilMonth)[1]:
            symptomsCount += len(self.getSymptomsAt(fromDay, untilMonth, untilYear))
            fromDay += 1
        fromDay -= 1
        
        if symptomsCount > 3:
            description = "Du bist sehr krank! Gehe umgehend zu einem Arzt!"
        elif symptomsCount > 0:
            description = "Mach langsam, aber das passt."
        else:
            description = "Du bist kerngesund!"
        return Diagnosis(self.id, fromDate, untilDate, description)

    def getName(self) -> str:
        return self.name

    def getEmail(self) -> str:
        return self.email
    


class Diagnosis:

    def __init__(self, userid, fromDate, untilDate, description):
        self.userid = userid
        self.fromDate = fromDate
        self.untilDate = untilDate
        self.description = description

    def getFromDate(self):
        return self.fromDate
    def getUntilDate(self):
        return self.untilDate
    def getDescription(self):
        return self.description


class Symptom:
    
    @classmethod
    def create(cls, userid, name, severity, first_occurrence, last_occurrence) -> 'Symptom':
        data = {"userid": userid, "name": name, "severity": severity, "first_occurrence": first_occurrence, "last_occurrence": last_occurrence}
        response = post(BASE_URL + "/symptom", json = data)
        responseData = response.json()
        return Symptom(convertToDatetime(responseData.get("timestamp")), 
                       responseData.get("userid"), 
                       responseData.get("name"), 
                       responseData.get("severity"), 
                       convertToDatetime(responseData.get("first_occurrence")), 
                       convertToDatetime(responseData.get("last_occurrence")))

    @classmethod
    def findByUserId(cls, userid) -> list['Symptom']:
        response = get(BASE_URL + "/symptom/search?userid=" + str(userid))
        responseData = response.json()
        l = []
        for s in responseData:
            l.append(Symptom(convertToDatetime(s.get("timestamp")), 
                            s.get("userid"), 
                            s.get("name"), 
                            s.get("severity"), 
                            convertToDatetime(s.get("first_occurrence")), 
                            convertToDatetime(s.get("last_occurrence"))))
        return l

    def __init__(self, timestamp, userid, name, severity, first_occurrence, last_occurrence):
        self.timestamp = timestamp
        self.userid = userid
        self.name = name
        self.severity = severity
        self.first_occurrence = first_occurrence
        self.last_occurrence = last_occurrence

    def getTimestamp(self) -> datetime:
        return self.timestamp
    def getUserId(self):
        return self.userid
    def getName(self):
        return self.name
    def getSeverity(self):
        return self.severity
    def getFirstOccurrence(self) -> datetime:
        return self.first_occurrence
    def getLastOccurrence(self) -> datetime:
        return self.last_occurrence
    

class Medicine:

    @classmethod
    def create(cls, userid, name, dose, first_intake, last_intake) -> 'Medicine':
        data = {"userid": userid, "name": name, "dose": dose, "first_intake": first_intake, "last_intake": last_intake}
        response = post(BASE_URL + "/medicine", json = data)
        responseData = response.json()
        return Medicine(convertToDatetime(responseData.get("timestamp")), 
                       responseData.get("userid"), 
                       responseData.get("name"), 
                       responseData.get("dose"), 
                       convertToDatetime(responseData.get("first_intake")), 
                       convertToDatetime(responseData.get("last_intake")))
    
    @classmethod
    def findByUserId(cls, userid) -> list['Medicine']:
        response = get(BASE_URL + "/medicine/search?userid=" + str(userid))
        responseData = response.json()
        l = []
        for m in responseData:
            l.append(Medicine(convertToDatetime(m.get("timestamp")), 
                            m.get("userid"), 
                            m.get("name"), 
                            m.get("dose"), 
                            convertToDatetime(m.get("first_intake")), 
                            convertToDatetime(m.get("last_intake"))))
        return l
        

    def __init__(self, timestamp, userid, name, dose, first_intake, last_intake):
        self.timestamp = timestamp
        self.userid = userid
        self.name = name
        self.dose = dose
        self.first_intake = first_intake
        self.last_intake = last_intake

    def getTimestamp(self) -> datetime:
        return self.timestamp
    def getUserId(self):
        return self.userid
    def getName(self):
        return self.name
    def getDose(self):
        return self.dose
    def getFirstIntake(self) -> datetime:
        return self.first_intake
    def getLastIntake(self) -> datetime:
        return self.last_intake

