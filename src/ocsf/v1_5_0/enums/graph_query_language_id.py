"""The normalized identifier of a graph query language that can be used to interact with the graph. enumeration."""

from enum import IntEnum


class GraphQueryLanguageId(IntEnum):
    """The normalized identifier of a graph query language that can be used to interact with the graph.

    See: https://schema.ocsf.io/1.5.0/data_types/graph_query_language_id
    """

    CYPHER = 1  # A declarative graph query language developed by Neo4j that allows for expressive and efficient querying of graph databases.
    GRAPHQL = 2  # A query language for APIs that enables declarative data fetching and provides a complete description of the data in the API.
    GREMLIN = 3  # A graph traversal language and virtual machine developed by Apache TinkerPop that enables graph computing across different graph databases.
    GQL = 4  # An ISO standard graph query language designed to provide a unified way to query graph databases.
    G_CORE = 5  # A graph query language that combines features from existing languages while adding support for paths as first-class citizens.
    PGQL = 6  # Property Graph Query Language developed by Oracle that provides SQL-like syntax for querying property graphs.
    SPARQL = 7  # A semantic query language for databases that enables querying and manipulating data stored in RDF format.
