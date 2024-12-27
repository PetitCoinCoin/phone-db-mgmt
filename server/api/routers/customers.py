from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError

from api.db import get_session
from api.models import Customer
from api.serializers import CustomerType, CustomerWriteOnlyType

router = APIRouter()
CUSTOMER_TAG = "Customers"
CUSTOMER_BASE_URL = "/customers"


@router.get(
        CUSTOMER_BASE_URL,
        tags=[CUSTOMER_TAG],
        response_model=list[CustomerType],
    )
def list_customers():
    session = next(get_session())
    query = session.query(Customer)
    return query.all()


@router.post(
        CUSTOMER_BASE_URL,
        tags=[CUSTOMER_TAG],
        response_model=CustomerType,
        status_code=status.HTTP_201_CREATED,
    )
def create_customer(new_customer: CustomerWriteOnlyType):
    customer: Customer = Customer(**new_customer.model_dump())
    session = next(get_session())
    try:
        session.add(customer)
        session.commit()
        session.refresh(customer)
        return customer
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This customer already exists.")


@router.get(
        CUSTOMER_BASE_URL + "/{id}",
        tags=[CUSTOMER_TAG],
        response_model=CustomerType,
    )
def get_customer(id: int):
    session = next(get_session())
    customer = session.query(Customer).filter(Customer.id==id).first()
    if customer:
        return customer
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This customer does not exist.")


@router.delete(
        CUSTOMER_BASE_URL + "/{id}",
        tags=[CUSTOMER_TAG],
        status_code=status.HTTP_204_NO_CONTENT,
    )
def delete_customer(id: int):
    session = next(get_session())
    customer = session.query(Customer).filter(Customer.id==id).first()
    if customer:
        session.delete(customer)
        session.commit()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This customer does not exist.")
