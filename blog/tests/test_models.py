import pytest
from django.db import IntegrityError
from blog.models import Post
from .factories import PostFactory, UserFactory


@pytest.mark.django_db
def test_word_count():
    post = PostFactory(body="hello world python pytest")
    assert post.word_count == 4


@pytest.mark.django_db
def test_unique_title_per_author():
    author = UserFactory()
    PostFactory(author=author, title="Same Title")
    with pytest.raises(IntegrityError):
        PostFactory(author=author, title="Same Title")
