from request_handlers.context_request import ContextRequestHandler


class MainHandler(ContextRequestHandler):

    def get(self):
        self.render("index.html")