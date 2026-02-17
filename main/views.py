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

# Models imports
from .models import (
    StudentInquiry, LandownerInquiry, EnthusiastInquiry, OtherInquiry,
    Course, Testimonial, DeploymentLocation, FAQ, ContactMessage,
    NewsletterSubscriber, NewsletterTracking, Certificate, CertificateVerificationLog,
    UserDocument,  # Add this import
)

# Utils and Forms
from .utils import send_contact_notification
from .forms import CustomUserCreationForm, NewsletterSignupForm

# Set up logging
logger = logging.getLogger(__name__)

# =============================================================================
# REGISTRATION VIEW (With File Uploads)
# =============================================================================

def register(request):
    """User registration view with file uploads"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            
            messages.success(
                request, 
                f'Thank you for registering, {user.first_name}! Your documents have been uploaded successfully.'
            )
            return redirect('main:home')
        else:
            # Form errors will be displayed in the template
            print(form.errors)  # For debugging
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'main/register.html', {'form': form})

# ... rest of your views.py remains the same ...
