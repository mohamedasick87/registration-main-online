from django.db import models

# Event model to represent both technical and non-technical events
class Event(models.Model):
    EVENT_TYPE_CHOICES = [
        ('technical', 'Technical'),
        ('non_technical', 'Non-Technical'),
    ]
    
    name = models.CharField(max_length=100)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES)

    def __str__(self):
        return self.name

class Registration(models.Model):
    PAYMENT_MODE_CHOICES = [
        ('Online', 'Online'),
        ('Offline', 'Offline'),
    ]
    
    # Participant Details
    member_id = models.CharField(max_length=20, null=True, blank=True)  # Unique member ID (Optional)
    name = models.CharField(max_length=100, null=True, blank=True)  # Participant's name (Optional)
    college = models.CharField(max_length=255, null=True, blank=True)  # College (Optional)
    department = models.CharField(max_length=100, null=True, blank=True)  # Department (Optional)
    phone = models.CharField(max_length=15, null=True, blank=True)  # Phone number (Optional)
    email = models.EmailField(null=True, blank=True)  # Email address (Optional)
    payment_mode = models.CharField(max_length=10, choices=PAYMENT_MODE_CHOICES, null=True, blank=True)  # Payment mode (Optional)

    # Paper Submission
    paper_title = models.CharField(max_length=255, null=True, blank=True)  # Paper title (Optional)
    paper_abstract = models.TextField(null=True, blank=True)  # Paper abstract (Optional)

    # Food Preference
    FOOD_PREFERENCE_CHOICES = [
        ('Vegetarian', 'Vegetarian'),
        ('Non-Vegetarian', 'Non-Vegetarian'),
    ]
    food_preference = models.CharField(max_length=20, choices=FOOD_PREFERENCE_CHOICES, null=True, blank=True)  # Food preference (Optional)

    # Event Participation
    technical_events = models.ManyToManyField(Event, related_name='technical_registrations', blank=True)  # Technical events (Optional)
    non_technical_events = models.ManyToManyField(Event, related_name='non_technical_registrations', blank=True)  # Non-technical events (Optional)

    # Payment Details
    payment_link = models.URLField(null=True, blank=True)  # Payment submission link (Optional)
    transaction_number = models.CharField(max_length=100, null=True, blank=True)  # Transaction number (Optional)
    paid_status = models.BooleanField(default=False)  # Field to track payment status (False = Not Paid, True = Paid)

    def __str__(self):
        return f'{self.name} ({self.college})'

class RegistrationStatus(models.Model):
    is_open = models.BooleanField(default=True)

    def __str__(self):
        return "Registration Open" if self.is_open else "Registration Closed"


