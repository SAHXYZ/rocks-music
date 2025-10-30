from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultPhoto,
    InlineQuery,
)
from youtubesearchpython.__future__ import VideosSearch

from RocksMusic import app
from RocksMusic.utils.inlinequery import answer as default_answer
from config import BANNED_USERS


@app.on_inline_query(~BANNED_USERS)
async def inline_query_handler(client, query: InlineQuery):
    text = query.query.strip().lower()
    results = []

    if not text:
        try:
            await client.answer_inline_query(query.id, results=default_answer, cache_time=10)
        except:
            return
        return

    search = VideosSearch(text, limit=20)
    response = (await search.next()).get("result")

    for item in response[:15]:
        title = item["title"].title()
        duration = item["duration"]
        views = item["viewCount"]["short"]
        thumbnail = item["thumbnails"][0]["url"].split("?")[0]
        channel_name = item["channel"]["name"]
        channel_link = item["channel"]["link"]
        video_link = item["link"]
        published = item["publishedTime"]

        description = f"{views} | {duration} ᴍɪɴᴜᴛᴇs | {channel_name} | {published}"
        buttons = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text="ʏᴏᴜᴛᴜʙᴇ 🎄", url=video_link)]
            ]
        )

        caption = f"""
❄ <b>ᴛɪᴛʟᴇ :</b> <a href='{video_link}'>{title}</a>

⏳ <b>ᴅᴜʀᴀᴛɪᴏɴ :</b> {duration} ᴍɪɴᴜᴛᴇs
👀 <b>ᴠɪᴇᴡs :</b> <code>{views}</code>
🎥 <b>ᴄʜᴀɴɴᴇʟ :</b> <a href='{channel_link}'>{channel_name}</a>
⏰ <b>ᴘᴜʙʟɪsʜᴇᴅ ᴏɴ :</b> {published}

<u><b>➻ ɪɴʟɪɴᴇ sᴇᴀʀᴄʜ ᴍᴏᴅᴇ ʙʏ {app.name}</b></u>
"""

        results.append(
            InlineQueryResultPhoto(
                photo_url=thumbnail,
                title=title,
                thumb_url=thumbnail,
                description=description,
                caption=caption,
                reply_markup=buttons,
            )
        )

    try:
        await client.answer_inline_query(query.id, results=results, cache_time=10)
    except:
        return
