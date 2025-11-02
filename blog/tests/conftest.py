# tests/conftest.py
import pytest
from freezegun import freeze_time
from django.conf import settings
from rest_framework.test import APIClient


@pytest.fixture(autouse=True, scope="session")
def _fast_settings():
    # 这些在 test.py 里已有，这里只是示例，常用于动态覆盖 settings
    settings.DEBUG = False


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(django_user_model, db):
    return django_user_model.objects.create_user(
        username="alice", email="a@a.com", password="pwd"
    )


@pytest.fixture
def another_user(django_user_model, db):
    return django_user_model.objects.create_user(
        username="bob", email="b@b.com", password="pwd"
    )


# 可复用的冻结时间上下文
@pytest.fixture
def frozen_2025():
    with freeze_time("2025-01-01 00:00:00"):
        yield
