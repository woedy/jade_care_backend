from django.contrib.auth import get_user_model
from rest_framework import serializers

from appointments.models import Appointment, AppointmentForOther, Payment
from posts.models import Post, PostFile
from user_profile.models import Doctor, PersonalInfo

User = get_user_model()


class ArticlePersonalInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = PersonalInfo
        fields = ['id', 'photo']

class ArticleAuthorSerializer(serializers.ModelSerializer):
    personal_info = ArticlePersonalInfoSerializer()

    class Meta:
        model = User
        fields = ['id', 'last_name', 'first_name', 'personal_info']

class ArticleFileSerializer(serializers.ModelSerializer):


    class Meta:
        model = PostFile
        fields = ['id', 'caption', 'file']







class ListAllArticlesSerializer(serializers.ModelSerializer):
    post_files = ArticleFileSerializer(many=True)
    author = ArticleAuthorSerializer()


    class Meta:
        model = Post
        fields = ['id', 'name', 'body', 'date_published', 'created_at', 'updated_at', 'post_files', 'author']

