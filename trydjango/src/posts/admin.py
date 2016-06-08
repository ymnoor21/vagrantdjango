from django.contrib import admin

# Register your models here.
from .models import Post


class PostModelAdmin(admin.ModelAdmin):
    list_display = ["title", "updated_at", "created_at"]
    list_display_links = ["title"]
    list_filter = ["title", "updated_at"]
    search_fields = ["title", "content"]

    class Meta:
        model = Post

admin.site.register(Post, PostModelAdmin)
