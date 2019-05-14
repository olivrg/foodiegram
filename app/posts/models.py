from django.db import models

from config import helper
from users.models import User


class Post(models.Model):
    random_post_id = models.CharField(
        'Random Post Id',
        editable=False,
        max_length=32,
        default=helper.random_id,
        unique=True,
        primary_key=True
    )
    image = models.ImageField(upload_to='images', blank=False)
    caption = models.CharField(
        max_length=255, blank=True, null=True, editable=True)
    likes = models.ManyToManyField(
        User, related_name="likers", blank=True, symmetrical=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-timestamp']

    def number_of_likes(self):
        if self.likes.count():
            return self.likes.count()
        else:
            return 0

    def __str__(self):
        return f'{self.owner}\'s post'
