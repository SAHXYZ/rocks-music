from loguru import logger

class ErrorGuard:
    @staticmethod
    async def swallow(awaitable, *, context: str = ''):
        try:
            return await awaitable
        except Exception as e:
            logger.warning(f"[guard] {context} → {e}")
            return None
