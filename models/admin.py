from django.contrib import admin
from .models import Profile, Message, Group

# Register your models here.


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'external_id', 'name')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile', 'text', 'group_name', 'created_at')

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
	list_display = ('id', 'group_name', 'profile')


