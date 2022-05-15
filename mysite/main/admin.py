from django.contrib import admin
from .models import Project
from django.db import models
from ckeditor.fields import RichTextField

# Register your models here.

class ProjectAdmin(admin.ModelAdmin):
    # This just changes the order we see the model attributes on the admin page
    # i.e. published is now first, then title, then content
              
    # This is used to group the model attributes into 'sections'/dividers
    
    fieldsets = [
        ('Title/date', {'fields': ['project_title', 'project_published']}),
        ('URL', {'fields':['project_slug']}),
        ('Content', {'fields':['project_content']}),
        ('Photo', {'fields':['project_image']}),     
    ]

    formfield_overrides = {
        models.TextField: {'widget': RichTextField()},
    }

admin.site.register(Project, ProjectAdmin)