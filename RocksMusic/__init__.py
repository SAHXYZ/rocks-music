from RocksMusic.logging import LOGGER

# Deferred imports to avoid circular dependencies
try:
    import RocksMusic.core.bot as core_bot
    import RocksMusic.core.userbot as core_userbot
    from RocksMusic.misc import dbb, heroku, sudo

    # Initialize optional services safely
    try:
        dbb()
    except Exception:
        LOGGER.warning("dbb() init failed or skipped.")

    try:
        heroku()
    except Exception:
        LOGGER.info("heroku() init skipped or failed.")

    try:
        sudo()
    except Exception:
        LOGGER.info("sudo() init skipped or failed.")

    # Expose instances
    app = getattr(core_bot, "app", None)
    userbot = getattr(core_userbot, "userbot", None)

    LOGGER.info("RocksMusic core initialized successfully.")

except Exception as e:
    LOGGER.error(f"RocksMusic __init__ initialization error: {e}")

__all__ = ["LOGGER", "app", "userbot"]
