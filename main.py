from typing import List, Optional
from datetime import date

from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import select, and_

from db import SessionLocal
from models import User, Account
from schemas import User as UserSchema, Account as AccountSchema, UserWithAccounts

app = FastAPI(title="User Accounts API", version="0.1.0")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/users", response_model=List[UserSchema])
def list_users(db: Session = Depends(get_db)):
    stmt = select(User)
    users = db.execute(stmt).scalars().all()
    return users

@app.get("/users/{user_id}", response_model=UserWithAccounts)
def get_user(user_id: int, db: Session = Depends(get_db)):
    stmt = select(User).where(User.id == user_id)
    user = db.execute(stmt).scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

@app.get("/accounts", response_model=List[AccountSchema])
def list_accounts(
    open_date: Optional[date] = Query(None),
    min_balance: Optional[float] = Query(None),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    stmt = select(Account)
    conditions = []

    if open_date:
        conditions.append(Account.open_date >= open_date)
    if min_balance is not None:
        conditions.append(Account.balance >= min_balance)
    if status is not None:
        conditions.append(Account.status == status)

    if conditions:
        stmt = stmt.where(and_(*conditions))
    
    accounts = db.execute(stmt).scalars().all()
    return accounts