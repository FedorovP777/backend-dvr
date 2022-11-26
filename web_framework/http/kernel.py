from typing import Optional

import tornado.web

from web_framework.http.controller import RestController
from web_framework.http.middleware.middleware_handler import handle_middleware
from web_framework.http.response import Response, JsonResponse


def handle_response(self, response) -> None:
    """Handle response from controller."""
    if isinstance(response, JsonResponse):
        self.set_header('Content-Type', 'application/json')

    if isinstance(response, Response):
        self.write(response.body)
        self.set_status(response.status)

        for key, value in response.headers.items():
            self.add_header(key, value)

        for key, value in response.cookie.items():
            self.set_cookie(key, value)


def wrap_request(cls, middlewares, middleware_groups, map_methods: Optional[dict] = None) -> tornado.web.RequestHandler:
    """Adapter between tornado handler and application controller."""
    controller = type('Controller', (tornado.web.RequestHandler,), {})
    setattr(controller, 'get_original_controller', lambda: cls)
    setattr(controller, 'get_map_methods', lambda: map_methods)

    def make_wrap_method(method_name):
        """Return method for http handler."""

        async def wrap_method(self, *args, **kwargs):
            """This method will be call every request."""
            controller_method = getattr(cls(self), method_name)
            handled_request = await handle_middleware(self.request, cls.middleware, middlewares, middleware_groups)
            handle_request = await controller_method(handled_request)
            handle_response(self, handle_request)

        return wrap_method

    methods = ['get', 'post', 'put', 'delete']

    if map_methods:
        for http_method, controller_method in map_methods.items():

            if hasattr(cls, controller_method):
                setattr(controller, http_method, make_wrap_method(controller_method))
    else:
        for method in methods:
            if hasattr(cls, method):
                setattr(controller, method, make_wrap_method(method))

    return controller


class Kernel:
    def make_tornado_routes(self, urls: list, middleware_registry: dict, middleware_group_registry: dict) -> list:
        routes = []
        for path, handler in urls:

            if issubclass(handler, RestController):

                if not path.endswith('/'):
                    path += '/'

                routes.append(
                    (path, wrap_request(handler, middleware_registry, middleware_group_registry, {'get': 'index', 'post': 'store'})))
                routes.append((f'{path}create', wrap_request(handler, middleware_registry, middleware_group_registry, {'get': 'create'})))
                routes.append((f'{path}(.*)/edit', wrap_request(handler, middleware_registry, middleware_group_registry, {'get': 'edit'})))
                routes.append((f'{path}(.*)/', wrap_request(handler, middleware_registry, middleware_group_registry,
                                                            {'get': 'get', 'put': 'update', 'delete': 'delete'})))

            else:
                routes.append((path, wrap_request(handler, middleware_registry, middleware_group_registry)))
        return routes
