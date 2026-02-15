from django import forms
from .models import ContactMessage, Course
from .models import NewsletterSubscriber

class CourseInquiryForm(forms.Form):
    course = forms.ModelChoiceField(queryset=Course.objects.filter(is_active=True))
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.CharField(max_length=20)
    message = forms.CharField(widget=forms.Textarea, required=False)
    
    def send_inquiry(self):
        # Logic to send email or save to database
        pass
class NewsletterSignupForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscriber
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your email address'}),
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Additional validation if needed
        return email