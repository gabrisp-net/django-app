from django.shortcuts import render, redirect


# Create your views here.

def handler404(request, exception, template_name="404.html"):
    return redirect("http://localhost:3000/404")
