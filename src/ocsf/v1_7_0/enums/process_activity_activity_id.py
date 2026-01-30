"""The normalized identifier of the activity that triggered the event. enumeration."""

from enum import IntEnum


class ProcessActivityActivityId(IntEnum):
    """The normalized identifier of the activity that triggered the event.

    See: https://schema.ocsf.io/1.7.0/data_types/process_activity_activity_id
    """

    LAUNCH = 1  # A request by the actor to launch another process. Refer to the <code>launch_type_id</code> attribute for details of the specific launch type.
    TERMINATE = 2  # A request by the actor to terminate a process. This activity is most commonly reflexive, this being the case when a process exits at its own initiation. Note too that Windows security products cannot always identify the actor in the case of inter-process termination. In this case, <code>actor.process</code> and <code>process</code> refer to the exiting process, i.e. indistinguishable from the reflexive case.
    OPEN = 3  # A request by the actor to obtain a handle or descriptor to a process with the aim of performing further actions upon that process. The target is usually a different process but this activity can also be reflexive.
    INJECT = 4  # A request by the actor to execute code within the context of a process. The target is usually a different process but this activity can also be reflexive. Refer to the <code>injection_type_id</code> attribute for details of the specific injection type.
    SET_USER_ID = 5  # A request by the actor to change its user identity by invoking the <code>setuid()</code> system call. Common programs like <code>su</code> and <code>sudo</code> use this mechanism. Note that the <em>impersonation</em> mechanism on Windows is not directly equivalent because it acts at the thread level.
