import json

from request_handlers.context_request import ContextRequestHandler


class StatusHandler(ContextRequestHandler):

    async def post(self):
        self.write(self.ctx.to_json())
        self.ctx.error = None
