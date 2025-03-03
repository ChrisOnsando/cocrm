from django.contrib import admin

from .models import Lead,Interaction,Task,Reply
admin.site.register(Lead)
admin.site.register(Interaction)
admin.site.register(Task)
admin.site.register(Reply)
