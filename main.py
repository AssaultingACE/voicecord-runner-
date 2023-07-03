import os
import sys
import json
import time
import requests
import websocket
from keep_alive import keep_alive

status = "online"  # online/dnd/idle

GUILD_ID = os.getenv("GUILD_ID")
CHANNEL_ID = os.getenv("CHANNEL_ID")
SELF_MUTE = True
SELF_DEAF = False

# Add your tokens here as a list of strings
usertokens = [
      os.getenv("TOKEN1"),
      os.getenv("TOKEN2"),
      os.getenv("TOKEN3"),
      os.getenv("TOKEN4"),
      os.getenv("TOKEN5"),
      os.getenv("TOKEN6"),
      os.getenv("TOKEN7"),
      os.getenv("TOKEN8"),
      os.getenv("TOKEN9"),
      os.getenv("TOKEN10"),
      os.getenv("TOKEN11"),
      os.getenv("TOKEN12"),
      os.getenv("TOKEN13"),
      os.getenv("TOKEN14"),
      os.getenv("TOKEN15"),
      os.getenv("TOKEN16"),
      os.getenv("TOKEN17"),
      os.getenv("TOKEN18"),
      os.getenv("TOKEN19"),
      os.getenv("TOKEN20")
]

valid_tokens = []

for usertoken in usertokens:
    if usertoken:
        headers = {"Authorization": usertoken, "Content-Type": "application/json"}

        validate = requests.get('https://discordapp.com/api/v9/users/@me', headers=headers)
        if validate.status_code != 200:
            print(f"[ERROR] Token '{usertoken}' might be invalid. Please check it again.")
        else:
            valid_tokens.append(usertoken)
    else:
        break

if not valid_tokens:
    print("[ERROR] Please add at least one valid token inside Secrets.")
    sys.exit()

headers = {"Content-Type": "application/json"}

def joiner(token, status):
    ws = websocket.create_connection('wss://gateway.discord.gg/?v=9&encoding=json')
    start = json.loads(ws.recv())
    heartbeat = start['d']['heartbeat_interval']
    auth = {
        "op": 2,
        "d": {
            "token": token,
            "properties": {
                "$os": "Windows 10",
                "$browser": "Google Chrome",
                "$device": "Windows"
            },
            "presence": {
                "status": status,
                "afk": False
            }
        },
        "s": None,
        "t": None
    }
    vc = {
        "op": 4,
        "d": {
            "guild_id": GUILD_ID,
            "channel_id": CHANNEL_ID,
            "self_mute": SELF_MUTE,
            "self_deaf": SELF_DEAF
        }
    }
    ws.send(json.dumps(auth))
    ws.send(json.dumps(vc))
    time.sleep(heartbeat / 1000)
    ws.send(json.dumps({"op": 1, "d": None}))

def run_joiner():
    os.system("clear")
    print(f"Logged in as {username}#{discriminator} ({userid}).")
    while True:
        for token in valid_tokens:
            joiner(token, status)
        time.sleep(30)

keep_alive()
run_joiner()
