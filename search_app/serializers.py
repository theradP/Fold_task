from rest_framework import serializers
from .models import Projects, Users, Hashtags
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from .documents import ProjectDocument


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ("id", "name", )


class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtags
        fields = ("name", )


class ProjectSerializer(serializers.ModelSerializer):
    users = UserSerializer(source='user_set', many=True)
    hashtags = HashtagSerializer(source='hashtag_set', many=True)

    class Meta:
        model = Projects
        fields = ("id", "name", "slug", "description", "created_at", "hashtags", "users")


class ProjectDocumentSerializer(DocumentSerializer):
    users = UserSerializer(many=True)
    hashtags = HashtagSerializer(many=True)

    class Meta:
        document = ProjectDocument
        fields = (
            'id',
            'name',
            'slug',
            'description',
            'created_at',
            'hashtags',
            'users',
        )

