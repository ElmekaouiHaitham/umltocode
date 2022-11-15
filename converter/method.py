from converter.programming_languages import ProgrammingLangs
from converter.super_type import SuperType
from converter.visibility import Visibility

class Method:
    """to model the methods"""

    def __init__(self,methodString:str, progLang: ProgrammingLangs, superType = SuperType.CLASS):

        self.superType = superType

        self.progLang = progLang

        self.visibility = Visibility.getVisibility(methodString[0])

        methodString = methodString[1:]

        if "(" in methodString and ")" in methodString:
            # index of (
            i1 = methodString.index("(")
            i2 = methodString.index(")")
            parameterString = methodString[i1+1:i2]
            # remove the parameter list from original string
            methodString = methodString[0:i1]+methodString[i2+1:]
            # get the list of parameters
            paramList = parameterString.split(',')

            self.parameters = []
            if parameterString != "":
                for param in paramList:
                    [name,type] = param.split(':')
                    self.parameters.append({'name':name,'type':type})
        else:
            raise "missing parameter list"
        if ":" in methodString:
            [self.name, self.returnType] = methodString.split(":")
        else:
            self.returnType = "void"
            self.name = methodString

    def __str__(self):
        if self.progLang == ProgrammingLangs.DART:
            return self.getDartCode()
        return f"def {self.name}({self.getParameters()}) -> {self.returnType}\n        pass" + '\n'

    def getDartCode(self):
        if self.superType == SuperType.INTERFACE:
             return self.getInterfaceDartCode()
        return self.getClassDartCode()
    def getInterfaceDartCode(self):
        s = f"{self.returnType} "
        if self.visibility == Visibility.PRIVATE:
            s += "_"
        s += f"{self.name}({self.getParameters()});"
        return s


    def getClassDartCode(self):
        s = f"{self.returnType} "
        if self.visibility == Visibility.PRIVATE:
            s += "_"
        s += f"{self.name}({self.getParameters()})"
        s += f"""{"{"}
        // TODO: implement {self.name}
        throw "unimplemented";
    {"}"}"""
        return s + '\n'

    def getParameters(self):
        s = ""
        for param in self.parameters:
            s += param["type"] + " " +param["name"]
            if self.parameters.index(param) < len(self.parameters) -1:
                s += ",  "
        return s
