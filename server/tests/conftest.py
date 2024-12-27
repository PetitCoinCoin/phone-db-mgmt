from datetime import datetime, timezone

import pytest

from api.db import Session
from api.models import Customer, PhoneNumber, PhoneRange


@pytest.fixture(name="session", scope="function")
def session_fixture():
    with Session() as session:
        yield session
        session.rollback()

  
@pytest.fixture(scope="function")
def mock_customer(session):
    customer = Customer(name="Test Customer")
    session.add(customer)
    session.commit()
    yield customer
    session.delete(customer)
    session.commit()
    session.close()

  
@pytest.fixture(scope="function")
def mock_phonerange(session):
    phone_range = PhoneRange(lower="0150000000", upper="0160000000")
    session.add(phone_range)
    session.commit()
    yield phone_range
    session.delete(phone_range)
    session.commit()
    session.close()

  
@pytest.fixture(scope="function")
def mock_phonenumber(session, mock_customer, mock_phonerange):
    phone_number = PhoneNumber(
        phone="0152098792",
        customer_id=mock_customer.id,
        phone_range_id=mock_phonerange.id,
        allocation_date=datetime.now(tz=timezone.utc),
    )
    session.add(phone_number)
    session.commit()
    yield phone_number
    session.delete(phone_number)
    session.commit()
    session.close()
