from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError

from api.db import get_session
from api.models import Customer, PhoneNumber, PhoneRange
from api.serializers import PhoneNumberType, PhoneNumberWriteOnlyType

router = APIRouter()
PHONE_NUMBER_TAG = "Phone numbers"
PHONE_NUMBER_BASE_URL = "/phone_numbers"


@router.get(
        PHONE_NUMBER_BASE_URL,
        tags=[PHONE_NUMBER_TAG],
        response_model=list[PhoneNumberType],
    )
def list_phone_numbers():
    session = next(get_session())
    query = session.query(PhoneNumber)
    return query.all()


@router.post(
        PHONE_NUMBER_BASE_URL,
        tags=[PHONE_NUMBER_TAG],
        response_model=PhoneNumberType,
        status_code=status.HTTP_201_CREATED,
    )
def create_phone_number(new_phone_number: PhoneNumberWriteOnlyType):
    # should match phone regex
    session = next(get_session())
    customer = session.query(Customer).filter(Customer.id==new_phone_number.customer_id).first()
    phone_range = session.query(PhoneRange).filter(
        PhoneRange.lower<=new_phone_number.phone,
        PhoneRange.upper>=new_phone_number.phone
    ).first()
    phone_number = None
    if not phone_range:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Phone number does not belong to your phone ranges.")
    if not customer:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This customer does not exist yet.")
    phone_number = PhoneNumber(
        phone=new_phone_number.phone,
        customer_id=new_phone_number.customer_id,
        phone_range_id=phone_range.id,
        allocation_date=datetime.now(tz=timezone.utc),
    )
    try:
        session.add(phone_number)
        session.commit()
        session.refresh(phone_number)
        return phone_number
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This phone number already exists.")


@router.get(
        PHONE_NUMBER_BASE_URL + "/{id}",
        tags=[PHONE_NUMBER_TAG],
        response_model=PhoneNumberType,
    )
def get_phone_number(id: int):
    session = next(get_session())
    phone_number = session.query(PhoneNumber).filter(PhoneNumber.id==id).first()
    if phone_number:
        return phone_number
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This phone number does not exist.")


@router.delete(
        PHONE_NUMBER_BASE_URL + "/{id}",
        tags=[PHONE_NUMBER_TAG],
        status_code=status.HTTP_204_NO_CONTENT,
    )
def delete_phone_number(id: int):
    session = next(get_session())
    phone_number = session.query(PhoneNumber).filter(PhoneNumber.id==id).first()
    if phone_number:
        session.delete(phone_number)
        session.commit()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This phone number does not exist.")

