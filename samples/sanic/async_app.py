# ------------------------------------------------
# instead of slack_bolt in requirements.txt
import sys

sys.path.insert(1, "../..")
# ------------------------------------------------

from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.sanic import AsyncSlackRequestHandler

app = AsyncApp()
app_handler = AsyncSlackRequestHandler(app)


@app.event("app_mention")
async def handle_app_mentions(payload, say, logger):
    logger.info(payload)
    await say("What's up?")


from sanic import Sanic
from sanic.request import Request

api = Sanic()


@api.post("/slack/events")
async def endpoint(req: Request):
    return await app_handler.handle(req)


# pip install -r requirements.txt
# export SLACK_SIGNING_SECRET=***
# export SLACK_BOT_TOKEN=xoxb-***
# uvicorn async_app:api --reload --port 3000 --log-level debug
