# -*- coding: utf-8 -*-
"""
Created on Wed Dec  3 11:52:37 2025

@author: daneg
"""

import random
import requests

from datetime import datetime, timedelta

import argparse
import numpy as np
import pandas as pd


class Args(argparse.Namespace):
    user_count: int
    max_accounts_per_user: int
    

def parse_args() -> Args:
    """
    Parse arguments from command line invocation.

    Returns
    -------
    Args
        argparse.Namespace with user-defined or Default arguments.

    """
    
    parser = argparse.ArgumentParser(description = "Parse command line arguments for mock data generation")
    
    parser.add_argument("-u", "--user_count", type=int, default=10, help="Number of Users to create.")
    parser.add_argument("-a", "--max_accounts_per_user", type=int, default=3, help="Maximum number of accounts a User can have.")
    
    return parser.parse_args(namespace=Args())


def generate_users(user_count: int) -> pd.DataFrame:
    """
    Create a pandas DataFrame populated with mock user data generated from API
    call to randomuser.me api.
        
    Parameters
    ----------
    user_count: int
        Number of User records to generate
        
    Returns
    -------
    pd.DataFrame
        Pandas DataFrame with mock user data

    """
    response = requests.get(f"https://randomuser.me/api/?nat=us&&results={user_count}").json()
    
    new_users = []
    for generated_user in response.get('results'):
        first_name = generated_user.get("name").get("first")
        last_name = generated_user.get("name").get("last")
        email = generated_user.get("email")
        location = generated_user.get("location")
        address = f"{' '.join([str(v) for v in location.get('street').values()])}, {location.get('city')}, {location.get('state')}, {location.get('postcode')}, {location.get('country')}"
        
        new_users.append(
            {
                'name': f"{first_name} {last_name}",
                'email': email,
                'address': address
            }
        )
        
    users_df = pd.DataFrame.from_records(new_users)
    
    return users_df


def generate_accounts(users_df: pd.DataFrame, max_accounts_per_user: int) -> pd.DataFrame:
    """
    Create between 1 - {max_accounts_per_user} Account records for each User.

    Parameters
    ----------
    users_df : pd.DataFrame
        Pandas DataFrame with mock user data
        
    max_accounts_per_user: int
        Maximum number of Account records that a User can have

    Returns
    -------
    pd.DataFrame
        Pandas DataFrame with mock account data

    """
        
    new_accounts = []
    for _, row in users_df.iterrows():
        user = row['name']
        number_accounts = np.random.choice(3) + 1
        for i in range(number_accounts):
            account = create_account(user)
            new_accounts.append(account)
            
    accounts_df = pd.DataFrame.from_records(new_accounts)
    
    return accounts_df

        
def create_account(user: str) -> dict:
    """
    Create a mock account

    Parameters
    ----------
    user : str
        Name of User the new Account will belong to
        
    Returns
    -------
    dict
        DESCRIPTION.

    """
    status = np.random.choice(["Open", "Closed"], p=[0.9, 0.1])
    if status == "Open":
        balance = np.random.choice(range(10000, 20000))
    else:
        balance = 0
    
    today_date = datetime.now()
    bound_date = today_date - timedelta(days=5 * 356)
    time_diff_seconds = int((today_date - bound_date).total_seconds())
    random_seconds = random.randrange(time_diff_seconds)
    
    open_date = bound_date + timedelta(seconds=random_seconds)
    
    return {
        "user": user,
        "open_date": open_date,
        "balance": balance,
        "status": status
        }


def main(user_count: int, max_accounts_per_user: int):
    
    users_df = generate_users(user_count)
    
    accounts_df = generate_accounts(users_df, max_accounts_per_user)
    
    users_df.to_csv("users.csv", index=False)
    accounts_df.to_csv("accounts.csv", index=False)
    

if __name__ == "__main__":
    args = parse_args()
    
    user_count = args.user_count
    max_accounts_per_user = args.max_accounts_per_user
    
    main(user_count, max_accounts_per_user)