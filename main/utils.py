from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from .models import NewsletterSubscriber, NewsletterCampaign, NewsletterTracking
import hashlib
import time
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone
import logging
import traceback

def send_contact_notification(contact_message):
    """Send email notification for new contact form submission"""
    subject = f"New Contact Form Message: {contact_message.subject}"
    
    # HTML email content
    html_content = render_to_string('emails/contact_notification.html', {
        'contact': contact_message,
        'site_url': settings.SITE_URL,
    })
    
    # Plain text version
    text_content = strip_tags(html_content)
    
    # Send to admin
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=settings.ADMIN_EMAILS,
        reply_to=[contact_message.email],
    )
    email.attach_alternative(html_content, "text/html")
    email.send()
    
    # Send auto-reply to user
    user_subject = "Thank you for contacting GRTTS"
    user_html = render_to_string('emails/contact_autoreply.html', {
        'name': contact_message.name,
        'site_url': settings.SITE_URL,
    })
    user_text = strip_tags(user_html)
    
    user_email = EmailMultiAlternatives(
        user_subject,
        user_text,
        settings.DEFAULT_FROM_EMAIL,
        [contact_message.email],
    )
    user_email.attach_alternative(user_html, "text/html")
    user_email.send()

def send_course_inquiry_notification(inquiry):
    """Send notification for course inquiry"""
    subject = f"Course Inquiry: {inquiry.course.title}"
    
    html_content = render_to_string('emails/course_inquiry.html', {
        'inquiry': inquiry,
        'site_url': settings.SITE_URL,
    })
    
    email = EmailMultiAlternatives(
        subject,
        strip_tags(html_content),
        settings.DEFAULT_FROM_EMAIL,
        settings.ADMIN_EMAILS,
        reply_to=[inquiry.email],
    )
    email.attach_alternative(html_content, "text/html")
    email.send()
def subscribe_newsletter(email, first_name='', last_name='', request=None):
    """Subscribe email to newsletter"""
    subscriber, created = NewsletterSubscriber.objects.get_or_create(
        email=email,
        defaults={
            'first_name': first_name,
            'last_name': last_name,
            'ip_address': request.META.get('REMOTE_ADDR') if request else None,
        }
    )
    
    if not created and not subscriber.is_active:
        subscriber.is_active = True
        subscriber.save()
    
    # Send confirmation email
    if created:
        send_confirmation_email(subscriber)
    
    return subscriber

def send_confirmation_email(subscriber):
    """Send subscription confirmation"""
    subject = "Welcome to GRTTS Newsletter"
    
    html_content = render_to_string('emails/newsletter_confirmation.html', {
        'subscriber': subscriber,
        'site_url': settings.SITE_URL,
    })
    
    email = EmailMultiAlternatives(
        subject,
        strip_tags(html_content),
        settings.DEFAULT_FROM_EMAIL,
        [subscriber.email],
    )
    email.attach_alternative(html_content, "text/html")
    email.send()

# Set up logging
logger = logging.getLogger(__name__)

def send_newsletter_campaign(campaign_id):
    """Send newsletter campaign to all active subscribers with debugging"""
    from .models import NewsletterCampaign, NewsletterSubscriber
    
    print(f"\n{'='*60}")
    print(f"📧 Starting newsletter campaign: {campaign_id}")
    print(f"{'='*60}")
    
    try:
        campaign = NewsletterCampaign.objects.get(id=campaign_id)
        print(f"Campaign: {campaign.title}")
        print(f"Subject: {campaign.subject}")
        print(f"Content length: {len(campaign.content)} chars")
        
        subscribers = NewsletterSubscriber.objects.filter(is_active=True)
        print(f"Active subscribers: {subscribers.count()}")
        
        if not subscribers:
            print("❌ No active subscribers found!")
            return
        
        sent_count = 0
        for subscriber in subscribers:
            try:
                print(f"\n--- Sending to: {subscriber.email} ---")
                
                # Create tracking record
                tracking = NewsletterTracking.objects.create(
                    campaign=campaign,
                    subscriber=subscriber
                )
                print(f"✓ Tracking record created: {tracking.id}")
                
                # Generate tracking pixel URL
                tracking_pixel = f"{settings.SITE_URL}/newsletter/track/open/{tracking.id}/"
                
                # Render HTML email
                html_content = render_to_string('emails/newsletter_template.html', {
                    'campaign': campaign,
                    'subscriber': subscriber,
                    'tracking_pixel': tracking_pixel,
                    'site_url': settings.SITE_URL,
                })
                print(f"✓ HTML template rendered ({len(html_content)} chars)")
                
                # Create email
                email = EmailMultiAlternatives(
                    subject=campaign.subject,
                    body=strip_tags(html_content),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[subscriber.email],
                )
                email.attach_alternative(html_content, "text/html")
                print(f"✓ Email object created")
                
                # Send
                email.send(fail_silently=False)
                print(f"✓ Email sent successfully!")
                
                sent_count += 1
                
            except Exception as e:
                print(f"❌ Error sending to {subscriber.email}:")
                print(f"   Error type: {type(e).__name__}")
                print(f"   Error message: {str(e)}")
                print(traceback.format_exc())
        
        # Update campaign
        campaign.recipients_count = sent_count
        campaign.sent_at = timezone.now()
        campaign.save()
        
        print(f"\n{'='*60}")
        print(f"✅ Campaign complete! Sent: {sent_count}/{subscribers.count()}")
        print(f"{'='*60}")
        
    except Exception as e:
        print(f"❌ Fatal error in send_newsletter_campaign:")
        print(f"   Error type: {type(e).__name__}")
        print(f"   Error message: {str(e)}")
        print(traceback.format_exc())