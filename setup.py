#! /usr/bin/env python
# coding: UTF-8

# input: <contest's name> <contest's number>
# example: python setup.py abc 199

# 1. Read AtCoder's username and password from config.ini
# 2. Login to AtCoder
# 3. Create directory structure
# 4. Download sample test cases

#! /usr/bin/env python
# coding: UTF-8
import requests
import configparser
import os
import re
import sys
import time
from bs4 import BeautifulSoup

# AtCoder domain
domain = "https://atcoder.jp"
session = requests.Session()

def http_get(url):
    response = session.get(url)
    if response.status_code != 200:
        print("Failed to fetch URL: {0}".format(url))
        return
    return response

def http_get_with_retry(url, retries=3, delay=2):
    for i in range(retries):
        response = http_get(url)
        if response is not None and response.status_code == 200:
            return response
        print(f"Retrying... ({i+1}/{retries})")
        time.sleep(delay)
    print(f"Failed to fetch URL after {retries} retries: {url}")
    return None

def login():
    # URL for login
    login_url = "{0}/{1}".format(domain, "login")

    # Create a session object
    session = requests.Session()

    # First, get the login page to retrieve any necessary hidden form fields (e.g., CSRF tokens)
    response = session.get(login_url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract CSRF token (if needed by AtCoder's login form)
    csrf_token = soup.find("input", {"name": "csrf_token"}).get("value")

    # Read AtCoder's username and password from config.ini
    config = configparser.ConfigParser()
    config.read("config.ini")
    username = config["user"]["username"]
    password = config["user"]["password"]

    # Login payload
    payload = {"username": username, "password": password, "csrf_token": csrf_token}

    # Send POST request to login
    login_response = session.post(login_url, data=payload)

    # Check if login was successful
    if login_response.status_code == 200 and "Sign Out" in login_response.text:
        print("Successfully logged in!")
        return session
    else:
        print("Login failed.")
        return None


def get_list_task_url(contest_name, contest_number):
    tasks_uri = "{0}/contests/{1}{2}/tasks".format(domain, contest_name, contest_number)
    response = requests.get(tasks_uri)
    if response.status_code != 200:
        print("Failed to retrieve tasks.")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    task_links = soup.find("tbody").find_all("tr")

    # from task_links, extract the links that match the pattern
    pattern_task_link = "{0}{1}_[a-z]".format(contest_name, contest_number)
    list_task_url = [
        link.find("a")["href"]
        for link in task_links
        if re.search(pattern_task_link, link.find("a")["href"])
    ]

    return list_task_url


def create_local_contest_base_dir(contest_name, contest_number):
    # Create directory structure
    if not os.path.exists("contests"):
        os.makedirs("contests")
    local_contest_base_dir = "contests/{0}/{1}".format(contest_name, contest_number)
    if not os.path.exists(local_contest_base_dir):
        os.makedirs(local_contest_base_dir)
    print("Base contest directory created.")
    return local_contest_base_dir


def create_local_task_dir(local_contest_base_dir, list_task):
    for task in list_task:
        task_dir = "{0}/{1}".format(local_contest_base_dir, task)
        if not os.path.exists(task_dir):
            os.makedirs(task_dir)
            # copy main.cpp and main_test.cpp from template
            with open("template/main.cpp", "r") as f:
                with open("{0}/main.cpp".format(task_dir), "w") as g:
                    g.write(f.read())
            with open("template/main_test.cpp", "r") as f:
                with open("{0}/main_test.cpp".format(task_dir), "w") as g:
                    g.write(f.read())
    print("Task directory created.")


def download_sample_testcases(local_contest_base_dir, list_task_url):
    # Download sample test cases
    for task_url in list_task_url:
        sample_dir = "{0}/{1}/sample".format(local_contest_base_dir, task_url.split("/")[-1])
        if not os.path.exists(sample_dir):
            os.makedirs(sample_dir)

        task_uri = "{0}/{1}".format(domain.rstrip('/'), task_url.lstrip('/'))
        print("task_uri:", task_uri)
        response = http_get_with_retry(task_uri)
        if response is None:
            print(f"Failed to fetch the task URL: {task_url}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        # h3 "入力例 n" are the sample input test cases
        i = 1
        while True:
            if soup.find("h3", string="入力例 {}".format(i)):
                tc = soup.find("h3", string="入力例 {}".format(i)).next_sibling.text
                tc.replace("\r", "")
                with open("{0}/{1}_input.txt".format(sample_dir, i), "w") as f:
                    f.write(tc)
            else:
                break
            i = i + 1

        # h3 "出力例 n" are the sample output test cases
        i = 1
        while True:
            if soup.find("h3", string="出力例 {}".format(i)):
                tc = soup.find("h3", string="出力例 {}".format(i)).next_sibling.text
                tc.replace("\r", "")
                with open("{0}/{1}_output.txt".format(sample_dir, i), "w") as f:
                    f.write(tc)
            else:
                break
            i = i + 1
    print("Sample test cases downloaded.")


def main():
    # Login to AtCoder
    session = login()
    if session is None:
        print("Failed to login.")
        return
    args = sys.argv
    if len(args) < 3:
        print("Usage: python setup.py <contest's name> <contest's number>")
        return
    contest_name = args[1]
    contest_number = args[2]
    list_task_url = get_list_task_url(contest_name, contest_number)

    local_contest_base_dir = create_local_contest_base_dir(contest_name, contest_number)
    print("local_contest_base_dir:", local_contest_base_dir)
    list_task = []
    for task_url in list_task_url:
        list_task.append(task_url.split("/")[-1])
    print("list_task:", list_task)

    create_local_task_dir(local_contest_base_dir, list_task)
    download_sample_testcases(local_contest_base_dir, list_task_url)


if __name__ == "__main__":
    main()
