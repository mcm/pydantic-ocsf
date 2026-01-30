"""Graph object."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import Field, model_validator

from ocsf._base import OCSFBaseModel
from ocsf._sibling_enum import SiblingEnum

if TYPE_CHECKING:
    from ocsf.v1_5_0.objects.edge import Edge
    from ocsf.v1_5_0.objects.node import Node


class Graph(OCSFBaseModel):
    """A graph data structure representation with nodes and edges.

    See: https://schema.ocsf.io/1.5.0/objects/graph
    """

    # Nested Enums for sibling attribute pairs
    class QueryLanguageId(SiblingEnum):
        """The normalized identifier of a graph query language that can be used to interact with the graph.

        OCSF Attribute: query_language_id
        """

        CYPHER = 1
        GRAPHQL = 2
        GREMLIN = 3
        GQL = 4
        G_CORE = 5
        PGQL = 6
        SPARQL = 7

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                1: "Cypher",
                2: "GraphQL",
                3: "Gremlin",
                4: "GQL",
                5: "G-CORE",
                6: "PGQL",
                7: "SPARQL",
            }

    nodes: list[Node] = Field(
        ...,
        description="The nodes/vertices of the graph - contains the collection of <code>node</code> objects that make up the graph.",
    )
    desc: str | None = Field(
        default=None,
        description="The graph description - provides additional details about the graph's purpose and contents.",
    )
    edges: list[Edge] | None = Field(
        default=None,
        description="The edges/connections between nodes in the graph - contains the collection of <code>edge</code> objects defining relationships between nodes.",
    )
    is_directed: bool | None = Field(
        default=None,
        description="Indicates if the graph is directed (<code>true</code>) or undirected (<code>false</code>).",
    )
    name: str | None = Field(
        default=None, description="The graph name - a human readable identifier for the graph."
    )
    query_language: str | None = Field(
        default=None,
        description="The graph query language, normalized to the caption of the <code>query_language_id</code> value.",
    )
    query_language_id: QueryLanguageId | None = Field(
        default=None,
        description="The normalized identifier of a graph query language that can be used to interact with the graph. [Recommended]",
    )
    type_: str | None = Field(
        default=None,
        description="The graph type. Typically useful to represent the specifc type of graph that is used.",
    )
    uid: str | None = Field(
        default=None,
        description="Unique identifier of the graph - a unique ID to reference this specific graph.",
    )

    @model_validator(mode="before")
    @classmethod
    def _reconcile_siblings(cls, data: Any) -> Any:
        """Reconcile sibling attribute pairs during parsing.

        For each sibling pair (e.g., activity_id/activity_name):
        - If both present: validate they match, use canonical label casing
        - If only ID: extrapolate label from enum
        - If only label: extrapolate ID from enum (unknown → OTHER=99)
        - If neither: leave for field validation to handle required/optional
        """
        if not isinstance(data, dict):
            return data

        # Sibling pairs for this object class
        siblings: list[tuple[str, str, type[SiblingEnum]]] = [
            ("query_language_id", "query_language", cls.QueryLanguageId),
        ]

        for id_field, label_field, enum_cls in siblings:
            id_val = data.get(id_field)
            label_val = data.get(label_field)

            has_id = id_val is not None
            has_label = label_val is not None

            if has_id and has_label:
                # Both present: validate consistency
                assert id_val is not None  # Type narrowing for mypy
                try:
                    enum_member = enum_cls(id_val)
                except (ValueError, KeyError) as e:
                    raise ValueError(f"Invalid {id_field} value: {id_val}") from e

                expected_label = enum_member.label

                # OTHER (99) allows any custom label
                if enum_member.value != 99:
                    if expected_label.lower() != str(label_val).lower():
                        raise ValueError(
                            f"{id_field}={id_val} ({expected_label}) "
                            f"does not match {label_field}={label_val!r}"
                        )
                    # Use canonical label casing
                    data[label_field] = expected_label
                # For OTHER, preserve the custom label as-is

            elif has_id:
                # Only ID provided: extrapolate label
                assert id_val is not None  # Type narrowing for mypy
                try:
                    enum_member = enum_cls(id_val)
                    data[label_field] = enum_member.label
                except (ValueError, KeyError) as e:
                    raise ValueError(f"Invalid {id_field} value: {id_val}") from e

            elif has_label:
                # Only label provided: extrapolate ID
                try:
                    enum_member = enum_cls(str(label_val))
                    data[id_field] = enum_member.value
                    data[label_field] = enum_member.label  # Canonical casing
                except (ValueError, KeyError):
                    # Unknown label during JSON parsing → map to OTHER (99) if available
                    # This is lenient for untrusted data, unlike direct enum construction
                    if hasattr(enum_cls, "OTHER"):
                        data[id_field] = 99
                        data[label_field] = "Other"  # Use canonical OTHER label
                    else:
                        raise ValueError(
                            f"Unknown {label_field} value: {label_val!r} "
                            f"and {enum_cls.__name__} has no OTHER member"
                        ) from None

        return data
