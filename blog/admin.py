from django.contrib import admin
from blog.models import BlogPost, BlogPostImage
from ckeditor.widgets import CKEditorWidget
from django.db import models
from django.utils.html import mark_safe


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'priority', 'pub_date', 'is_deleted')
    list_filter = ('priority', 'is_deleted')
    search_fields = ('title', 'content')
    date_hierarchy = 'pub_date'
    readonly_fields = ('pub_date',)
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget()},
    }


@admin.register(BlogPostImage)
class BlogPostImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'url', 'uploaded_at', 'image_preview')

    def url(self, obj):
        if obj.image:
            return obj.image.url
        else:
            return 'no url!'


    def image_preview(self, obj):
        if obj.image:
            return mark_safe('<img src="%s" style="max-width:150px;max-height:150px;" />' % obj.image.url)
        else:
            return '(No image)'

    image_preview.short_description = 'Image Preview'
