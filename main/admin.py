from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Course, Testimonial, ContactMessage, DeploymentLocation, 
    LocationImage, FAQ, PaymentMethod, Donation, CourseRegistration,
    Payment, PaymentWebhook, NewsletterSubscriber, NewsletterCampaign,
    NewsletterTracking, User, ApplicantProfile, CourseApplication,
    Certificate, CertificateVerificationLog,
    # Add the new inquiry models here
    StudentInquiry, LandownerInquiry, EnthusiastInquiry, OtherInquiry,
    # Add UserDocument model
    UserDocument
)

class LocationImageInline(admin.TabularInline):
    model = LocationImage
    extra = 3
    fields = ['image', 'caption', 'is_featured', 'image_preview']
    readonly_fields = ['image_preview']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />', obj.image.url)
        return "No image"
    image_preview.short_description = "Preview"

@admin.register(DeploymentLocation)
class DeploymentLocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_training_center', 'is_deployment_location', 'main_image_preview']
    list_filter = ['is_training_center', 'is_deployment_location']
    list_editable = ['is_training_center', 'is_deployment_location']
    search_fields = ['name', 'description']
    inlines = [LocationImageInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description')
        }),
        ('Location Type', {
            'fields': ('is_training_center', 'is_deployment_location')
        }),
        ('Main Image', {
            'fields': ('main_image',),
            'classes': ('wide',)
        }),
    )
    
    def main_image_preview(self, obj):
        if obj.main_image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px; border-radius: 5px;" />', obj.main_image.url)
        return "No main image"
    main_image_preview.short_description = "Main Image"

@admin.register(LocationImage)
class LocationImageAdmin(admin.ModelAdmin):
    list_display = ['location', 'image_preview', 'caption', 'is_featured', 'uploaded_at']
    list_filter = ['location', 'is_featured']
    search_fields = ['location__name', 'caption']
    list_editable = ['is_featured']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px; border-radius: 5px;" />', obj.image.url)
        return "No image"
    image_preview.short_description = "Preview"

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'course_type', 'duration', 'price', 'is_active']
    list_filter = ['course_type', 'is_active']
    search_fields = ['title', 'description']
    list_editable = ['is_active']
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'course_type', 'duration', 'price')
        }),
        ('Content', {
            'fields': ('description', 'intake_dates', 'image')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'image_preview', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'content']
    list_editable = ['is_active']
    readonly_fields = ['image_preview']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'position', 'content')
        }),
        ('Image', {
            'fields': ('image', 'image_preview'),
            'classes': ('wide',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 100px; border-radius: 10px;" />', obj.image.url)
        return "No image uploaded"
    image_preview.short_description = "Image Preview"

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'subject', 'created_at', 'is_read']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'message']
    readonly_fields = ['name', 'email', 'phone', 'subject', 'message', 'created_at']
    actions = ['mark_as_read']
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected messages as read"
    
    fieldsets = (
        ('Sender Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Message Details', {
            'fields': ('subject', 'message', 'created_at')
        }),
        ('Status', {
            'fields': ('is_read',)
        }),
    )

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    search_fields = ['question']
    fieldsets = (
        ('Question', {
            'fields': ('question', 'answer')
        }),
        ('Display Settings', {
            'fields': ('order', 'is_active')
        }),
    )

@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ['display_name', 'name', 'is_active', 'logo_preview']
    list_filter = ['is_active', 'name']
    search_fields = ['display_name']
    list_editable = ['is_active']
    
    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="max-height: 30px;" />', obj.logo.url)
        return "No logo"
    logo_preview.short_description = "Logo"

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ['transaction_id', 'donor_name', 'amount', 'payment_method', 'status', 'created_at']
    list_filter = ['status', 'payment_method', 'created_at']
    search_fields = ['donor_name', 'donor_email', 'transaction_id']
    readonly_fields = ['transaction_id', 'created_at', 'completed_at']
    fieldsets = (
        ('Donor Information', {
            'fields': ('donor_name', 'donor_email', 'donor_phone', 'is_anonymous')
        }),
        ('Donation Details', {
            'fields': ('amount', 'payment_method', 'status', 'transaction_id')
        }),
        ('Recurring', {
            'fields': ('is_recurring', 'recurring_frequency'),
            'classes': ('collapse',)
        }),
        ('Payment Info', {
            'fields': ('payment_reference', 'payment_response'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'completed_at')
        }),
    )

@admin.register(CourseRegistration)
class CourseRegistrationAdmin(admin.ModelAdmin):
    list_display = ['registration_number', 'full_name', 'course', 'status', 'payment_status', 'registered_at']
    list_filter = ['status', 'payment_status', 'course', 'registered_at']
    search_fields = ['full_name', 'email', 'registration_number']
    readonly_fields = ['registration_number', 'registered_at']
    fieldsets = (
        ('Registration Info', {
            'fields': ('registration_number', 'course', 'status')
        }),
        ('Personal Details', {
            'fields': ('full_name', 'id_number', 'date_of_birth', 'gender')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'alternate_phone', 'address')
        }),
        ('Emergency Contact', {
            'fields': ('emergency_name', 'emergency_phone', 'emergency_relationship')
        }),
        ('Medical & Dietary', {
            'fields': ('medical_conditions', 'dietary_requirements'),
            'classes': ('collapse',)
        }),
        ('Payment', {
            'fields': ('payment_method', 'amount_paid', 'payment_status')
        }),
        ('Accommodation', {
            'fields': ('needs_accommodation', 'accommodation_dates'),
            'classes': ('collapse',)
        }),
        ('Admin', {
            'fields': ('admin_notes', 'confirmed_at', 'registered_at')
        }),
    )

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'payment_type', 'amount', 'provider', 'status', 'created_at']
    list_filter = ['payment_type', 'provider', 'status', 'created_at']
    search_fields = ['provider_reference']
    readonly_fields = ['created_at', 'updated_at', 'completed_at']
    fieldsets = (
        ('Payment Type', {
            'fields': ('payment_type', 'donation', 'registration')
        }),
        ('Payment Details', {
            'fields': ('amount', 'provider', 'provider_reference', 'status')
        }),
        ('Mobile Money', {
            'fields': ('mobile_number',),
            'classes': ('collapse',)
        }),
        ('Card Details', {
            'fields': ('card_last4', 'card_brand'),
            'classes': ('collapse',)
        }),
        ('Data', {
            'fields': ('request_data', 'response_data'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'completed_at')
        }),
    )

@admin.register(PaymentWebhook)
class PaymentWebhookAdmin(admin.ModelAdmin):
    list_display = ['provider', 'event_type', 'processed', 'created_at']
    list_filter = ['provider', 'processed', 'created_at']
    readonly_fields = ['payload', 'created_at']

@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'is_active', 'subscribed_at']
    list_filter = ['is_active', 'subscribed_at']
    search_fields = ['email', 'first_name', 'last_name']
    actions = ['export_subscribers']
    
    def export_subscribers(self, request, queryset):
        import csv
        from django.http import HttpResponse
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="subscribers.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Email', 'First Name', 'Last Name', 'Subscribed Date'])
        
        for subscriber in queryset:
            writer.writerow([subscriber.email, subscriber.first_name, 
                           subscriber.last_name, subscriber.subscribed_at])
        
        return response
    export_subscribers.short_description = "Export selected subscribers"

@admin.register(StudentInquiry)
class StudentInquiryAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'course', 'created_at', 'is_read']
    list_filter = ['course', 'is_read', 'created_at']
    search_fields = ['name', 'email']
    actions = ['mark_as_read']
    readonly_fields = ['created_at']
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected as read"
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'email', 'phone', 'age', 'nationality')
        }),
        ('Course Interest', {
            'fields': ('education', 'course', 'intake', 'experience')
        }),
        ('Status', {
            'fields': ('is_read', 'created_at')
        }),
    )


@admin.register(LandownerInquiry)
class LandownerInquiryAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'service', 'property_size', 'created_at', 'is_read']
    list_filter = ['service', 'is_read', 'created_at']
    search_fields = ['name', 'email', 'organization']
    readonly_fields = ['created_at']
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected as read"
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone', 'organization')
        }),
        ('Service Required', {
            'fields': ('service', 'property_size', 'property_location')
        }),
        ('Concerns', {
            'fields': ('concerns_poaching', 'concerns_human_wildlife', 
                      'concerns_livestock', 'concerns_trespassing')
        }),
        ('Details', {
            'fields': ('details',)
        }),
        ('Status', {
            'fields': ('is_read', 'created_at')
        }),
    )


@admin.register(EnthusiastInquiry)
class EnthusiastInquiryAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'interest', 'created_at', 'is_read']
    list_filter = ['interest', 'is_read', 'created_at']
    search_fields = ['name', 'email']
    readonly_fields = ['created_at']
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected as read"
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'email')
        }),
        ('Interest', {
            'fields': ('interest', 'background', 'availability', 'message')
        }),
        ('Status', {
            'fields': ('is_read', 'created_at')
        }),
    )


@admin.register(OtherInquiry)
class OtherInquiryAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'category', 'subject', 'created_at', 'is_read']
    list_filter = ['category', 'urgency', 'is_read', 'created_at']
    search_fields = ['name', 'email', 'subject']
    readonly_fields = ['created_at']
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected as read"
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone', 'organization')
        }),
        ('Inquiry Details', {
            'fields': ('category', 'subject', 'message', 'urgency')
        }),
        ('Status', {
            'fields': ('is_read', 'created_at')
        }),
    )

@admin.register(NewsletterCampaign)
class NewsletterCampaignAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'sent_at', 'recipients_count', 'opens_count']
    actions = ['send_newsletter']
    
    def send_newsletter(self, request, queryset):
        from .utils import send_newsletter_campaign
        
        for campaign in queryset:
            if campaign.sent_at:
                self.message_user(request, f"Campaign '{campaign.title}' was already sent on {campaign.sent_at}", level='WARNING')
            else:
                # Call the send function
                try:
                    send_newsletter_campaign(campaign.id)
                    self.message_user(request, f"Newsletter '{campaign.title}' sent successfully!")
                except Exception as e:
                    self.message_user(request, f"Error sending '{campaign.title}': {str(e)}", level='ERROR')
    
    send_newsletter.short_description = "Send selected newsletters"

@admin.register(NewsletterTracking)
class NewsletterTrackingAdmin(admin.ModelAdmin):
    list_display = ['campaign', 'subscriber', 'opened_at', 'clicked_at']
    list_filter = ['campaign', 'opened_at']
    search_fields = ['subscriber__email']

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'username', 'user_type', 'email_verified', 'is_active']
    list_filter = ['user_type', 'email_verified', 'is_active']
    search_fields = ['email', 'username', 'first_name', 'last_name']
    fieldsets = (
        ('User Info', {
            'fields': ('username', 'email', 'first_name', 'last_name')
        }),
        ('Profile', {
            'fields': ('user_type', 'phone', 'id_number', 'profile_image')
        }),
        ('Verification', {
            'fields': ('email_verified', 'email_verification_token')
        }),
        ('Password Reset', {
            'fields': ('reset_token', 'reset_token_created'),
            'classes': ('collapse',)
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
    )

# ===== FIXED APPLICANTPROFILE ADMIN =====
@admin.register(ApplicantProfile)
class ApplicantProfileAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'phone', 'nationality', 'created_at']
    list_filter = ['gender', 'nationality', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'phone']
    readonly_fields = ['created_at', 'updated_at', 'full_name']
    
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = "Full Name"
    
    def email(self, obj):
        return obj.email
    email.short_description = "Email"
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'date_of_birth', 'gender', 'nationality')
        }),
        ('Address', {
            'fields': ('address', 'city', 'province')
        }),
        ('Emergency Contact', {
            'fields': ('emergency_name', 'emergency_phone', 'emergency_relationship')
        }),
        ('Health', {
            'fields': ('medical_conditions', 'dietary_requirements')
        }),
        ('Documents', {
            'fields': ('id_document', 'cv', 'certificates'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(CourseApplication)
class CourseApplicationAdmin(admin.ModelAdmin):
    list_display = ['applicant', 'course', 'status', 'application_date', 'payment_status']
    list_filter = ['status', 'payment_status', 'course', 'application_date']
    search_fields = ['applicant__user__email', 'applicant__user__first_name']
    fieldsets = (
        ('Application', {
            'fields': ('applicant', 'course', 'status')
        }),
        ('Review', {
            'fields': ('reviewed_by', 'reviewed_date', 'admin_notes')
        }),
        ('Interview', {
            'fields': ('interview_date', 'interview_notes', 'interview_score'),
            'classes': ('collapse',)
        }),
        ('Payment', {
            'fields': ('payment_required', 'payment_made', 'payment_status')
        }),
        ('Documents', {
            'fields': ('motivation_letter', 'additional_docs'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('application_date',)
        }),
    )
    readonly_fields = ['application_date']


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ['certificate_number', 'full_name', 'course_name', 'is_valid', 'issue_date', 'view_count']
    list_filter = ['is_valid', 'issue_date']
    search_fields = ['certificate_number', 'full_name', 'course_name']
    readonly_fields = ['verification_token', 'view_count', 'created_at']
    fieldsets = (
        ('Certificate Info', {
            'fields': ('certificate_number', 'verification_token', 'is_valid')
        }),
        ('Recipient', {
            'fields': ('full_name', 'course_name', 'completion_date')
        }),
        ('Details', {
            'fields': ('grade', 'score', 'duration')
        }),
        ('Related Records', {
            'fields': ('registration', 'application'),
            'classes': ('collapse',)
        }),
        ('File', {
            'fields': ('pdf_file',)
        }),
        ('Issuance', {
            'fields': ('issued_by', 'issue_date', 'created_at')
        }),
    )


@admin.register(CertificateVerificationLog)
class CertificateVerificationLogAdmin(admin.ModelAdmin):
    list_display = ['certificate', 'ip_address', 'successful', 'verified_at']
    list_filter = ['successful', 'verified_at']
    search_fields = ['certificate__certificate_number', 'ip_address']
    readonly_fields = ['certificate', 'ip_address', 'user_agent', 'verified_at', 'successful']


# ===== NEW: Register UserDocument Model =====
@admin.register(UserDocument)
class UserDocumentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_display', 'document_type', 'file_link', 'uploaded_at']
    list_filter = ['document_type', 'uploaded_at']
    search_fields = ['user__email', 'description']
    readonly_fields = ['uploaded_at']
    
    def user_display(self, obj):
        if obj.user:
            return obj.user.email
        return "Anonymous"
    user_display.short_description = "User"
    
    def file_link(self, obj):
        if obj.file:
            return format_html('<a href="{}" target="_blank">View File</a>', obj.file.url)
        return "No file"
    file_link.short_description = "File"
    
    fieldsets = (
        ('Document Info', {
            'fields': ('user', 'document_type', 'file', 'description')
        }),
        ('Timestamps', {
            'fields': ('uploaded_at',)
        }),
    )
