from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

class NetlabLog(models.Model):
    # Updated choices: Just Student and Guest
    ROLE_CHOICES = [
        ('STUDENT', 'Student'),
        ('GUEST', 'Guest'),
    ]

    numeric_validator = RegexValidator(
        regex=r'^\d+$',
        message='ID Number must contain only numbers.'
    )
    name = models.CharField(max_length=150, help_text="Full name of the user.")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='STUDENT')
    
    # We leave this blank=True, null=True here so the form doesn't block Guests
    # The actual requirement logic is handled in the clean() method below.
    id_number = models.CharField(
        max_length=50, 
        blank=True, 
        null=True, 
        validators=[numeric_validator],
        help_text="Required for Students (Numbers only). Leave blank for Guests."
    )
    
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
            # If a guest somehow inputs an ID, we strip it out to keep data clean
            self.id_number = None

    def save(self, *args, **kwargs):
        # Ensure the clean method runs every time a log is saved
        self.full_clean()
        super().save(*args, **kwargs)