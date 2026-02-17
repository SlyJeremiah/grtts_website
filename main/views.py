from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect, csrf_exempt
from django.views.decorators.http import require_POST
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils import timezone
import traceback
import uuid
import logging
import json

# Models imports - Use custom User model
from .models import (
    StudentInquiry, LandownerInquiry, EnthusiastInquiry, OtherInquiry,
    Course, Testimonial, DeploymentLocation, FAQ, ContactMessage,
    NewsletterSubscriber, NewsletterTracking, Certificate, CertificateVerificationLog,
    UserDocument, ApplicantProfile, CourseApplication, User  # Import custom User
)

# Utils and Forms
from .utils import send_contact_notification
from .forms import ApplicantRegistrationForm, NewsletterSignupForm

# Set up logging
logger = logging.getLogger(__name__)

# =============================================================================
# APPLICANT REGISTRATION VIEW (Creates User + ApplicantProfile)
# =============================================================================

def register(request):
    """Applicant registration view - creates User and ApplicantProfile"""
    if request.method == 'POST':
        form = ApplicantRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            # Get cleaned data
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            
            # Create username from email
            username = email.split('@')[0]
            
            # Check if user already exists
            if User.objects.filter(email=email).exists():
                messages.error(request, 'A user with this email already exists.')
                return render(request, 'main/register.html', {'form': form})
            
            # Create the User (using custom User model)
            user = User.objects.create_user(
                username=username,
                email=email,
                password=None,
                first_name=first_name,
                last_name=last_name
            )
            user.set_unusable_password()
            user.phone = phone  # Save phone to User model
            user.user_type = 'applicant'  # Set user type
            user.save()
            
            # Create the ApplicantProfile
            applicant = ApplicantProfile.objects.create(
                user=user,
                date_of_birth=form.cleaned_data.get('date_of_birth'),
                gender=form.cleaned_data.get('gender'),
                nationality=form.cleaned_data.get('nationality', ''),
                address=form.cleaned_data.get('address', ''),
                city=form.cleaned_data.get('city', ''),
                province=form.cleaned_data.get('province', ''),
                emergency_name=form.cleaned_data.get('emergency_name', ''),
                emergency_phone
