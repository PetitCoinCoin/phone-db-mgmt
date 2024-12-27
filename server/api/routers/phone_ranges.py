from fastapi import APIRouter, HTTPException, status

from api.db import get_session
from api.models import PhoneRange
from api.serializers import PhoneRangeType, PhoneRangeWriteOnlyType

router = APIRouter()
PHONE_RANGE_TAG = "Phone ranges"
PHONE_RANGE_BASE_URL = "/phone_ranges"


@router.get(
        PHONE_RANGE_BASE_URL,
        tags=[PHONE_RANGE_TAG],
        response_model=list[PhoneRangeType],
    )
def list_phone_ranges():
    session = next(get_session())
    query = session.query(PhoneRange)
    return query.all()


@router.post(
        PHONE_RANGE_BASE_URL,
        tags=[PHONE_RANGE_TAG],
        response_model=PhoneRangeType,
        status_code=status.HTTP_201_CREATED,
        )
def create_phone_range(new_phone_range: PhoneRangeWriteOnlyType):
    # should check for overlap and respond with 409
    # should match phone regex
    session = next(get_session())
    phone_range: PhoneRange = PhoneRange(**new_phone_range.model_dump())
    session.add(phone_range)
    session.commit()
    session.refresh(phone_range)
    return phone_range


@router.get(
        PHONE_RANGE_BASE_URL + "/{id}",
        tags=[PHONE_RANGE_TAG],
        response_model=PhoneRangeType,
    )
def get_phone_range(id: int):
    session = next(get_session())
    phone_range = session.query(PhoneRange).filter(PhoneRange.id==id).first()
    if phone_range:
        return phone_range
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This phone range does not exist.")


@router.delete(
        PHONE_RANGE_BASE_URL + "/{id}",
        tags=[PHONE_RANGE_TAG],
        status_code=status.HTTP_204_NO_CONTENT,
    )
def delete_phone_range(id: int):
    session = next(get_session())
    phone_range = session.query(PhoneRange).filter(PhoneRange.id==id).first()
    if phone_range:
        session.delete(phone_range)
        session.commit()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This phone range does not exist.")
