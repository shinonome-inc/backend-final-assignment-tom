from django.conf import settings
from django.db import models


class Tweet(models.Model):
    # 関連するオブジェクトが削除された場合に、それに関連するすべてのオブジェクトも一緒に削除される
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
