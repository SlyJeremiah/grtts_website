from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    # =========================================================================
    # BASIC PAGES
    # =========================================================================
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('faq/', views.faq, name='faq'),
    
    # =========================================================================
    # COURSE URLS
    # =========================================================================
    path('courses/', views.courses, name='courses'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    
    # =========================================================================
    # LOCATION URLS
    # =========================================================================
    path('locations/', views.locations, name='locations'),
    path('locations/<int:location_id>/', views.location_detail, name='location_detail'),
    
    # =========================================================================
    # CONTACT & INQUIRY URLS
    # =========================================================================
    path('contact/', views.contact, name='contact'),
    path('inquiry/', views.inquiry_page, name='inquiry'),
    path('inquiry/student/', views.inquiry_student, name='inquiry_student'),
    path('inquiry/landowner/', views.inquiry_landowner, name='inquiry_landowner'),
    path('inquiry/enthusiast/', views.inquiry_enthusiast, name='inquiry_enthusiast'),
    path('inquiry/other/', views.inquiry_other, name='inquiry_other'),
    
    # =========================================================================
    # NEWSLETTER URLS
    # =========================================================================
    path('newsletter/signup/', views.newsletter_signup, name='newsletter_signup'),
    path('newsletter/test/', views.newsletter_test, name='newsletter_test'),
    path('newsletter-test-page/', views.newsletter_test_page, name='newsletter_test_page'),
    path('newsletter/track/open/<int:tracking_id>/', views.track_newsletter_open, name='track_newsletter_open'),
    path('newsletter/unsubscribe/<str:email>/', views.unsubscribe_newsletter, name='unsubscribe_newsletter'),
    
    # =========================================================================
    # CERTIFICATE URLS
    # =========================================================================
    path('verify-certificate/', views.verify_certificate, name='verify_certificate'),
    path('certificate/<str:cert_number>/', views.certificate_detail, name='certificate_detail'),
    
    # =========================================================================
    # AUTHENTICATION URLS (registration handled in views)
    # =========================================================================
    path('register/', views.register, name='register'),
    
    # =========================================================================
    # PROFILE & APPLICATION URLS
    # =========================================================================
    # Profile management
    path('profile/create/', views.create_profile, name='create_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    
    # Course applications
    path('apply/<int:course_id>/', views.apply_for_course, name='apply_for_course'),
    path('application/<int:application_id>/edit/', views.edit_application, name='edit_application'),
    path('application/<int:application_id>/', views.application_detail, name='application_detail'),
    path('applications/', views.my_applications, name='my_applications'),
    
    # =========================================================================
    # TEST URLS
    # =========================================================================
    path('test-email/', views.test_email, name='test_email'),
    
    # =========================================================================
    # PAYMENT URLS (COMMENTED OUT - ENABLE WHEN READY)
    # =========================================================================
    # path('donate/', views.donation_page, name='donation'),
    # path('process-donation/', views.process_donation, name='process_donation'),
    # path('register/<int:course_id>/', views.course_registration_page, name='course_registration'),
    # path('process-registration/', views.process_registration, name='process_registration'),
    # path('payment-webhook/', views.payment_webhook, name='payment_webhook'),
    # path('payment-success/', views.payment_success, name='payment_success'),
    # path('payment-cancel/', views.payment_cancel, name='payment_cancel'),
]
