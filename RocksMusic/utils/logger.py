
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

from pyrogram.enums import ParseMode

from RocksMusic import app
from RocksMusic.utils.database import is_on_off
from config import LOG_GROUP_ID


async def play_logs(message, streamtype):
    if await is_on_off(2):
        logger_text = f"""
<b>{app.mention} ᴘʟᴀʏ ʟᴏɢ</b>

<b>ᴄʜᴀᴛ ɪᴅ :</b> <code>{message.chat.id}</code>
<b>ᴄʜᴀᴛ ɴᴀᴍᴇ :</b> {message.chat.title}
<b>ᴄʜᴀᴛ ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.chat.username}

<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>
<b>ɴᴀᴍᴇ :</b> {message.from_user.mention}
<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}

<b>ǫᴜᴇʀʏ :</b> {message.text.split(None, 1)[1]}
<b>sᴛʀᴇᴀᴍᴛʏᴘᴇ :</b> {streamtype}"""
        if message.chat.id != LOG_GROUP_ID:
            try:
                await app.send_message(
                    chat_id=LOG_GROUP_ID,
                    text=logger_text,
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True,
                )
            except:
                pass
        return
