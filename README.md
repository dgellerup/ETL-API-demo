# A Small Project to Demonstrate Data Generation, Database Creation, ETL, and API Deployment
## Setup
### Development Environment
- Clone this repository to your local projects directory.
    - `cd ~/Projects`
    - `git clone https://github.com/dgellerup/ETL-API-demo.git`
- Create an Anaconda/Miniconda Environment with Python 3.12
    - `conda create -n test-env python=3.12`
    - `conda activate test-env`
#### Optional
- Install `virtualenv`
    - `conda install virtualenv`
- Create a virtualenv environment using your Conda environment's Python 3.12
    - `virtualenv venv`
- Activate venv
    - Unix
        - `source venv/bin/activate`
    - Windows
        - `source venv/Scripts/activate`
#### Finally
- Install dependencies
    - `pip install -r requirements.txt`

### Generating Mock User and Account Data
With `venv` activated, generate mock User and Account data with `generate_mock_data.py`. To create 10 mock Users, who can each have up to 5 Accounts:  

`python generate_mock_data.py -u 10 -a 5`  
-or-  
`python generate_mock_data.py --user_count 10 --max_accounts_per_user 5`  

This script will generate `users.csv` and `accounts.csv` with 10 Users and between 1 and 5 Accounts associated with each User.

### Deployment
Once mock data is generated, use Docker to spin up a Docker Compose deployment with `db` and `api` services.
- Ensure [Docker Desktop](https://www.docker.com/products/docker-desktop/) is running
- `docker compose up --build`  

Now the database and API should be up and running, with our generated mock data loaded into the database.  

## Usage
To test the database and API out, open a web browser and go to: `http://localhost:8000/docs`. This opens the FastAPI Swagger UI. The three API endpoints are listed under `default`:  
- `GET` /users
    - Click to expand -> `Try it out`, then click Execute to see the Response. Note who is listed second with `id: 2`.
- `GET` /users/{user_id}
    - Click to expand -> `Try it out`, enter a number for the `user_id` parameter (let's use `2`), and click Execute. The Response provides details about the individual with `id: 2` that we noted above.
- `GET` /accounts
    - Click to expand -> `Try it out`, enter a date within the last 5 years (let's use 2024-12-03), a minimum balance (say, 5000), and status Open, then click Execute. The Response shows Accounts opened in the past 5 years with at least $5000.
