#!/usr/bin/env python3

import requests
import webbrowser
import json
import sys

from env import *

def err_on_status_code(request, text, exit=True):
    if request.status_code != 200:
        print(f"{text} : {r.status_code} - {r.text}")
        if exit:
            sys.exit(1)

# REQUESTS CONFIG
headers = {'X-Accept': 'application/json'}

# 1 + 2 - send request to get request token
payload = {
    'consumer_key': POCKET_CONSUMER_KEY,
    'redirect_uri': REDIRECT_URI,
}
r = requests.post(f"{POCKET_URL}/oauth/request", data=payload, headers=headers)

err_on_status_code(r, "[pocket] error while getting request token")

POCKET_REQUEST_TOKEN = r.json()['code']
print(f"[pocket] request_token = {POCKET_REQUEST_TOKEN}")

# 3 - redirect user
webbrowser.open(f"https://getpocket.com/auth/authorize?request_token={POCKET_REQUEST_TOKEN}&redirect_uri={REDIRECT_URI}", new=2)
print(f"if your browser did not open, please go to : https://getpocket.com/auth/authorize?request_token={POCKET_REQUEST_TOKEN}&redirect_uri={REDIRECT_URI}")

# TODO replace this input with a socket that will listen to the callback of the oAuth, so we dont have to use a user interaction
input("If you have authorized the app, please press Enter to continue...")

# 4 - get access token
payload = {
    'consumer_key': POCKET_CONSUMER_KEY,
    'code': POCKET_REQUEST_TOKEN,
}
r = requests.post(f"{POCKET_URL}/oauth/authorize", data=payload, headers=headers)

err_on_status_code(r, "[pocket] error while getting access token")

POCKET_ACCESS_TOKEN = r.json()['access_token']
print(f"[pocket] access_token = {POCKET_ACCESS_TOKEN}")

# 5 - get items
payload = {
    "consumer_key": POCKET_CONSUMER_KEY,
    "access_token": POCKET_ACCESS_TOKEN,
    "state": "unread",
    "sort": "oldest",
    "detailType": "simple"
}
r = requests.post(f"{POCKET_URL}/get", data=payload, headers=headers)

err_on_status_code(r, "[pocket] error while getting items")

# 6 - create list of urls
all_items = r.json()['list']
urls = [item['given_url'] for item in all_items.values()]

# 7 - wallabag oAuth - get access token
payload = {
    "grant_type": "password",
    "client_id": WALLABAG_CLIENT_ID,
    "client_secret": WALLABAG_CLIENT_SECRET,
    "username": WALLABAG_USERNAME,
    "password": WALLABAG_PASSWORD
}
r = requests.post(f"{WALLABAG_URL}/oauth/v2/token", data=payload, headers=headers)

err_on_status_code(r, "[wallabag] error while getting access token")

WALLABAG_ACCESS_TOKEN=r.json()['access_token']
print(f"[wallabag] access_token = {WALLABAG_ACCESS_TOKEN}")

# 8 - import urls in wallabag
# the API to import a list of urls seems buggy, I dont know why, so we'll import one by one
# https://app.wallabag.it/api/doc#post--api-entries-lists.{_format}
headers = {
    "X-Accept": "application/json",
    "Authorization": f"Bearer {WALLABAG_ACCESS_TOKEN}"
}
# TODO make it faster (concurrency, threads, asyncio, futures, gevent ...)
for index, url in enumerate(urls):
    print(f"[wallabag] importing {index}/{len(urls)} : {url} ...")

    payload = {
        "url": url,
    }
    r = requests.post(f"{WALLABAG_URL}/api/entries.json", data=payload, headers=headers)

    err_on_status_code(r, "[wallabag] error while importing", exit=False)

    print(f"[wallabag] success : {r.status_code}")

print("done :) gg! your pocket items were successfully migrated to wallabag")