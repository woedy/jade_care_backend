from django.contrib import admin

from posts.models import PostFile, Post

admin.site.register(Post)
admin.site.register(PostFile)