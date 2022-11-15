

"""class template you need to format it by giving thr following properties:
name, generalization, fields, constructorFields, constructorInit, methods"""
dartClassTemplate : str = """

class {name} {generalization} {{
{fields}

    {name}({{{constructorFields}}}){{
{constructorInit}
    }}

{methods}
}}
"""


