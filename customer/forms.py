from django import forms
from .models import SupportTicket

class SupportTicketForm(forms.ModelForm):
    class Meta:
        model = SupportTicket
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter a brief title for the ticket',
                    'maxlength': 100
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Describe the issue or request in detail',
                    'rows': 5
                }
            ),
        }
        labels = {
            'title': 'Ticket Title',
            'description': 'Detailed Description',
        }
        help_texts = {
            'title': 'Provide a concise title for your support ticket.',
            'description': 'Include all relevant details for the issue or request.',
        }
