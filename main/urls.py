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
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='main/password_reset.html',
             email_template_name='main/password_reset_email.html',
             subject_template_name='main/password_reset_subject.txt',
             success_url='/password-reset-done/'
         ),
         name='password_reset'),
    path('password-reset-done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='main/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='main/password_reset_confirm.html',
             success_url='/reset-done/'
         ),
         name='password_reset_confirm'),
    path('reset-done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='main/password_reset_complete.html'
         ),
         name='password_reset_complete'),
    path('password-change/',
         auth_views.PasswordChangeView.as_view(
             template_name='main/password_change.html',
             success_url='/'
         ),
         name='password_change'),
    path('login/', auth_views.LoginView.as_view(template_name='main/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),     
]