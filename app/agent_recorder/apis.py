import json

from pydantic import ValidationError

from app.agent_recorder.serializers import AgentRecorderEventListSerializer
from app.agent_recorder.services import AgentRecorderEventService

from web_framework.http.controller import Controller
from web_framework.http.response import JsonResponse


class HandleAgentEvent(Controller):
    middleware = ['api']

    async def post(self, request):

        try:
            request = AgentRecorderEventListSerializer(__root__=json.loads(request.body)).copy()
        except ValidationError as e:
            return JsonResponse(e.json(), 422)

        AgentRecorderEventService().handle_event(request.__root__)

        return JsonResponse(request.json())
