from datetime import datetime
from typing import ClassVar

from pydantic import AnyUrl

from ocsf.objects._entity import Entity
from ocsf.objects.product import Product


class TransformationInfo(Entity):
    schema_name: ClassVar[str] = "transformation_info"

    # Recommended
    name: str | None = None
    time: datetime | None = None
    url_string: AnyUrl | None = None

    # Optional
    lang: str | None = None
    product: Product | None = None
    uid: str | None = None
