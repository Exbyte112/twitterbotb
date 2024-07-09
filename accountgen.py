from solver import solve_captcha, solver_funcaptcha, balance
import requests
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.proxy import Proxy, ProxyType
import time
from bs4 import BeautifulSoup
from faker import Faker
import random
from mailgen import get_email_message, get_email
from pymongo import MongoClient

import logging
import os

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)

fake = Faker()
prox = Proxy()
prox.proxy_type = ProxyType.MANUAL
try:
    print("Connecting to database...")
    cluster = MongoClient(
        "mongodb+srv://exbyte:1234@cluster0.aw1f22q.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    )
    db = cluster["KronosTwikit"]
    secondary_collection = db["KronosTwikitSecondary"]
    
    if secondary_collection != None:
        print("Connected to database")
    else:
        print("Error connecting to database")
except Exception as e:
    print("Error connecting to database")
    exit()


proxy_strings = [
    "MrAndersonFlushed01:wxvyskd1q5rb:x282.fxdx.in:14361",
    "MrAndersonFlushed02:sbkpmgmsb99s:x174.fxdx.in:16469",
    "MrAndersonFlushed03:vzcy5g5xw572:x314.fxdx.in:14033",
    "MrAndersonFlushed04:hzadxjwrm3p3:x314.fxdx.in:14034",
    "MrAndersonFlushed05:pszf1mzrhhfy:x321.fxdx.in:14274",
]


def parse_proxy(proxy_string):
    username, password, host, port = proxy_string.split(":")
    proxy = f"http://{username}:{password}@{host}:{port}"
    return {"host": host, "port": port, "http": proxy}


proxies_list = [parse_proxy(proxy) for proxy in proxy_strings]
selected_proxy = random.choice(proxies_list)
prox.http_proxy = selected_proxy
prox.socks_proxy = selected_proxy
prox.ssl_proxy = selected_proxy

#capabilities = webdriver.DesiredCapabilities.FIREFOX["proxy"] = prox

def generate():
    # = fake.email(safe=False, domain="gmail.com")
    password = fake.password()
    number = fake.phone_number()
    return {"password": password, "number": number}

def my_proxy(PROXY_HOST, PROXY_PORT):
  fp = webdriver.FirefoxProfile()
  # ... rest of your profile settings ...
  options = webdriver.FirefoxOptions()
  options.add_argument("--ignore-certificate-errors")
  options.add_argument("start-maximized")
  options.add_argument(f"--proxy-server={PROXY_HOST}:{PROXY_PORT}")  # Pass directly
  driver = webdriver.Firefox(options=options)
  return driver

def scraper():
    # signup on x
    email = ""
    url = "https://x.com/signup"
    #driver = my_proxy(PROXY_HOST=selected_proxy["host"],PROXY_PORT=selected_proxy["port"])
    #driver = webdriver.Firefox()
    options = webdriver.ChromeOptions()
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("start-maximized")
    extension_path = os.path.abspath('./CapSolver.Browser.Extension')
    options.add_argument(f'--load-extension={extension_path}')
    driver = webdriver.Chrome(options=options)
    # use proxy

    driver.get(url)

    driver.implicitly_wait(30)

    try:
        driver.find_element(
            By.XPATH,
            "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/button[2]/div[1]/span[1]/span[1]",
        ).click()
    except:
        print("Error loading signup page")
        driver.quit()
        return

    details = generate()
    password = details["password"]
    number = details["number"]

    name_space = driver.find_element(
        By.XPATH,
        "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/div[1]/label[1]/div[1]/div[2]/div[1]/input[1]",
    )

    # send the name
    name_space.send_keys(fake.name())

    def send_email(email_or_number):
        email = get_email()
        email_space = driver.find_element(
            By.XPATH,
            "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/div[2]/label[1]/div[1]/div[2]/div[1]/input[1]",
        )
        if email_or_number == "number":
            email_space.send_keys(number)
        else:
            email_space.send_keys(email)
        # email_space.send_keys("exbytevpn@gmail.com")
        return email

    # check if use email instead shows
    try:
        link = driver.find_element(
            By.XPATH,
            "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/button[1]/span[1]",
        )
        if link.text == "Use email instead":
            link.click()
            time.sleep(1)
            send_email("email")
    except:
        send_email("email")
    
    
    send_email("email")

    month_space = Select(
        driver.find_element(
            By.XPATH,
            "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/div[3]/div[3]/div[1]/div[1]/select[1]",
        )
    ).select_by_index(random.randint(1, 11))

    day_space = Select(
        driver.find_element(
            By.XPATH,
            "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/div[3]/div[3]/div[1]/div[2]/select[1]",
        )
    ).select_by_index(random.randint(1, 27))

    year_space = Select(
        driver.find_element(
            By.XPATH,
            "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/div[3]/div[3]/div[1]/div[3]/select[1]",
        )
    ).select_by_index(random.randint(20, 40))

    driver.implicitly_wait(10)
    # click next
    try:
        error_message = driver.find_element(
            By.CSS_SELECTOR, "div.r-n6v787 > span:nth-child(1)"
        )
    except:
        error_message = None
    email_or_number_counter = 0
    while error_message:
        global selected_email
        details = generate()
        #email = get_email()
        password = details["password"]
        number = details["number"]
        try:
            error_message = driver.find_element(
                By.CSS_SELECTOR, "div.r-n6v787 > span:nth-child(1)"
            )
        except:
            error_message = None
        if error_message:
            email = get_email()
            #print("\n\n\nEmail is already taken.\n\n\n")

            email_space = driver.find_element(
            By.XPATH,
            "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/div[2]/label[1]/div[1]/div[2]/div[1]/input[1]",
            )
            email_space.send_keys(Keys.CONTROL + "a", Keys.DELETE)
            time.sleep(1)
            print("text cleared")
            email = send_email("email")
            email_or_number_counter += 1
            selected_email = email
            time.sleep(3)
        else:
            print(f"\n\n\nEmail {selected_email} will be used.\n\n\n")
            break

    driver.find_element(
        By.CSS_SELECTOR,
        "span[class='css-1jxf684 r-dnmrzs r-1udh08x r-3s2u2q r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3 r-1inkyih r-rjixqe'] span[class='css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3']",
    ).click()
    
    # wait for the page to load
    time.sleep(3)
    
    # check if another next button is available
    try:
        driver.find_element(
            By.XPATH,
            "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[1]/div[1]/button[1]/div[1]"
        ).click()
    except:
        print("No next button available")
        pass
    
    # wait for captcha to load
    time.sleep(10)
    print("Solving captcha\n\n")
    """
    # check for captcha
    try:
        print("Solving captcha II")
        solver_funcaptcha()
        print("Captcha II solved")
    except:
        print("Error solving captcha II")

    time.sleep(10)"""
    # wait until verification code is available
    webdriver.support.ui.WebDriverWait(driver, 300).until(
        EC.presence_of_element_located(
            (By.XPATH, "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/label[1]/div[1]/div[2]/div[1]/input[1]")
        )
    )
    print("Finished solving captcha\n\n")
    
    # wait for the verification code to arrive
    time.sleep(10)
    
    print("Getting verification code\n")
    
    try:
        # insert verification code
        verification_code = get_email_message(selected_email)
    except:
        print("Error getting verification code")
        # try again
        time.sleep(5)
        try:
            verification_code = get_email_message(selected_email)
        except:
            print("Error getting verification code")
            print("Skipping")
            return
    print("Verification code: ", verification_code)
    
    verification_code_space = driver.find_element(
        By.XPATH,
        "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/label[1]/div[1]/div[2]/div[1]/input[1]",
    )
    try:
        verification_code_space.send_keys(verification_code)
    except:
        print("Error inserting verification code")
        print("Skipping")
        return
    
    time.sleep(1)
    
    # click Next
    driver.find_element(
        By.XPATH,
        "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[1]/div[1]/button[1]/div[1]",
    ).click()
    
    time.sleep(5)
    
    # Insert password
    
    password_space = driver.find_element(
        By.XPATH,
        "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[2]/div[1]/label[1]/div[1]/div[2]/div[1]/input[1]"
    )
    password_space.send_keys(password)
    
    # click Next
    time.sleep(5)
    driver.find_element(
        By.XPATH,
        "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[1]/div[1]/div[2]/button[1]/div[1]"
    ).click()
    
    # wait for the page to load
    time.sleep(5)
    
    # optional tab comes up
    try:
        driver.find_element(
            By.XPATH,
            "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/button[1]/div[1]/span[1]/span[1]"
        ).click()
        
        time.sleep(3)
        
        # scroll down
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        # click agree
        driver.find_element(
            By.XPATH,
            "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[1]/div[1]/button[1]/div[1]/span[1]/span[1]"
        ).click()
    except:
        pass
    
    time.sleep(5)
    
    #check if account is created
    try:
        post_space = driver.find_element(
            By.XPATH,
            "/html[1]/body[1]/div[1]/div[1]/div[1]/div[2]/main[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[3]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]"
        )
        if post_space:
            print("Account created")
            # add to database
            secondary_collection.insert_one({"email": selected_email, "password": password})
            driver.quit()
            return selected_email, password
    except:
        pass
    
    time.sleep(5)
    
    # click skip
    
    driver.find_element(
        By.XPATH,
        "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[1]/div[1]/button[1]/div[1]/span[1]/span[1]"
    ).click()
    
    # wait for the page to load
    time.sleep(3)
    
    # click skip
    driver.find_element(
        By.XPATH,
        "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[1]/div[1]/button[1]/div[1]/span[1]/span[1]"
    ).click()
    
    # wait for the page to load
    time.sleep(3)
    
    # click skip
    driver.find_element(
        By.XPATH,
        "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/button[2]/div[1]/span[1]/span[1]"
    ).click()
    
    # wait for the page to load
    time.sleep(5)
    
    # click on the first 3 interests
    music = driver.find_element(
        By.XPATH,
        "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/section[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/li[1]/div[1]/div[1]/div[1]/button[1]/div[1]/div[1]/div[1]/div[1]"
    )
    music.click()
    entertainment = driver.find_element(
        By.XPATH,
        "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/section[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/li[2]/div[1]/div[1]/div[1]/button[1]/div[1]/div[1]/div[1]"
    )
    entertainment.click()
    sports = driver.find_element(
        By.XPATH,
        "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/section[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/li[3]/div[1]/div[1]/div[1]/button[1]/div[1]/div[1]/div[1]/div[1]/span[1]"
    )
    sports.click()
    
    # click next
    
    driver.find_element(
        By.XPATH,
        "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[1]/button[1]/div[1]/span[1]/span[1]"
    ).click()
    
    # wait for the page to load
    time.sleep(3)
    
    # click next
    driver.find_element(
        By.XPATH,
        "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/button[1]/div[1]"
    ).click()
    
    # wait for the page to load
    time.sleep(3)
    
    # click on the first account
    driver.find_element(
        By.XPATH,
        "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/section[1]/div[1]/div[1]/div[3]/div[1]/div[1]/button[1]/div[1]/div[2]/div[1]/div[2]/button[1]/div[1]/span[1]/span[1]"
    ).click()
    
    time.sleep(1)
    
    # click next
    driver.find_element(
        By.XPATH,
        "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[1]/div[1]/button[1]/div[1]"
    ).click()
    
    # wait for the page to load
    
    time.sleep(5)
    print("Done")
    print(f"Account created with email: {selected_email} and password: {password} and email {selected_email}")
    
    # add to database
    secondary_collection.insert_one({"email": selected_email, "password": password})
    driver.quit()
    return selected_email, password

import argparse

from art import text2art

def display_branding():
    # set colour to green
    os.system("color 0a")
    art_text = text2art("Exbyte-Bots", font="bulbhead")  # You can change the font as desired
    print(art_text)

def main():
    display_branding()
    print("\nWelcome to the Twitter Signup Bot!")
    print("This bot will create accounts for you on x.")
    print(balance())
    count = input("Please enter the number of accounts you want to create: ")
    if count == "":
        print("You did not enter a number.")
        return
    elif not count.isdigit():
        print("You did not enter a valid number.")
        return
    print(f"\nThis may take a while depending on the number of accounts you want to create.\n")
    print(f"\nCreating {count} account(s)...")
    # Here you would call your main function to create accounts
    # e.g., signup_bot.main(int(count))
    for i in range(int(count)):
        print(f"\n\nCreating account {i+1}/{count}...")
        scraper()

if __name__ == "__main__":
    main()