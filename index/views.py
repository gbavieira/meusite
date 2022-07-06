from django.shortcuts import render

def index(request):
    return render (request, 'index.html')

def about(request):
    return render (request, 'about.html')

def service(request):
    return render (request, 'service.html')

def projects(request):
    return render (request, 'projects.html')
