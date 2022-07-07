from django.shortcuts import render, redirect
from .forms import ContactForm
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse

def index(request):
    return render (request, 'index.html')

def about(request):
    return render (request, 'about.html')

def service(request):
    return render (request, 'service.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = "Web Inquiry"
            data = {
                'name': form.cleaned_data['name'],
                'email': form.cleaned_data['email'],
                'subject': form.cleaned_data['subject'],
                'message': form.cleaned_data['message'],
            }
            message = "\n".join(data.values())
        try:
            send_mail(subject, message, 'gabrielattie@gmail.com',['gabrielattie@gmail.com'])
        except BadHeaderError:
            return HttpResponse('Invalid header')
        return redirect('index')
    form = ContactForm()        
    return render (request, 'contact.html', {'form': form})
