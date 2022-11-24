

"""class template you need to format it by giving thr following properties:
name, generalization, fields, constructorFields, constructorInit, methods"""
import copy
from textwrap import indent

from converter.relation import RelationType
from converter.super_type import SuperType


dartClassTemplate : str = """

class {name} {generalization} {{
{fields}

    {name}({constructorFields}){{
{constructorInit}
    }}

{methods}
}}
"""



class Dart:
    @staticmethod
    def getClassCode(cl):
        return dartClassTemplate.format(name=cl.name, generalization=Dart.getGeneralizationCode(cl), fields=Dart.getFieldsCode(cl), methods=Dart.getMethodsCode(cl), constructorFields=Dart.getConstructorFields(cl), constructorInit=Dart.getConstructorInit(cl))

    def getGeneralizationCode(cl):

        s = ''
        classes = []
        interfaces = []
        for relation in cl.relations:
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
                    cl.methods.append(nm)
                s += i.name + ","
            s = s[:len(s)-1]
        return s

    def getMethodsCode(cl):
        s = ''
        for method in cl.methods:
            s += str(method)
        return indent(s, " "*4)

    def getFieldsCode(cl):
        s = ''
        for field in cl.fields:
            s += str(field)

        for relation in cl.relations:
            if relation.RelationType == RelationType.COMPOSITION:
                s += f'late {relation.destination.name} {relation.destination.name.lower()};'
        return indent(s, " "*4)

    def getConstructorFields(cl):
        s = '{'
        for field in cl.fields:
            if field.defaultValue != None:
                s += f"this.{field.name} = {field.defaultValue}, "
            else:
                s += f"required this.{field.name}, "

        s += '}'
        if s == '{}':
            return ''
        return s

    def getConstructorInit(cl):
        s = ''
        for relation in cl.relations:
            if relation.RelationType == RelationType.COMPOSITION:
                s += indent(
                    f"// TODO: initialize {relation.destination.name.lower()}\n", " "*2)
                s += indent(f"this.{relation.destination.name.lower()};", " "*2)
        return indent(s, " "*4)

