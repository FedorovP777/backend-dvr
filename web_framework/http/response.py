class Response:
    def __init__(self, body: any, status: int = 200, cookie=None, headers=None):
        if cookie is None:
            cookie = {}
        if headers is None:
            headers = {}
        self.body = body
        self.status = status
        self.cookie = cookie
        self.headers = headers


class JsonResponse(Response):
    pass
