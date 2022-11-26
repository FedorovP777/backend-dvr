import pytest
import tornado
import tornado.web
from tornado.httpclient import HTTPClientError

from app.agent_recorder.urls import urls
from web_framework.http.kernel import Kernel
from app.main.middleware.config import middleware, middleware_group


@pytest.fixture
def app():
    kernel = Kernel()
    return tornado.web.Application(kernel.make_tornado_routes(urls, middleware, middleware_group))


async def test_http_server_client(http_server_client):
    try:
        resp = await http_server_client.fetch('/')
    except HTTPClientError as e:
        assert 404 == e.code
