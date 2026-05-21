from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

alpha_only = RegexValidator(r'^[a-zA-Z ]*$', 'Only letters and spaces are allowed.')

numeric_validator = RegexValidator(
    regex=r'^\d{8}$', 
    message='ID Number must contain only numbers and be up to 8 digits long.'
)

class Department(models.TextChoices):
    CCS = 'CCS'
    CBA = 'CBA'
    COE = 'COE'
    CASED = 'CASED'
    CON = 'CON'
    COA = 'COA'

class LearnerProfile(models.Model):
    id_number = models.CharField(
        max_length=8, 
        unique=True, 
        validators=[numeric_validator],
        help_text="The official Learner ID Number."
    )
    full_name = models.CharField(
        max_length=150, 
        validators=[alpha_only],
        help_text="The official Full Name of the Learner."
    )
    department = models.CharField(
        max_length=10,
        choices=Department.choices,
        default=None,
        blank=True, 
        null=True
    )

    class Meta:
        verbose_name = "Learner Profile"
        verbose_name_plural = "Learner Profiles"
        ordering = ['id_number']

    def __str__(self):
        return f"{self.id_number} - {self.full_name} ({self.department})"
    
class NetlabLog(models.Model):
    ROLE_CHOICES = [
        ('STUDENT', 'Student'),
        ('GUEST', 'Guest'),
    ]
    
    name = models.CharField(
        max_length=150, 
        validators=[alpha_only],
        help_text="Full name of the user."
    )
    
    role = models.CharField(choices=ROLE_CHOICES, default='STUDENT')
    id_number = models.CharField(
        max_length=8, 
        blank=True, 
        null=True, 
        validators=[numeric_validator],
        help_text="Required for Students (Numbers only). Leave blank for Guests."
    )

    purpose = models.CharField(
        max_length=50, 
        blank=True, 
        null=True,
        help_text="The purpose of the visit (e.g., Internet, Print)."
    )
    

    department = models.CharField(
        max_length=10,
        choices=Department.choices,
        blank=True, 
        null=True
    )

    logged_at = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Netlab Log"
        verbose_name_plural = "Netlab Logs"
        ordering = ['-timestamp'] 

    def __str__(self):
        return f"{self.name} - {self.get_role_display()} ({self.timestamp.strftime('%Y-%m-%d %H:%M')})"

    def clean(self):
        # Backend validation to strictly enforce your rules
        if self.role == 'STUDENT' and not self.id_number:
            raise ValidationError({'id_number': 'An ID Number is required for Students.'})
        
        if self.role == 'GUEST' and self.id_number:
            self.id_number = None

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)