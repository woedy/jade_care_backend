import base64
import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.utils import timezone

from appointments.api.serializers.serializers import ListUserAppointmentSerializer, AppointmentForOtherSerializer
from appointments.models import Appointment
from mysite.exceeptions import ClientError
from mysite.socket_utils import get_user
from posts.api.serializers.serializers import ListAllArticlesSerializer
from posts.models import Post, PostFile


User = get_user_model()


class AddArticleConsumers(AsyncJsonWebsocketConsumer):

    async def connect(self):

        self.user = None
        self.room_id = None
        self.room_group_name = None

        self.data = {}
        self.user_data = None
        self.all_articles = None


        await self.accept()

    async def receive_json(self, content):
        print("AddArticleConsumers: receive_json")
        command = content.get("command", None)
        user_id = content.get("user_id", None)
        data = content.get("data", None)

        try:
            if command == "add_article":
                print("CONTENT: Command: " + str(command))
               # print("CONTENT: Data: " + str(data))
                print("CONTENT: USER ID: " + str(user_id))

                self.user = await get_user(user_id)
                self.room_group_name = 'add_article_%s' % user_id

                await self.channel_layer.group_add(
                    self.room_group_name,
                    self.channel_name
                )

                await self.add_article(user_id, data)

                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'add_article_message',
                        'add_article_message': self.all_articles
                    }
                )




        except ClientError as e:
            await self.handle_client_error(e)

    ####################
    #### SEND ARTICLES MESSAGE
    ####################

    async def add_article_message(self, event):
        add_article_message = event['add_article_message']
        # Send message to WebSocket
        await self.send_json({
            "add_article_message": add_article_message
        })

    async def add_article(self, user_id, data):

        print(" PROJECT DETAIL: add_article")
        #is_auth = is_authenticated(self.user)
        try:
            articles = await add_article_or_error(user_id, data)
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
def add_article_or_error(user_id, data):

    title = data["name"]
    body = data["body"]
    post_images = data["post_files"]

    print(title)
    print(body)
    #print(post_images)

    try:
        user = User.objects.get(id=user_id)

        new_article = Post.objects.create(
            name=title,
            body=body,
            author=user
        )
        new_article.save()

        for image in post_images:
            new_img = PostFile.objects.create(
                post=new_article,
                file=base64_file(image['file']),
            )
            new_img.save()

        articles = Post.objects.all().order_by('-id')
        serializers = ListAllArticlesSerializer(articles, many=True)

        if serializers:
            data = serializers.data
            print(json.dumps(data))
            return json.dumps(data)
    except Post.DoesNotExist:
        raise ClientError("OBJECT_INVALID", "Invalid object.")




def base64_file(data, name="File_name", ext=".jpg"):
    print("############## DAAATAAAAAA")
    file = ContentFile(base64.b64decode(data), name=name+ext)
    return file

