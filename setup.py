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
import subprocess
import json
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
    # Check if we have saved cookies first
    cookie_file = "atcoder_cookies.json"
    
    if os.path.exists(cookie_file):
        print("Found existing cookies, attempting to use them...")
        if try_login_with_cookies():
            return session
        else:
            print("Saved cookies are invalid, removing them...")
            os.remove(cookie_file)
    
    print("Manual login required due to CloudFlare protection.")
    print("Opening Chrome browser for manual login...")
    
    # Open Chrome with AtCoder login page
    login_url = "https://atcoder.jp/login"
    try:
        # Use macOS 'open' command to launch Chrome
        subprocess.run(["open", "-a", "Google Chrome", login_url], check=True)
        print("Chrome opened with AtCoder login page.")
        print("\nPlease complete the following steps:")
        print("1. Login to AtCoder in the opened Chrome window")
        print("2. Complete CloudFlare challenges")
        print("3. Open Chrome DevTools (F12 or Cmd+Option+I)")
        print("4. Go to Application tab -> Storage -> Cookies -> https://atcoder.jp")
        print("5. Find and copy the 'REVEL_SESSION' cookie value")
        print("\nPress Enter when you have completed login and are ready to continue...")
        input()
        
        # Try to extract cookies from Chrome (simplified approach)
        return extract_cookies_and_login()
        
    except subprocess.CalledProcessError:
        print("Failed to open Chrome. Please open Chrome manually and navigate to:")
        print(login_url)
        input("Press Enter after you have logged in...")
        return extract_cookies_and_login()
    except Exception as e:
        print(f"Error opening browser: {e}")
        return None

def try_login_with_cookies():
    """Try to login using saved cookies"""
    try:
        with open("atcoder_cookies.json", "r") as f:
            cookies = json.load(f)
        
        # Set cookies in session
        for cookie in cookies:
            session.cookies.set(cookie['name'], cookie['value'], domain=cookie.get('domain', '.atcoder.jp'))
        
        # Test if login is successful by accessing a protected page
        response = session.get("https://atcoder.jp/settings")
        if response.status_code == 200 and "Sign Out" in response.text:
            print("Successfully logged in using saved cookies!")
            return True
        else:
            return False
    except Exception as e:
        print(f"Error using saved cookies: {e}")
        return False

def extract_cookies_and_login():
    """Extract cookies manually and save them"""
    print("\nCookie extraction method:")
    print("Please provide the essential cookie from your browser:")
    print("From Chrome DevTools -> Application -> Cookies -> https://atcoder.jp")
    
    cookie_data = []
    
    # Only ask for REVEL_SESSION which actually exists
    while True:
        value = input("Enter value for cookie 'REVEL_SESSION' (required for login): ").strip()
        if value:
            cookie_data.append({
                'name': 'REVEL_SESSION',
                'value': value,
                'domain': '.atcoder.jp'
            })
            break
        print("REVEL_SESSION cookie is required. Please enter a valid value.")
    
    # Optional language cookie
    lang_value = input("Enter value for cookie 'language' (optional, press Enter to skip): ").strip()
    if lang_value:
        cookie_data.append({
            'name': 'language',
            'value': lang_value,
            'domain': '.atcoder.jp'
        })
    
    # Save cookies
    with open("atcoder_cookies.json", "w") as f:
        json.dump(cookie_data, f, indent=2)
    
    # Set cookies in session
    for cookie in cookie_data:
        session.cookies.set(cookie['name'], cookie['value'], domain=cookie['domain'])
    
    # Test the session
    response = session.get("https://atcoder.jp/settings")
    if response.status_code == 200 and ("Sign Out" in response.text or "ログアウト" in response.text):
        print("Successfully authenticated with provided cookies!")
        return session
    else:
        print("Cookie authentication failed, but continuing with current session...")
        return session


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
            input_header = soup.find("h3", string="入力例 {}".format(i))
            if input_header:
                # Find the next pre element
                pre_element = input_header.find_next("pre")
                if pre_element:
                    tc = pre_element.get_text()
                    with open("{0}/{1}_input.txt".format(sample_dir, i), "w") as f:
                        f.write(tc)
                else:
                    break
            else:
                break
            i = i + 1

        # h3 "出力例 n" are the sample output test cases
        i = 1
        while True:
            output_header = soup.find("h3", string="出力例 {}".format(i))
            if output_header:
                # Find the next pre element
                pre_element = output_header.find_next("pre")
                if pre_element:
                    tc = pre_element.get_text()
                    with open("{0}/{1}_output.txt".format(sample_dir, i), "w") as f:
                        f.write(tc)
                else:
                    break
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
