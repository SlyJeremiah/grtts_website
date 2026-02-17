from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, UserDocument

class CustomUserCreationForm(UserCreationForm):
    """
    Custom registration form with first name, last name, and file uploads
    """
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your first name'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your surname'
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your.email@example.com'
        })
    )
    
    # File upload fields
    profile_photo = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*'
        }),
        help_text='Upload a profile photo (JPG, PNG). Max 5MB.'
    )
    
    id_document = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.pdf,.jpg,.jpeg,.png'
        }),
        help_text='Upload your ID or Passport (PDF, JPG, PNG). Max 10MB.'
    )
    
    cv = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.pdf,.doc,.docx,.txt'
        }),
        help_text='Upload your CV/Resume (PDF, DOC, DOCX, TXT). Max 10MB.'
    )
    
    certificates = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.pdf,.jpg,.jpeg,.png'
        }),
        help_text='Upload any relevant certificates (PDF, JPG, PNG). Max 10MB.'
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to default fields
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Choose a username'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Create a password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm your password'
        })

    def clean_profile_photo(self):
        photo = self.cleaned_data.get('profile_photo')
        if photo:
            if photo.size > 5 * 1024 * 1024:  # 5MB limit
                raise forms.ValidationError("Profile photo size cannot exceed 5MB.")
        return photo

    def clean_id_document(self):
        doc = self.cleaned_data.get('id_document')
        if doc:
            if doc.size > 10 * 1024 * 1024:  # 10MB limit
                raise forms.ValidationError("ID document size cannot exceed 10MB.")
        return doc

    def clean_cv(self):
        cv = self.cleaned_data.get('cv')
        if cv:
            if cv.size > 10 * 1024 * 1024:  # 10MB limit
                raise forms.ValidationError("CV size cannot exceed 10MB.")
        return cv

    def clean_certificates(self):
        cert = self.cleaned_data.get('certificates')
        if cert:
            if cert.size > 10 * 1024 * 1024:  # 10MB limit
                raise forms.ValidationError("Certificate size cannot exceed 10MB.")
        return cert

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
            
            # Save uploaded files as UserDocument objects
            file_mappings = [
                ('profile_photo', 'photo', 'Profile photo'),
                ('id_document', 'id', 'ID document'),
                ('cv', 'cv', 'CV/Resume'),
                ('certificates', 'certificate', 'Certificate'),
            ]
            
            for field_name, doc_type, description in file_mappings:
                file = self.cleaned_data.get(field_name)
                if file:
                    UserDocument.objects.create(
                        user=user,
                        document_type=doc_type,
                        file=file,
                        description=f"{description} uploaded during registration"
                    )
        
        return user


class NewsletterSignupForm(forms.Form):
    """Form for newsletter subscription"""
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your email address',
            'aria-label': 'Email address'
        })
    )
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        return email
