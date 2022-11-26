from unittest.mock import Mock

from web_framework.http.response import JsonResponse


def test_response_json():
    body = Mock()
    json_response = JsonResponse(body, 200)
    assert json_response.body == body
    assert json_response.status == 200
    assert json_response.cookie == {}
    assert json_response.headers == {}
