from django.db import models
import os
from datetime import datetime

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

def get_image_path(instance, filename):
    return os.path.join('static/main/images/article_photos', filename)

# Create your models here.

class Project(models.Model):
    project_title = models.CharField(max_length=200)
    project_content = RichTextUploadingField(blank=True,null=True)
    project_published = models.DateTimeField('date published', default=datetime.now())
    project_slug = models.CharField(max_length=200, default=1)
    project_image = models.ImageField(upload_to=get_image_path, blank=True, null=True)

    def __str__(self):
        return self.project_title

