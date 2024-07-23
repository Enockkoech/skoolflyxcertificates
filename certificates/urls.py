from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create_school/', views.create_school, name='create_school'),
    path('create_student/', views.create_student, name='create_student'),
    path('generate_certificate/<int:student_id>/', views.generate_certificate, name='generate_certificate'),
    path('verify_certificate/', views.verify_certificate, name='verify_certificate'),
    path('certificate_list/', views.certificate_list, name='certificate_list'),
] 

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # Serve media files during development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)