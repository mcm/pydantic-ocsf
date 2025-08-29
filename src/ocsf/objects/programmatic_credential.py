from datetime import datetime
from typing import ClassVar

from ocsf.objects.object import Object


class ProgrammaticCredential(Object):
    schema_name: ClassVar[str] = "programmatic_credential"

    # Required
    uid: str

    # Recommended
    type_: str | None = None

    # Optional
    last_used_time: datetime | None = None
