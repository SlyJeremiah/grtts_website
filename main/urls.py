from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    # Basic pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('faq/', views.faq, name='faq'),
    
    # Course URLs
    path('courses/', views.courses, name='courses'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    
    # Location URLs
    path('locations/', views.locations, name='locations'),
    path('locations/<int:location_id>/', views.location_detail, name='location_detail'),
    
    # Contact & Inquiry URLs
    path('contact/', views.contact, name='contact'),
    path('inquiry/', views.inquiry_page, name='inquiry_page'),
    path('inquiry/student/', views.inquiry_student, name='inquiry_student'),
    path('inquiry/landowner/', views.inquiry_landowner, name='inquiry_landowner'),
    path('inquiry/enthusiast/', views.inquiry_enthusiast, name='inquiry_enthusiast'),
    path('inquiry/other/', views.inquiry_other, name='inquiry_other'),
    
    # Newsletter URLs
    path('newsletter/signup/', views.newsletter_signup, name='newsletter_signup'),
    path('newsletter/test/', views.newsletter_test, name='newsletter_test'),
    path('newsletter/test-page/', views.newsletter_test_page, name='newsletter_test_page'),
    path('newsletter/unsubscribe/<str:email>/', views.unsubscribe_newsletter, name='unsubscribe_newsletter'),
    path('newsletter/track/<uuid:tracking_id>/', views.track_newsletter_open, name='track_newsletter_open'),
    # Add these with your other URL patterns
path('gis-applications/', views.gis_applications, name='gis_applications'),
path('apply-now/', views.apply_now, name='apply_now'),
path('careers/', views.careers, name='careers'),
    path('job/<int:job_id>/apply/', views.job_apply, name='job_apply'),
    
    # Certificate URLs
    path('verify-certificate/', views.verify_certificate, name='verify_certificate'),
    path('certificate/<str:cert_number>/', views.certificate_detail, name='certificate_detail'),
    
    # Registration
    path('register/', views.register, name='register'),
    
    # Email test
    path('test-email/', views.test_email, name='test_email'),
]
