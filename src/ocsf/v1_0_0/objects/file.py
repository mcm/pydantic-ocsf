"""File object."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import Field, model_validator

from ocsf._base import OCSFBaseModel
from ocsf._sibling_enum import SiblingEnum

if TYPE_CHECKING:
    from ocsf.v1_0_0.objects.digital_signature import DigitalSignature
    from ocsf.v1_0_0.objects.fingerprint import Fingerprint
    from ocsf.v1_0_0.objects.object import Object
    from ocsf.v1_0_0.objects.product import Product
    from ocsf.v1_0_0.objects.user import User


class File(OCSFBaseModel):
    """The File object represents the metadata associated with a file stored in a computer system. It encompasses information about the file itself, including its attributes, properties, and organizational details. Defined by D3FEND <a target='_blank' href='https://next.d3fend.mitre.org/dao/artifact/d3f:File/'>d3f:File</a>.

    See: https://schema.ocsf.io/1.0.0/objects/file
    """

    # Nested Enums for sibling attribute pairs
    class ConfidentialityId(SiblingEnum):
        """The normalized identifier of the file content confidentiality indicator.

        OCSF Attribute: confidentiality_id
        """

        UNKNOWN = 0
        NOT_CONFIDENTIAL = 1
        CONFIDENTIAL = 2
        SECRET = 3
        TOP_SECRET = 4
        OTHER = 99

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                0: "Unknown",
                1: "Not Confidential",
                2: "Confidential",
                3: "Secret",
                4: "Top Secret",
                99: "Other",
            }

    class TypeId(SiblingEnum):
        """The file type ID.

        OCSF Attribute: type_id
        """

        UNKNOWN = 0
        REGULAR_FILE = 1
        FOLDER = 2
        CHARACTER_DEVICE = 3
        BLOCK_DEVICE = 4
        LOCAL_SOCKET = 5
        NAMED_PIPE = 6
        SYMBOLIC_LINK = 7
        OTHER = 99

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                0: "Unknown",
                1: "Regular File",
                2: "Folder",
                3: "Character Device",
                4: "Block Device",
                5: "Local Socket",
                6: "Named Pipe",
                7: "Symbolic Link",
                99: "Other",
            }

    name: Any = Field(
        ..., description="The name of the file. For example: <code>svchost.exe</code>"
    )
    type_id: TypeId = Field(..., description="The file type ID.")
    accessed_time: int | None = Field(
        default=None, description="The time when the file was last accessed."
    )
    accessor: User | None = Field(
        default=None, description="The name of the user who last accessed the object."
    )
    attributes: int | None = Field(
        default=None, description="The bitmask value that represents the file attributes."
    )
    company_name: str | None = Field(
        default=None,
        description="The name of the company that published the file. For example: <code>Microsoft Corporation</code>.",
    )
    confidentiality: str | None = Field(
        default=None,
        description="The file content confidentiality, normalized to the confidentiality_id value. In the case of 'Other', it is defined by the event source.",
    )
    confidentiality_id: ConfidentialityId | None = Field(
        default=None,
        description="The normalized identifier of the file content confidentiality indicator.",
    )
    created_time: int | None = Field(
        default=None, description="The time when the file was created."
    )
    creator: User | None = Field(default=None, description="The user that created the file.")
    desc: str | None = Field(
        default=None,
        description="The description of the file, as returned by file system. For example: the description as returned by the Unix file command or the Windows file type.",
    )
    hashes: list[Fingerprint] | None = Field(
        default=None, description="An array of hash attributes. [Recommended]"
    )
    is_system: bool | None = Field(
        default=None,
        description="The indication of whether the object is part of the operating system.",
    )
    mime_type: str | None = Field(
        default=None,
        description="The Multipurpose Internet Mail Extensions (MIME) type of the file, if applicable.",
    )
    modified_time: int | None = Field(
        default=None, description="The time when the file was last modified."
    )
    modifier: User | None = Field(default=None, description="The user that last modified the file.")
    owner: User | None = Field(default=None, description="The user that owns the file/object.")
    parent_folder: str | None = Field(
        default=None,
        description="The parent folder in which the file resides. For example: <code>c:\\windows\\system32</code>",
    )
    path: str | None = Field(
        default=None,
        description="The full path to the file. For example: <code>c:\\windows\\system32\\svchost.exe</code>. [Recommended]",
    )
    product: Product | None = Field(
        default=None, description="The product that created or installed the file."
    )
    security_descriptor: str | None = Field(
        default=None, description="The object security descriptor."
    )
    signature: DigitalSignature | None = Field(
        default=None, description="The digital signature of the file."
    )
    size: int | None = Field(default=None, description="The size of data, in bytes.")
    type_: str | None = Field(default=None, description="The file type.")
    uid: str | None = Field(
        default=None,
        description="The unique identifier of the file as defined by the storage system, such the file system file ID.",
    )
    version: str | None = Field(
        default=None, description="The file version. For example: <code>8.0.7601.17514</code>."
    )
    xattributes: Object | None = Field(
        default=None,
        description="An unordered collection of zero or more name/value pairs where each pair represents a file or folder extended attribute.</p>For example: Windows alternate data stream attributes (ADS stream name, ADS size, etc.), user-defined or application-defined attributes, ACL, owner, primary group, etc. Examples from DCS: </p><ul><li><strong>ads_name</strong></li><li><strong>ads_size</strong></li><li><strong>dacl</strong></li><li><strong>owner</strong></li><li><strong>primary_group</strong></li><li><strong>link_name</strong> - name of the link associated to the file.</li><li><strong>hard_link_count</strong> - the number of links that are associated to the file.</li></ul>",
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
            ("confidentiality_id", "confidentiality", cls.ConfidentialityId),
            ("type_id", "type", cls.TypeId),
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
