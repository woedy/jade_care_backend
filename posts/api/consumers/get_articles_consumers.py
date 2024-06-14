import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from appointments.api.serializers.serializers import ListUserAppointmentSerializer, AppointmentForOtherSerializer
from appointments.models import Appointment
from mysite.exceeptions import ClientError
from mysite.socket_utils import get_user
from posts.api.serializers.serializers import ListAllArticlesSerializer
from posts.models import Post


class GetAllArticlesConsumers(AsyncJsonWebsocketConsumer):

    async def connect(self):

        self.user = None
        self.room_id = None
        self.room_group_name = None

        self.data = {}
        self.user_data = None
        self.all_articles = None


        await self.accept()

    async def receive_json(self, content):
        print("GetAllArticlesConsumers: receive_json")
        command = content.get("command", None)
        user_id = content.get("user_id", None)
        data = content.get("data", None)

        try:
            if command == "get_all_articles":
                print("CONTENT: Command: " + str(command))
                print("CONTENT: Data: " + str(data))
                print("CONTENT: USER ID: " + str(user_id))

                self.user = await get_user(user_id)
                self.room_group_name = 'get_all_articles_%s' % user_id

                await self.channel_layer.group_add(
                    self.room_group_name,
                    self.channel_name
                )

                await self.get_all_articles(user_id, data)

                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'get_all_articles_message',
                        'get_all_articles_message': self.all_articles
                    }
                )




        except ClientError as e:
            await self.handle_client_error(e)

    ####################
    #### SEND ARTICLES MESSAGE
    ####################

    async def get_all_articles_message(self, event):
        get_all_articles_message = event['get_all_articles_message']
        # Send message to WebSocket
        await self.send_json({
            "get_all_articles_message": get_all_articles_message
        })

    async def get_all_articles(self, user_id, data):

        print(" PROJECT DETAIL: get_all_articles")
        #is_auth = is_authenticated(self.user)
        try:
            articles = await get_all_articles_or_error(user_id, data)
            self.all_articles = json.loads(articles)
        except ClientError as e:
            await self.handle_client_error(e)

    async def handle_client_error(self, e):
        errorData = {}
        errorData['error'] = e.code
        if e.message:
            errorData['message'] = e.message
            await self.send_json(errorData)
        return


@database_sync_to_async
def get_all_articles_or_error(user_id, data):

    try:
        articles = Post.objects.all().order_by('-id')
        serializers = ListAllArticlesSerializer(articles, many=True)

        if serializers:
            data = serializers.data
            print(json.dumps(data))
            return json.dumps(data)
    except Post.DoesNotExist:
        raise ClientError("OBJECT_INVALID", "Invalid object.")

