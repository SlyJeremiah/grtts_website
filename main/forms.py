from django import forms
from .models import ApplicantProfile, UserDocument

class ApplicantRegistrationForm(forms.ModelForm):
    """
    Registration form for applicants - creates ApplicantProfile only, not User
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
    phone = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+263 123 456 789'
        })
    )
    date_of_birth = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    gender = forms.ChoiceField(
        choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')],
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    nationality = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., Zimbabwean'
        })
    )
    address = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 2,
            'placeholder': 'Your physical address'
        })
    )
    city = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'City/Town'
        })
    )
    province = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Province'
        })
    )
    emergency_name = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Emergency contact full name'
        })
    )
    emergency_phone = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Emergency contact phone'
        })
    )
    emergency_relationship = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Relationship to contact'
        })
    )
    medical_conditions = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 2,
            'placeholder': 'Any medical conditions we should know about'
        })
    )
    dietary_requirements = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 2,
            'placeholder': 'Any dietary requirements'
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
        model = ApplicantProfile
        fields = []  # We're handling all fields manually above

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
        applicant = super().save(commit=False)
        
        # Set all the fields from cleaned_data
        applicant.first_name = self.cleaned_data['first_name']
        applicant.last_name = self.cleaned_data['last_name']
        applicant.email = self.cleaned_data['email']
        applicant.phone = self.cleaned_data['phone']
        applicant.date_of_birth = self.cleaned_data['date_of_birth']
        applicant.gender = self.cleaned_data['gender']
        applicant.nationality = self.cleaned_data['nationality']
        applicant.address = self.cleaned_data['address']
        applicant.city = self.cleaned_data['city']
        applicant.province = self.cleaned_data['province']
        applicant.emergency_name = self.cleaned_data['emergency_name']
        applicant.emergency_phone = self.cleaned_data['emergency_phone']
        applicant.emergency_relationship = self.cleaned_data['emergency_relationship']
        applicant.medical_conditions = self.cleaned_data.get('medical_conditions', '')
        applicant.dietary_requirements = self.cleaned_data.get('dietary_requirements', '')
        
        if commit:
            applicant.save()
            
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
                        user=None,
                        document_type=doc_type,
                        file=file,
                        description=f"{description} uploaded during registration for {applicant.email}"
                    )
        
        return applicant


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
