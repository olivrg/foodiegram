from __future__ import unicode_literals

from django.contrib import admin

from posts.models import Comment, Post


class PostModelAdmin(admin.ModelAdmin):
    list_display = ["owner", "caption", "number_of_likes", "timestamp"]
    list_display_links = ["owner"]

    search_fields = ["owner", "caption"]

    class Meta:
        model = Post


admin.site.register(Post, PostModelAdmin)

class CommentModelAdmin(admin.ModelAdmin):
    list_display = ["content", "owner", "timestamp"]

    search_fields = ["owner", "content"]

    class Meta:
        model = Comment


admin.site.register(Comment, CommentModelAdmin)
