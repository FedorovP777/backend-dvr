from typing import Callable

from web_framework.http.controller import Controller, RestController
from web_framework.http.kernel import Kernel
from web_framework.http.response import JsonResponse


class TestController(Controller):
    middleware = []

    async def get(self, request):
        return JsonResponse({})

    async def post(self, request):
        return JsonResponse({})


class TestRestController(RestController):

    async def index(self, request):
        return JsonResponse({'a': 1})

    #
    async def store(self, request, pk):
        return JsonResponse({'a': 1})

    async def create(self, request):
        return JsonResponse({'a': 1})

    async def edit(self, request, pk):
        return JsonResponse({'a': 1})

    async def update(self, pk):
        return JsonResponse({'a': 1})

    async def destroy(self, pk):
        return JsonResponse({'a': 1})


def test_controller():
    result = Kernel().make_tornado_routes([(r"/test", TestController)], {}, {})
    route, handler = result[0]
    assert isinstance(handler, Callable)
    assert isinstance(route, str)
    assert len(result) == 1


def test_rest_controller():
    result = Kernel().make_tornado_routes([(r"/test/", TestRestController)], {}, {})

    route_paths = [path for (path, _) in result]
    assert len(result) == 4
    assert '/test/' in route_paths
    assert '/test/create' in route_paths
    assert '/test/(.*)/edit' in route_paths
    assert '/test/(.*)/' in route_paths
