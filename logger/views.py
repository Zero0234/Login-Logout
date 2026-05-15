from django.shortcuts import render
from django.http import JsonResponse
from django.contrib import messages
from .models import NetlabLog, LearnerProfile

def log_entry(request):
    if request.method == 'POST':
        # 1. Get the data from the form
        role = request.POST.get('role').upper()  # 'STUDENT' or 'GUEST'
        id_number = request.POST.get('id_number')
        name_from_form = request.POST.get('name')

        if role == 'STUDENT':
            # 2. Find the student in the Master List using their ID
            student_profile = LearnerProfile.objects.filter(id_number=id_number).first()
            
            if student_profile:
                # 3. Create the log using the official name from the Master List
                NetlabLog.objects.create(
                    name=student_profile.full_name, 
                    role='STUDENT', # Matches your model's 'LEARNER' choice
                    id_number=id_number
                )
                messages.success(request, f"Thank you, {student_profile.full_name}! Entry recorded.")
            else:
                messages.error(request, "Error: Student ID not found.")
        
        else:
            # 4. Guest Logic: Use the name typed in the form
            if name_from_form:
                NetlabLog.objects.create(name=name_from_form, role='GUEST')
                messages.success(request, f"Welcome, {name_from_form}!")
            else:
                messages.error(request, "Name is required for Guests.")

    return render(request, 'logger/index.html')

# This function handles the "Is this you?" search
def lookup_learner(request):
    id_number = request.GET.get('id_number', None)
    # Searching for the student profile
    student = LearnerProfile.objects.filter(id_number=id_number).first()
    if student:
        return JsonResponse({'success': True, 'name': student.full_name})
    return JsonResponse({'success': False})