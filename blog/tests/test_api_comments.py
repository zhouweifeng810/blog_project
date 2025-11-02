import pytest
from rest_framework import status
from .factories import PostFactory, UserFactory, CommentFactory

@pytest.mark.django_db
def test_comment_delete_by_owner(api_client):
    owner = UserFactory()
    comment = CommentFactory(author=owner)
    api_client.force_authenticate(user=owner)
    res = api_client.delete(f"/api/comments/{comment.id}/")
    assert res.status_code in (204, 200, 202)

@pytest.mark.django_db
def test_comment_delete_by_other_forbidden(api_client):
    owner = UserFactory()
    other = UserFactory()
    comment = CommentFactory(author=owner)
    api_client.force_authenticate(user=other)
    res = api_client.delete(f"/api/comments/{comment.id}/")
    assert res.status_code == status.HTTP_403_FORBIDDEN
