from django.contrib import admin

from .models import Goal, Step, StepComment

admin.site.register(Goal),
admin.site.register(Step),
admin.site.register(StepComment),