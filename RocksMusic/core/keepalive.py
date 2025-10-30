from aiohttp import web
import os
import asyncio

async def ping(request):
    return web.Response(text="OK")

def run_keepalive():
    port = os.environ.get("PORT")
    if not port:
        return  # Only run in Heroku-like environments
    app = web.Application()
    app.router.add_get("/", ping)
    runner = web.AppRunner(app)
    loop = asyncio.get_event_loop()
    async def _run():
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", int(port))
        await site.start()
    loop.create_task(_run())
