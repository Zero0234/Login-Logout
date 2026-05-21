import json
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.core.exceptions import ValidationError
from .models import NetlabLog, LearnerProfile

def log_entry(request):
    context = {'selected_role': 'STUDENT', 'name_val': '', 'id_val': ''}

    if request.method == 'POST':
        role = request.POST.get('role', 'STUDENT').upper() 
        id_number = request.POST.get('id_number', '').strip()
        name_from_form = request.POST.get('name', '').strip()
        purpose_selected = request.POST.get('purpose', '').strip()
        
        department_from_form = request.POST.get('department', 'CCS')

        context['selected_role'] = role
        context['name_val'] = name_from_form
        context['id_val'] = id_number

        try:
            if not purpose_selected:
                raise ValidationError({'purpose': 'Please select a log entry purpose interaction choice.'})

            if role == 'STUDENT':
                if not id_number.isdigit() or len(id_number) != 8:
                    raise ValidationError({'id_number': 'ID Number must contain only numbers and be exactly 8 digits long.'})
                
                student_profile = LearnerProfile.objects.filter(id_number=id_number).first()
                if student_profile:
                    NetlabLog.objects.create(
                        name=student_profile.full_name, 
                        role='STUDENT', 
                        id_number=id_number,
                        department=student_profile.department,
                        purpose=purpose_selected
                    )
                    messages.success(request, f"Thank you, {student_profile.full_name}! Entry recorded for {purpose_selected}.")
                    context = {'selected_role': 'STUDENT'}
                else:
                    messages.error(request, "Error: Student ID record registration path not found.")
            
            else:

                if name_from_form:
                    NetlabLog.objects.create(
                        name=name_from_form, 
                        role='GUEST',
                        department=department_from_form,
                        purpose=purpose_selected
                    )
                    messages.success(request, f"Welcome, {name_from_form}! Entry recorded for {purpose_selected}.")
                    context = {'selected_role': 'STUDENT'} 
                else:
                    messages.error(request, "Name parameters are required for Guest interactions.")
                    
        except ValidationError as e:
            if hasattr(e, 'message_dict'):
                for field, errors in e.message_dict.items():
                    for error in errors:
                        messages.error(request, f"{error}")
            else:
                for error in e.messages:
                    messages.error(request, f"{error}")

    return render(request, 'logger/index.html', context)

def lookup_learner(request):
    id_number = request.GET.get('id_number', None)
    student = LearnerProfile.objects.filter(id_number=id_number).first()
    if student:
        return JsonResponse({'success': True, 'name': student.full_name})
    return JsonResponse({'success': False})

@require_POST
def register_learner_ajax(request):
    try:
        data = json.loads(request.body)
        
        id_number = str(data.get('id_number', '')).strip()
        full_name = data.get('full_name')
        department = data.get('department')
        purpose = data.get('purpose')
        
        new_learner = LearnerProfile(
            id_number=id_number,
            full_name=full_name,
            department=department
        )
        new_learner.full_clean() 
        new_learner.save()
        
        NetlabLog.objects.create(
            name=full_name, 
            role='STUDENT', 
            id_number=id_number,
            department=department,
            purpose=purpose
        )
        
        success_msg = f"Welcome, {full_name}! Entry recorded for {purpose}."
        return JsonResponse({'success': True, 'message': success_msg})
        
    except ValidationError as e:
        error_message = e.message_dict.get('id_number', ["Validation Error: Check your inputs."])[0]
        return JsonResponse({'success': False, 'error': error_message})
    except Exception as e:
        return JsonResponse({'success': False, 'error': "An unexpected error occurred."})