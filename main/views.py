from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from .forms import CustomUserCreationForm
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect, csrf_exempt
from django.views.decorators.http import require_POST
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
import traceback
import uuid
import logging
from .models import StudentInquiry, LandownerInquiry, EnthusiastInquiry, OtherInquiry
from django.views.decorators.http import require_POST
import json

from .models import (
    Course, Testimonial, DeploymentLocation, FAQ, ContactMessage,
    NewsletterSubscriber, NewsletterTracking, Certificate, CertificateVerificationLog,
    ApplicantProfile, CourseApplication
)
from .utils import send_contact_notification
from .forms import NewsletterSignupForm, CourseApplicationForm, ApplicantProfileForm

# Set up logging
logger = logging.getLogger(__name__)

# =============================================================================
# AUTHENTICATION VIEWS
# =============================================================================
# =============================================================================
# REGISTRATION VIEW (No Login Required)
# =============================================================================

def register(request):
    """User registration view - no login required, just sign up"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(
                request, 
                f'Thank you for registering, {user.first_name}! You can now explore our site.'
            )
            return redirect('main:home')
        else:
            # Form errors will be displayed in the template
            print(form.errors)  # For debugging
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'main/register.html', {'form': form})
# =============================================================================
# EMAIL NOTIFICATION HELPER FUNCTIONS
# =============================================================================

def send_inquiry_notification(inquiry, inquiry_type):
    """Send email notification for any inquiry type and auto-reply to user"""
    try:
        # ===== EMAIL TO ADMIN (YOU) =====
        # Prepare email subject and body based on inquiry type
        if inquiry_type == 'student':
            subject = f"New Student Inquiry: {inquiry.name}"
            body = f"""
NEW STUDENT INQUIRY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Name: {inquiry.name}
Email: {inquiry.email}
Phone: {inquiry.phone}
Age: {inquiry.age}
Nationality: {inquiry.nationality}
Education: {inquiry.education or 'Not specified'}
Course Interested: {inquiry.course}
Intake: {inquiry.intake or 'Not specified'}
Experience: {inquiry.experience or 'Not specified'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Submitted: {timezone.now().strftime('%Y-%m-%d %H:%M')}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        elif inquiry_type == 'landowner':
            subject = f"New Landowner Inquiry: {inquiry.name}"
            body = f"""
NEW LANDOWNER INQUIRY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Name: {inquiry.name}
Email: {inquiry.email}
Phone: {inquiry.phone}
Organization: {inquiry.organization or 'Not specified'}
Service Needed: {inquiry.service}
Property Size: {inquiry.property_size or 'Not specified'} hectares
Property Location: {inquiry.property_location or 'Not specified'}

CONCERNS:
• Poaching: {'✓' if inquiry.concerns_poaching else '✗'}
• Human-Wildlife Conflict: {'✓' if inquiry.concerns_human_wildlife else '✗'}
• Livestock Protection: {'✓' if inquiry.concerns_livestock else '✗'}
• Trespassing: {'✓' if inquiry.concerns_trespassing else '✗'}

Details: {inquiry.details or 'No additional details'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Submitted: {timezone.now().strftime('%Y-%m-%d %H:%M')}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        elif inquiry_type == 'enthusiast':
            subject = f"New Enthusiast Inquiry: {inquiry.name}"
            body = f"""
NEW ENTHUSIAST INQUIRY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Name: {inquiry.name}
Email: {inquiry.email}
Interest: {inquiry.interest}
Background: {inquiry.background or 'Not specified'}
Availability: {inquiry.availability or 'Not specified'}

Message: {inquiry.message or 'No message'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Submitted: {timezone.now().strftime('%Y-%m-%d %H:%M')}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        elif inquiry_type == 'other':
            subject = f"New General Inquiry: {inquiry.name}"
            body = f"""
NEW GENERAL INQUIRY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Name: {inquiry.name}
Email: {inquiry.email}
Phone: {inquiry.phone or 'Not provided'}
Organization: {inquiry.organization or 'Not provided'}
Category: {inquiry.category}
Subject: {inquiry.subject}
Urgency: {inquiry.urgency}

Message:
{inquiry.message}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Submitted: {timezone.now().strftime('%Y-%m-%d %H:%M')}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        else:
            # Generic for any other type
            subject = f"New {inquiry_type.title()} Inquiry"
            body = f"New inquiry received. Check admin panel for details."

        # Send email to admin
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            ['shanyaslym19@gmail.com'],  # Your email
            fail_silently=False,
        )
        logger.info(f"Admin notification sent for {inquiry_type} inquiry from {inquiry.name}")
        
        # ===== AUTO-REPLY TO USER =====
        auto_reply_subject = f"Thank You for Contacting GRTTS"
        auto_reply_body = f"""
Dear {inquiry.name},

Thank you for reaching out to GRTTS (Game Ranger & Tracker Training Specialist).

We have received your inquiry and one of our team members will get back to you within 48 hours. Your inquiry details have been saved and we'll respond as soon as possible.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
YOUR INQUIRY SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Type: {inquiry_type.title()} Inquiry
Name: {inquiry.name}
Email: {inquiry.email}
Phone: {getattr(inquiry, 'phone', 'Not provided')}

We will contact you shortly at the email or phone number provided.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
In the meantime, you can:
• Visit our website: https://grtts-website.vercel.app
• Check our training programs: https://grtts-website.vercel.app/courses
• Read our FAQ: https://grtts-website.vercel.app/faq
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Best regards,
The GRTTS Team
Training That Saves Lives
www.grtts.co.zw
"""
        
        send_mail(
            auto_reply_subject,
            auto_reply_body,
            settings.DEFAULT_FROM_EMAIL,
            [inquiry.email],  # Send to the user who made the inquiry
            fail_silently=False,
        )
        logger.info(f"Auto-reply sent to {inquiry.email}")
        
        return True
        
    except Exception as e:
        logger.error(f"Failed to send email for {inquiry_type} inquiry: {e}")
        return False


def send_contact_notification(contact):
    """Send notification for contact form submissions"""
    try:
        subject = f"New Contact Message: {contact.subject}"
        body = f"""
NEW CONTACT MESSAGE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Name: {contact.name}
Email: {contact.email}
Phone: {contact.phone or 'Not provided'}
Subject: {contact.subject}

Message:
{contact.message}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Submitted: {timezone.now().strftime('%Y-%m-%d %H:%M')}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            ['shanyaslym19@gmail.com'],
            fail_silently=False,
        )
        logger.info(f"Email notification sent for contact from {contact.name}")
        return True
    except Exception as e:
        logger.error(f"Failed to send contact email: {e}")
        return False


def send_newsletter_notification(email):
    """Send notification when someone subscribes to newsletter"""
    try:
        subject = "New Newsletter Subscriber"
        body = f"""
NEW NEWSLETTER SUBSCRIBER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Email: {email}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Time: {timezone.now().strftime('%Y-%m-%d %H:%M')}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            ['shanyaslym19@gmail.com'],
            fail_silently=False,
        )
        logger.info(f"Email notification sent for newsletter subscriber: {email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send newsletter notification: {e}")
        return False


# =============================================================================
# HOME & BASIC PAGES
# =============================================================================

def home(request):
    """Home page view"""
    # Get featured courses (limit to 3)
    featured_courses = Course.objects.filter(is_active=True)[:3]
    
    # Get active testimonials
    testimonials = Testimonial.objects.filter(is_active=True)[:3]
    
    context = {
        'featured_courses': featured_courses,
        'testimonials': testimonials,
        'stats': {
            'rangers_trained': 500,
            'hectares_protected': 45000,
            'locations': 5,
            'year_founded': 2017
        }
    }
    return render(request, 'main/home.html', context)


def about(request):
    """About us page"""
    return render(request, 'main/about.html')


def faq(request):
    """FAQ page"""
    faqs = FAQ.objects.filter(is_active=True)
    return render(request, 'main/faq.html', {'faqs': faqs})


# =============================================================================
# COURSE VIEWS
# =============================================================================

def courses(request):
    """All courses listing with filtering"""
    # Get all active courses
    courses = Course.objects.filter(is_active=True)
    
    # Get filter type from URL query parameters
    course_type = request.GET.get('type')
    
    # Apply filter if specified
    if course_type:
        if course_type == 'basic':
            courses = courses.filter(course_type='BASIC')
        elif course_type == 'specialist':
            courses = courses.filter(course_type='SPECIALIST')
        elif course_type == 'advanced':
            courses = courses.filter(course_type='ADVANCED')
        elif course_type == 'tracking':
            courses = courses.filter(course_type='TRACKING')
    
    # Get search query if any
    search_query = request.GET.get('q')
    if search_query:
        courses = courses.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    # Organize courses by type for display
    context = {
        'courses': courses,
        'basic_courses': courses.filter(course_type='BASIC'),
        'specialist_courses': courses.filter(course_type='SPECIALIST'),
        'advanced_courses': courses.filter(course_type='ADVANCED'),
        'tracking_courses': courses.filter(course_type='TRACKING'),
        'current_filter': course_type,
        'search_query': search_query,
        'course_types': Course.COURSE_TYPES,
    }
    return render(request, 'main/courses.html', context)


def course_detail(request, course_id):
    """Individual course detail"""
    course = get_object_or_404(Course, id=course_id, is_active=True)
    
    # Check if user has already applied (if logged in)
    existing_application = None
    if request.user.is_authenticated:
        try:
            applicant_profile = ApplicantProfile.objects.get(user=request.user)
            existing_application = CourseApplication.objects.filter(
                applicant=applicant_profile,
                course=course
            ).first()
        except ApplicantProfile.DoesNotExist:
            pass
    
    context = {
        'course': course,
        'existing_application': existing_application,
    }
    return render(request, 'main/course_detail.html', context)


# =============================================================================
# LOCATION VIEWS
# =============================================================================

def locations(request):
    """Training and deployment locations with filtering"""
    # Get all locations
    locations = DeploymentLocation.objects.all()
    
    # Get filter from URL query parameters
    center = request.GET.get('center')
    
    # Apply filter if specified
    if center:
        # Convert URL-friendly name to proper case for filtering
        center_name = center.replace('-', ' ').title()
        locations = locations.filter(name__icontains=center_name)
    
    # Separate training centers and deployment locations
    training_centers = locations.filter(is_training_center=True)
    deployment_sites = locations.filter(is_deployment_location=True)
    
    context = {
        'locations': locations,
        'training_centers': training_centers,
        'deployment_sites': deployment_sites,
        'current_filter': center,
    }
    return render(request, 'main/locations.html', context)


def location_detail(request, location_id):
    """Individual location detail page with gallery"""
    location = get_object_or_404(DeploymentLocation, id=location_id)
    other_locations = DeploymentLocation.objects.exclude(id=location_id)[:5]
    
    context = {
        'location': location,
        'locations': other_locations,
    }
    return render(request, 'main/location_detail.html', context)


# =============================================================================
# CONTACT VIEW
# =============================================================================

@ensure_csrf_cookie
def contact(request):
    """Contact page with form"""
    # Check for course parameter in URL
    course_param = request.GET.get('course')
    initial_subject = ''
    
    if course_param:
        if course_param == 'basic':
            initial_subject = 'Inquiry about Basic Ranger Course'
        elif course_param == 'specialist':
            initial_subject = 'Inquiry about Specialist Courses'
        elif course_param == 'advanced':
            initial_subject = 'Inquiry about Advanced Ranger Course'
        elif course_param == 'tracking':
            initial_subject = 'Inquiry about Tracking Course'
    
    if request.method == 'POST':
        # Save to database
        try:
            contact = ContactMessage(
                name=request.POST.get('name'),
                email=request.POST.get('email'),
                phone=request.POST.get('phone', ''),
                subject=request.POST.get('subject', 'Website Contact Form'),
                message=request.POST.get('message')
            )
            contact.save()
            
            # Send email notification
            send_contact_notification(contact)
            
            messages.success(request, 'Thank you for your message! We will contact you soon.')
            
        except Exception as e:
            logger.error(f"Contact form error: {e}")
            messages.error(request, 'There was an error sending your message. Please try again.')
        
        return redirect('main:contact')
    
    context = {
        'initial_subject': initial_subject,
        'faqs': FAQ.objects.filter(is_active=True)[:5],
    }
    return render(request, 'main/contact.html', context)


def inquiry_page(request):
    """Main inquiry page with all forms"""
    return render(request, 'main/inquiry.html')


@require_POST
def inquiry_student(request):
    """Process student inquiry"""
    try:
        inquiry = StudentInquiry.objects.create(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            age=request.POST.get('age'),
            nationality=request.POST.get('nationality'),
            education=request.POST.get('education', ''),
            course=request.POST.get('course'),
            intake=request.POST.get('intake', ''),
            experience=request.POST.get('experience', ''),
        )
        
        # Send email notification
        send_inquiry_notification(inquiry, 'student')
        
        return JsonResponse({
            'success': True,
            'message': 'Your student inquiry has been submitted successfully. We will contact you within 48 hours.'
        })
    except Exception as e:
        logger.error(f"Student inquiry error: {e}")
        return JsonResponse({
            'success': False,
            'message': f'Error submitting form. Please try again.'
        }, status=400)


@require_POST
def inquiry_landowner(request):
    """Process landowner inquiry"""
    try:
        inquiry = LandownerInquiry.objects.create(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            organization=request.POST.get('organization', ''),
            service=request.POST.get('service'),
            property_size=request.POST.get('property_size') or None,
            property_location=request.POST.get('property_location', ''),
            concerns_poaching=bool(request.POST.get('concerns_poaching')),
            concerns_human_wildlife=bool(request.POST.get('concerns_human_wildlife')),
            concerns_livestock=bool(request.POST.get('concerns_livestock')),
            concerns_trespassing=bool(request.POST.get('concerns_trespassing')),
            details=request.POST.get('details', ''),
        )
        
        # Send email notification
        send_inquiry_notification(inquiry, 'landowner')
        
        return JsonResponse({
            'success': True,
            'message': 'Your landowner inquiry has been submitted successfully. We will contact you within 48 hours.'
        })
    except Exception as e:
        logger.error(f"Landowner inquiry error: {e}")
        return JsonResponse({
            'success': False,
            'message': f'Error submitting form. Please try again.'
        }, status=400)


@require_POST
def inquiry_enthusiast(request):
    """Process enthusiast inquiry"""
    try:
        inquiry = EnthusiastInquiry.objects.create(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            interest=request.POST.get('interest'),
            background=request.POST.get('background', ''),
            availability=request.POST.get('availability', ''),
            message=request.POST.get('message', ''),
        )
        
        # Send email notification
        send_inquiry_notification(inquiry, 'enthusiast')
        
        return JsonResponse({
            'success': True,
            'message': 'Your enthusiast inquiry has been submitted successfully. We will contact you within 48 hours.'
        })
    except Exception as e:
        logger.error(f"Enthusiast inquiry error: {e}")
        return JsonResponse({
            'success': False,
            'message': f'Error submitting form. Please try again.'
        }, status=400)


@require_POST
def inquiry_other(request):
    """Process general inquiry"""
    try:
        inquiry = OtherInquiry.objects.create(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone', ''),
            organization=request.POST.get('organization', ''),
            category=request.POST.get('category'),
            subject=request.POST.get('subject'),
            message=request.POST.get('message'),
            urgency=request.POST.get('urgency', 'normal'),
        )
        
        # Send email notification
        send_inquiry_notification(inquiry, 'other')
        
        return JsonResponse({
            'success': True,
            'message': 'Your inquiry has been submitted successfully. We will respond within 48 hours.'
        })
    except Exception as e:
        logger.error(f"Other inquiry error: {e}")
        return JsonResponse({
            'success': False,
            'message': f'Error submitting form. Please try again.'
        }, status=400)


# =============================================================================
# NEWSLETTER VIEWS
# =============================================================================

@require_POST
@csrf_protect
def newsletter_signup(request):
    """AJAX endpoint for newsletter signup"""
    print("="*50)
    print("📧 Newsletter signup attempted")
    print(f"Time: {timezone.now()}")
    print(f"Method: {request.method}")
    print(f"POST data: {request.POST}")
    print(f"AJAX: {request.headers.get('X-Requested-With')}")
    print("="*50)
    
    try:
        # Get email from POST
        email = request.POST.get('email', '').strip()
        
        if not email:
            return JsonResponse({
                'success': False,
                'message': 'Email address is required.'
            }, status=400)
        
        # Validate email format
        try:
            validate_email(email)
        except ValidationError:
            return JsonResponse({
                'success': False,
                'message': 'Please enter a valid email address.'
            }, status=400)
        
        # Check if subscriber exists
        subscriber, created = NewsletterSubscriber.objects.get_or_create(
            email=email,
            defaults={
                'ip_address': request.META.get('REMOTE_ADDR', ''),
                'source': 'website_footer'
            }
        )
        
        print(f"Subscriber exists: {not created}")
        print(f"Is active: {subscriber.is_active}")
        
        if created:
            # New subscriber
            message = 'Thank you for subscribing to our newsletter!'
            print(f"✅ New subscriber created: {email}")
            
            # Send notification email to admin
            send_newsletter_notification(email)
            
        else:
            if not subscriber.is_active:
                # Reactivate
                subscriber.is_active = True
                subscriber.ip_address = request.META.get('REMOTE_ADDR', '')
                subscriber.save()
                message = 'Your subscription has been reactivated!'
                print(f"🔄 Subscriber reactivated: {email}")
                
                # Send notification email to admin
                send_newsletter_notification(email)
                
            else:
                # Already active
                print(f"⚠️ Already subscribed: {email}")
                return JsonResponse({
                    'success': False,
                    'message': 'This email is already subscribed to our newsletter.'
                }, status=400)
        
        return JsonResponse({
            'success': True,
            'message': message
        })
        
    except Exception as e:
        # Print full error for debugging
        print("❌ ERROR in newsletter_signup:")
        print(traceback.format_exc())
        logger.error(f"Newsletter signup error: {e}")
        
        return JsonResponse({
            'success': False,
            'message': f'Server error. Please try again later.'
        }, status=500)


@csrf_exempt
def track_newsletter_open(request, tracking_id):
    """Track newsletter opens via pixel"""
    try:
        tracking = NewsletterTracking.objects.get(id=tracking_id)
        tracking.opened_at = timezone.now()
        tracking.save()
        
        # Update campaign stats
        if tracking.campaign:
            tracking.campaign.opens_count += 1
            tracking.campaign.save()
        
        # Return 1x1 transparent GIF
        pixel = b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b'
        return HttpResponse(pixel, content_type='image/gif')
    except NewsletterTracking.DoesNotExist:
        return HttpResponse(status=404)


def unsubscribe_newsletter(request, email):
    """Unsubscribe from newsletter"""
    try:
        subscriber = NewsletterSubscriber.objects.get(email=email)
        subscriber.is_active = False
        subscriber.unsubscribed_at = timezone.now()
        subscriber.save()
        
        return render(request, 'main/unsubscribe_confirmed.html', {'email': email})
    except NewsletterSubscriber.DoesNotExist:
        return render(request, 'main/unsubscribe_not_found.html')


def newsletter_test(request):
    """Simple test endpoint for debugging newsletter signup"""
    print(f"🔍 Test endpoint accessed! Method: {request.method}")
    print(f"POST data: {request.POST}")
    print(f"Headers: {request.headers}")
    
    if request.method == 'POST':
        email = request.POST.get('email', '')
        
        return JsonResponse({
            'success': True,
            'message': f'Test successful! Email received: {email}',
            'debug': {
                'method': request.method,
                'email': email,
                'csrf_token': request.POST.get('csrfmiddlewaretoken', 'Not sent'),
                'ajax': request.headers.get('X-Requested-With', 'Not AJAX')
            }
        })
    
    return JsonResponse({
        'success': False,
        'message': 'This endpoint requires a POST request. Use it to test newsletter signup.',
        'usage': 'Send a POST request with email parameter'
    })


def newsletter_test_page(request):
    """Simple page to test newsletter"""
    return render(request, 'main/newsletter_test.html')


# =============================================================================
# CERTIFICATE VIEWS
# =============================================================================

def verify_certificate(request):
    """Certificate verification page"""
    certificate = None
    verified = False
    
    if request.method == 'POST':
        cert_number = request.POST.get('certificate_number')
        try:
            certificate = Certificate.objects.get(
                certificate_number=cert_number,
                is_valid=True
            )
            certificate.view_count += 1
            certificate.save()
            
            # Log verification
            CertificateVerificationLog.objects.create(
                certificate=certificate,
                ip_address=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                successful=True
            )
            
            verified = True
        except Certificate.DoesNotExist:
            messages.error(request, 'Invalid certificate number or certificate not found')
    
    context = {
        'certificate': certificate,
        'verified': verified,
    }
    return render(request, 'main/verify_certificate.html', context)


def certificate_detail(request, cert_number):
    """Public certificate detail page"""
    certificate = get_object_or_404(Certificate, certificate_number=cert_number, is_valid=True)
    
    # Log view
    CertificateVerificationLog.objects.create(
        certificate=certificate,
        ip_address=request.META.get('REMOTE_ADDR'),
        user_agent=request.META.get('HTTP_USER_AGENT', ''),
        successful=True
    )
    
    return render(request, 'main/certificate_detail.html', {'certificate': certificate})


# =============================================================================
# COURSE APPLICATION VIEWS
# =============================================================================

@login_required
def create_profile(request):
    """Create applicant profile (first step before applying)"""
    # Check if profile already exists
    try:
        profile = ApplicantProfile.objects.get(user=request.user)
        messages.info(request, 'You already have a profile. You can edit it here.')
        return redirect('main:edit_profile')
    except ApplicantProfile.DoesNotExist:
        pass
    
    if request.method == 'POST':
        form = ApplicantProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, 'Your profile has been created successfully! You can now apply for courses.')
            return redirect('main:courses')
    else:
        form = ApplicantProfileForm()
    
    return render(request, 'main/create_profile.html', {
        'form': form,
    })


@login_required
def edit_profile(request):
    """Edit applicant profile"""
    try:
        profile = ApplicantProfile.objects.get(user=request.user)
    except ApplicantProfile.DoesNotExist:
        return redirect('main:create_profile')  # FIXED: Added main: namespace
    
    if request.method == 'POST':
        form = ApplicantProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('main:my_applications')  # FIXED: Added main: namespace
    else:
        form = ApplicantProfileForm(instance=profile)
    
    return render(request, 'main/edit_profile.html', {
        'form': form,
        'profile': profile,
    })


@login_required
def apply_for_course(request, course_id):
    """Apply for a specific course"""
    course = get_object_or_404(Course, id=course_id, is_active=True)
    
    # Get or create applicant profile
    try:
        applicant_profile = ApplicantProfile.objects.get(user=request.user)
    except ApplicantProfile.DoesNotExist:
        messages.warning(request, 'Please complete your profile before applying.')
        return redirect('main:create_profile')  # FIXED: Added main: namespace
    
    # Check if already applied
    existing_application = CourseApplication.objects.filter(
        applicant=applicant_profile,
        course=course
    ).first()
    
    if existing_application:
        if existing_application.status == 'draft':
            messages.info(request, 'You have a draft application. Please complete it.')
            return redirect('main:edit_application', application_id=existing_application.id)  # FIXED: Added main: namespace
        else:
            messages.warning(request, f'You have already applied for {course.title}. You can track your application in your dashboard.')
            return redirect('main:application_detail', application_id=existing_application.id)  # FIXED: Added main: namespace
    
    if request.method == 'POST':
        form = CourseApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.applicant = applicant_profile
            application.course = course
            application.status = 'submitted'
            application.save()
            
            # Send confirmation emails
            try:
                # Email to applicant
                subject = f"Application Received: {course.title}"
                message = f"""
Dear {request.user.get_full_name() or request.user.username},

Thank you for applying for {course.title} at GRTTS.

Your application has been submitted successfully. You can track its status in your dashboard:
https://grtts-website.vercel.app/applications/

Application Details:
- Course: {course.title}
- Application Number: {application.application_number}
- Submitted: {application.application_date.strftime('%Y-%m-%d %H:%M')}

We will review your application and contact you within 48 hours.

Best regards,
GRTTS Team
Training That Saves Lives
                """
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [request.user.email],
                    fail_silently=False,
                )
                logger.info(f"Application confirmation email sent to {request.user.email}")
            except Exception as e:
                logger.error(f"Application confirmation email failed: {e}")
            
            # Email to admin
            try:
                admin_subject = f"New Course Application: {course.title}"
                admin_message = f"""
New application received:

Applicant: {request.user.get_full_name() or request.user.username}
Email: {request.user.email}
Course: {course.title}
Application Number: {application.application_number}

Check admin panel for full details and uploaded documents.
                """
                send_mail(
                    admin_subject,
                    admin_message,
                    settings.DEFAULT_FROM_EMAIL,
                    ['shanyaslym19@gmail.com'],
                    fail_silently=False,
                )
                logger.info("Admin notification sent for new application")
            except Exception as e:
                logger.error(f"Admin application notification failed: {e}")
            
            messages.success(request, 'Your application has been submitted successfully! Check your email for confirmation.')
            return redirect('main:application_detail', application_id=application.id)  # FIXED: Added main: namespace
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CourseApplicationForm()
    
    return render(request, 'main/apply_course.html', {
        'course': course,
        'form': form,
        'applicant_profile': applicant_profile,
    })


@login_required
def edit_application(request, application_id):
    """Edit a draft application"""
    try:
        applicant_profile = ApplicantProfile.objects.get(user=request.user)
        application = get_object_or_404(
            CourseApplication,
            id=application_id,
            applicant=applicant_profile,
            status='draft'
        )
    except ApplicantProfile.DoesNotExist:
        messages.error(request, 'Profile not found.')
        return redirect('main:create_profile')  # FIXED: Added main: namespace
    
    if request.method == 'POST':
        form = CourseApplicationForm(request.POST, request.FILES, instance=application)
        if form.is_valid():
            application = form.save(commit=False)
            application.status = 'submitted'
            application.save()
            
            # Send confirmation emails (similar to above)
            try:
                subject = f"Application Submitted: {application.course.title}"
                message = f"""
Dear {request.user.get_full_name() or request.user.username},

Your application for {application.course.title} has been submitted successfully.

Application Number: {application.application_number}

You can track your application status in your dashboard.

Best regards,
GRTTS Team
                """
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [request.user.email],
                    fail_silently=False,
                )
            except Exception as e:
                logger.error(f"Application submission email failed: {e}")
            
            messages.success(request, 'Your application has been submitted successfully!')
            return redirect('main:application_detail', application_id=application.id)  # FIXED: Added main: namespace
    else:
        form = CourseApplicationForm(instance=application)
    
    return render(request, 'main/apply_course.html', {
        'course': application.course,
        'form': form,
        'applicant_profile': applicant_profile,
        'is_editing': True,
        'application': application,
    })


@login_required
def my_applications(request):
    """List all applications for the logged-in user"""
    try:
        applicant_profile = ApplicantProfile.objects.get(user=request.user)
        applications = CourseApplication.objects.filter(applicant=applicant_profile)
        
        # Count by status for dashboard stats
        stats = {
            'draft': applications.filter(status='draft').count(),
            'submitted': applications.filter(status='submitted').count(),
            'under_review': applications.filter(status='under_review').count(),
            'accepted': applications.filter(status='accepted').count(),
            'waitlisted': applications.filter(status='waitlisted').count(),
            'rejected': applications.filter(status='rejected').count(),
            'enrolled': applications.filter(status='enrolled').count(),
            'completed': applications.filter(status='completed').count(),
            'total': applications.count(),
        }
    except ApplicantProfile.DoesNotExist:
        applications = []
        stats = {k: 0 for k in ['draft', 'submitted', 'under_review', 'accepted', 
                                 'waitlisted', 'rejected', 'enrolled', 'completed', 'total']}
    
    return render(request, 'main/my_applications.html', {
        'applications': applications,
        'stats': stats,
    })


@login_required
def application_detail(request, application_id):
    """View details of a specific application"""
    try:
        applicant_profile = ApplicantProfile.objects.get(user=request.user)
        application = get_object_or_404(
            CourseApplication,
            id=application_id,
            applicant=applicant_profile
        )
    except ApplicantProfile.DoesNotExist:
        messages.error(request, 'Application not found.')
        return redirect('main:my_applications')  # FIXED: Added main: namespace
    
    return render(request, 'main/application_detail.html', {
        'application': application,
    })


# =============================================================================
# EMAIL TEST VIEW
# =============================================================================

def test_email(request):
    """Simple test to verify email sending"""
    try:
        send_mail(
            'Test Email from GRTTS',
            'This is a test email to verify SMTP settings.',
            settings.DEFAULT_FROM_EMAIL,
            ['shanyaslym19@gmail.com'],
            fail_silently=False,
        )
        return HttpResponse('Email sent successfully! Check your inbox.')
    except Exception as e:
        logger.error(f"Test email error: {e}")
        return HttpResponse(f'Error sending email: {str(e)}')


# =============================================================================
# PAYMENT VIEWS (COMMENTED OUT)
# =============================================================================

"""
def donation_page(request):
    # Donation page with payment options
    payment_methods = PaymentMethod.objects.filter(is_active=True)
    
    context = {
        'payment_methods': payment_methods,
        'donation_amounts': [10, 20, 50, 100, 500, 1000],
    }
    return render(request, 'main/donation.html', context)

def process_donation(request):
    # Process donation payment
    if request.method == 'POST':
        amount = request.POST.get('amount')
        payment_method_id = request.POST.get('payment_method')
        donor_name = request.POST.get('donor_name')
        donor_email = request.POST.get('donor_email')
        donor_phone = request.POST.get('donor_phone')
        
        # Create donation record
        donation = Donation.objects.create(
            transaction_id=str(uuid.uuid4()),
            amount=amount,
            payment_method_id=payment_method_id,
            donor_name=donor_name,
            donor_email=donor_email,
            donor_phone=donor_phone,
            status='pending'
        )
        
        messages.success(request, 'Thank you for your donation! You will receive a confirmation soon.')
        return redirect('donation')
    
    return redirect('donation_page')
"""
