import factory
from factory.declarations import (
    LazyAttribute,
    PostGenerationMethodCall,
    Sequence,
    SubFactory,
)
from factory.faker import Faker as FactoryFaker
from django.contrib.auth import get_user_model
from faker import Faker
from blog.models import Post, Comment


fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = Sequence(lambda n: f"user{n}")
    email = LazyAttribute(lambda o: f"{o.username}@ex.com")
    password = PostGenerationMethodCall("set_password", "pwd")


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    author = SubFactory(UserFactory)
    title = FactoryFaker("sentence", nb_words=4)
    slug = FactoryFaker("slug")
    body = FactoryFaker("paragraph")


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    post = SubFactory(PostFactory)
    author = SubFactory(UserFactory)
    body = FactoryFaker("sentence")
