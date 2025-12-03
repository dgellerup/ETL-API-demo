import pandas as pd
from pathlib import Path
from datetime import datetime

from create_tables import main as create_tables
from db import SessionLocal, engine
from models import Base, User, Account


BASE_DIR = Path(__file__).resolve().parent


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


def main(users_csv: str | Path = BASE_DIR / "users.csv", accounts_csv: str | Path = BASE_DIR / "accounts.csv"):
    create_tables()

    session = SessionLocal()
    try:
        load_users(users_csv, session)
        load_accounts(accounts_csv, session)

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