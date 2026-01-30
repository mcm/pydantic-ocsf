"""The type of SBOM. enumeration."""

from enum import IntEnum


class SbomTypeId(IntEnum):
    """The type of SBOM.

    See: https://schema.ocsf.io/1.5.0/data_types/sbom_type_id
    """

    SPDX = 1  # System Package Data Exchange (SPDX®) is an open standard capable of representing systems with software components in as SBOMs (Software Bill of Materials) and other AI, data and security references supporting a range of risk management use cases. The SPDX specification is a freely available international open standard (ISO/IEC 5692:2021).
    CYCLONEDX = 2  # CycloneDX is an International Standard for Bill of Materials (ECMA-424).
    SWID = 3  # The International Organization for Standardization (ISO) and the International Electrotechnical Commission (IEC) publishes, ISO/IEC 19770-2, a standard for software identification (SWID) tags that defines a structured metadata format for describing a software product. A SWID tag document is composed of a structured set of data elements that identify the software product
