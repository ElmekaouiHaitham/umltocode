import csv
from enum import Enum
import io

from converter._class import Class

from converter.interface import Interface
from converter.programming_languages import ProgrammingLangs

from converter.relation import Relation, RelationType


class Converter :

    def __init__(self, pl = "dart"):
        self.elements = []
        self.programmingLang = self.getProgrammingLang(pl)

    def getProgrammingLang(self, pl:str):
        if pl == "dart":return ProgrammingLangs.DART
        elif pl == "python":return ProgrammingLangs.PYTHON
        else: raise "unsupported language"


    def createClass(self, row):
        return Class(row,self.programmingLang)

    def createInterface(self, row):
        return Interface(row,self.programmingLang)

    def createRelation(self, row):
        if row['Source Arrow'] == "Hollow Arrow":
            return Relation(self.getElementById(int(row['Line Destination'])),self.getElementById(int(row['Line Source'])),RelationType.INHERITANCE)
        elif row['Source Arrow'] == "Composition":
            return Relation(self.getElementById(int(row['Line Source'])),self.getElementById(int(row['Line Destination'])),RelationType.COMPOSITION)
        elif row['Source Arrow'] == "Aggregation":
            return Relation(self.getElementById(int(row['Line Source'])),self.getElementById(int(row['Line Destination'])),RelationType.AGGREGATION)

        elif row['Destination Arrow'] == "Hollow Arrow":

            return Relation(self.getElementById(int(row['Line Source'])),self.getElementById(int(row['Line Destination'])),RelationType.INHERITANCE)
        elif row['Destination Arrow'] == "Composition":
            return Relation(self.getElementById(int(row['Line Destination'])),self.getElementById(int(row['Line Source'])),RelationType.COMPOSITION)
        elif row['Destination Arrow'] == "Aggregation":
            return Relation(self.getElementById(int(row['Line Destination'])),self.getElementById(int(row['Line Source'])),RelationType.AGGREGATION)


    def addRelation(self, relation:Relation):
        relation.source.addRelation(relation)

    def getElementById(self, ID:int):
        for element in self.elements:
            if element.id == ID:
                return element
        error = f"element with id: {ID} does not exist!"
        raise Exception(error)

    def getCode(self,path):
        self.elements.clear()
        with open(path) as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                if row["Name"] == "Class" :
                    if  "<<interface>>" in row["Text Area 1"]:
                        self.elements.append(self.createInterface(row))
                    else:
                        self.elements.append(self.createClass(row))
        with open(path) as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                if row["Name"] == "Line":
                    self.addRelation(self.createRelation(row))
        return self.elements

