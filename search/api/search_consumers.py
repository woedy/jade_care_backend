import json
from itertools import chain

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.auth import get_user_model

from appointments.api.serializers.list_appointment_serializers import ListUserAppointmentSerializer
from appointments.models import Appointment
from mysite.exceeptions import ClientError
from mysite.socket_utils import get_user, is_authenticated

User = get_user_model()


class SearchConsumers(AsyncJsonWebsocketConsumer):

    async def connect(self):

        self.user = None
        self.room_id = None
        self.room_group_name = None
        self.search_results = None

        self.data = {}

        await self.accept()


    async def receive_json(self, content):
        print("SearchConsumers: receive_json")
        command = content.get("command", None)
        user_id = content.get("user_id", None)
        query = content.get("query", None)

        try:
            ####################
            #### SEARCH
            ####################
            if command == "search_database":
                print("CONTENT: Command: " + str(command))
                print("CONTENT: User ID: " + str(user_id))
                print("CONTENT: Query: " + str(query))



                self.user = await get_user(user_id)
                self.room_group_name = 'search_database_%s' % user_id

                await self.channel_layer.group_add(
                    self.room_group_name,
                    self.channel_name
                )

                await self.get_all_user_search(self.user, query)

                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'search_message',
                        'search_message': self.search_results
                    }
                )

        except ClientError as e:
            await self.handle_client_error(e)

    ####################
    #### SEND SEARCH MESSAGE
    ####################
    async def search_message(self, event):
        search_message = event['search_message']

        # Send message to WebSocket
        await self.send_json({
            "search_message": search_message
        })


    async def handle_client_error(self, e):
        errorData = {}
        errorData['error'] = e.code
        if e.message:
            errorData['message'] = e.message
            await self.send_json(errorData)
        return

    ####################
    #### SEARCH
    ####################
    async def get_all_user_search(self, user, query):

        print("SEARCH DATABASE: get_all_user_search")
        #is_auth = is_authenticated(self.user)
        try:
            searches = await get_all_user_search_or_error(user, query)
            self.search_results = json.loads(searches)
        except ClientError as e:
            await self.handle_client_error(e)


############################################################
######## DATABASE
############################################################

####################
##### SEARCH CABINET DATABASE
####################
@database_sync_to_async
def get_all_user_search_or_error(user, query):


    print(query)

    if query != "" and query != " ":
        appointments = Appointment.objects.search(query)

        appointment_serializer = ListUserAppointmentSerializer(appointments, many=True)

        q_chain = chain(appointment_serializer.data)
        new_l = list(q_chain)

        new_l.sort(key=lambda x: x['id'], reverse=False)

        data = new_l
        print(json.dumps(data))
        return json.dumps(data)





