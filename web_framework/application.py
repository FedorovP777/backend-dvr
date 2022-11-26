import argparse
import asyncio
from typing import List, Tuple

import tornado.web

from web_framework.http.generate_middleware import generate_middleware
from web_framework.http.kernel import Kernel


class Application:
    def __init__(self,
                 middleware: dict,
                 middleware_group: dict,
                 routes: list,
                 port=8881
                 ):
        self.middleware = middleware
        self.middleware_group = middleware_group
        self.routes = routes
        self.port = port

    async def start(self):
        kernel = Kernel()
        app = tornado.web.Application(kernel.make_tornado_routes(self.routes, self.middleware, self.middleware_group))
        app.listen(self.port)
        await asyncio.Event().wait()

    def show_urls(self) -> None:
        """Print registered urls."""
        registered_routes = Kernel().make_tornado_routes(self.routes, self.middleware, self.middleware_group)

        for (path, controller) in registered_routes:
            controller_name = f'{controller.get_original_controller().__module__}.{controller.get_original_controller().__name__}'
            print(f'url: {path} -> {controller_name}')

        exit(0)

    def cli_process(self):
        """Handle cli commands."""
        parser = argparse.ArgumentParser()

        subparsers = parser.add_subparsers(help='sub-command help')
        parser_b = subparsers.add_parser('make:middleware', help='Generate new middleware')
        parser_b.add_argument('classname', help='Middleware Name')
        parser_b.set_defaults(func=lambda x: generate_middleware(x.classname))

        parser_c = subparsers.add_parser('show_urls', help='Print urls')
        parser_c.set_defaults(func=lambda _: self.show_urls())
        args = parser.parse_args()

        if hasattr(args, 'func'):
            args.func(args)
