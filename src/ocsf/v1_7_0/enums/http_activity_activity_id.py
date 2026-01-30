"""The normalized identifier of the activity that triggered the event. enumeration."""

from enum import IntEnum


class HttpActivityActivityId(IntEnum):
    """The normalized identifier of the activity that triggered the event.

    See: https://schema.ocsf.io/1.7.0/data_types/http_activity_activity_id
    """

    CONNECT = 1  # The CONNECT method establishes a tunnel to the server identified by the target resource.
    DELETE = 2  # The DELETE method deletes the specified resource.
    GET = 3  # The GET method requests a representation of the specified resource. Requests using GET should only retrieve data.
    HEAD = 4  # The HEAD method asks for a response identical to a GET request, but without the response body.
    OPTIONS = 5  # The OPTIONS method describes the communication options for the target resource.
    POST = 6  # The POST method submits an entity to the specified resource, often causing a change in state or side effects on the server.
    PUT = 7  # The PUT method replaces all current representations of the target resource with the request payload.
    TRACE = 8  # The TRACE method performs a message loop-back test along the path to the target resource.
    PATCH = 9  # The PATCH method applies partial modifications to a resource.
