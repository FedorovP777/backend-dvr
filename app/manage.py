import asyncio
from app.video.urls import urls as video_urls
from app.agent_recorder.urls import urls as agent_recorder_urls
from app.main.middleware.config import middleware, middleware_group
from web_framework.application import Application

urls = []
urls += video_urls
urls += agent_recorder_urls

app = Application(middleware, middleware_group, urls)
app.cli_process()
asyncio.run(app.start())
