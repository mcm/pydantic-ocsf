"""Account object."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import Field, model_validator

from ocsf._base import OCSFBaseModel
from ocsf._sibling_enum import SiblingEnum

if TYPE_CHECKING:
    from ocsf.v1_6_0.objects.key_value_object import KeyValueObject


class Account(OCSFBaseModel):
    """The Account object contains details about the account that initiated or performed a specific activity within a system or application. Additionally, the Account object refers to logical Cloud and Software-as-a-Service (SaaS) based containers such as AWS Accounts, Azure Subscriptions, Oracle Cloud Compartments, Google Cloud Projects, and otherwise.

    See: https://schema.ocsf.io/1.6.0/objects/account
    """

    # Nested Enums for sibling attribute pairs
    class TypeId(SiblingEnum):
        """The normalized account type identifier.

        OCSF Attribute: type_id
        """

        UNKNOWN = 0
        LDAP_ACCOUNT = 1
        WINDOWS_ACCOUNT = 2
        AWS_IAM_USER = 3
        AWS_IAM_ROLE = 4
        GCP_ACCOUNT = 5
        AZURE_AD_ACCOUNT = 6
        MAC_OS_ACCOUNT = 7
        APPLE_ACCOUNT = 8
        LINUX_ACCOUNT = 9
        AWS_ACCOUNT = 10
        GCP_PROJECT = 11
        OCI_COMPARTMENT = 12
        AZURE_SUBSCRIPTION = 13
        SALESFORCE_ACCOUNT = 14
        GOOGLE_WORKSPACE = 15
        SERVICENOW_INSTANCE = 16
        M365_TENANT = 17
        EMAIL_ACCOUNT = 18
        OTHER = 99

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                0: "Unknown",
                1: "LDAP Account",
                2: "Windows Account",
                3: "AWS IAM User",
                4: "AWS IAM Role",
                5: "GCP Account",
                6: "Azure AD Account",
                7: "Mac OS Account",
                8: "Apple Account",
                9: "Linux Account",
                10: "AWS Account",
                11: "GCP Project",
                12: "OCI Compartment",
                13: "Azure Subscription",
                14: "Salesforce Account",
                15: "Google Workspace",
                16: "Servicenow Instance",
                17: "M365 Tenant",
                18: "Email Account",
                99: "Other",
            }

    labels: list[str] | None = Field(
        default=None, description="The list of labels associated to the account."
    )
    name: str | None = Field(
        default=None,
        description="The name of the account (e.g. <code> GCP Project name </code>, <code> Linux Account name </code> or <code> AWS Account name</code>).",
    )
    tags: list[KeyValueObject] | None = Field(
        default=None,
        description="The list of tags; <code>{key:value}</code> pairs associated to the account.",
    )
    type_: str | None = Field(
        default=None,
        description="The account type, normalized to the caption of 'account_type_id'. In the case of 'Other', it is defined by the event source.",
    )
    type_id: TypeId | None = Field(
        default=None, description="The normalized account type identifier. [Recommended]"
    )
    uid: str | None = Field(
        default=None,
        description="The unique identifier of the account (e.g. <code> AWS Account ID </code>, <code> OCID </code>, <code> GCP Project ID </code>, <code> Azure Subscription ID </code>, <code> Google Workspace Customer ID </code>, or <code> M365 Tenant UID</code>).",
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
