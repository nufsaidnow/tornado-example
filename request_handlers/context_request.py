import asyncio
from functools import partial

import invoke
import tornado.web
from fabric import Result
from invoke import UnexpectedExit

from request_handlers.app_context import ApplicationState


class CommandWatcher(invoke.watchers.StreamWatcher):
    def __init__(self, loop, callback):
        super().__init__()
        self.len = 0
        self.loop = loop
        self.callback = callback

    def submit(self, stream):
        new = stream[self.len:]
        self.loop.call_soon_threadsafe(self.callback, new.strip())
        self.len = len(stream)
        return []


class NotReadyException(Exception):
    pass


class ContextRequestHandler(tornado.web.RequestHandler):

    def initialize(self, ctx):
        self.ctx = ctx

    def command_callback(self, msg):
        self.ctx.current_command.output = msg

    async def execute(self, command):
        if self.ctx.state != ApplicationState.WAITING_FOR_COMMAND:
            self.ctx.error = "NOT_READY"
            return

        self.ctx.current_command = command
        self.ctx.state = ApplicationState.EXECUTING

        loop = asyncio.get_event_loop()
        watcher = CommandWatcher(loop, self.command_callback)
        c = command.target.get_connection()
        func_run = partial(c.run, command.script, watchers=[watcher], hide=True)
        try:
            fut = await loop.run_in_executor(None, func_run)
            return fut
        except UnexpectedExit as ue:
            self.ctx.error = f"Exit({ue.reason})"
        finally:
            self.ctx.state = ApplicationState.WAITING_FOR_COMMAND
            self.ctx.current_command = None
