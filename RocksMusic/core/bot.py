
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

from pyrogram import Client, errors
from pyrogram.enums import ChatMemberStatus, ParseMode
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import config
from ..logging import LOGGER



class Rocks(Client):
    def __init__(self):
        LOGGER(__name__).info("Starting Bot...")
        super().__init__(
            name="RocksMusic",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            in_memory=True,
            parse_mode=ParseMode.HTML,
            max_concurrent_transmissions=7,
        )

    async def start(self):
        await super().start()
        self.id = self.me.id
        self.name = self.me.first_name
        self.username = self.me.username
        self.mention = self.me.mention

        try:
            await self.send_message(
                chat_id=config.LOG_GROUP_ID,
                text=f"<u><b>» {self.mention} ʙᴏᴛ sᴛᴀʀᴛᴇᴅ :</b><u>\n\nɪᴅ : <code>{self.id}</code>\nɴᴀᴍᴇ : {self.name}\nᴜsᴇʀɴᴀᴍᴇ : @{self.username}",
            )
        except (errors.ChannelInvalid, errors.PeerIdInvalid):
            LOGGER(__name__).error(
                "Bot has failed to access the log group/channel. Make sure that you have added your bot to your log group/channel."
            )
            raise SystemExit
        except Exception as ex:
            LOGGER(__name__).error(
                f"Bot has failed to access the log group/channel.\n  Reason : {type(ex).__name__}."
            )
            raise SystemExit

        a = await self.get_chat_member(config.LOG_GROUP_ID, self.id)
        if a.status != ChatMemberStatus.ADMINISTRATOR:
            LOGGER(__name__).error(
                "Please promote your bot as an admin in your log group/channel."
            )
            raise SystemExit
        LOGGER(__name__).info(f"Music Bot Started as {self.name}")

    async def stop(self):
        await super().stop()

