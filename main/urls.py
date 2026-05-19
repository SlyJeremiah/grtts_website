from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    # Home & basic pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('faq/', views.faq, name='faq'),

    # Courses
    path('courses/', views.courses, name='courses'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),

    # Locations
    path('locations/', views.locations, name='locations'),
    path('locations/<int:location_id>/', views.location_detail, name='location_detail'),

    # Contact & inquiries
    path('contact/', views.contact, name='contact'),
    path('inquiry/', views.inquiry_page, name='inquiry_page'),
    path('inquiry/student/', views.inquiry_student, name='inquiry_student'),
    path('inquiry/landowner/', views.inquiry_landowner, name='inquiry_landowner'),
    path('inquiry/enthusiast/', views.inquiry_enthusiast, name='inquiry_enthusiast'),
    path('inquiry/other/', views.inquiry_other, name='inquiry_other'),

    # Newsletter
    path('newsletter/signup/', views.newsletter_signup, name='newsletter_signup'),
    path('newsletter/track/<int:tracking_id>/', views.track_newsletter_open, name='track_newsletter_open'),
    path('newsletter/unsubscribe/<str:email>/', views.unsubscribe_newsletter, name='unsubscribe_newsletter'),
    path('newsletter/test/', views.newsletter_test, name='newsletter_test'),
    path('newsletter/test-page/', views.newsletter_test_page, name='newsletter_test_page'),

    # Certificate verification
    path('verify-certificate/', views.verify_certificate, name='verify_certificate'),
    path('certificate/<str:cert_number>/', views.certificate_detail, name='certificate_detail'),

    # GIS, Apply, Careers
    path('gis-applications/', views.gis_applications, name='gis_applications'),
    path('apply-now/', views.apply_now, name='apply_now'),
    path('careers/', views.careers, name='careers'),
    path('careers/<int:job_id>/apply/', views.job_apply, name='job_apply'),

    # Registration (user signup)
    path('register/', views.register, name='register'),

    # Email test (debug)
    path('test-email/', views.test_email, name='test_email'),
    path('debug-media/', views.debug_media, name='debug_media'),
]