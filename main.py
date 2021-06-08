import os
import tornado.web
import tornado.ioloop
from request_handlers import MainHandler, StopHandler, StatusHandler, StartHandler, AppContext


def make_handlers(context):
    return [
        (r"/", MainHandler, dict(ctx=context)),
        (r"/api/v1/stop", StopHandler, dict(ctx=context)),
        (r"/api/v1/start", StartHandler, dict(ctx=context)),
        (r"/api/v1/status", StatusHandler, dict(ctx=context)),
    ]


def make_settings():
    return {
        "cookie_secret": "__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
        "template_path": os.path.join(os.path.dirname(__file__), "templates"),
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
        "xsrf_cookies": True,
        "debug": True,
    }


def make_app():
    context = AppContext()
    handlers = make_handlers(context)
    settings = make_settings()
    return tornado.web.Application(
        handlers,
        **settings,
    )


def run(app):
    app.listen(3000)
    try:
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        print("\nCtrl+C, exiting...")


def main():
    app = make_app()
    run(app)


if __name__ == "__main__":
    main()
