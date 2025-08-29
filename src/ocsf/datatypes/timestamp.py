from datetime import datetime
from typing import Annotated

from pydantic import PlainSerializer, PlainValidator


def serialize_timestamp_t(value: datetime) -> int:
    return int(value.timestamp() * 1000)


def validate_timestamp_t(value: int) -> datetime:
    return datetime.fromtimestamp(value / 1000)


Timestamp = Annotated[datetime, PlainValidator(validate_timestamp_t), PlainSerializer(serialize_timestamp_t)]
