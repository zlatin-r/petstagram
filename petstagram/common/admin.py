from django.contrib import admin
from petstagram.common.models import Comment, Like


# Register your models here.

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_time_of_publication', 'to_photo_id')

    @staticmethod
    def to_photo_id(obj):
        return obj.id


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('to_photo_id', )

    @staticmethod
    def to_photo_id(obj):
        return obj.id