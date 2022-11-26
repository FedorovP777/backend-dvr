import asyncio

from web_framework.http.middleware.middleware_handler import handle_middleware


def get_test_middleware():
    class TestIncrementMiddleware:
        async def handle(self, request, next):
            request['a'] = request['a'] + 1
            next(request)

    return TestIncrementMiddleware


def test_handle_middleware_by_alias(monkeypatch):
    request = {'a': 0}
    middlewares = ['inc_middleware1', 'inc_middleware2']
    loop = asyncio.new_event_loop()
    middleware_group = {}
    middleware_aliases = {
        'inc_middleware1': get_test_middleware(),
        'inc_middleware2': get_test_middleware()
    }
    result = loop.run_until_complete(handle_middleware(request, middlewares, middleware_aliases, middleware_group))
    assert result == {'a': 2}


def test_handle_middleware_group():
    request = {'a': 0}
    middlewares = ['group1']
    loop = asyncio.new_event_loop()
    middleware_aliases = {}
    middleware_group = {'group1': [
        get_test_middleware(),
        get_test_middleware()
    ]
    }
    result = loop.run_until_complete(handle_middleware(request, middlewares, middleware_aliases, middleware_group))
    assert result == {'a': 2}


def test_handle_middleware_combine():
    request = {'a': 0}
    middlewares = ['group1', 'inc_middleware1']
    loop = asyncio.new_event_loop()
    middleware_aliases = {
        'inc_middleware1': get_test_middleware()
    }
    middleware_group = {'group1': [
        get_test_middleware(),
    ]
    }
    result = loop.run_until_complete(handle_middleware(request, middlewares, middleware_aliases, middleware_group))
    assert result == {'a': 2}
