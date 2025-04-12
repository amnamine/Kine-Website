from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Service, Testimonial, FAQ, BlogPost
from .forms import ContactForm, AppointmentForm, TestimonialForm

def home(request):
    testimonials = Testimonial.objects.filter(is_approved=True).order_by('-created_at')[:3]
    latest_posts = BlogPost.objects.filter(is_published=True).order_by('-published_date')[:3]
    return render(request, 'clinic/home.html', {
        'testimonials': testimonials,
        'latest_posts': latest_posts
    })

def services(request):
    services = Service.objects.all()
    return render(request, 'clinic/services.html', {'services': services})

def service_detail(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    testimonials = Testimonial.objects.filter(service_received=service, is_approved=True)
    return render(request, 'clinic/service_detail.html', {
        'service': service,
        'testimonials': testimonials
    })

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your message. We will get back to you soon!')
            return redirect('contact')
    else:
        form = ContactForm()
    
    return render(request, 'clinic/contact.html', {'form': form})

def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your appointment request has been submitted. We will contact you shortly to confirm.')
            return redirect('book_appointment')
    else:
        form = AppointmentForm()
    
    return render(request, 'clinic/book_appointment.html', {'form': form})

def testimonials(request):
    testimonials = Testimonial.objects.filter(is_approved=True).order_by('-created_at')
    if request.method == 'POST':
        form = TestimonialForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your testimonial. It will be reviewed and published soon.')
            return redirect('testimonials')
    else:
        form = TestimonialForm()
    
    return render(request, 'clinic/testimonials.html', {
        'testimonials': testimonials,
        'form': form
    })

def faqs(request):
    faqs = FAQ.objects.all()
    categories = FAQ.objects.values_list('category', flat=True).distinct()
    return render(request, 'clinic/faqs.html', {
        'faqs': faqs,
        'categories': categories
    })

def blog(request):
    posts = BlogPost.objects.filter(is_published=True).order_by('-published_date')
    return render(request, 'clinic/blog.html', {'posts': posts})

def blog_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id, is_published=True)
    return render(request, 'clinic/blog_post.html', {'post': post})
