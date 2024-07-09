from pathlib import Path
import os
import base64
import capsolver
import requests

capsolver.api_key = "CAP-827FCD2828969345F7A3A4767D206F0B"
PAGE_URL = "https://iframe.arkoselabs.com"
PAGE_KEY = "2CB16598-CB82-4CF7-B332-5990DB66F3AB"

def solver_funcaptcha():
    solution = capsolver.solve({
        "type": "FunCaptchaTaskProxyless",
        "websiteURL": PAGE_URL,
        "websitePublicKey": PAGE_KEY,
    })
    return solution

def set_session_headers(session, user_agent=None):
    headers = {
        "cache-control": "max-age=0",
        "sec-ch-ua": '"Not/A)Brand";v="99", "Google Chrome";v="107", "Chromium";v="107"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "upgrade-insecure-requests": "1",
        "user-agent": user_agent if user_agent else "'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "navigate",
        "sec-fetch-user": "?1",
        "sec-fetch-dest": "document",
        "accept-encoding": "gzip, deflate",
        "accept-language": "en,fr-FR;q=0.9,fr;q=0.8,en-US;q=0.7"
    }
    session.headers.update(headers)

def main():
    s = requests.Session()
    
    print("Solving Funcaptcha...")
    solution = solver_funcaptcha(PAGE_URL, PAGE_KEY)
    print("Solution: ", solution)


def balance():
    balance = capsolver.balance()
    text = f"Capsolver balance: {balance['balance']}"
    return text


# capsolver.api_key = "..."

"""
# RecognitionTask
img_path = os.path.join(Path(__file__).resolve().parent,"queue-it.jpg")
with open(img_path,'rb') as f:
    solution = capsolver.solve({
        "type":"ImageToTextTask",
        "module":"queueit",
        "body":base64.b64encode(f.read()).decode("utf8")
    })
    print(solution)"""


def solve_captcha(type, websiteKey, websiteURL):
    solution = capsolver.solve({
        "type": type,
        "websiteKey": websiteKey,
        "websiteURL": websiteURL,
    })
    return solution