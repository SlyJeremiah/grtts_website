from django.db import models
from django.core.validators import EmailValidator, RegexValidator
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import uuid
import os

class StudentInquiry(models.Model):
    """Student training inquiries"""
    COURSE_CHOICES = [
        ('basic', 'Basic Ranger Course'),
        ('specialist', 'Specialist Courses'),
        ('advanced', 'Advanced Ranger'),
        ('unsure', 'Not Sure'),
    ]
    
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    age = models.IntegerField()
    nationality = models.CharField(max_length=100)
    education = models.CharField(max_length=50, blank=True)
    course = models.CharField(max_length=50, choices=COURSE_CHOICES)
    intake = models.CharField(max_length=50, blank=True)
    experience = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Student: {self.name} - {self.email}"
    
    class Meta:
        ordering = ['-created_at']


class LandownerInquiry(models.Model):
    """Landowner and conservation project inquiries"""
    SERVICE_CHOICES = [
        ('deployment', 'Ranger Deployment'),
        ('training', 'Staff Training'),
        ('management', 'Ranger Management'),
        ('consultation', 'Consultation'),
    ]
    
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    organization = models.CharField(max_length=200, blank=True)
    service = models.CharField(max_length=50, choices=SERVICE_CHOICES)
    property_size = models.IntegerField(blank=True, null=True)
    property_location = models.CharField(max_length=200, blank=True)
    concerns_poaching = models.BooleanField(default=False)
    concerns_human_wildlife = models.BooleanField(default=False)
    concerns_livestock = models.BooleanField(default=False)
    concerns_trespassing = models.BooleanField(default=False)
    details = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Landowner: {self.name} - {self.email}"
    
    class Meta:
        ordering = ['-created_at']


class EnthusiastInquiry(models.Model):
    """Wildlife enthusiast inquiries"""
    INTEREST_CHOICES = [
        ('volunteer', 'Volunteer'),
        ('donate', 'Donate'),
        ('advocate', 'Advocate'),
        ('visit', 'Visit'),
    ]
    
    name = models.CharField(max_length=200)
    email = models.EmailField()
    interest = models.CharField(max_length=50, choices=INTEREST_CHOICES)
    background = models.TextField(blank=True)
    availability = models.CharField(max_length=50, blank=True)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Enthusiast: {self.name} - {self.email}"
    
    class Meta:
        ordering = ['-created_at']


class OtherInquiry(models.Model):
    """General inquiries"""
    CATEGORY_CHOICES = [
        ('media', 'Media / Press'),
        ('partnership', 'Partnership / Collaboration'),
        ('research', 'Research / Academic'),
        ('employment', 'Employment Opportunities'),
        ('supplier', 'Supplier / Vendor'),
        ('general', 'General Information'),
        ('other', 'Other'),
    ]
    
    URGENCY_CHOICES = [
        ('normal', 'Normal - Response within 3-5 days'),
        ('urgent', 'Urgent - Require prompt attention'),
        ('routine', 'Routine - No specific timeframe'),
    ]
    
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    organization = models.CharField(max_length=200, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    urgency = models.CharField(max_length=50, choices=URGENCY_CHOICES, default='normal')
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"General: {self.name} - {self.subject}"
    
    class Meta:
        ordering = ['-created_at']


class Course(models.Model):
    COURSE_TYPES = [
        ('BASIC', 'Basic Ranger Course'),
        ('SPECIALIST', 'Specialist Course'),
        ('ADVANCED', 'Advanced Ranger & Patrol'),
        ('TRACKING', 'Tracking Course'),
    ]
    
    title = models.CharField(max_length=200)
    course_type = models.CharField(max_length=20, choices=COURSE_TYPES)
    duration = models.CharField(max_length=100)
    description = models.TextField()
    intake_dates = models.CharField(max_length=200, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    image = models.ImageField(upload_to='courses/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['course_type', 'title']


class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100, help_text="e.g., Game Ranger, Landowner")
    content = models.TextField()
    image = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.position}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    subject = models.CharField(max_length=200, blank=True, default='Website Contact Form')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.subject}"
    
    class Meta:
        ordering = ['-created_at']


class DeploymentLocation(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_training_center = models.BooleanField(default=True)
    is_deployment_location = models.BooleanField(default=True)
    main_image = models.ImageField(upload_to='locations/main/', blank=True, null=True, help_text="Main display image")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def get_all_images(self):
        images = []
        if self.main_image:
            images.append({
                'image': self.main_image,
                'is_main': True,
                'caption': f"{self.name} - Main Image"
            })
        for gallery_image in self.gallery_images.all():
            images.append({
                'image': gallery_image.image,
                'is_main': False,
                'caption': gallery_image.caption or f"{self.name} - Gallery Image"
            })
        return images
    
    class Meta:
        ordering = ['name']


class LocationImage(models.Model):
    location = models.ForeignKey(DeploymentLocation, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ImageField(upload_to='locations/gallery/')
    caption = models.CharField(max_length=200, blank=True, null=True)
    is_featured = models.BooleanField(default=False, help_text="Show this image first in gallery")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Image for {self.location.name}"
    
    class Meta:
        ordering = ['-is_featured', '-uploaded_at']


class FAQ(models.Model):
    question = models.CharField(max_length=300)
    answer = models.TextField()
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.question
    
    class Meta:
        ordering = ['order']
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"


class PaymentMethod(models.Model):
    METHOD_TYPES = [
        ('ecocash', 'EcoCash'),
        ('onemoney', 'OneMoney'),
        ('mastercard', 'Mastercard'),
        ('visa', 'Visa'),
        ('bank_transfer', 'Bank Transfer'),
        ('cash', 'Cash'),
    ]
    
    name = models.CharField(max_length=50, choices=METHOD_TYPES)
    display_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    logo = models.ImageField(upload_to='payment_methods/', blank=True, null=True)
    instructions = models.TextField(blank=True, help_text="Payment instructions for users")
    merchant_number = models.CharField(max_length=20, blank=True, help_text="Merchant number for mobile money")
    api_key = models.CharField(max_length=255, blank=True)
    api_secret = models.CharField(max_length=255, blank=True)
    
    def __str__(self):
        return self.display_name
    
    class Meta:
        verbose_name = "Payment Method"
        verbose_name_plural = "Payment Methods"


class Donation(models.Model):
    DONATION_STATUS = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    transaction_id = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True)
    donor_name = models.CharField(max_length=200)
    donor_email = models.EmailField()
    donor_phone = models.CharField(max_length=20, blank=True)
    is_anonymous = models.BooleanField(default=False)
    is_recurring = models.BooleanField(default=False)
    recurring_frequency = models.CharField(max_length=20, blank=True, choices=[
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly'),
    ])
    status = models.CharField(max_length=20, choices=DONATION_STATUS, default='pending')
    payment_reference = models.CharField(max_length=255, blank=True)
    payment_response = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.transaction_id} - {self.amount}"
    
    class Meta:
        ordering = ['-created_at']


class CourseRegistration(models.Model):
    REGISTRATION_STATUS = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('attended', 'Attended'),
    ]
    
    registration_number = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='registrations')
    full_name = models.CharField(max_length=200)
    id_number = models.CharField(max_length=50, help_text="National ID or Passport")
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')])
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    alternate_phone = models.CharField(max_length=20, blank=True)
    address = models.TextField()
    emergency_name = models.CharField(max_length=200)
    emergency_phone = models.CharField(max_length=20)
    emergency_relationship = models.CharField(max_length=50)
    medical_conditions = models.TextField(blank=True, help_text="Any medical conditions we should know about")
    dietary_requirements = models.TextField(blank=True)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('partial', 'Partial'),
        ('paid', 'Paid'),
        ('refunded', 'Refunded'),
    ], default='pending')
    needs_accommodation = models.BooleanField(default=False)
    accommodation_dates = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=20, choices=REGISTRATION_STATUS, default='pending')
    registered_at = models.DateTimeField(auto_now_add=True)
    confirmed_at = models.DateTimeField(blank=True, null=True)
    admin_notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.registration_number} - {self.full_name} - {self.course.title}"
    
    class Meta:
        ordering = ['-registered_at']


class Payment(models.Model):
    PAYMENT_TYPES = [
        ('donation', 'Donation'),
        ('registration', 'Course Registration'),
    ]
    
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    PAYMENT_PROVIDERS = [
        ('ecocash', 'EcoCash'),
        ('onemoney', 'OneMoney'),
        ('paypal', 'PayPal'),
        ('stripe', 'Stripe'),
        ('paynow', 'PayNow'),
        ('bank', 'Bank Transfer'),
    ]
    
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPES)
    donation = models.ForeignKey(Donation, on_delete=models.SET_NULL, null=True, blank=True)
    registration = models.ForeignKey(CourseRegistration, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    provider = models.CharField(max_length=20, choices=PAYMENT_PROVIDERS)
    provider_reference = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    mobile_number = models.CharField(max_length=20, blank=True)
    card_last4 = models.CharField(max_length=4, blank=True)
    card_brand = models.CharField(max_length=20, blank=True)
    request_data = models.JSONField(blank=True, null=True)
    response_data = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.payment_type} - {self.amount} - {self.status}"
    
    class Meta:
        ordering = ['-created_at']


class PaymentWebhook(models.Model):
    provider = models.CharField(max_length=50)
    event_type = models.CharField(max_length=100)
    payload = models.JSONField()
    processed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.provider} - {self.event_type} - {self.created_at}"
    
    class Meta:
        ordering = ['-created_at']


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    unsubscribed_at = models.DateTimeField(blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    source = models.CharField(max_length=100, blank=True, help_text="Where they subscribed from")
    
    def __str__(self):
        return self.email
    
    class Meta:
        ordering = ['-subscribed_at']


class NewsletterCampaign(models.Model):
    title = models.CharField(max_length=200)
    subject = models.CharField(max_length=200)
    content = models.TextField()
    sent_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    recipients_count = models.IntegerField(default=0)
    opens_count = models.IntegerField(default=0)
    clicks_count = models.IntegerField(default=0)
    
    def __str__(self):
        return self.title


class NewsletterTracking(models.Model):
    campaign = models.ForeignKey(NewsletterCampaign, on_delete=models.CASCADE)
    subscriber = models.ForeignKey(NewsletterSubscriber, on_delete=models.CASCADE)
    opened_at = models.DateTimeField(blank=True, null=True)
    clicked_at = models.DateTimeField(blank=True, null=True)
    clicked_url = models.URLField(blank=True)
    
    class Meta:
        unique_together = ['campaign', 'subscriber']


class User(AbstractUser):
    USER_TYPES = [
        ('applicant', 'Course Applicant'),
        ('ranger', 'Ranger'),
        ('trainer', 'Trainer'),
        ('admin', 'Administrator'),
    ]
    
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='applicant')
    phone = models.CharField(max_length=20, blank=True)
    id_number = models.CharField(max_length=50, blank=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    email_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=100, blank=True)
    reset_token = models.CharField(max_length=100, blank=True)
    reset_token_created = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return self.email


class ApplicantProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='applicant_profile')
    
    # Personal Information - Now all optional
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=10, 
        choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], 
        blank=True
    )
    nationality = models.CharField(max_length=100, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    province = models.CharField(max_length=100, blank=True)
    
    # Emergency Contact - Now all optional
    emergency_name = models.CharField(max_length=200, blank=True)
    emergency_phone = models.CharField(max_length=20, blank=True)
    emergency_relationship = models.CharField(max_length=50, blank=True)
    
    # Health - Already optional
    medical_conditions = models.TextField(blank=True)
    dietary_requirements = models.TextField(blank=True)
    
    # Documents - Already optional
    id_document = models.FileField(upload_to='applicants/id/', blank=True)
    cv = models.FileField(upload_to='applicants/cv/', blank=True)
    certificates = models.FileField(upload_to='applicants/certificates/', blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.user.email}"
    
    def get_full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"


class CourseApplication(models.Model):
    """Comprehensive course application with file uploads and tracking"""
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('waitlisted', 'Waitlisted'),
        ('enrolled', 'Enrolled'),
        ('completed', 'Completed'),
    ]
    
    applicant = models.ForeignKey(ApplicantProfile, on_delete=models.CASCADE, related_name='course_applications')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='applications')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    application_number = models.CharField(max_length=50, unique=True, blank=True, null=True)
    application_date = models.DateTimeField(auto_now_add=True)
    
    motivation_text = models.TextField(blank=True, help_text="Why you want to take this course")
    previous_experience = models.TextField(blank=True, help_text="Relevant experience in conservation, military, security, etc.")
    medical_conditions = models.TextField(blank=True, help_text="Any medical conditions we should be aware of")
    dietary_requirements = models.TextField(blank=True)
    
    profile_photo = models.ImageField(
        upload_to='applications/photos/',
        blank=True,
        null=True,
        help_text="Passport-sized photo (JPG, PNG)"
    )
    id_document = models.FileField(
        upload_to='applications/id_documents/',
        blank=True,
        null=True,
        help_text="Upload your ID or Passport (PDF, JPG, PNG)"
    )
    cv_resume = models.FileField(
        upload_to='applications/cv/',
        blank=True,
        null=True,
        help_text="Upload your CV/Resume (PDF, DOC, DOCX)"
    )
    certificates = models.FileField(
        upload_to='applications/certificates/',
        blank=True,
        null=True,
        help_text="Upload any relevant certificates (PDF, JPG, PNG)"
    )
    motivation_letter = models.FileField(
        upload_to='applications/motivation/',
        blank=True,
        null=True,
        help_text="Upload your motivation letter (PDF, DOC, DOCX)"
    )
    additional_docs = models.FileField(
        upload_to='applications/additional/',
        blank=True,
        null=True,
        help_text="Any other supporting documents"
    )
    
    interview_date = models.DateTimeField(blank=True, null=True)
    interview_notes = models.TextField(blank=True)
    interview_score = models.IntegerField(blank=True, null=True)
    
    payment_required = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_made = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('partial', 'Partial'),
        ('paid', 'Paid'),
    ], default='pending')
    
    reviewed_date = models.DateTimeField(blank=True, null=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_applications')
    admin_notes = models.TextField(blank=True)
    
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['applicant', 'course']
        ordering = ['-application_date']
    
    def __str__(self):
        return f"{self.applicant.user.get_full_name()} - {self.course.title}"
    
    def save(self, *args, **kwargs):
        if not self.application_number:
            year = timezone.now().year
            last_app = CourseApplication.objects.filter(
                application_number__startswith=f"APP-{year}"
            ).order_by('-application_number').first()
            
            if last_app and last_app.application_number:
                last_num = int(last_app.application_number.split('-')[-1])
                new_num = last_num + 1
            else:
                new_num = 1
            
            self.application_number = f"APP-{year}-{new_num:04d}"
        
        super().save(*args, **kwargs)


class Certificate(models.Model):
    certificate_number = models.CharField(max_length=50, unique=True)
    registration = models.OneToOneField(CourseRegistration, on_delete=models.CASCADE, null=True, blank=True)
    application = models.OneToOneField(CourseApplication, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=200)
    course_name = models.CharField(max_length=200)
    completion_date = models.DateField()
    issue_date = models.DateField(auto_now_add=True)
    grade = models.CharField(max_length=50, blank=True)
    score = models.IntegerField(blank=True, null=True)
    duration = models.CharField(max_length=100, help_text="e.g., 6 weeks")
    is_valid = models.BooleanField(default=True)
    verification_token = models.CharField(max_length=100, unique=True)
    view_count = models.IntegerField(default=0)
    pdf_file = models.FileField(upload_to='certificates/', blank=True)
    issued_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.certificate_number} - {self.full_name}"
    
    def verify(self):
        self.view_count += 1
        self.save()
        return self.is_valid
    
    class Meta:
        ordering = ['-issue_date']


class CertificateVerificationLog(models.Model):
    certificate = models.ForeignKey(Certificate, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    verified_at = models.DateTimeField(auto_now_add=True)
    successful = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.certificate.certificate_number} - {self.verified_at}"
    
    class Meta:
        ordering = ['-verified_at']


class UserDocument(models.Model):
    """Model to store user-uploaded documents"""
    DOCUMENT_TYPES = [
        ('cv', 'CV/Resume'),
        ('id', 'ID Document'),
        ('certificate', 'Certificate'),
        ('photo', 'Profile Photo'),
        ('other', 'Other Document'),
    ]
    
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='documents', null=True, blank=True)
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    file = models.FileField(upload_to='user_documents/%Y/%m/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255, blank=True)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        if self.user:
            return f"{self.user.username} - {self.get_document_type_display()}"
        else:
            return f"Anonymous - {self.get_document_type_display()} - {self.uploaded_at}"
    
    def filename(self):
        return os.path.basename(self.file.name)
