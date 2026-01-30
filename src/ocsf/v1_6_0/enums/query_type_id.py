"""The normalized type of system query performed against a device or system component. enumeration."""

from enum import IntEnum


class QueryTypeId(IntEnum):
    """The normalized type of system query performed against a device or system component.

    See: https://schema.ocsf.io/1.6.0/data_types/query_type_id
    """

    UNKNOWN = 0  # The query type was unknown or not specified.
    KERNEL = 1  # A query about kernel resources including system calls, shared mutex, or other kernel components.
    FILE = 2  # A query about file attributes, metadata, content, hash values, or properties.
    FOLDER = 3  # A query about folder attributes, metadata, content, or structure.
    ADMIN_GROUP = 4  # A query about group membership, privileges, domain, or group properties.
    JOB = 5  # A query about scheduled jobs, their command lines, run states, or execution times.
    MODULE = 6  # A query about loaded modules, their base addresses, load types, or function entry points.
    NETWORK_CONNECTION = (
        7  # A query about active network connections, boundaries, protocols, or TCP states.
    )
    NETWORK_INTERFACES = (
        8  # A query about physical or virtual network interfaces, their IP/MAC addresses, or types.
    )
    PERIPHERAL_DEVICE = 9  # A query about attached peripheral devices, their classes, models, or vendor information.
    PROCESS = 10  # A query about running processes, command lines, ancestry, loaded modules, or execution context.
    SERVICE = 11  # A query about system services, their names, versions, labels, or properties.
    SESSION = 12  # A query about authenticated user or service sessions, their creation times, or issuer details.
    USER = 13  # A query about user accounts, their properties, credentials, or domain information.
    USERS = 14  # A query about multiple users belonging to an administrative group.
    STARTUP_ITEM = 15  # A query about startup configuration items, their run modes, start types, or current states.
    REGISTRY_KEY = 16  # A Windows-specific query about registry keys, their paths, security descriptors, or modification times.
    REGISTRY_VALUE = (
        17  # A Windows-specific query about registry values, their data types, content, or names.
    )
    PREFETCH = 18  # A Windows-specific query about prefetch files, their run counts, last execution times, or existence.
    OTHER = 99  # The query type was not mapped to a standard category. See the query_type attribute for source-specific value.
