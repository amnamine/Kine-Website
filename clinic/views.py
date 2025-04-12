from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Service, Testimonial, FAQ, BlogPost, VirtualConsultation, PatientPortal, TreatmentRecord
from .forms import ContactForm, AppointmentForm, TestimonialForm, UserSignupForm
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView

def home(request):
    services = Service.objects.all()[:3]
    testimonials = Testimonial.objects.filter(is_approved=True)[:3]
    latest_posts = BlogPost.objects.filter(is_published=True)[:3]
    return render(request, 'clinic/home.html', {
        'services': services,
        'testimonials': testimonials,
        'latest_posts': latest_posts
    })

def services(request):
    services = Service.objects.all()
    return render(request, 'clinic/services.html', {'services': services})

def service_detail(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    testimonials = Testimonial.objects.filter(service_received=service, is_approved=True)
    related_services = Service.objects.exclude(id=service_id)[:3]
    return render(request, 'clinic/service_detail.html', {
        'service': service,
        'testimonials': testimonials,
        'related_services': related_services
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
    services = Service.objects.all()
    
    if request.method == 'POST':
        form = TestimonialForm(request.POST)
        if form.is_valid():
            testimonial = form.save(commit=False)
            testimonial.is_approved = False  # New testimonials need admin approval
            testimonial.save()
            messages.success(request, 'Thank you for your testimonial! It will be reviewed and published soon.')
            return redirect('testimonials')
    else:
        form = TestimonialForm()
    
    context = {
        'testimonials': testimonials,
        'services': services,
        'form': form
    }
    return render(request, 'clinic/testimonials.html', context)

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

@login_required
def virtual_consultation(request):
    if request.method == 'POST':
        # Handle the consultation form submission
        consultation = VirtualConsultation.objects.create(
            patient=request.user,
            symptoms=request.POST.get('symptoms'),
            medical_history=request.POST.get('medical_history'),
            current_medications=request.POST.get('current_medications'),
            preferred_date=request.POST.get('preferred_date'),
            preferred_time=request.POST.get('preferred_time')
        )
        messages.success(request, 'Your virtual consultation request has been submitted. A doctor will review it soon.')
        return redirect('patient_portal')
    
    return render(request, 'clinic/virtual_consultation.html', {
        'user': request.user
    })

def price_calculator(request):
    if request.method == 'POST':
        service_id = request.POST.get('service')
        sessions = int(request.POST.get('sessions', 1))
        
        service = get_object_or_404(Service, id=service_id)
        base_price = float(service.price)
        
        # Apply any discounts or special pricing logic here
        total_price = base_price * sessions
        
        return JsonResponse({
            'total_price': total_price,
            'base_price': base_price,
            'sessions': sessions
        })
    
    services = Service.objects.all()
    return render(request, 'clinic/price_calculator.html', {'services': services})

@login_required
def patient_portal(request):
    try:
        portal = PatientPortal.objects.get(user=request.user)
    except PatientPortal.DoesNotExist:
        portal = PatientPortal.objects.create(user=request.user)
    
    consultations = VirtualConsultation.objects.filter(patient=request.user)
    treatments = TreatmentRecord.objects.filter(patient=request.user)
    
    return render(request, 'clinic/patient_portal.html', {
        'portal': portal,
        'consultations': consultations,
        'treatments': treatments
    })

def signup(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully! Welcome to PhysioCare.')
            return redirect('home')
    else:
        form = UserSignupForm()
    
    return render(request, 'clinic/signup.html', {'form': form})
