from django.shortcuts import render, redirect
from .models import NetlabLog
from django.contrib import messages

def log_entry(request):
    if request.method == "POST":
        name = request.POST.get('name')
        role = request.POST.get('role')
        id_number = request.POST.get('id_number')

        # Basic save logic
        try:
            log = NetlabLog(name=name, role=role, id_number=id_number)
            log.save()
            messages.success(request, f"Welcome, {name}! You have been logged in.")
            return redirect('log_entry')
        except Exception as e:
            messages.error(request, "There was an error. Please ensure all fields are correct.")

    return render(request, 'logger/index.html')