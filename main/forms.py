from django import forms
from .models import ContactMessage, Course, NewsletterSubscriber, CourseApplication, ApplicantProfile

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


class ApplicantProfileForm(forms.ModelForm):
    """Form for updating applicant profile"""
    class Meta:
        model = ApplicantProfile
        fields = [
            'date_of_birth', 'gender', 'nationality',
            'address', 'city', 'province',
            'emergency_name', 'emergency_phone', 'emergency_relationship',
            'medical_conditions', 'dietary_requirements',
            'id_document', 'cv', 'certificates'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'nationality': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Zimbabwean'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Your physical address'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City/Town'}),
            'province': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Province'}),
            'emergency_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Emergency contact full name'}),
            'emergency_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Emergency contact phone'}),
            'emergency_relationship': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Relationship to contact'}),
            'medical_conditions': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Any medical conditions we should know about'}),
            'dietary_requirements': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Any dietary requirements'}),
            'id_document': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf,.jpg,.jpeg,.png'}),
            'cv': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf,.doc,.docx'}),
            'certificates': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf,.jpg,.jpeg,.png'}),
        }
        labels = {
            'date_of_birth': 'Date of Birth',
            'gender': 'Gender',
            'nationality': 'Nationality',
            'address': 'Address',
            'city': 'City',
            'province': 'Province',
            'emergency_name': 'Emergency Contact Name',
            'emergency_phone': 'Emergency Contact Phone',
            'emergency_relationship': 'Relationship',
            'medical_conditions': 'Medical Conditions',
            'dietary_requirements': 'Dietary Requirements',
            'id_document': 'ID Document (Passport/National ID)',
            'cv': 'CV/Resume',
            'certificates': 'Certificates',
        }


class CourseApplicationForm(forms.ModelForm):
    """Comprehensive application form for course enrollment with file uploads"""
    
    # Text fields that override profile defaults
    motivation_text = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Tell us why you want to take this course. What are your goals and aspirations?'
        }),
        label="Motivation"
    )
    
    previous_experience = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Any relevant experience in conservation, military, security, or related fields.'
        }),
        label="Previous Experience"
    )
    
    medical_conditions = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Any medical conditions we should be aware of for training purposes.'
        }),
        label="Medical Conditions"
    )
    
    dietary_requirements = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 2,
            'placeholder': 'Any dietary requirements or restrictions.'
        }),
        label="Dietary Requirements"
    )
    
    class Meta:
        model = CourseApplication
        fields = [
            # File uploads
            'profile_photo', 'id_document', 'cv_resume', 'certificates',
            'motivation_letter', 'additional_docs',
            
            # Text fields (handled above)
            # Note: These are already defined as form fields above
        ]
        widgets = {
            'profile_photo': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
                'aria-describedby': 'profile_photo_help'
            }),
            'id_document': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.jpg,.jpeg,.png',
                'aria-describedby': 'id_document_help'
            }),
            'cv_resume': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx',
                'aria-describedby': 'cv_resume_help'
            }),
            'certificates': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.jpg,.jpeg,.png',
                'aria-describedby': 'certificates_help'
            }),
            'motivation_letter': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx',
                'aria-describedby': 'motivation_letter_help'
            }),
            'additional_docs': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx,.jpg,.jpeg,.png',
                'aria-describedby': 'additional_docs_help'
            }),
        }
        labels = {
            'profile_photo': 'Profile Photo',
            'id_document': 'ID Document (Passport/National ID)',
            'cv_resume': 'CV / Resume',
            'certificates': 'Certificates',
            'motivation_letter': 'Motivation Letter',
            'additional_docs': 'Additional Documents',
        }
        help_texts = {
            'profile_photo': 'Upload a recent passport-sized photo (JPG, PNG). Max 2MB.',
            'id_document': 'Upload your ID or Passport (PDF, JPG, PNG). Max 5MB.',
            'cv_resume': 'Upload your CV/Resume (PDF, DOC, DOCX). Max 5MB.',
            'certificates': 'Upload any relevant certificates (PDF, JPG, PNG). Max 5MB per file.',
            'motivation_letter': 'Upload your motivation letter (PDF, DOC, DOCX). Max 5MB.',
            'additional_docs': 'Any other supporting documents. Max 5MB per file.',
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
