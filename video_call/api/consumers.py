import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.auth import get_user_model
from django.db.models import Q

from appointments.api.serializers.appointment_detail_serializers import AppointmentDetailSerializer
from appointments.api.serializers.list_appointment_serializers import ListUserAppointmentSerializer
from appointments.models import Appointment
from mysite.exceeptions import ClientError
from mysite.socket_utils import get_user
from video_call.api.serializers import VideoCallRoomSerializer
from video_call.models import Room, CallerCandidate, Offer, CalleeCandidate, Answer

User = get_user_model()


class VideoCallConsumers(AsyncJsonWebsocketConsumer):

    async def connect(self):

        self.user = None
        self.room_id = None
        self.room_group_name = None

        self.data = {}
        self.user_data = None
        self.video_call_room_data = None

        await self.accept()

    async def receive_json(self, content):
        print("VideoCallConsumers: receive_json")
        command = content.get("command", None)
        user_id = content.get("user_id", None)
        other_user_id = content.get("other_user_id", None)
        appointment_id = content.get("appointment_id", None)
        room_id = content.get("room_id", None)
        room_data = content.get("room_data", None)
        room_candidate = content.get("room_candidate", None)
        offer = content.get("offer", None)
        answer = content.get("answer", None)

        try:

            if command == "get_video_call":
                print("CONTENT: Command: " + str(command))
                print("CONTENT: USER ID: " + str(user_id))
                print("CONTENT: OTHER USER ID: " + str(other_user_id))
                print("CONTENT: APPOINTMENT ID: " + str(appointment_id))

                self.user = await get_user(user_id)
                self.room_group_name = 'video_call_%s' % appointment_id

                await self.channel_layer.group_add(
                    self.room_group_name,
                    self.channel_name
                )

                await self.get_video_call_room_data(user_id, other_user_id)

                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'video_call_room_data_message',
                        'video_call_room_data_message': self.video_call_room_data
                    }
                )

            if command == "create_room":
                print("CONTENT: Command: " + str(command))
                print("CONTENT: USER ID: " + str(user_id))
                print("CONTENT: ROOM DATA: " + str(room_data))

                self.user = await get_user(user_id)
                self.room_group_name = 'video_call_%s' % appointment_id

                await self.channel_layer.group_add(
                    self.room_group_name,
                    self.channel_name
                )

                await self.create_video_call_room(user_id)

                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'video_call_room_data_message',
                        'video_call_room_data_message': self.video_call_room_data
                    }
                )

            if command == "set_room_callee_candidate":
                print("CONTENT: Command: " + str(command))
                print("CONTENT: USER ID: " + str(user_id))
                print("CONTENT: CANDIDATE DATA: " + str(room_candidate))

                self.user = await get_user(user_id)
                self.room_group_name = 'video_call_%s' % appointment_id

                await self.channel_layer.group_add(
                    self.room_group_name,
                    self.channel_name
                )

                await self.set_room_callee_candidate(user_id, self.room_id, room_candidate)

                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'video_call_room_data_message',
                        'video_call_room_data_message': self.video_call_room_data
                    }
                )

            if command == "set_room_caller_candidate":
                print("CONTENT: Command: " + str(command))
                print("CONTENT: USER ID: " + str(user_id))
                print("CONTENT: CANDIDATE DATA: " + str(room_candidate))

                self.user = await get_user(user_id)
                self.room_group_name = 'video_call_%s' % appointment_id

                await self.channel_layer.group_add(
                    self.room_group_name,
                    self.channel_name
                )

                await self.set_room_caller_candidate(user_id, self.room_id, room_candidate)

                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'video_call_room_data_message',
                        'video_call_room_data_message': self.video_call_room_data
                    }
                )

            if command == "set_offer":
                print("CONTENT: Command: " + str(command))
                print("CONTENT: USER ID: " + str(user_id))
                # print("CONTENT: OFFER DATA: " + str(offer))

                self.user = await get_user(user_id)
                self.room_group_name = 'video_call_%s' % appointment_id

                await self.channel_layer.group_add(
                    self.room_group_name,
                    self.channel_name
                )

                await self.set_offer(user_id, self.room_id, offer)

                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'video_call_room_data_message',
                        'video_call_room_data_message': self.video_call_room_data
                    }
                )

            if command == "set_answer":
                print("CONTENT: Command: " + str(command))
                print("CONTENT: USER ID: " + str(user_id))
                # print("CONTENT: OFFER DATA: " + str(offer))

                self.user = await get_user(user_id)
                self.room_group_name = 'video_call_%s' % appointment_id

                await self.channel_layer.group_add(
                    self.room_group_name,
                    self.channel_name
                )

                await self.set_answer(user_id, self.room_id, answer)

                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'video_call_room_data_message',
                        'video_call_room_data_message': self.video_call_room_data
                    }
                )

            if command == "hangup":
                print("CONTENT: Command: " + str(command))
                print("CONTENT: USER ID: " + str(user_id))
                # print("CONTENT: OFFER DATA: " + str(offer))

                self.user = await get_user(user_id)
                self.room_group_name = 'video_call_%s' % appointment_id

                await self.channel_layer.group_add(
                    self.room_group_name,
                    self.channel_name
                )

                await self.hangup(user_id, self.room_id)

                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'video_call_room_data_message',
                        'video_call_room_data_message': self.video_call_room_data
                    }
                )


        except ClientError as e:
            await self.handle_client_error(e)

    ####################
    #### SEND VIDEO CALL ROOM DATA
    ####################

    async def video_call_room_data_message(self, event):
        video_call_room_data_message = event['video_call_room_data_message']
        # Send message to WebSocket
        await self.send_json({
            "video_call_room_data_message": video_call_room_data_message
        })

    async def get_video_call_room_data(self, user_id, other_user_id):

        print("VIDEO CALL: get_video_call_room_data")
        # is_auth = is_authenticated(self.user)
        try:
            video_call_data = await get_video_call_room_data_or_error(user_id, other_user_id)
            self.video_call_room_data = json.loads(video_call_data)
            self.room_id = json.loads(video_call_data)
        except ClientError as e:
            await self.handle_client_error(e)

    async def create_video_call_room(self, user_id):

        print("VIDEO CALL: create_video_call_room")
        # is_auth = is_authenticated(self.user)
        try:
            video_call_data = await create_video_call_room_or_error(user_id)
            self.video_call_room_data = json.loads(video_call_data)
            self.room_id = json.loads(video_call_data)
        except ClientError as e:
            await self.handle_client_error(e)

    async def set_room_caller_candidate(self, user_id, room_id, room_candidate):

        print("VIDEO CALL: set_room_candidate")
        # is_auth = is_authenticated(self.user)
        try:
            video_call_data = await set_room_caller_candidate_or_error(user_id, room_id, room_candidate)
            self.video_call_room_data = json.loads(video_call_data)
        except ClientError as e:
            await self.handle_client_error(e)

    async def set_room_callee_candidate(self, user_id, room_id, room_candidate):

        print("VIDEO CALL: set_room_callee_candidate")
        # is_auth = is_authenticated(self.user)
        try:
            video_call_data = await set_room_callee_candidate_or_error(user_id, room_id, room_candidate)
            self.video_call_room_data = json.loads(video_call_data)
        except ClientError as e:
            await self.handle_client_error(e)

    async def set_offer(self, user_id, room_id, offer):

        print("VIDEO CALL: set_offer")
        # is_auth = is_authenticated(self.user)
        try:
            video_call_data = await set_offer_or_error(user_id, room_id, offer)
            self.video_call_room_data = json.loads(video_call_data)
        except ClientError as e:
            await self.handle_client_error(e)

    async def set_answer(self, user_id, room_id, answer):

        print("VIDEO CALL: set_offer")
        # is_auth = is_authenticated(self.user)
        try:
            video_call_data = await set_answer_or_error(user_id, room_id, answer)
            self.video_call_room_data = json.loads(video_call_data)
        except ClientError as e:
            await self.handle_client_error(e)

    async def hangup(self, user_id, room_id):

        print("VIDEO CALL: hangup")
        # is_auth = is_authenticated(self.user)
        try:
            video_call_data = await hangup_or_error(user_id, room_id)
            self.video_call_room_data = json.loads(video_call_data)
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
def create_video_call_room_or_error(user_id):
    user = User.objects.get(id=user_id)

    try:
        video_call_data = Room.objects.create(user=user)
        serializers = VideoCallRoomSerializer(video_call_data, many=False)
        if serializers:
            data = serializers.data
            print(json.dumps(data))
            return json.dumps(data)
    except Room.DoesNotExist:
        raise ClientError("OBJECT_INVALID", "Invalid object.")


@database_sync_to_async
def get_video_call_room_data_or_error(user_id, other_user_id):
    user = User.objects.get(id=user_id)
    other_user = User.objects.get(id=other_user_id)
    print(user)
    print(other_user)

    caller_user_room = Room.objects.filter(caller_user=user).first()
    callee_user_room = Room.objects.filter(callee_user=user).first()

    if caller_user_room is not None or callee_user_room is not None:
        print("Room Available")

        # caller_user_room = Room.objects.filter(caller_user=user).first()
        room = Room.objects.filter(Q(caller_user=user) | Q(callee_user=user)).first()
        print(room)

        serializers = VideoCallRoomSerializer(room, many=False)
        if serializers:
            data = serializers.data
            print(json.dumps(data))
            return json.dumps(data)
    elif caller_user_room is None and callee_user_room is None:
        print("No Room")
        video_call_data = Room.objects.create(caller_user=user, callee_user=other_user)

        serializers = VideoCallRoomSerializer(video_call_data, many=False)
        if serializers:
            data = serializers.data
            print(json.dumps(data))
            return json.dumps(data)


@database_sync_to_async
def set_room_caller_candidate_or_error(user_id, room_id, room_candidate):
    candidate = room_candidate['candidate']
    sdp_mid = room_candidate['sdpMid']
    sdp_m_line_index = room_candidate['sdpMlineIndex']

    print(candidate)
    print(sdp_mid)
    print(sdp_m_line_index)

    print("THY ROOOOMMMM IIIIDDDD")
    print(room_id['id'])

    video_call_data = Room.objects.get(id=room_id['id'])

    caller_candidate = CallerCandidate.objects.create(
        room=video_call_data,
        candidate=candidate,
        sdp_mid=sdp_mid,
        sdp_m_line_index=sdp_m_line_index
    )
    caller_candidate.save()

    serializers = VideoCallRoomSerializer(video_call_data, many=False)
    if serializers:
        data = serializers.data
        print(json.dumps(data))
        return json.dumps(data)


@database_sync_to_async
def set_room_callee_candidate_or_error(user_id, room_id, room_candidate):
    candidate = room_candidate['candidate']
    sdp_mid = room_candidate['sdpMid']
    sdp_m_line_index = room_candidate['sdpMlineIndex']

    print(candidate)
    print(sdp_mid)
    print(sdp_m_line_index)

    print("THY ROOOOMMMM IIIIDDDD")
    print(room_id['id'])

    video_call_data = Room.objects.get(id=room_id['id'])

    callee_candidate = CalleeCandidate.objects.create(
        room=video_call_data,
        candidate=candidate,
        sdp_mid=sdp_mid,
        sdp_m_line_index=sdp_m_line_index
    )
    callee_candidate.save()

    serializers = VideoCallRoomSerializer(video_call_data, many=False)
    if serializers:
        data = serializers.data
        print(json.dumps(data))
        return json.dumps(data)





@database_sync_to_async
def set_offer_or_error(user_id, room_id, offer):
    sdp = offer['sdp']
    type = offer['type']

    print(sdp)
    print(type)

    print("THY ROOOOMMMM IIIIDDDD")
    print(room_id['id'])

    video_call_data = Room.objects.get(id=room_id['id'])

    offer = Offer.objects.all().filter(room=video_call_data)
    print("Offeeerrrrrr")
    print(offer)

    if offer.exists():
        print("YESSS OFFEEERRR")
        serializers = VideoCallRoomSerializer(video_call_data, many=False)
        if serializers:
            data = serializers.data
            print(json.dumps(data))
            return json.dumps(data)
    else:
        print("NOOOO OFFEEERR")

        new_offer = Offer.objects.create(
            room=video_call_data,
            sdp=sdp,
            type=type,
        )
        new_offer.save()

        video_call_data = Room.objects.get(id=room_id['id'])
        serializers = VideoCallRoomSerializer(video_call_data, many=False)
        if serializers:
            data = serializers.data
            print(json.dumps(data))
            return json.dumps(data)



@database_sync_to_async
def set_answer_or_error(user_id, room_id, answer):
    sdp = answer['sdp']
    type = answer['type']

    print(sdp)
    print(type)

    print("THY ROOOOMMMM IIIIDDDD")
    print(room_id['id'])

    video_call_data = Room.objects.get(id=room_id['id'])

    answer = Answer.objects.all().filter(room=video_call_data)
    print("Answerrrrr")
    print(answer)

    if answer.exists():
        print("YESSS ANSWEERRRRR")
        serializers = VideoCallRoomSerializer(video_call_data, many=False)
        if serializers:
            data = serializers.data
            print(json.dumps(data))
            return json.dumps(data)
    else:
        print("NOOOO ANSSWERRRR")

        new_answer = Answer.objects.create(
            room=video_call_data,
            sdp=sdp,
            type=type,
        )
        new_answer.save()

        video_call_data = Room.objects.get(id=room_id['id'])
        serializers = VideoCallRoomSerializer(video_call_data, many=False)
        if serializers:
            data = serializers.data
            print(json.dumps(data))
            return json.dumps(data)





@database_sync_to_async
def hangup_or_error(user_id, room_id):
    print("THY ROOOOMMMM IIIIDDDD")
    print(room_id['id'])

    try:
        video_call_data = Room.objects.get(id=room_id['id'])
        video_call_data.delete()

        serializers = VideoCallRoomSerializer(video_call_data, many=False)
        if serializers:
            data = serializers.data
            print(json.dumps(data))
            return json.dumps(data)
    except Room.DoesNotExist:
        raise ClientError("OBJECT_INVALID", "Invalid object.")
