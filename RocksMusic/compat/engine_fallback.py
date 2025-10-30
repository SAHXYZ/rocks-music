import sys
try:
    import pyrogram  # noqa: F401
except Exception:
    try:
        import kurigram as _k
        sys.modules.setdefault("pyrogram", _k)
        for name in ("raw", "types", "errors"):
            if hasattr(_k, name):
                sys.modules.setdefault(f"pyrogram.{name}", getattr(_k, name))
        print("[compat] Fallback engaged: aliased 'kurigram' as 'pyrogram'")
    except Exception as e:
        print(f"[compat] Fallback failed: kurigram not available ({e})")
