from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import relationship

from db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullalbe=False)
    address = Column(String, nullable=True)

    accounts = relationship("Account", back_populates="user")


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    open_date = Column(Date, nullable=False)
    balance = Column(Float, nullable=False)
    status = Column(String, nullable=False)

    user = relationship("User", back_populates="accounts")