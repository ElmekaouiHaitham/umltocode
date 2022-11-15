from converter.method import Method
from converter.programming_languages import ProgrammingLangs
from converter.super_type import SuperType


class Interface:
    """models a interface with name methods .. """

    def __init__(self, interfaceString: str, progLang: ProgrammingLangs):
        self.type = SuperType.INTERFACE
        self.progLang = progLang
        self.id = int(interfaceString["Id"])
        self.name = interfaceString["Text Area 1"].split('\n')[1]
        self.methods = self.makeMethods(interfaceString["Text Area 2"])
        self.relations = []

    def __str__(self):
        if self.progLang == ProgrammingLangs.DART:
            return self.getDartCode()
        s = f"interface {self.name}:"
        indentation = "    "
        s += "\n"
        for method in self.methods:
            s += "\n" + indentation + method.__str__()
        return s

    def getDartCode(self):
        s = f"abstract class {self.name}{'{'}"
        indentation = "    "
        for method in self.methods:
            s += "\n" + indentation + method.__str__()
        return s + '\n}'

    def makeMethods(self, methodsString: str):
        # # remove some weird chars â€‹
        methodsString = methodsString[3:]
        # # separate the fields in list
        methodStringList = methodsString.replace(" ", "").split("\n")
        methods = []
        for method in methodStringList:
            if len(method) != 0:
                methods.append(Method(method, self.progLang, self.type))
        return methods

    def addRelation(self, relation):
        self.relations.append(relation)
