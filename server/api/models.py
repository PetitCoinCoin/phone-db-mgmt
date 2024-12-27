from sqlalchemy import (
    event,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.sql.expression import text

from .db import engine


class Base(DeclarativeBase):
    pass


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    phone_numbers = relationship("PhoneNumber", cascade="all,delete", backref="customer", lazy="subquery")


class PhoneRange(Base):
    __tablename__ = "phoneranges"

    id = Column(Integer, primary_key=True)
    lower = Column(String(10), nullable=False)
    upper = Column(String(10), nullable=False)
    phone_numbers = relationship("PhoneNumber", cascade="all,delete", backref="phone_range", lazy="subquery")


class PhoneNumber(Base):
    __tablename__ = "phonenumbers"

    id = Column(Integer, primary_key=True)
    phone = Column(String(10), unique=True)
    phone_range_id = Column(Integer, ForeignKey("phoneranges.id"), nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    allocation_date = Column(DateTime, nullable=False)
    cancellation_date = Column(DateTime())


@event.listens_for(PhoneRange.__table__, "after_create")
def after_create(target, connection, **_k):
    connection.execute(
        text("INSERT INTO %s (lower, upper) VALUES ('0162050000', '0162059999'), ('0939010000', '0939019999')" % (target.name))
    )
    # with engine.connect as connection:
    # session = next(get_session())
    # session.add(PhoneRange(lower="0162050000", upper="0162059999"))
    # session.add(PhoneRange(lower="0939010000", upper="0939019999"))
    # session.commit()

Base.metadata.create_all(engine)
