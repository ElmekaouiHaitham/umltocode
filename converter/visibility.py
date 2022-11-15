from enum import Enum


class Visibility(Enum):
    PRIVATE = "-"
    PUBLIC = "+"
    PROTECTED = "#"
    def getVisibility(s:str):
        if Visibility.PRIVATE.value==s[0]:
            return Visibility.PRIVATE
        elif Visibility.PUBLIC.value==s[0]:
            return Visibility.PUBLIC
        elif Visibility.PROTECTED.value==s[0]:
            return Visibility.PROTECTED
        else:
            error = f"visibility wasn't set at {s}"
            raise Exception(error)

