"""Script object."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import Field, model_validator

from ocsf._base import OCSFBaseModel
from ocsf._sibling_enum import SiblingEnum

if TYPE_CHECKING:
    from ocsf.v1_7_0.objects.file import File
    from ocsf.v1_7_0.objects.fingerprint import Fingerprint
    from ocsf.v1_7_0.objects.long_string import LongString


class Script(OCSFBaseModel):
    """The Script object describes a script or command that can be executed by a shell, script engine, or interpreter. Examples include Bash, JavsScript, PowerShell, Python, VBScript, etc. Note that the term <em>script</em> here denotes not only a script contained within a file but also a script or command typed interactively by a user, supplied on the command line, or provided by some other file-less mechanism.

    See: https://schema.ocsf.io/1.7.0/objects/script
    """

    # Nested Enums for sibling attribute pairs
    class TypeId(SiblingEnum):
        """The normalized script type ID.

        OCSF Attribute: type_id
        """

        UNKNOWN = 0
        WINDOWS_COMMAND_PROMPT = 1
        POWERSHELL = 2
        PYTHON = 3
        JAVASCRIPT = 4
        VBSCRIPT = 5
        UNIX_SHELL = 6
        VBA = 7
        OTHER = 99

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                0: "Unknown",
                1: "Windows Command Prompt",
                2: "PowerShell",
                3: "Python",
                4: "JavaScript",
                5: "VBScript",
                6: "Unix Shell",
                7: "VBA",
                99: "Other",
            }

    script_content: LongString = Field(
        ...,
        description="The script content, normalized to UTF-8 encoding irrespective of its original encoding. When emitting this attribute, it may be appropriate to truncate large scripts. When consuming this attribute, large scripts should be anticipated.",
    )
    type_id: TypeId = Field(..., description="The normalized script type ID.")
    file: File | None = Field(
        default=None,
        description="Present if this script is associated with a file. Not present in the case of a file-less script.",
    )
    hashes: list[Fingerprint] | None = Field(
        default=None,
        description="An array of the script's cryptographic hashes. Note that these hashes are calculated on the script in its original encoding, and not on the normalized UTF-8 encoding found in the <code>script_content</code> attribute. [Recommended]",
    )
    name: str | None = Field(
        default=None,
        description="Unique identifier for the script or macro, independent of the containing file, used for tracking, auditing, and security analysis.",
    )
    parent_uid: str | None = Field(
        default=None,
        description="This attribute relates a sub-script to a parent script having the matching <code>uid</code> attribute. In the case of PowerShell, sub-script execution can be identified by matching the activity correlation ID of the raw ETW events provided by the OS.",
    )
    type_: str | None = Field(
        default=None,
        description="The script type, normalized to the caption of the <code>type_id</code> value. In the case of 'Other', it is defined by the event source.",
    )
    uid: str | None = Field(
        default=None,
        description="Some script engines assign a unique ID to each individual execution of a given script. This attribute captures that unique ID. In the case of PowerShell, the unique ID corresponds to the <code>ScriptBlockId</code> in the raw ETW events provided by the OS.",
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
