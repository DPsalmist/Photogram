from django.contrib import admin
from .models import Photo,Category, Comment
# Register your models here.
admin.site.register(Category)

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
	list_display = ('description', 'image', 'owner', 'created')
	list_filter = ('description', 'created',)
	search_fields = ('category',)
	date_hierarchy = 'created'
	ordering = ('created',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	list_display = ('name', 'email', 'photo', 'created', 'active')
	list_filter = ('active', 'created', 'updated')
	search_fields = ('name', 'email', 'body')
