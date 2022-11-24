from textwrap import indent
from converter.field import Field
from converter.method import Method
from converter.programming_languages import ProgrammingLangs
from converter.relation import Relation, RelationType
from converter.super_type import SuperType
import copy
from converter.code.dart.class_gen import Dart


class Class:
    """models a class with name relations, methods, fields .. """

    def __init__(self, classString: str, progLang: ProgrammingLangs):
        self.type = SuperType.CLASS
        self.progLang = progLang
        self.id = int(classString["Id"])
        self.name = classString["Text Area 1"]
        self.fields = self.makeFields(classString["Text Area 2"])
        self.methods = self.makeMethods(classString["Text Area 3"])
        self.relations = []

    def __str__(self):
        if self.progLang == ProgrammingLangs.DART:
            return Dart.getClassCode(self)


    def getConstructor(self, indentation):
        s = f"{self.name}({'{'}\n"
        for field in self.fields:
            if field.defaultValue != None:
                s += indentation+f"this.{field.name} = {field.defaultValue},\n"
            else:
                s += indentation+f"required this.{field.name},\n"

        s += '}){'+"\n"
        # check if there is a composition relation;
        for relation in self.relations:
            if relation.RelationType == RelationType.COMPOSITION:
                s += indentation + \
                    f"// TODO: initialize {relation.destination.name.lower()}\n"
                s += indentation + \
                    f"this.{relation.destination.name.lower()};"
        s += "\n}\n"
        return s

    def makeFields(self, fieldsString: str):
        # remove some weird chars â€‹
        fieldsString = fieldsString[3:]
        # separate the fields in list
        fieldStringList = fieldsString.replace(" ", "").split("\n")
        fields = []
        for field in fieldStringList:
            if field != "":
                fields.append(Field(field, self.progLang))
        return fields

    def makeMethods(self, methodsString: str):

        # remove some weird chars â€‹
        methodsString = methodsString[3:]
        # separate the fields in list
        methodStringList = methodsString.replace(" ", "").split("\n")
        methods = []
        for method in methodStringList:
            # ignore empty lines
            if len(method) != 0:
                methods.append(Method(method, self.progLang))
        return methods

    def addRelation(self, relation: Relation):
        self.relations.append(relation)
        if relation.RelationType == RelationType.AGGREGATION:
            self.fields.append(Field(
                f"-{relation.destination.name.lower()}:{relation.destination.name}", self.progLang))

    