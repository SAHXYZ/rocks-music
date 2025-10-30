from typing import Union

from pyrogram import filters, types
from pyrogram.types import InlineKeyboardMarkup, Message

from RocksMusic import app
from RocksMusic.utils import help_pannel
from RocksMusic.utils.database import get_lang
from RocksMusic.utils.decorators.language import LanguageStart, languageCB
from RocksMusic.utils.inline.help import help_back_markup, private_help_panel
from config import BANNED_USERS, START_IMG_URL, SUPPORT_GROUP
from strings import get_string, helpers


# -------------------- PRIVATE HELP COMMAND -------------------- #
@app.on_message(filters.command(["help"]) & filters.private & ~BANNED_USERS)
async def helper_private(client: app, message: Message):
    language = await get_lang(message.chat.id)
    _ = get_string(language)
    keyboard = help_pannel(_, True)
    await message.reply_photo(
        photo=START_IMG_URL,
        caption=_["help_1"].format(SUPPORT_GROUP),
        reply_markup=keyboard,
    )


# -------------------- GROUP HELP COMMAND -------------------- #
@app.on_message(filters.command(["help"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def helper_group(client, message: Message, _):
    keyboard = private_help_panel(_)
    await message.reply_text(_["help_2"], reply_markup=InlineKeyboardMarkup(keyboard))


# -------------------- CALLBACK HANDLER FOR HELP -------------------- #
@app.on_callback_query(filters.regex("help_callback") & ~BANNED_USERS)
@languageCB
async def helper_callback(client, CallbackQuery, _):
    cb_data = CallbackQuery.data.strip().split(None, 1)[1]

    # Determine which help section to show
    if cb_data == "hb16":
        text = helpers.HELP_16.format(app.name)
    else:
        text = getattr(helpers, f"HELP_{cb_data[2:]}", helpers.HELP_16.format(app.name))

    # Add back button
    keyboard = help_back_markup(_)
    await CallbackQuery.edit_message_text(text, reply_markup=keyboard)
    try:
        await CallbackQuery.answer()
    except:
        pass


# -------------------- CALLBACK HANDLER FOR BACK BUTTON -------------------- #
@app.on_callback_query(filters.regex("settings_back_helper") & ~BANNED_USERS)
async def helper_back(client, CallbackQuery):
    try:
        await CallbackQuery.answer()
    except:
        pass

    chat_id = CallbackQuery.message.chat.id
    language = await get_lang(chat_id)
    _ = get_string(language)
    keyboard = help_pannel(_, True)
    await CallbackQuery.edit_message_text(
        _["help_1"].format(SUPPORT_GROUP), reply_markup=keyboard
    )
