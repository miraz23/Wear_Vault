from django.shortcuts import render, redirect
from contact.models import contact

def index(request):
    return render(request, "index.html")

def aboutUs(request):
    return render(request, "about.html")

def contactUs(request):
    if request.method == 'POST':
       
        data = contact(
            contact_name = request.POST.get('contact-name'),
            contact_email = request.POST.get('contact-email'),
            contact_subject = request.POST.get('contact-subject'),
            contact_message = request.POST.get('contact-message'),
        )
        data.save()
        return redirect('/')
    
    return render(request, "contact.html")