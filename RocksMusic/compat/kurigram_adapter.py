import asyncio
from loguru import logger

try:
    # Import whichever is installed
    from pyrogram import Client, errors
except Exception:  # pragma: no cover
    Client = None
    errors = None

_flood_max_sleep = 60

if Client:
    _orig_start = Client.start

    async def _patched_start(self):
        # Call original start
        res = await _orig_start(self)
        # Tune nearest DC for Kurigram (recommended in channel notes)
        try:
            if hasattr(self, "set_dc"):
                await self.set_dc()
                logger.info("[compat] set_dc() applied for optimal DC")
        except Exception as e:
            logger.debug(f"[compat] set_dc skipped: {e}")
        return res

    Client.start = _patched_start  # type: ignore

    # Wrap send utilities with FloodWait backoff
    async def _fw_send_message(self, chat_id, text, **kwargs):
        try:
            return await Client.send_message(self, chat_id, text, **kwargs)
        except Exception as e:
            if errors and isinstance(e, errors.FloodWait):
                delay = min(getattr(e, "value", 5), _flood_max_sleep)
                logger.warning(f"[compat] FloodWait {delay}s on send_message; backing off")
                await asyncio.sleep(delay)
                return await Client.send_message(self, chat_id, text, **kwargs)
            raise

    Client._send_message_orig = Client.send_message  # type: ignore
    Client.send_message = _fw_send_message  # type: ignore

    logger.info("[compat] Kurigram/Pyrogram adapter loaded")
