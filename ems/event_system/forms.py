from django import forms
from .models import Feedback, Event

class FeedbackForm(forms.ModelForm):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    class Meta:
        model = Feedback
        fields = [
            "comment",
            "rating",
        ]
        widgets = {
            "comment": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Enter the feedback...",
                "rows": 4
            }),
            "rating": forms.Select(choices=[(i, str(i)) for i in range(1, 6)], attrs={
                "class": "btn btn-secondary w-auto h-auto p-1 dropdown fw-bolder"
            }),
        }
            
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            "title",
            "location",
            "is_private",
            "date_start",
            "date_end",
            "category",
            "description",
            "banner",
        ]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control form-control-lg",
                "placeholder": "Event title"
            }),
            "location": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Event location"
            }),
            "is_private": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "date_start": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"},
                format="%Y-%m-%dT%H:%M"
            ),
            "date_end": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"},
                format="%Y-%m-%dT%H:%M"
            ),
            "category": forms.Select(attrs={
                "class": "form-select"
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Describe the event..."
            }),
            "banner": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["date_start"].input_formats = ["%Y-%m-%dT%H:%M"]
        self.fields["date_end"].input_formats = ["%Y-%m-%dT%H:%M"]
        self.fields["category"].empty_label = "Select Category"
