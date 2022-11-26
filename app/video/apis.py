import asyncio
import json

from tornado.web import HTTPError

from app.main.middleware.config import middleware
from app.video.serializers import UserModel, VideoResponseSerializer
from web_framework.http.controller import Controller, RestController
from web_framework.http.response import Response, JsonResponse

from pydantic import BaseModel, ValidationError, validator


class VideoApi(Controller):
    middleware = ['api']

    async def get(self, request):

        try:
            user = UserModel(**request.query)
        except ValidationError as errors:
            return Response(body=errors.json(), status=402)

        data = {'id': 1, 'body': [{'id': 1}]}
        result = VideoResponseSerializer(**data)
        return JsonResponse(result.json())

    async def post(self, request, user_id):

        try:
            user = UserModel(**request.query)
        except ValidationError as errors:
            return Response(body=errors.json(), status=402)
        data = {'id': 1, 'body': [{'id': 1}]}
        result = VideoResponseSerializer(**data)
        return JsonResponse(result.json())


class RestVideoController(RestController):

    async def index(self, request):
        return JsonResponse({'a': 1})

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
