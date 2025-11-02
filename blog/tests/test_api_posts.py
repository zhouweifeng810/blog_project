import pytest
from rest_framework import status
from .factories import PostFactory, UserFactory


@pytest.mark.django_db
def test_list_posts(api_client):
    PostFactory.create_batch(3)
    res = api_client.get("/api/posts/")
    assert res.status_code == status.HTTP_200_OK
    assert len(res.json()) == 3


@pytest.mark.django_db
def test_create_post_requires_auth(api_client):
    res = api_client.post("/api/posts/", {"title": "X", "body": "Y"}, format="json")
    assert res.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_author_can_create_and_edit(api_client):
    user = UserFactory()
    api_client.force_authenticate(user=user)
    res = api_client.post("/api/posts/", {"title": "Z", "body": "Y"}, format="json")
    assert res.status_code == 201
    pid = res.json()["id"]
    res2 = api_client.patch(f"/api/posts/{pid}/", {"body": "updated"}, format="json")
    assert res2.status_code == 200


@pytest.mark.django_db
def test_non_author_cannot_edit(api_client):
    author = UserFactory()
    post_res = None
    # 作者创建
    client1 = api_client
    client1.force_authenticate(user=author)
    post_res = client1.post("/api/posts/", {"title": "K", "body": "B"}, format="json")
    pid = post_res.json()["id"]

    # 其他人试图修改
    other = UserFactory()
    api_client.force_authenticate(user=other)
    res = api_client.patch(f"/api/posts/{pid}/", {"body": "hack"}, format="json")
    assert res.status_code in (403, 404)
