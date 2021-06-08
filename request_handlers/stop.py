from request_handlers.app_context import Command, Target
from request_handlers.context_request import ContextRequestHandler


class StopHandler(ContextRequestHandler):

    async def post(self):
        target = Target(host="localhost", user="vagrant", port=2222)
        command = Command("STOP", "for i in {1..10}; do echo 'stopping...'; sleep 1; done", target)
        try:
            await self.execute(command)
        except Exception as e:
            self.ctx.error = e.args
        self.write("stop")