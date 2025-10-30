
import pyrogram
from pyrogram.errors import RPCError
from pyrogram.errors.exceptions.bad_request_400 import ChannelInvalid

async def _safe_send(client, *args, **kwargs):
    try:
        # prefer send_message if available else call method as-is
        if hasattr(client, 'send_message'):
            return await client.send_message(*args, **kwargs)
        # fallback, attempt generic call
        return await getattr(client, kwargs.pop('_method', 'send_message'))(*args, **kwargs)
    except ChannelInvalid as e:
        try:
            LOGGER.error(f"Channel invalid or bot missing access: {e}")
        except Exception:
            print(f"Channel invalid: {e}")
        return None
    except (TimeoutError, RPCError) as e:
        try:
            LOGGER.warning(f"Send timeout or RPC error, will skip: {e}")
        except Exception:
            print(f"Send error: {e}")
        return None

import asyncio
from datetime import datetime
from pyrogram.enums import ChatType
from pytgcalls.exceptions import GroupCallNotFound
import config
from RocksMusic import app
from RocksMusic.misc import db
from RocksMusic.core.call import Rocks, autoend, counter
from RocksMusic.utils.database import get_client, set_loop, is_active_chat, is_autoend, is_autoleave
import logging

async def auto_leave():
    while not await asyncio.sleep(900):
        from RocksMusic.core.userbot import assistants
        ender = await is_autoleave()
        if not ender:
            continue
        for num in assistants:
            client = await get_client(num)
            left = 0
            try:
                async for i in client.get_dialogs():
                    if i.chat.type in [
                        ChatType.SUPERGROUP,
                        ChatType.GROUP,
                        ChatType.CHANNEL,
                    ]:
                        if (
                            i.chat.id != config.LOG_GROUP_ID
                            and i.chat.id != -1002016928980
                            and i.chat.id != -1002200386150
                            and i.chat.id != -1001397779415
                        ):
                            if left == 20:
                                continue
                            if not await is_active_chat(i.chat.id):
                                try:
                                    await client.leave_chat(i.chat.id)
                                    left += 1
                                except Exception as e:
                                    logging.error(f"Error leaving chat {i.chat.id}: {e}")
                                    continue
            except Exception as e:
                logging.error(f"Error processing dialogs: {e}")

asyncio.create_task(auto_leave())

async def auto_end():
    global autoend, counter
    while True:
        await asyncio.sleep(60)
        try:
            ender = await is_autoend()
            if not ender:
                continue
            chatss = autoend
            keys_to_remove = []
            nocall = False
            for chat_id in chatss:
                try:
                    users = len(await Rocks.call_listeners(chat_id))
                except GroupCallNotFound:
                    users = 1
                    nocall = True
                except Exception:
                    users = 100
                timer = autoend.get(chat_id)
                if users == 1:
                    res = await set_loop(chat_id, 0)
                    keys_to_remove.append(chat_id)
                    try:
                        await db[chat_id][0]["mystic"].delete()
                    except Exception:
                        pass
                    try:
                        await Rocks.stop_stream(chat_id)
                    except Exception:
                        pass
                    try:
                        if not nocall:
                            await app.send_message(chat_id, "» ʙᴏᴛ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ʟᴇғᴛ ᴠɪᴅᴇᴏᴄʜᴀᴛ ʙᴇᴄᴀᴜsᴇ ɴᴏ ᴏɴᴇ ᴡᴀs ʟɪsᴛᴇɴɪɴɢ ᴏɴ ᴠɪᴅᴇᴏᴄʜᴀᴛ.")
                    except Exception:
                        pass
            for chat_id in keys_to_remove:
                del autoend[chat_id]
        except Exception as e:
            logging.info(e)

asyncio.create_task(auto_end())
