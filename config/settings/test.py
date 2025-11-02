# config/settings/test.py
from .base import *  # noqa


# 用内存邮箱、快速密码哈希、最少中间件，尽量快
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]


# 用临时 SQLite（pytest-django 会创建临时 test DB）
DATABASES["default"]["NAME"] = BASE_DIR / "test_db.sqlite3"


# DRF 减少全局开销（可选）
REST_FRAMEWORK = {
    **REST_FRAMEWORK,
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
}
