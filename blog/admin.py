from django.contrib import admin
from .models import Blogger, BlogPost, Comment

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ('author', 'created_at', 'text_preview')
    fields = ('author', 'created_at', 'text_preview')
    can_delete = True

    def text_preview(self, obj):
        return str(obj)  # uses __str__ truncation
    text_preview.short_description = 'Comment (truncated)'

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    list_filter = ('author', 'created_at')
    inlines = [CommentInline]
    search_fields = ('title', 'content')

@admin.register(Blogger)
class BloggerAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at')
    search_fields = ('name', 'bio')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'post', 'author', 'created_at')
    readonly_fields = ('created_at',)
    search_fields = ('text',)

