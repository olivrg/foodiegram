from __future__ import unicode_literals

from django.contrib import admin

from posts.models import Comment, Post, Report


class PostModelAdmin(admin.ModelAdmin):
    list_display = ["owner", "caption", "number_of_likes", "timestamp"]
    list_display_links = ["owner"]

    search_fields = ["owner", "caption"]

    class Meta:
        model = Post


admin.site.register(Post, PostModelAdmin)

class ReportModelAdmin(admin.ModelAdmin):
    list_display = ["message", "user", "timestamp"]

    search_fields = ["user", "message"]

    class Meta:
        model = Report


admin.site.register(Report, ReportModelAdmin)
