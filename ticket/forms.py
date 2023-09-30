from django import forms
from ticket.models import Ticket


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'status']


class TicketReplyForm(forms.Form):
    message = forms.CharField(
        label='پیام جدید',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        required=True
    )
