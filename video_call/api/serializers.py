from rest_framework import serializers

from video_call.models import Room, CallerCandidate, CalleeCandidate, Offer, Answer


class CallerCandidateSerializer(serializers.ModelSerializer):

    class Meta:
        model = CallerCandidate
        fields = ['id', 'candidate', 'sdp_m_line_index', 'sdp_mid']


class CalleeCandidateSerializer(serializers.ModelSerializer):

    class Meta:
        model = CalleeCandidate
        fields = ['id', 'candidate', 'sdp_m_line_index', 'sdp_mid']

class OfferSerializer(serializers.ModelSerializer):

    class Meta:
        model = Offer
        fields = ['id', 'sdp', 'type']

class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = ['id', 'sdp', 'type']

class VideoCallRoomSerializer(serializers.ModelSerializer):
    caller_candidates = CallerCandidateSerializer(many=True)
    callee_candidates = CalleeCandidateSerializer(many=True)
    offer = OfferSerializer()
    answer = AnswerSerializer()

    class Meta:
        model = Room
        fields = ['id', 'caller_user', 'callee_user',  'caller_candidates', 'callee_candidates', 'offer', 'answer']