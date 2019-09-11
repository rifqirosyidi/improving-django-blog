from django.contrib import admin
from .models import Post


# Customize admin site
class PostModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'content', 'updated', 'timestamp']
    # if you use list_editable make sure to add list_display_link to reference other than title
    list_editable = ['title']
    list_display_links = ['content']
    list_filter = ['updated', 'timestamp']
    search_fields = ['title', 'content']
    # list_display_links = ['updated']  # Focused Link

    class Meta:
        model = Post


# Register your models here.
admin.site.register(Post, PostModelAdmin)
