from typing import ClassVar

from pydantic import BaseModel


class Object(BaseModel):
    schema_name: ClassVar[str] = "object"
