from django.contrib import admin
from .models import TeamMember, Project, Task

admin.site.register(TeamMember)
admin.site.register(Project)
admin.site.register(Task)
