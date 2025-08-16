# main.py
from os import access
import asyncio, json, time, random, threading, websockets

def load_tokens():
    with open("tokens.txt", "r") as f:
        return [line.strip() for line in f if line.strip()]

def activity_status():
    tokens = load_tokens()
    if not tokens:
        return
    print("""
                                          \033[38;5;27m   __  ___ ____ __  ___ ____   ___   ____ ____ ____
                                          \033[38;5;33m  /  |/  // __//  |/  // __ \ / _ \ /  _// __// __/
                                          \033[38;5;111m / /|_/ // _/ / /|_/ // /_/ // , _/_/ / / _/ _\ \\
                                          \033[38;5;255m/_/  /_//___//_/  /_/ \____//_/|_|/___//___//___/  

                                                            \033[38;5;27m[\033[0m00\033[38;5;27m]\033[0m Playing
                                                            \033[38;5;27m[\033[0m01\033[38;5;27m]\033[0m Streaming
                                                            \033[38;5;27m[\033[0m02\033[38;5;27m]\033[0m Listening
                                                            \033[38;5;27m[\033[0m03\033[38;5;27m]\033[0m Watching
    """)
    activity_type = int(input("                                                    \033[38;5;8m[\033[38;5;27mMemories\033[38;5;8m] -> \033[38;5;27mStatus Type\033[0m ").strip())
    activity_name = input("                                                    \033[38;5;8m[\033[38;5;27mMemories\033[38;5;8m] -> \033[38;5;27mActivity Name\033[0m ").strip()

    GATEWAY = "wss://gateway.discord.gg/?v=9&encoding=json"

    async def set_activity(token):
        try:
            async with websockets.connect(GATEWAY) as ws:
                hello = await ws.recv()
                heartbeat_interval = json.loads(hello)['d']['heartbeat_interval'] / 1000

                payload = {
                    "op": 2,
                    "d": {
                        "token": token,
                        "intents": 0,
                        "properties": {
                            "$os": "windows",
                            "$browser": "chrome",
                            "$device": "pc"
                        },
                        "presence": {
                            "status": "online",
                            "afk": False,
                            "activities": [{
                                "type": activity_type,
                                "name": activity_name
                            }]
                        }
                    }
                }
                await ws.send(json.dumps(payload))

                while True:
                    await ws.send(json.dumps({"op": 1, "d": None}))
                    await asyncio.sleep(heartbeat_interval)
                    
        except Exception as e:
            pass

    def run_token(token):
        asyncio.run(set_activity(token))

    for token in tokens:
        threading.Thread(target=run_token, args=(token,), daemon=True).start()
        time.sleep(random.uniform(1, 2))

    while True:
        time.sleep(1)

if __name__ == "__main__":
    activity_status()
