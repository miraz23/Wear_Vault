from django.shortcuts import render, redirect

def index(request):
    return render(request, "index.html")

def about(request):
    return render(request, "about.html")