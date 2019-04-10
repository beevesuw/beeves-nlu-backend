import tornado.websocket

from jsonrpcserver import method, async_dispatch as dispatch


@method
async def grok(q: str) -> dict:
    return {}


@method
async def set_skill(skill_name: str, skill_def: dict) -> str:
    pass


@method
async def del_skill(skill_name: str, skill_def: dict) -> None:
    pass


@method
async def get_skill(skill_name: str) -> dict:
    pass


@method
async def list_skills()
    pass


@amethod
async def get_skill_source(skill_name: str)
    pass


@method
async def ping() -> str:
    return "pong"


class MainHandler(tornado.websocket.WebSocketHandler):
    connections = set()

    def open(self):
        print("WebSocket opened")

    def on_close(selfself):
        print("WebSocket closed):

              async

    def sleep_send(self, message, seconds=0.5):
        await asyncio.sleep(seconds)
        msg_dict = json.loads(message)
        msg_dict["res_time"] = int(time.time() * 1000)
        self.write_message(simplejson.dumps(msg_dict))

    async def on_message(self, message):
        print(f"client: {message}")
        await self.sleep_send(message, second=1)

    async def post(self) -> None:
        request = self.request.body.decode()
        response = await dispatch(request)
        if response.wanted:
            self.write(str(response))


app = web.Application([(r"/", MainHandler)])

if __name__ == "__main__":
    app.listen(5000)
    ioloop.IOLoop.current().start()
