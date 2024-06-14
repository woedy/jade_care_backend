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


class EditArticleConsumers(AsyncJsonWebsocketConsumer):

    async def connect(self):

        self.user = None
        self.room_id = None
        self.room_group_name = None

        self.data = {}
        self.user_data = None
        self.all_articles = None
        self.article = None


        await self.accept()

    async def receive_json(self, content):
        print("EditArticleConsumers: receive_json")
        command = content.get("command", None)
        user_id = content.get("user_id", None)
        data = content.get("data", None)
        article_id = content.get("article_id", None)
        file_id = content.get("file_id", None)

        try:
            if command == "get_article_data":
                print("CONTENT: Command: " + str(command))
               # print("CONTENT: Data: " + str(data))
                print("CONTENT: USER ID: " + str(user_id))
                print("CONTENT: ARYTTICLE: " + str(article_id))

                self.user = await get_user(user_id)
                self.room_group_name = 'edit_article_%s' % user_id

                await self.channel_layer.group_add(
                    self.room_group_name,
                    self.channel_name
                )

                await self.get_article_data(user_id, data, article_id)

                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'get_article_data_message',
                        'get_article_data_message': self.article
                    }
                )

            if command == "edit_article":
                print("CONTENT: Command: " + str(command))
               # print("CONTENT: Data: " + str(data))
                print("CONTENT: USER ID: " + str(user_id))
                print("CONTENT: ARYTTICLE: " + str(article_id))

                self.user = await get_user(user_id)
                self.room_group_name = 'edit_article_%s' % user_id

                await self.channel_layer.group_add(
                    self.room_group_name,
                    self.channel_name
                )

                await self.edit_article(user_id, data, article_id)

                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'get_article_data_message',
                        'get_article_data_message': self.article
                    }
                )

            if command == "delete_file":
                print("CONTENT: Command: " + str(command))
               # print("CONTENT: Data: " + str(data))
                print("CONTENT: USER ID: " + str(user_id))
                print("CONTENT: FileID: " + str(file_id))

                self.user = await get_user(user_id)
                self.room_group_name = 'edit_article_%s' % user_id

                await self.channel_layer.group_add(
                    self.room_group_name,
                    self.channel_name
                )

                await self.delete_file(user_id, article_id, file_id)

                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'get_article_data_message',
                        'get_article_data_message': self.article
                    }
                )


        except ClientError as e:
            await self.handle_client_error(e)

    ####################
    #### SEND ARTICLES MESSAGE
    ####################





    async def get_article_data_message(self, event):
        get_article_data_message = event['get_article_data_message']
        # Send message to WebSocket
        await self.send_json({
            "get_article_data_message": get_article_data_message,
        })

    async def get_article_data(self, user_id, data, article_id):

        print(" ARITICLE : get_article_data")
        #is_auth = is_authenticated(self.user)
        try:
            article = await get_article_data_or_error(user_id, data, article_id)
            self.article = json.loads(article)
        except ClientError as e:
            await self.handle_client_error(e)


    async def edit_article(self, user_id, data, article_id):

        print(" ARITICLE : edit_article")
        #is_auth = is_authenticated(self.user)
        try:
            article = await edit_article_or_error(user_id, data, article_id)
            self.article = json.loads(article)
        except ClientError as e:
            await self.handle_client_error(e)

    async def delete_file(self, user_id, article_id, file_id):

        print(" ARITICLE : delete_file")
        #is_auth = is_authenticated(self.user)
        try:
            article = await delete_file_or_error(user_id, article_id, file_id)
            self.article = json.loads(article)
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
def get_article_data_or_error(user_id, data, article_id):
    try:

        article = Post.objects.get(id=article_id)
        serializers = ListAllArticlesSerializer(article, many=False)

        if serializers:
            data = serializers.data

            final_data = {}
            final_data['article_data'] = data
            final_data['success_message'] = "Got Data"

            print(json.dumps(final_data))
            return json.dumps(final_data)
    except Post.DoesNotExist:
        raise ClientError("OBJECT_INVALID", "Invalid object.")


@database_sync_to_async
def edit_article_or_error(user_id, data, article_id):

    title = data["name"]
    body = data["body"]
    post_images = data["post_files"]

    print(title)
    #print(body)
    #print(post_images)

    try:

        article = Post.objects.get(id=article_id)
        print(article)

        if title != None:
            article.name = title
            article.save()

        if body != None:
            article.body = body
            article.save()

        for image in post_images:
            new_img = PostFile.objects.create(
                post=article,
                file=base64_file(image['file']),
            )
            new_img.save()

        article = Post.objects.get(id=article_id)
        serializers = ListAllArticlesSerializer(article, many=False)

        if serializers:
            data = serializers.data

            final_data = {}
            final_data['article_data'] = data
            final_data['success_message'] = "Edit Successful"

            print(json.dumps(final_data))
            return json.dumps(final_data)
    except Post.DoesNotExist:
        raise ClientError("OBJECT_INVALID", "Invalid object.")



@database_sync_to_async
def delete_file_or_error(user_id, article_id, file_id):
    try:
        post_file = PostFile.objects.get(id=file_id)
        post_file.delete()

        article = Post.objects.get(id=article_id)
        serializers = ListAllArticlesSerializer(article, many=False)

        if serializers:
            data = serializers.data

            final_data = {}
            final_data['article_data'] = data
            final_data['success_message'] = "Delete Successful"

            print(json.dumps(final_data))
            return json.dumps(final_data)

    except PostFile.DoesNotExist:
        raise ClientError("OBJECT_INVALID", "Invalid object.")




def base64_file(data, name="File_name", ext=".jpg"):
    print("############## DAAATAAAAAA")
    file = ContentFile(base64.b64decode(data), name=name+ext)
    return file

