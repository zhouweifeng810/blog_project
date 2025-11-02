import pytest
from django.core.management import call_command
from freezegun import freeze_time
from blog.models import Post
from .factories import PostFactory


@pytest.mark.django_db
def test_publish_scheduled():
    PostFactory(status=Post.Status.DRAFT, scheduled_at="2025-01-01 00:00:00")
    with freeze_time("2025-01-02 00:00:00"):
        call_command("publish_scheduled")
        assert Post.objects.filter(status=Post.Status.PUBLISHED).count() == 1
