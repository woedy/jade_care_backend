import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from mysite.exceeptions import ClientError


class LoginConsumers(AsyncJsonWebsocketConsumer):

    async def connect(self):

        self.user = None
        self.room_id = None
        self.room_group_name = None

        self.data = {}
        self.user_data = None


        await self.accept()

    async def receive_json(self, content):
        print("LoginConsumers: receive_json")
        command = content.get("command", None)
        data = content.get("data", None)

        try:
            if command == "login_user":
                print("CONTENT: Command: " + str(command))
                print("CONTENT: Data: " + str(data))

        except ClientError as e:
            await self.handle_client_error(e)

    async def handle_client_error(self, e):
        errorData = {}
        errorData['error'] = e.code
        if e.message:
            errorData['message'] = e.message
            await self.send_json(errorData)
        return