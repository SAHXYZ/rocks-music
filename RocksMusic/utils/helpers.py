from loguru import logger

def safe_contains_live(queued):
    try:
        return bool(queued) and ('live_' in queued)
    except Exception as e:
        logger.debug(f"[helpers] contains_live failed: {e}")
        return False
