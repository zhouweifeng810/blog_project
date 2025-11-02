# blog/management/commands/publish_scheduled.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from blog.models import Post


class Command(BaseCommand):
    help = "Publish scheduled posts whose scheduled_at <= now"

    def handle(self, *args, **options):
        now = timezone.now()
        qs = Post.objects.filter(status=Post.Status.DRAFT, scheduled_at__lte=now)
        count = 0
        for post in qs:
            post.publish(when=now)
            count += 1
        self.stdout.write(self.style.SUCCESS(f"Published {count} posts"))
