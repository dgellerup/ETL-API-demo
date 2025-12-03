import pandas as pd
from pathlib import Path
from datetime import datetime

from create_tables import main as create_tables
from db import SessionLocal
from models import User, Account
from sqlalchemy import text


BASE_DIR = Path(__file__).resolve().parent


def reset_tables(session):
    # Drop all existing rows and reset IDs
    session.execute(text("TRUNCATE TABLE accounts RESTART IDENTITY CASCADE"))
    session.execute(text("TRUNCATE TABLE users RESTART IDENTITY CASCADE"))


def load_users(csv_path: str, session):
    df = pd.read_csv(csv_path)
    df["email"] = df["email"].str.lower()

    users = []
    for _, row in df.iterrows():
        user = User(
            name=row["name"],
            email=row["email"],
            address=row.get("address"),
        )
        users.append(user)

    session.add_all(users)
    session.flush()

    return {u.name: u.id for u in session.query(User).all()}


def load_accounts(csv_path: str, session, name_to_id):
    df = pd.read_csv(csv_path)

    accounts = []
    for _, row in df.iterrows():
        user_name = row["user"]
        user_id = name_to_id.get(user_name)
        if user_id is None:
            raise ValueError(f"Account references unknown user: {user_name}")

        account = Account(
            user_id=user_id,
            open_date=datetime.strptime(row["open_date"].split(" ")[0], "%Y-%m-%d").date(),
            balance=float(row["balance"]),
            status=row["status"],
        )
        accounts.append(account)

    session.add_all(accounts)


def main(users_csv: str | Path = BASE_DIR / "users.csv", accounts_csv: str | Path = BASE_DIR / "accounts.csv"):
    create_tables()

    session = SessionLocal()
    try:
        print("Resetting tables")
        reset_tables(session)

        name_to_id = load_users(users_csv, session)
        load_accounts(accounts_csv, session, name_to_id)

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