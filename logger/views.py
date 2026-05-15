from django.shortcuts import render
from django.http import JsonResponse
from django.contrib import messages
from .models import NetlabLog, LearnerProfile
from django.core.exceptions import ValidationError

def log_entry(request):
    if request.method == 'POST':
        role = request.POST.get('role').upper()  # 'STUDENT' or 'GUEST'
        id_number = request.POST.get('id_number')
        name_from_form = request.POST.get('name')

        try:
            if role == 'STUDENT':
                student_profile = LearnerProfile.objects.filter(id_number=id_number).first()
                if student_profile:
                    NetlabLog.objects.create(
                        name=student_profile.full_name, 
                        role='STUDENT', 
                        id_number=id_number
                    )
                    messages.success(request, f"Thank you, {student_profile.full_name}! Entry recorded.")
                else:
                    messages.error(request, "Error: Student ID not found.")
            
            else:
                # Guest Logic
                if name_from_form:
                    # Wrapping this in the try block catches the alpha_only regex error here
                    NetlabLog.objects.create(name=name_from_form, role='GUEST')
                    messages.success(request, f"Welcome, {name_from_form}!")
                else:
                    messages.error(request, "Name is required for Guests.")
                    
        except ValidationError as e:
            # Catch the regex validation error and turn it into a clean web message
            for field, errors in e.message_dict.items():
                for error in errors:
                    messages.error(request, f"{error}")

    return render(request, 'logger/index.html')

# This function handles the "Is this you?" search
def lookup_learner(request):
    id_number = request.GET.get('id_number', None)
    # Searching for the student profile
    student = LearnerProfile.objects.filter(id_number=id_number).first()
    if student:
        return JsonResponse({'success': True, 'name': student.full_name})
    return JsonResponse({'success': False})