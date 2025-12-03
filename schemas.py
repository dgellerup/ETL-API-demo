from datetime import date
from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    email: str
    address: str | None = None


class User(UserBase):
    id: int

    class Config:
        from_attributes = True


class AccountBase(BaseModel):
    user_id: int
    open_date: date
    balance: float
    status: str


class Account(AccountBase):
    id: int

    class Config:
        from_attributes = True


class UserWithAccounts(User):
    accounts: list[Account] = []