from django.shortcuts import render
from .models import Project

# Create your views here.

def homepage(request):
    all_posts = Project.objects.all()

    return render(request=request, 
                  template_name='main/homepage.html',
                  context={'all_projects': all_posts})
