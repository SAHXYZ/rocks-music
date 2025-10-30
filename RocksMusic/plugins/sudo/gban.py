import asyncio

from pyrogram import filters
from pyrogram.errors import FloodWait
from pyrogram.types import Message

from RocksMusic import app
from RocksMusic.misc import SUDOERS
from RocksMusic.utils import get_readable_time
from RocksMusic.utils.database import (
    add_banned_user,
    get_banned_count,
    get_banned_users,
    get_served_chats,
    is_banned_user,
    remove_banned_user,
)
from RocksMusic.utils.decorators.language import language
from RocksMusic.utils.extraction import extract_user
from config import BANNED_USERS


@app.on_message(filters.command(["gban", "globalban"]) & SUDOERS)
@language
async def global_ban(client, message: Message, _):
    if not message.reply_to_message and len(message.command) != 2:
        return await message.reply_text(_["general_1"])
    
    user = await extract_user(message)
    
    if user.id in [message.from_user.id, app.id] or user.id in SUDOERS:
        return await message.reply_text(_["gban_invalid"])
    
    if await is_banned_user(user.id):
        return await message.reply_text(_["gban_4"].format(user.mention))
    
    if user.id not in BANNED_USERS:
        BANNED_USERS.add(user.id)

    served_chats = [int(chat["chat_id"]) for chat in await get_served_chats()]
    time_expected = get_readable_time(len(served_chats))
    
    mystic = await message.reply_text(_["gban_5"].format(user.mention, time_expected))
    
    count = 0
    for chat_id in served_chats:
        try:
            await app.ban_chat_member(chat_id, user.id)
            count += 1
        except FloodWait as fw:
            await asyncio.sleep(int(fw.value))
        except:
            continue
    
    await add_banned_user(user.id)
    await message.reply_text(_["gban_6"].format(
        app.mention,
        message.chat.title,
        message.chat.id,
        user.mention,
        user.id,
        message.from_user.mention,
        count,
    ))
    await mystic.delete()


@app.on_message(filters.command(["ungban"]) & SUDOERS)
@language
async def global_unban(client, message: Message, _):
    if not message.reply_to_message and len(message.command) != 2:
        return await message.reply_text(_["general_1"])
    
    user = await extract_user(message)
    
    if not await is_banned_user(user.id):
        return await message.reply_text(_["gban_7"].format(user.mention))
    
    if user.id in BANNED_USERS:
        BANNED_USERS.remove(user.id)

    served_chats = [int(chat["chat_id"]) for chat in await get_served_chats()]
    time_expected = get_readable_time(len(served_chats))
    
    mystic = await message.reply_text(_["gban_8"].format(user.mention, time_expected))
    
    count = 0
    for chat_id in served_chats:
        try:
            await app.unban_chat_member(chat_id, user.id)
            count += 1
        except FloodWait as fw:
            await asyncio.sleep(int(fw.value))
        except:
            continue
    
    await remove_banned_user(user.id)
    await message.reply_text(_["gban_9"].format(user.mention, count))
    await mystic.delete()


@app.on_message(filters.command(["gbannedusers", "gbanlist"]) & SUDOERS)
@language
async def gbanned_list(client, message: Message, _):
    counts = await get_banned_count()
    if counts == 0:
        return await message.reply_text(_["gban_10"])
    
    mystic = await message.reply_text(_["gban_11"])
    msg = _["gban_12"]
    count = 0
    
    for user_id in await get_banned_users():
        count += 1
        try:
            user = await app.get_users(user_id)
            user = user.first_name if not user.mention else user.mention
            msg += f"{count}➤ {user}\n"
        except:
            msg += f"{count}➤ {user_id}\n"
    
    if count == 0:
        await mystic.edit_text(_["gban_10"])
    else:
        await mystic.edit_text(msg)
