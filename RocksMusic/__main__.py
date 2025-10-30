# __main__.py - safe startup for RocksMusic
import asyncio
import importlib
import sys
import time
from RocksMusic.core.keepalive import run_keepalive
from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from config import BANNED_USERS
from RocksMusic.logging import LOGGER
from RocksMusic.core.call import Rocks
from RocksMusic.misc import sudo
from RocksMusic.plugins import ALL_MODULES
from RocksMusic.utils.database import get_banned_users, get_gbanned

# Import bot and userbot from core modules directly to avoid circular package import
from RocksMusic.core.bot import app
from RocksMusic.core.userbot import userbot

async def init():
    if not any([config.STRING1, config.STRING2, config.STRING3, config.STRING4, config.STRING5]):
        LOGGER.error("Assistant client variables not defined, exiting...")
        sys.exit(0)

    await sudo()

    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except Exception as e:
        LOGGER.warning(f"Could not fetch banned users: {e}")

    await app.start()

    for all_module in ALL_MODULES:
        importlib.import_module("RocksMusic.plugins." + all_module)
    LOGGER.info("Successfully Imported Modules...")

    await userbot.start()
    await Rocks.start()

    try:
        await Rocks.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
    except NoActiveGroupCall:
        LOGGER.error("Please turn on the videochat of your log group/channel. Stopping Bot...")
        sys.exit(0)
    except Exception as e:
        LOGGER.warning(f"Stream call failed: {e}")

    await Rocks.decorators()
    LOGGER.info("RocksMusic Started Successfully.")

    await idle()

    # Graceful shutdown
    try:
        await app.stop()
        await userbot.stop()
    except Exception as e:
        LOGGER.warning(f"Error during shutdown: {e}")
    LOGGER.info("Stopping RocksMusic Bot...")

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(init())
