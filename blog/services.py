# blog/services.py
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from .models import Post


def create_post(*, author, title: str, body: str) -> Post:
    title = title.strip()
    if not title:
        raise ValidationError("title required")
    if Post.objects.filter(author=author, title=title).exists():
        raise ValidationError("duplicated title for this author")
    slug = slugify(title) or "post"
    return Post.objects.create(author=author, title=title, slug=slug, body=body)
