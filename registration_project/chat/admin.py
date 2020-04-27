from django.contrib import admin

from .models import GroupChat, GroupMembers

admin.site.register(GroupChat),
admin.site.register(GroupMembers)
