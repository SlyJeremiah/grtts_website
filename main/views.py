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
                emergency_phone=form.cleaned_data.get('emergency_phone', ''),
                emergency_relationship=form.cleaned_data.get('emergency_relationship', ''),
                medical_conditions=form.cleaned_data.get('medical_conditions', ''),
                dietary_requirements=form.cleaned_data.get('dietary_requirements', '')
            )
            
            # Save uploaded files as UserDocument objects
            file_mappings = [
                ('profile_photo', 'photo', 'Profile photo'),
                ('id_document', 'id', 'ID document'),
                ('cv', 'cv', 'CV/Resume'),
                ('certificates', 'certificate', 'Certificate'),
            ]
            
            for field_name, doc_type, description in file_mappings:
                file = form.cleaned_data.get(field_name)
                if file:
                    UserDocument.objects.create(
                        user=user,
                        document_type=doc_type,
                        file=file,
                        description=f"{description} uploaded during registration for {email}"
                    )
            
            messages.success(
                request, 
                f'Thank you for registering, {first_name}! Your information has been saved.'
            )
            return redirect('main:home')
        else:
            print("FORM ERRORS:")
            print(form.errors)
            logger.error(f"Registration form errors: {form.errors}")
    else:
        form = ApplicantRegistrationForm()
    
    return render(request, 'main/register.html', {'form': form})

# =============================================================================
# EMAIL NOTIFICATION HELPER FUNCTIONS
# =============================================================================

def send_inquiry_notification(inquiry, inquiry_type):
    """Send email notification for any inquiry type and auto-reply to user"""
    try:
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
            subject = f"New {inquiry_type.title()} Inquiry"
            body = f"New inquiry received. Check admin panel for details."

        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            ['shanyaslym19@gmail.com'],
            fail_silently=False,
        )
        logger.info(f"Admin notification sent for {inquiry_type} inquiry from {inquiry.name}")
        
        auto_reply_subject = f"Thank You for Contacting GRTTS"
        auto_reply_body = f"""
Dear {inquiry.name},

Thank you for reaching out to GRTTS.

We have received your inquiry and one of our team members will get back to you within 48 hours.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
YOUR INQUIRY SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Type: {inquiry_type.title()} Inquiry
Name: {inquiry.name}
Email: {inquiry.email}
Phone: {getattr(inquiry, 'phone', 'Not provided')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Best regards,
The GRTTS Team
www.grtts.co.zw
"""
        
        send_mail(
            auto_reply_subject,
            auto_reply_body,
            settings.DEFAULT_FROM_EMAIL,
            [inquiry.email],
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
    featured_courses = Course.objects.filter(is_active=True)[:3]
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
    courses = Course.objects.filter(is_active=True)
    course_type = request.GET.get('type')
    
    if course_type:
        if course_type == 'basic':
            courses = courses.filter(course_type='BASIC')
        elif course_type == 'specialist':
            courses = courses.filter(course_type='SPECIALIST')
        elif course_type == 'advanced':
            courses = courses.filter(course_type='ADVANCED')
        elif course_type == 'tracking':
            courses = courses.filter(course_type='TRACKING')
    
    search_query = request.GET.get('q')
    if search_query:
        courses = courses.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
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
    context = {'course': course}
    return render(request, 'main/course_detail.html', context)


# =============================================================================
# LOCATION VIEWS
# =============================================================================

def locations(request):
    """Training and deployment locations with filtering"""
    locations = DeploymentLocation.objects.all()
    center = request.GET.get('center')
    
    if center:
        center_name = center.replace('-', ' ').title()
        locations = locations.filter(name__icontains=center_name)
    
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
        try:
            contact = ContactMessage(
                name=request.POST.get('name'),
                email=request.POST.get('email'),
                phone=request.POST.get('phone', ''),
                subject=request.POST.get('subject', 'Website Contact Form'),
                message=request.POST.get('message')
            )
            contact.save()
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
        send_inquiry_notification(inquiry, 'student')
        return JsonResponse({'success': True, 'message': 'Your student inquiry has been submitted successfully.'})
    except Exception as e:
        logger.error(f"Student inquiry error: {e}")
        return JsonResponse({'success': False, 'message': 'Error submitting form.'}, status=400)


@require_POST
def inquiry_landowner(request):
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
        send_inquiry_notification(inquiry, 'landowner')
        return JsonResponse({'success': True, 'message': 'Your landowner inquiry has been submitted successfully.'})
    except Exception as e:
        logger.error(f"Landowner inquiry error: {e}")
        return JsonResponse({'success': False, 'message': 'Error submitting form.'}, status=400)


@require_POST
def inquiry_enthusiast(request):
    try:
        inquiry = EnthusiastInquiry.objects.create(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            interest=request.POST.get('interest'),
            background=request.POST.get('background', ''),
            availability=request.POST.get('availability', ''),
            message=request.POST.get('message', ''),
        )
        send_inquiry_notification(inquiry, 'enthusiast')
        return JsonResponse({'success': True, 'message': 'Your enthusiast inquiry has been submitted successfully.'})
    except Exception as e:
        logger.error(f"Enthusiast inquiry error: {e}")
        return JsonResponse({'success': False, 'message': 'Error submitting form.'}, status=400)


@require_POST
def inquiry_other(request):
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
        send_inquiry_notification(inquiry, 'other')
        return JsonResponse({'success': True, 'message': 'Your inquiry has been submitted successfully.'})
    except Exception as e:
        logger.error(f"Other inquiry error: {e}")
        return JsonResponse({'success': False, 'message': 'Error submitting form.'}, status=400)


# =============================================================================
# NEWSLETTER VIEWS
# =============================================================================

@require_POST
@csrf_protect
def newsletter_signup(request):
    try:
        email = request.POST.get('email', '').strip()
        
        if not email:
            return JsonResponse({'success': False, 'message': 'Email address is required.'}, status=400)
        
        try:
            validate_email(email)
        except ValidationError:
            return JsonResponse({'success': False, 'message': 'Please enter a valid email address.'}, status=400)
        
        subscriber, created = NewsletterSubscriber.objects.get_or_create(
            email=email,
            defaults={
                'ip_address': request.META.get('REMOTE_ADDR', ''),
                'source': 'website_footer'
            }
        )
        
        if created:
            message = 'Thank you for subscribing to our newsletter!'
            send_newsletter_notification(email)
        else:
            if not subscriber.is_active:
                subscriber.is_active = True
                subscriber.ip_address = request.META.get('REMOTE_ADDR', '')
                subscriber.save()
                message = 'Your subscription has been reactivated!'
                send_newsletter_notification(email)
            else:
                return JsonResponse({'success': False, 'message': 'This email is already subscribed.'}, status=400)
        
        return JsonResponse({'success': True, 'message': message})
        
    except Exception as e:
        logger.error(f"Newsletter signup error: {e}")
        return JsonResponse({'success': False, 'message': 'Server error. Please try again later.'}, status=500)


@csrf_exempt
def track_newsletter_open(request, tracking_id):
    try:
        tracking = NewsletterTracking.objects.get(id=tracking_id)
        tracking.opened_at = timezone.now()
        tracking.save()
        pixel = b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b'
        return HttpResponse(pixel, content_type='image/gif')
    except NewsletterTracking.DoesNotExist:
        return HttpResponse(status=404)


def unsubscribe_newsletter(request, email):
    try:
        subscriber = NewsletterSubscriber.objects.get(email=email)
        subscriber.is_active = False
        subscriber.unsubscribed_at = timezone.now()
        subscriber.save()
        return render(request, 'main/unsubscribe_confirmed.html', {'email': email})
    except NewsletterSubscriber.DoesNotExist:
        return render(request, 'main/unsubscribe_not_found.html')


def newsletter_test(request):
    return JsonResponse({'success': True, 'message': 'Newsletter test endpoint'})


def newsletter_test_page(request):
    return render(request, 'main/newsletter_test.html')


# =============================================================================
# CERTIFICATE VIEWS
# =============================================================================

def verify_certificate(request):
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
    certificate = get_object_or_404(Certificate, certificate_number=cert_number, is_valid=True)
    
    CertificateVerificationLog.objects.create(
        certificate=certificate,
        ip_address=request.META.get('REMOTE_ADDR'),
        user_agent=request.META.get('HTTP_USER_AGENT', ''),
        successful=True
    )
    
    return render(request, 'main/certificate_detail.html', {'certificate': certificate})


# =============================================================================
# EMAIL TEST VIEW
# =============================================================================

def test_email(request):
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
