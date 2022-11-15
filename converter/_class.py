from textwrap import indent
from converter.field import Field
from converter.method import Method
from converter.programming_languages import ProgrammingLangs
from converter.relation import Relation, RelationType
from converter.super_type import SuperType
import copy
from converter.snippets.dart.classd import dartClassTemplate


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

    def getDartSupers(self):
        s = ''
        classes = []
        interfaces = []
        for relation in self.relations:
            if relation.RelationType == RelationType.INHERITANCE:
                if relation.destination.type == SuperType.CLASS:
                    classes.append(relation.destination)
                else:
                    interfaces.append(relation.destination)

        if len(classes) != 0:
            s += "extends "
            s += classes[0].name
            classes = classes[1:]
            if len(classes) != 0:
                s += "with "
                for c in range(1, len(classes)):
                    s += c.name + ","
                s = s[:len(s)-1]
        elif len(interfaces) != 0:
            s += "implements "
            for i in interfaces:
                for m in i.methods:
                    nm = copy.deepcopy(m)
                    nm.superType = SuperType.CLASS
                    self.methods.append(nm)
                s += i.name + ","
            s = s[:len(s)-1]
        return s


class Dart:
    @staticmethod
    def getClassCode(cl:Class):
        return dartClassTemplate.format(name=cl.name, generalization=cl.getDartSupers(), fields=Dart.getFieldsCode(cl), methods=Dart.getMethodsCode(cl), constructorFields=Dart.getConstructorFields(cl), constructorInit=Dart.getConstructorInit(cl))

    def getMethodsCode(cl:Class):
        s = ''
        for method in cl.methods:
            s += str(method)
        return indent(s, " "*4)

    def getFieldsCode(cl:Class):
        s = ''
        for field in cl.fields:
            s += str(field)

        for relation in cl.relations:
            if relation.RelationType == RelationType.COMPOSITION:
                s += f'late {relation.destination.name} {relation.destination.name.lower()};'
        return indent(s, " "*4)

    def getConstructorFields(cl:Class):
        s = ''
        for field in cl.fields:
            if field.defaultValue != None:
                s += f"this.{field.name} = {field.defaultValue}, "
            else:
                s += f"required this.{field.name}, "


        return s

    def getConstructorInit(cl:Class):
        s = ''
        for relation in cl.relations:
            if relation.RelationType == RelationType.COMPOSITION:
                s += indent(
                    f"// TODO: initialize {relation.destination.name.lower()}\n", " "*2)
                s += indent(f"this.{relation.destination.name.lower()};", " "*2)
        return indent(s, " "*4)
