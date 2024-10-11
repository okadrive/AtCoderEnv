#! /usr/bin/env python
# coding: UTF-8

# input: <contest's name> <contest's number>
# example: python setup.py abc 199
# directory structure:
'''
AtCoderEnv/
└── contests/
    └── <contest_title>/             # e.g., abc/
        └── <contest_number>/        # e.g., 199/
            └── <question_alphabet>/ # e.g., a/
                ├── main.cpp         # template file
                ├── main_test.cpp    # template file
                └── sample/          # directory for test cases
                    ├── 1.in         # input file for test case 1
                    ├── 1.out        # output file for test case 1
                    ├── ...          # more test cases
                    ├── n.in         # input file for test case n
                    └── n.out        # output file for test case n
'''

# 1. Read AtCoder's username and password from config.ini
# 2. Login to AtCoder
# 3. Create directory structure
# 4. Download sample test cases

#! /usr/bin/env python
# coding: UTF-8
import requests
from bs4 import BeautifulSoup
import configparser

# AtCoder domain
domain = "https://atcoder.jp"

import requests

def login():
    # URL for login
    login_url = "{0}/{1}".format(domain, "login")

    # Create a session object
    session = requests.Session()

    # First, get the login page to retrieve any necessary hidden form fields (e.g., CSRF tokens)
    response = session.get(login_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract CSRF token (if needed by AtCoder's login form)
    csrf_token = soup.find("input", {"name": "csrf_token"}).get("value")

    # Read AtCoder's username and password from config.ini
    config = configparser.ConfigParser()
    config.read('config.ini')
    username = config['user']['username']
    password = config['user']['password']

    # Login payload
    payload = {
        "username": username,
        "password": password,
        "csrf_token": csrf_token
    }

    # Send POST request to login
    login_response = session.post(login_url, data=payload)

    # Check if login was successful
    if login_response.status_code == 200 and "Sign Out" in login_response.text:
        print("Successfully logged in!")
        return session
    else:
        print("Login failed.")
        return None

def main():
    # Login to AtCoder
    session = login()
    if session is None:
        return

if __name__ == "__main__":
    main()
