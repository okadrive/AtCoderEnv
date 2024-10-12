#! /usr/bin/env python
# coding: UTF-8

# input: <contest's name> <contest's number>
# example: python setup.py abc 199
# directory structure:
'''
AtCoderEnv/
├── setup.py
├── config.ini
└── template/
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
import configparser
import os
import sys
from bs4 import BeautifulSoup

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

def create_contest_directory(contest_name, contest_number):
    # Create directory structure
    if not os.path.exists("contests"):
        os.makedirs("contests")
    contest_directory = "contests/{0}/{1}".format(contest_name, contest_number)
    if not os.path.exists(contest_directory):
        os.makedirs(contest_directory)

    # Get the list of tasks from the contest page
    tasks_url = "{0}/contests/{1}{2}/tasks".format(domain, contest_name, contest_number)
    response = requests.get(tasks_url)
    if response.status_code != 200:
        print("Failed to retrieve tasks.")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    task_links = soup.find_all("a", href=True)

    for link in task_links:
        if "/tasks/" in link['href']:
            question = link['href'].split('/')[-1]
            question_directory = "{0}/{1}".format(contest_directory, question)
            if not os.path.exists(question_directory):
                os.makedirs(question_directory)
                # copy main.cpp and main_test.cpp from template
                with open("template/main.cpp", "r") as f:
                    with open("{0}/main.cpp".format(question_directory), "w") as g:
                        g.write(f.read())
                with open("template/main_test.cpp", "r") as f:
                    with open("{0}/main_test.cpp".format(question_directory), "w") as g:
                        g.write(f.read())
    print("Directory structure created.")
    print(contest_directory)

def main():
    # Login to AtCoder
    session = login()
    if session is None:
        return
    args = sys.argv
    if len(args) < 3:
        print("Usage: python setup.py <contest's name> <contest's number>")
        return
    contest_name = args[1]
    contest_number = args[2]
    create_contest_directory(contest_name, contest_number)

if __name__ == "__main__":
    main()
