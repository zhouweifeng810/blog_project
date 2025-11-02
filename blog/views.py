# blog/views.py
from typing import cast

from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import Post
from .models import Comment
from .serializers import CommentSerializer
from .permissions import IsCommentOwnerOrStaff
from .permissions import IsAuthorOrReadOnly
from .serializers import PostSerializer


class PostPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly & IsAuthorOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["title", "body"]
    ordering_fields = ["created_at", "published_at", "title"]
    ordering = ["-created_at"]
    pagination_class = PostPagination

    def get_queryset(self):
        qs = Post.objects.all().select_related("author")
        request = cast(Request, self.request)
        status_ = request.query_params.get("status")
        if status_:
            qs = qs.filter(status=status_)
        return qs

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def list(self, request, *args, **kwargs):
        request = cast(Request, request)
        query_params = request.query_params
        if any(
            param in query_params
            for param in ("page", "page_size", "search", "ordering")
        ):
            return super().list(request, *args, **kwargs)
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related("post", "author")
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly & IsCommentOwnerOrStaff]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
