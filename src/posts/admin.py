# from django.contrib import admin
# from . import models

# class InlineTagsModel(admin.TabularInline):
#     model = models.BlogPosts.tags.through  # Utilisez le modèle de liaison ManyToManyField
#     extra = 1 
    
# @admin.register(models.BlogPosts)
# class BlogPostsAdmin(admin.ModelAdmin):
#     list_display = [
#         'title', 'author', 'last_updated', 'created_on',
#         'published', 'category', 'tags_count'
#         ]
#     list_filter = ['category']
#     search_fields = ['title', 'author__username', 'content']
#     list_editable = ['published']
    
#     inlines = [
#         InlineTagsModel
#     ]
    

#     def tags_count(self, obj):
#         return obj.tags.count()
#     tags_count.shor_description = 'Tags Count'
    
from django.contrib import admin
from .models import BlogPosts, Tags, Photo


class PhotoInlineAdmin(admin.TabularInline):
    model = Photo

class BlogPostsAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'slug', 'author', 'last_updated', 'created_on',
        'published', 'category', 'tags_list'
    ]
    list_filter = ['category']
    search_fields = ['title', 'author__username', 'content']
    list_editable = ['published']
    
    inlines = [
        PhotoInlineAdmin
    ]
    
    def tags_list(self, obj):
        return ', '.join([tag.name for tag in obj.tags.all()])
    tags_list.short_description = 'Tags'
    
admin.site.register(BlogPosts, BlogPostsAdmin)
admin.site.register(Tags)
admin.site.register(Photo)

