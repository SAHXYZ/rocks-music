import asyncio
from loguru import logger

try:
    from pyrogram.errors import ChatSendPhotosForbidden, FloodWait, RPCError
except Exception:
    try:
        from kurigram.errors import ChatSendPhotosForbidden, FloodWait, RPCError  # type: ignore
    except Exception:
        ChatSendPhotosForbidden = Exception  # type: ignore
        FloodWait = Exception  # type: ignore
        RPCError = Exception  # type: ignore

async def safe_send_photo(app, chat_id, photo, **kwargs):
    caption = kwargs.pop('caption', None)
    try:
        return await app.send_photo(chat_id, photo, caption=caption, **kwargs)
    except ChatSendPhotosForbidden:
        logger.warning('[safe] CHAT_SEND_PHOTOS_FORBIDDEN → falling back to send_message')
        text = caption or (kwargs.get('caption') or '[photo]')
        return await app.send_message(chat_id, text)
    except FloodWait as e:
        delay = min(getattr(e, 'value', 5), 60)
        logger.warning(f'[safe] FloodWait {delay}s on send_photo')
        await asyncio.sleep(delay)
        try:
            return await app.send_photo(chat_id, photo, caption=caption, **kwargs)
        except Exception as err:
            logger.warning(f'[safe] retry failed: {err}; fallback to message')
            text = caption or '[photo]'
            return await app.send_message(chat_id, text)
    except RPCError as e:
        logger.warning(f'[safe] RPCError on send_photo: {e}; fallback to message')
        text = caption or '[photo]'
        return await app.send_message(chat_id, text)
