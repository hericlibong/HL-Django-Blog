    
from django.contrib import admin
from .models import BlogPosts, Tags, Comment

   
class CommentInlineAdmin(admin.TabularInline):
    model = Comment

class BlogPostsAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'slug', 'description', 'author', 'last_updated', 'created_on',
        'published', 'category', 'tags_list'
    ]
    list_filter = ['category']
    search_fields = ['title', 'author__username', 'content']
    list_editable = ['published']
    
    inlines = [
        CommentInlineAdmin
    ]
    
   
    
    def tags_list(self, obj):
        return ', '.join([tag.name for tag in obj.tags.all()])
    tags_list.short_description = 'Tags'
    
admin.site.register(BlogPosts, BlogPostsAdmin)
admin.site.register(Tags)
admin.site.register(Comment)

