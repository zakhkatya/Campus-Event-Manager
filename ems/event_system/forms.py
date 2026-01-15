from django import forms
from .models import Feedback

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
            "rating": forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)], attrs={
                "class": ""
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
