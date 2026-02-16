from django import forms
from .models import ContactMessage, Course, NewsletterSubscriber, CourseApplication

class CourseInquiryForm(forms.Form):
    """Simple inquiry form for course questions (not applications)"""
    course = forms.ModelChoiceField(
        queryset=Course.objects.filter(is_active=True),
        empty_label="Select a course",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your full name'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'your.email@example.com'})
    )
    phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+263 123 456 789'})
    )
    message = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Your question (optional)'})
    )
    
    def send_inquiry(self):
        """Logic to send email or save to database"""
        # This will be called from the view
        pass


class NewsletterSignupForm(forms.ModelForm):
    """Form for newsletter subscription"""
    class Meta:
        model = NewsletterSubscriber
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your email address',
                'aria-label': 'Email address'
            }),
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Additional validation if needed
        return email


class CourseApplicationForm(forms.ModelForm):
    """Comprehensive application form for course enrollment"""
    
    EDUCATION_LEVELS = [
        ('secondary', 'Secondary School'),
        ('diploma', 'Diploma'),
        ('degree', "Bachelor's Degree"),
        ('masters', "Master's Degree"),
        ('other', 'Other'),
    ]
    
    HEAR_ABOUT_CHOICES = [
        ('google', 'Google Search'),
        ('facebook', 'Facebook'),
        ('whatsapp', 'WhatsApp'),
        ('friend', 'Friend/Word of Mouth'),
        ('email', 'Email Newsletter'),
        ('other', 'Other'),
    ]
    
    # Override the education_level field to use our choices
    education_level = forms.ChoiceField(
        choices=EDUCATION_LEVELS,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    # Override the how_did_you_hear field
    how_did_you_hear = forms.ChoiceField(
        choices=HEAR_ABOUT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = CourseApplication
        fields = [
            'full_name', 'email', 'phone', 'date_of_birth',
            'nationality', 'education_level', 'previous_experience',
            'medical_conditions', 'emergency_contact_name',
            'emergency_contact_phone', 'how_did_you_hear', 'additional_notes'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your full name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your.email@example.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+263 123 456 789'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'nationality': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Zimbabwean'
            }),
            'previous_experience': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Tell us about any relevant experience (optional)'
            }),
            'medical_conditions': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'List any medical conditions we should know about (optional)'
            }),
            'emergency_contact_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Emergency contact full name'
            }),
            'emergency_contact_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Emergency contact phone'
            }),
            'additional_notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Any other information you\'d like to share (optional)'
            }),
        }
        labels = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone': 'Phone Number',
            'date_of_birth': 'Date of Birth',
            'nationality': 'Nationality',
            'education_level': 'Highest Education Level',
            'previous_experience': 'Previous Experience',
            'medical_conditions': 'Medical Conditions',
            'emergency_contact_name': 'Emergency Contact Name',
            'emergency_contact_phone': 'Emergency Contact Phone',
            'how_did_you_hear': 'How did you hear about us?',
            'additional_notes': 'Additional Notes',
        }
        help_texts = {
            'previous_experience': 'Any relevant experience in conservation, military, security, or related fields.',
            'medical_conditions': 'Please list any medical conditions we should be aware of for training purposes.',
        }


class ContactForm(forms.ModelForm):
    """Form for general contact inquiries"""
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your full name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your.email@example.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+263 123 456 789 (optional)'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'What is this about?'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Your message...'
            }),
        }
        labels = {
            'name': 'Name',
            'email': 'Email',
            'phone': 'Phone Number',
            'subject': 'Subject',
            'message': 'Message',
        }
