import asyncio, os
def apply():
    # Avoid 'Cannot add child handler, the child watcher does not have a loop' on some hosts
    try:
        if os.name != 'nt':
            asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())
    except Exception:
        pass
