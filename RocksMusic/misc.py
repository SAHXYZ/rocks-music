import socket
import asyncio
import time
import heroku3
from pyrogram import filters
import config
from RocksMusic.core.mongo import mongodb
from RocksMusic.logging import LOGGER

SUDOERS = filters.user()
HAPP = None
_boot_ = time.time()

def is_heroku():
    return "heroku" in socket.getfqdn()

# --- Local DB ---
def dbb():
    global db
    db = {}
    try:
        LOGGER(__name__).info("Local Database Initialized.")
    except Exception as e:
        LOGGER(__name__).warning(f"DB init failed: {e}")

# --- Load Sudoers ---
async def sudo():
    global SUDOERS
    try:
        SUDOERS.add(config.OWNER_ID)
        sudoersdb = mongodb.sudoers
        sudoers = await sudoersdb.find_one({"sudo": "sudo"}) or {"sudoers": []}
        if config.OWNER_ID not in sudoers["sudoers"]:
            sudoers["sudoers"].append(config.OWNER_ID)
            await sudoersdb.update_one(
                {"sudo": "sudo"},
                {"$set": {"sudoers": sudoers["sudoers"]}},
                upsert=True,
            )
        for user_id in sudoers["sudoers"]:
            SUDOERS.add(user_id)
        LOGGER(__name__).info("Sudoers Loaded Successfully.")
    except Exception as e:
        LOGGER(__name__).error(f"Failed to load sudoers: {e}")

# --- Heroku API ---
def heroku():
    global HAPP
    if not (config.HEROKU_API_KEY and config.HEROKU_APP_NAME):
        LOGGER(__name__).warning("Heroku credentials missing.")
        return
    try:
        Heroku = heroku3.from_key(config.HEROKU_API_KEY)
        HAPP = Heroku.app(config.HEROKU_APP_NAME)
        LOGGER(__name__).info("Heroku App Configured Successfully.")
    except Exception as e:
        LOGGER(__name__).warning(f"Heroku setup failed: {e}")
