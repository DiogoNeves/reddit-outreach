"""A simple OAuth server that listens for an authorization code."""

import asyncio
from aiohttp import web
from aiohttp.web_request import Request
from typing import Optional

class OAuthHandler:
    def __init__(self):
        self.auth_code_event: asyncio.Event = asyncio.Event()
        self.auth_code: Optional[str] = None

    async def handle(self, request: Request) -> web.Response:
        # Parse the URL to get the authorization code
        self.auth_code = request.query.get('code')

        if self.auth_code:
            # Signal that the authorization code has been received
            self.auth_code_event.set()
            # Send a simple response back to the browser
            return web.Response(
                text="Authorization code received. You can close this window."
            )
        else:
            return web.Response(
                text="Authorization code not found in the URL.", status=400
            )

    async def run_server(self) -> Optional[str]:
        app = web.Application()
        app.add_routes([web.get('/reddit', self.handle)])

        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, 'localhost', 8000)
        await site.start()
        print("Serving on http://localhost:8000/reddit")

        # Wait for the authorization code to be received
        await self.auth_code_event.wait()

        return self.auth_code

async def get_auth_code_from_server() -> str:
    handler = OAuthHandler()
    code = await handler.run_server()
    if code is None:
        raise RuntimeError("Failed to obtain authorization code.")
    return code
