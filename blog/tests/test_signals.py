import pytest
from blog.models import Post
from .factories import UserFactory


@pytest.mark.django_db
def test_slug_auto_generated():
    u = UserFactory()
    p = Post.objects.create(author=u, title="Hello Pytest", body="...")
    assert p.slug.startswith("hello-pytest")
