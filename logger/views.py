import json
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.core.exceptions import ValidationError
from .models import NetlabLog, LearnerProfile

def log_entry(request):
    # Default context when the page first loads
    context = {'selected_role': 'STUDENT', 'name_val': '', 'id_val': ''}

    if request.method == 'POST':
        role = request.POST.get('role').upper()  # 'STUDENT' or 'GUEST'
        id_number = request.POST.get('id_number', '')
        name_from_form = request.POST.get('name', '')
        purpose_selected = request.POST.get('purpose', '')

        # Remember what the user typed so we don't reset their screen on an error
        context['selected_role'] = role
        context['name_val'] = name_from_form
        context['id_val'] = id_number

        try:
            if role == 'STUDENT':
                student_profile = LearnerProfile.objects.filter(id_number=id_number).first()
                if student_profile:
                    NetlabLog.objects.create(
                        name=student_profile.full_name, 
                        role='STUDENT', 
                        id_number=id_number,
                        purpose=purpose_selected
                    )
                    messages.success(request, f"Thank you, {student_profile.full_name}! Entry recorded.")
                    context = {'selected_role': 'STUDENT'} # Reset on success
                else:
                    messages.error(request, "Error: Student ID not found.")
            
            else:
                # Guest Logic
                if name_from_form:
                    NetlabLog.objects.create(name=name_from_form, role='GUEST', purpose=purpose_selected)
                    messages.success(request, f"Welcome, {name_from_form}!")
                    context = {'selected_role': 'STUDENT'} # Reset on success
                else:
                    messages.error(request, "Name is required for Guests.")
                    
        except ValidationError as e:
            for field, errors in e.message_dict.items():
                for error in errors:
                    messages.error(request, f"{error}")

    return render(request, 'logger/index.html', context)

def lookup_learner(request):
    id_number = request.GET.get('id_number', None)
    student = LearnerProfile.objects.filter(id_number=id_number).first()
    if student:
        return JsonResponse({'success': True, 'name': student.full_name})
    return JsonResponse({'success': False})

# --- NEW AJAX REGISTRATION VIEW ---
@require_POST
def register_learner_ajax(request):
    try:
        data = json.loads(request.body)
        
        # Create the instance
        new_learner = LearnerProfile(
            id_number=data.get('id_number'),
            full_name=data.get('full_name'),
            department=data.get('department')
        )
        
        # full_clean() enforces your RegexValidators before saving
        new_learner.full_clean() 
        new_learner.save()
        
        return JsonResponse({'success': True})
        
    except ValidationError as e:
        # Returns the specific model validation errors (e.g. wrong ID format)
        return JsonResponse({'success': False, 'error': "Validation Error: Check your inputs."})
    except Exception as e:
        return JsonResponse({'success': False, 'error': "An unexpected error occurred."})