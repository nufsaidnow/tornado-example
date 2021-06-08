from request_handlers.app_context import Command, Target
from request_handlers.context_request import ContextRequestHandler


class StartHandler(ContextRequestHandler):

    async def post(self):
        target = Target(host="localhost", user="vagrant", port=2222)
        command_start = Command("START", "for i in {1..10}; do echo 'starting...'; sleep 1; done", target)
        command_stop = Command("KUBECTL", "kubectl get pods", target)
        try:
            # await self.execute(command_start)
            await self.execute(command_stop)
        except Exception as e:
            print(e)
            self.ctx.error = e.args
        self.write("stop")