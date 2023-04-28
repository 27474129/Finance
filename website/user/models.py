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

    @classmethod
    def create_user_profile_comment(
        cls, to_user: int, by_user: int, comment: str
    ):
        UserProfileComment.objects.create(
            to_user=User.objects.get(pk=to_user),
            by_user=User.objects.get(pk=by_user),
            comment=comment
        )

    @classmethod
    def get_user_profile_comments(cls, uid: int):
        return UserProfileComment.objects.filter(to_user_id=uid)

# TODO: Сделать модель, хранящую респекты к профайлам юзера
