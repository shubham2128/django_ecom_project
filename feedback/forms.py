from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['customer_name', 'product_name', 'product_id', 'feedback_text', 'star_rating']
        def clean_star_rating(self):
            star_rating = self.cleaned_data['star_rating']
            if star_rating < 0:
                raise forms.ValidationError("Rating cannot be less than 0.")
            elif star_rating > 5:
                raise forms.ValidationError("Rating cannot be more than 5.")
            return star_rating