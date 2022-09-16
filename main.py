import json
import time
import string
import random
import requests
import threading

from colorama import Fore, init

init(convert=True)


class Config():
    with open('config.json') as f:
        cfg = json.load(f)

    capkey = cfg['2captcha_key']
    bio = cfg['bio_text']


    url = "https://www.twitch.tv/"
    site_key = "E5554D43-23CC-1982-971D-6A2262A2CA24"


class Generator:
    def __init__(self):
        self.capkey = Config.capkey
        
        for _ in range(2):
            threading.Thread(target=self.get_captcha).start()


    def get_captcha(self):
        getcap = requests.get(f"https://2captcha.com/in.php?key={self.capkey}&method=funcaptcha&publickey={Config.site_key}&pageurl={Config.url}")

        getcapid = getcap.text.split("|")[1]
        time.sleep(2.8)
        capansw = requests.get(f"https://2captcha.com/res.php?key={self.capkey}&action=get&id={getcapid}")

        while "CAPCHA_NOT_READY" in capansw.text:
            time.sleep(1.6)
            capansw = requests.get(f"https://2captcha.com/res.php?key={self.capkey}&action=get&id={getcapid}")

        self.GenerateToken(capansw.text[3:])


    def GenerateToken(self, captcha_token):

        randomday = random.randint(1,30)
        randommon = random.randint(1,12)
        email = "".join(random.choices(string.ascii_letters + string.digits, k=10)) + "@gmail.com"
        username = "".join(random.choices(string.ascii_letters + string.digits, k=10)) + "hazey"
        password = "".join(random.choices(string.ascii_letters + string.digits, k=6)) + "H8_"

        proxy = open('proxies.txt','r').read().splitlines()
        proxyb = random.choice(proxy)
        proxies = {'http': f'http://{proxyb}','https':f'http://{proxyb}'}
        url = "https://passport.twitch.tv/register"

        json = {
            "username": username,
            "password": password,
            "email": email,
            "birthday":{"day":randomday,"month":randommon,"year":2000},
            "client_id": "kimne78kx3ncx6brgo4mv6wki5h1ko",
            "arkose":{"token":captcha_token}
            }

        headers = {
            "host": "passport.twitch.tv",
            "connection": "keep-alive",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36",
            "content-type": "text/plain;charset=UTF-8",
            "accept": "*/*",
            "origin": "https://www.twitch.tv",
            "sec-fetch-site": "same-site",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "referer": "https://www.twitch.tv/",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9",
            }
        r = requests.post(url, json=json, headers=headers, proxies=proxies)

        if "You are trying to sign up for accounts too fast." in r.text:
            print(Fore.LIGHTRED_EX + 'You Are Being Rate Limited')

        elif "Please complete the CAPTCHA correctly." in r.text:
            print(Fore.LIGHTRED_EX + 'Captcha Solved Incorrectly')

        elif "access_token" in r.text:
            token = r.json()["access_token"]
            user_id = r.json()["userID"]

            headers = {"Connection": "keep-alive","Pragma": "no-cache","Cache-Control": "no-cache","sec-ch-ua": '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',"Accept-Language": "pl-PL","sec-ch-ua-mobile": "?0","Client-Version": "e8881750-cfb7-4ff7-aaae-132abb1e8259","Authorization": f"OAuth {token}","Content-Type": "text/plain;charset=UTF-8","User-agent": f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36',"Client-Session-Id": "671362f9f83b6729","Client-Id": "kimne78kx3ncx6brgo4mv6wki5h1ko","X-Device-Id": "O1MrFLwPyZ2byJzoLFT0K5XNlORNRQ9F","sec-ch-ua-platform": '"Windows"',"Accept": "*/*","Origin": "https://dashboard.twitch.tv","Sec-Fetch-Site": "same-site","Sec-Fetch-Mode": "cors","Sec-Fetch-Dest": "empty","Referer": "https://dashboard.twitch.tv/",}
            json = [{"operationName": "UpdateUserProfile","variables": {"input": {"displayName": username,"description": Config.bio,"userID": user_id,}},"extensions": {"persistedQuery": {"version": 1,"sha256Hash": "991718a69ef28e681c33f7e1b26cf4a33a2a100d0c7cf26fbff4e2c0a26d15f2",}},}]
            r = requests.post("https://gql.twitch.tv/gql",headers=headers, json=json)
            
            open('Out/tokens.txt','a').write(f'{token}\n')
            open('Out/accounts.txt','a').write(f'{username}:{password}\n')
            print(Fore.GREEN + f"Generated | {Fore.RESET}{token}\n")





def start():
    print("CapyTwitch By Atsuyo\n")
    threads = input("Enter amount of threads > ")
    time.sleep(1)
    print(f"Please Wait while 5-10 seconds for captchas to solve\n")
    for i in range(int(threads)):
        threading.Thread(target=Generator).start()
    
start()
