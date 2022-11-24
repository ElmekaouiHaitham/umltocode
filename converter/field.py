from converter.programming_languages import ProgrammingLangs
from converter.visibility import Visibility


class Field:
    """to model the fields (class attributes)"""
    def __init__(self, fieldString:str, progLang: ProgrammingLangs):

        self.progLang = progLang

        self.visibility = Visibility.getVisibility(fieldString)

        fieldString = fieldString[1:]
        # check if there a default value
        self.defaultValue = None
        if "=" in fieldString:
            [rest,default] = fieldString.split("=")
            self.defaultValue = default
            fieldString = rest
        try:
            [self.name, self.type] = fieldString.split(":")
        except:
            error = f"problem at {fieldString}"
            raise Exception(error)


    def __str__(self):
        if self.progLang == ProgrammingLangs.DART:
            return self.getDartCode()

        s = f"{self.visibility}  {self.type}  {self.name}"
        if self.defaultValue != None:
            s += "  =  " +  self.defaultValue
        return s

    def getDartCode(self):
        return f"{self.type} {self.name};"+ '\n'
