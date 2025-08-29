from enum import Enum, property as enum_property
from typing import Any, ClassVar

from ocsf.objects._entity import Entity
from ocsf.objects.edge import Edge
from ocsf.objects.node import Node


class QueryLanguageId(Enum):
    UNKNOWN = 0
    CYPHER = 1
    GRAPHQL = 2
    GREMLIN = 3
    GQL = 4
    G_CORE = 5
    PGQL = 6
    SPARQL = 7
    OTHER = 99

    @classmethod
    def validate_python(cls, obj: Any):
        try:
            obj = int(obj)
        except ValueError:
            obj = str(obj).upper()
            return QueryLanguageId[obj]
        else:
            return QueryLanguageId(obj)

    @enum_property
    def name(self):
        name_map = {
            "UNKNOWN": "Unknown",
            "CYPHER": "Cypher",
            "GRAPHQL": "GraphQL",
            "GREMLIN": "Gremlin",
            "GQL": "GQL",
            "G_CORE": "G-CORE",
            "PGQL": "PGQL",
            "SPARQL": "SPARQL",
            "OTHER": "Other",
        }
        return name_map[super().name]


class Graph(Entity):
    schema_name: ClassVar[str] = "graph"

    # Required
    nodes: list[Node]

    # Recommended
    name: str | None = None
    query_language_id: QueryLanguageId | None = None
    uid: str | None = None

    # Optional
    desc: str | None = None
    edges: list[Edge] | None = None
    is_directed: bool | None = None
    query_language: str | None = None
    type_: str | None = None
