from __future__ import annotations

from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    avatar = models.ImageField(upload_to='avatars/%Y/%m/%d/')
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def get_user(cls, uid: int) -> User:
        user = User.objects.filter(id=uid)
        return user[0] if len(user) == 1 else None


class UserProfileComment(models.Model):
    to_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='to_user'
    )
    by_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='by_user'
    )
    comment = models.TextField()
