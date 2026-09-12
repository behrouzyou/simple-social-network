from django.contrib import admin
from .models import *
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user','slug','updated')
    search_fields = ('user','body')
    list_filter = ('updated',)
    raw_id_fields = ('user',)
    prepopulated_fields = {'slug':('body',)}
    date_hierarchy = 'created'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user','post','reply','body')
    raw_id_fields = ('user','post','reply')

admin.site.register(Vote)