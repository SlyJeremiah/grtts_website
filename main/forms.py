from django import forms
from .models import ApplicantProfile, UserDocument


class StyledFormMixin:
    """Give every widget the matching design-system class.

    The widgets used to carry a hardcoded Bootstrap `form-control` class.
    Deciding the class from the widget type here means a new field is styled
    correctly without anyone remembering to add it.
    """

    WIDGET_CLASSES = (
        (forms.Select, 'grtts-select'),
        (forms.SelectMultiple, 'grtts-select'),
        (forms.Textarea, 'grtts-textarea'),
        (forms.CheckboxInput, ''),
        (forms.RadioSelect, ''),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            css = 'grtts-input'
            for widget_type, widget_class in self.WIDGET_CLASSES:
                if isinstance(widget, widget_type):
                    css = widget_class
                    break
            existing = widget.attrs.get('class', '')
            if css and css not in existing.split():
                widget.attrs['class'] = (existing + ' ' + css).strip()
            if field.required:
                widget.attrs.setdefault('required', 'required')


class ApplicantRegistrationForm(StyledFormMixin, forms.ModelForm):
    """
    Registration form for applicants - creates User and ApplicantProfile
    """
    # Required fields
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your first name'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your surname'
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'your.email@example.com'
        })
    )
    phone = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': '+263 123 456 789'
        })
    )
    
    # Optional fields
    date_of_birth = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date'
        })
    )
    gender = forms.ChoiceField(
        choices=[('', 'Select Gender'), ('M', 'Male'), ('F', 'Female'), ('O', 'Other')],
        required=False,
        widget=forms.Select(attrs={})
    )
    nationality = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'e.g., Zimbabwean'
        })
    )
    address = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 2,
            'placeholder': 'Your physical address'
        })
    )
    city = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'City/Town'
        })
    )
    province = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Province'
        })
    )
    emergency_name = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Emergency contact full name'
        })
    )
    emergency_phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Emergency contact phone'
        })
    )
    emergency_relationship = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Relationship to contact'
        })
    )
    medical_conditions = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 2,
            'placeholder': 'Any medical conditions we should know about'
        })
    )
    dietary_requirements = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 2,
            'placeholder': 'Any dietary requirements'
        })
    )
    
    # File upload fields
    profile_photo = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'accept': 'image/*'
        }),
        help_text='Upload a profile photo (JPG, PNG). Max 5MB.'
    )
    
    id_document = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={
            'accept': '.pdf,.jpg,.jpeg,.png'
        }),
        help_text='Upload your ID or Passport (PDF, JPG, PNG). Max 10MB.'
    )
    
    cv = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={
            'accept': '.pdf,.doc,.docx,.txt'
        }),
        help_text='Upload your CV/Resume (PDF, DOC, DOCX, TXT). Max 10MB.'
    )
    
    certificates = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={
            'accept': '.pdf,.jpg,.jpeg,.png'
        }),
        help_text='Upload any relevant certificates (PDF, JPG, PNG). Max 10MB.'
    )

    class Meta:
        model = ApplicantProfile
        fields = []

    def clean_profile_photo(self):
        photo = self.cleaned_data.get('profile_photo')
        if photo:
            if photo.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Profile photo size cannot exceed 5MB.")
        return photo

    def clean_id_document(self):
        doc = self.cleaned_data.get('id_document')
        if doc:
            if doc.size > 10 * 1024 * 1024:
                raise forms.ValidationError("ID document size cannot exceed 10MB.")
        return doc

    def clean_cv(self):
        cv = self.cleaned_data.get('cv')
        if cv:
            if cv.size > 10 * 1024 * 1024:
                raise forms.ValidationError("CV size cannot exceed 10MB.")
        return cv

    def clean_certificates(self):
        cert = self.cleaned_data.get('certificates')
        if cert:
            if cert.size > 10 * 1024 * 1024:
                raise forms.ValidationError("Certificate size cannot exceed 10MB.")
        return cert


class NewsletterSignupForm(StyledFormMixin, forms.Form):
    """Form for newsletter subscription"""
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'Your email address',
            'aria-label': 'Email address'
        })
    )
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        return email
