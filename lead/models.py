from django.db import models

from userprofile.models import UserProfile


class Lead(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('qualified', 'Qualified'),
        ('lost', 'Lost'),
    ]

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    company = models.CharField(max_length=255, blank=True, null=True)  
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    assigned_to = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Interaction(models.Model):
    CALL = 'Call'
    EMAIL = 'Email'
    MEETING = 'Meeting'

    INTERACTION_TYPE_CHOICES = [
        (CALL, 'Call'),
        (EMAIL, 'Email'),
        (MEETING, 'Meeting'),
    ]

    lead = models.ForeignKey(Lead, related_name='interactions', on_delete=models.CASCADE)
    interaction_type = models.CharField(max_length=100, choices=INTERACTION_TYPE_CHOICES)  
    date = models.DateField()
    notes = models.TextField()

    def __str__(self):
        return f"{self.interaction_type} on {self.date}"
    