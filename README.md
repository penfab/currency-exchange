## Currency Exchange with FastAPI, httpx and async calls
## Author: Fabrizio Pensabene, 2022-07-08

# Instructions

1. Within the main folder execute ```docker compose up --build``` and wait for everything to be built and initialized

2. The SwaggerUI is then available at http://127.0.0.1:8000/docs to test the API

3. To run the unittest make sure you meet the requirements in your Python environment

   You can run these commands to install everything if needed:

   ```pip install --no-cache-dir -U pip setuptools wheel```

   ```pip install --no-cache-dir -r requirements```

   Then you can execute the tests from your shell by ```python test.py``` and wait for the tests results to show

# About the API

The API used in this project to retrieve currency exhanges is from https://exchangerate.host/#/

# Updates

1. Changed .post() to .get() for convert() endpoint as we don't save anything to a database
2. Added an .upper() for _from and _to
3. Some changes in my comments and including this file as well
