from django.contrib.auth.models import User
from django.db import models


class Tweet(models.Model):
    # 関連するオブジェクトが削除された場合に、それに関連するすべてのオブジェクトも一緒に削除される
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
