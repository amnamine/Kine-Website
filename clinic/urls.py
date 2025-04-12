from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('services/', views.services, name='services'),
    path('services/<int:service_id>/', views.service_detail, name='service_detail'),
    path('contact/', views.contact, name='contact'),
    path('book-appointment/', views.book_appointment, name='book_appointment'),
    path('testimonials/', views.testimonials, name='testimonials'),
    path('faqs/', views.faqs, name='faqs'),
    path('blog/', views.blog, name='blog'),
    path('blog/<int:post_id>/', views.blog_post, name='blog_post'),
] 