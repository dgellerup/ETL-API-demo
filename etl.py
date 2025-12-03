import pandas as pd
from datetime import datetime

from db import SessionLocal, engine
from models import Base, User, Account


def init_db():
    Base.metadata.create_all(bind=engine)


def load_users(csv_path: str, session):
    df = pd.read_csv(csv_path)

    df["email"] = df["email"].str.lower()

    users = []
    for _, row in df.iterrows():
        user = User(
            id=int(row["id"]),
            name=row["name"],
            email=row["email"],
            address=row.get("address"),
        )
        users.append(user)

    session.bulk_save_objects(users)


def load_accounts(csv_path: str, session):
    df = pd.read_csv(csv_path)

    accounts = []
    for _, row in df.iterrows():
        account = Account(
            id=int(row["id"]),
            user_id=int(row["user_id"]),
            open_date=datetime.strptime(row["open_date"], "%Y-%m-%d").date(),
            balance=float(row["balance"]),
            status=row["status"],
        )
        accounts.append(account)

    session.bulk_save_objects(accounts)


def main():
    init_db()

    session = SessionLocal()
    try:
        load_users("users.csv", session)
        load_accounts("accounts.csv", session)

        session.commit()
        print("Data loaded into DB successfully.")
    except Exception as e:
        session.rollback()
        print(f"Data loading error: {e}")
        raise
    finally:
        session.close()

if __name__ == "__main__":
    main()