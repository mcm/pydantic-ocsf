"""Test script to verify type stubs work correctly.

This script exercises various type annotations to ensure:
1. Object references show proper types (not Any)
2. Type checkers can infer types correctly
3. IDE autocomplete works
"""

from typing import TYPE_CHECKING

from ocsf.v1_7_0.events import ApiActivity, IncidentFinding
from ocsf.v1_7_0.objects import Actor, Api, FindingInfo, Metadata, Product, User

if TYPE_CHECKING:
    from typing import reveal_type  # noqa: F401


def test_incident_finding_types() -> None:
    """Test that IncidentFinding has proper type annotations."""
    # Create a finding
    finding = IncidentFinding(
        activity_id=1,
        severity_id=1,
        status_id=1,
        time=1234567890,
        metadata=Metadata(version="1.7.0", product=Product(name="Test")),
        finding_info_list=[
            FindingInfo(
                title="Security Issue",
                uid="finding-123",
            )
        ],
    )

    # Type checker should know these are proper types, not Any
    # The metadata field should be Metadata, not Any
    if TYPE_CHECKING:
        metadata: Metadata = finding.metadata
        reveal_type(metadata)  # Should show as Metadata

    # The assignee field should be User | None, not Any | None
    if finding.assignee:
        if TYPE_CHECKING:
            user: User = finding.assignee
            reveal_type(user)  # Should show as User

        # Should have User attributes
        print(f"Assignee: {finding.assignee.name}")

    # The finding_info_list should be list[FindingInfo], not list[Any]
    for info in finding.finding_info_list:
        if TYPE_CHECKING:
            finding_info: FindingInfo = info
            reveal_type(finding_info)  # Should show as FindingInfo

        # Should have FindingInfo attributes
        print(f"Finding: {info.title}")


def test_api_activity_types() -> None:
    """Test that ApiActivity has proper type annotations."""
    from ocsf.v1_7_0.objects import NetworkEndpoint

    activity = ApiActivity(
        activity_id=1,
        severity_id=1,
        time=1234567890,
        src_endpoint=NetworkEndpoint(),
        actor=Actor(
            user=User(name="alice@example.com", uid="user-123"),
        ),
        api=Api(
            operation="CreateBucket",
        ),
        metadata=Metadata(
            version="1.7.0",
            product=Product(name="AWS CloudTrail"),
        ),
    )

    # The actor field should be Actor | None, not Any | None
    if activity.actor:
        if TYPE_CHECKING:
            actor: Actor = activity.actor
            reveal_type(actor)  # Should show as Actor

        # Should have Actor attributes
        if activity.actor.user:
            print(f"User: {activity.actor.user.name}")

    # The api field should be Api | None, not Any | None
    if activity.api:
        if TYPE_CHECKING:
            api: Api = activity.api
            reveal_type(api)  # Should show as Api

        # Should have Api attributes
        print(f"Operation: {activity.api.operation}")

    # The metadata field should be Metadata, not Any
    if TYPE_CHECKING:
        metadata: Metadata = activity.metadata
        reveal_type(metadata)  # Should show as Metadata

    # Should have Metadata attributes
    print(f"Version: {activity.metadata.version}")


def test_list_types() -> None:
    """Test that list types are properly annotated."""
    finding = IncidentFinding(
        activity_id=1,
        severity_id=1,
        status_id=1,
        time=1234567890,
        metadata=Metadata(version="1.7.0", product=Product(name="Test")),
        finding_info_list=[
            FindingInfo(title="Issue 1", uid="f1"),
            FindingInfo(title="Issue 2", uid="f2"),
        ],
    )

    # finding_info_list should be list[FindingInfo], not list[Any]
    if TYPE_CHECKING:
        info_list: list[FindingInfo] = finding.finding_info_list
        reveal_type(info_list)  # Should show as list[FindingInfo]

    for info in finding.finding_info_list:
        # Each item should be FindingInfo, not Any
        if TYPE_CHECKING:
            finding_info: FindingInfo = info
            reveal_type(finding_info)  # Should show as FindingInfo

        print(f"Finding: {info.title}")


if __name__ == "__main__":
    print("Testing type annotations...")
    test_incident_finding_types()
    test_api_activity_types()
    test_list_types()
    print("✅ All tests passed!")
