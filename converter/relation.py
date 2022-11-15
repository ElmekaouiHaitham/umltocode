from enum import Enum


class RelationType(Enum):
    INHERITANCE = "inheritance"
    AGGREGATION = "aggregation"
    COMPOSITION = "composition"

class Relation:
    def __init__(self, source, destination, type:RelationType):
        self.source = source
        self.destination = destination
        self.RelationType = type
    def __str__(self):
        return f'from {self.source.name}  to {self.destination.name} with {self.RelationType}'
