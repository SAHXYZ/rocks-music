#!/usr/bin/env python3
# Unified launcher added by fixer. Defers heavy imports to avoid circular/import-time side effects.

import os, sys, asyncio

async def _amain():
    # Preload engine fallback & adapter
    try:
        import RocksMusic.compat.engine_fallback  # noqa: F401
    except Exception as e:
        print(f"[launcher] engine fallback preload skipped: {e}")
    try:
        import RocksMusic.compat.kurigram_adapter  # noqa: F401
    except Exception as e:
        print(f"[launcher] kurigram adapter preload skipped: {e}")

    # Preload compatibility adapter for Kurigram/Pyrogram
    try:
        import RocksMusic.compat.kurigram_adapter  # noqa: F401
    except Exception as e:
        print(f"[launcher] compat adapter load skipped: {e}")

    # Prefer explicit module if present
    candidates = [
        "RocksMusic.core.bot",
    ]
    for mod in candidates:
        try:
            module = __import__(mod, fromlist=['*'])
            if hasattr(module, 'main'):
                if asyncio.iscoroutinefunction(module.main):
                    return await module.main()
                else:
                    return module.main()
            # Pyrogram apps commonly expose 'app' or 'Client'
            app = getattr(module, 'app', None) or getattr(module, 'client', None) or getattr(module, 'Client', None)
            if app and hasattr(app, 'run'):
                return app.run()
        except Exception as e:
            print(f"[launcher] Tried {mod} failed: {e}", file=sys.stderr)
            continue
    # Fallback: try running as script
    try:
        __import__(candidates[0])
    except Exception as e:
        print(f"[launcher] Fallback import failed: {e}", file=sys.stderr)
        raise

def main():
    import os
    if os.environ.get('DYNO'):
        print('[runtime] Heroku environment detected → dyno mode')
    else:
        print('[runtime] VPS/local environment detected → direct mode')

    try:
        asyncio.run(_amain())
    except RuntimeError:
        # If already in loop (uvicorn/fastapi), just call _amain directly
        loop = asyncio.get_event_loop()
        loop.run_until_complete(_amain())

if __name__ == "__main__":
    main()
