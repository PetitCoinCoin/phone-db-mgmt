from datetime import datetime

from pydantic import BaseModel


class PhoneNumberType(BaseModel):
    id: int
    phone: str
    phone_range_id: int
    customer_id: int
    allocation_date: datetime
    cancellation_date: datetime | None


class PhoneNumberWriteOnlyType(BaseModel):
    phone: str
    customer_id: int


class PhoneRangeType(BaseModel):
    id: int
    lower: str
    upper: str
    phone_numbers: list[PhoneNumberType]


class PhoneRangeWriteOnlyType(BaseModel):
    lower: str
    upper: str


class CustomerType(BaseModel):
    id: int
    name: str
    phone_numbers: list[PhoneNumberType]


class CustomerWriteOnlyType(BaseModel):
    name: str
