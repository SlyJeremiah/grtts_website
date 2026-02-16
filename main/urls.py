from django.urls import path
from . import views

urlpatterns = [
    # Basic pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('faq/', views.faq, name='faq'),
    
    # Course URLs
    path('courses/', views.courses, name='courses'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    
    # Location URLs
    path('locations/', views.locations, name='locations'),
    path('locations/<int:location_id>/', views.location_detail, name='location_detail'),
    
    # Contact & Inquiry URLs
    path('contact/', views.contact, name='contact'),
    path('inquiry/', views.inquiry_page, name='inquiry'),
    path('inquiry/student/', views.inquiry_student, name='inquiry_student'),
    path('inquiry/landowner/', views.inquiry_landowner, name='inquiry_landowner'),
    path('inquiry/enthusiast/', views.inquiry_enthusiast, name='inquiry_enthusiast'),
    path('inquiry/other/', views.inquiry_other, name='inquiry_other'),
    
    # Newsletter URLs
    path('newsletter/signup/', views.newsletter_signup, name='newsletter_signup'),
    path('newsletter/test/', views.newsletter_test, name='newsletter_test'),
    path('newsletter-test-page/', views.newsletter_test_page, name='newsletter_test_page'),
    path('newsletter/track/open/<int:tracking_id>/', views.track_newsletter_open, name='track_newsletter_open'),
    path('newsletter/unsubscribe/<str:email>/', views.unsubscribe_newsletter, name='unsubscribe_newsletter'),
    
    # Certificate URLs
    path('verify-certificate/', views.verify_certificate, name='verify_certificate'),
    path('certificate/<str:cert_number>/', views.certificate_detail, name='certificate_detail'),
    
    # ===== AUTHENTICATION URLS =====
    path('register/', views.register, name='register'),
    # Login/Logout are handled in project URLs
    
    # ===== APPLICATION URLS =====
    # Profile management
    path('profile/create/', views.create_profile, name='create_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    
    # Course applications
    path('apply/<int:course_id>/', views.apply_for_course, name='apply_for_course'),
    path('application/<int:application_id>/edit/', views.edit_application, name='edit_application'),
    path('application/<int:application_id>/', views.application_detail, name='application_detail'),
    path('applications/', views.my_applications, name='my_applications'),
    
    # Email test
    path('test-email/', views.test_email, name='test_email'),  # This line MUST be here
    
    # Payment URLs - Commented out until ready
    # path('donate/', views.donation_page, name='donation'),
    # path('process-donation/', views.process_donation, name='process_donation'),
    # path('register/<int:course_id>/', views.course_registration_page, name='course_registration'),
    # path('process-registration/', views.process_registration, name='process_registration'),
    # path('payment-webhook/', views.payment_webhook, name='payment_webhook'),
    # path('payment-success/', views.payment_success, name='payment_success'),
    # path('payment-cancel/', views.payment_cancel, name='payment_cancel'),
]
