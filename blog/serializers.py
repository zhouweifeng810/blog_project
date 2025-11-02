# blog/serializers.py
from rest_framework import serializers
from .models import Post, Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id","post", "author", "body", "is_approved", "created_at"]
        read_only_fields = ["id", "created_at", "author"]


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "title",
            "slug",
            "body",
            "status",
            "scheduled_at",
            "published_at",
            "created_at",
            "updated_at",
            "comments",
        ]
        read_only_fields = [
            "id",
            "author",
            "slug",
            "published_at",
            "created_at",
            "updated_at",
        ]
