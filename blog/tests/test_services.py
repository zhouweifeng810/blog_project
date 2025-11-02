import pytest
from django.core.exceptions import ValidationError
from blog.services import create_post
from .factories import UserFactory


@pytest.mark.django_db
def test_create_post_happy_path():
    u = UserFactory()
    p = create_post(author=u, title="My Post", body="...")
    assert p.pk is not None
    assert p.slug.startswith("my-post")


@pytest.mark.django_db
def test_create_post_duplicate_title():
    u = UserFactory()
    create_post(author=u, title="Dup", body="1")
    with pytest.raises(ValidationError):
        create_post(author=u, title="Dup", body="2")
