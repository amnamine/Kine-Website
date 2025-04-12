from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Service, Testimonial, FAQ, BlogPost, VirtualConsultation, PatientPortal, TreatmentRecord
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

@login_required
def virtual_consultation(request):
    if request.method == 'POST':
        service_id = request.POST.get('service')
        preferred_date = request.POST.get('preferred_date')
        preferred_time = request.POST.get('preferred_time')
        symptoms = request.POST.get('symptoms')
        medical_history = request.POST.get('medical_history')

        consultation = VirtualConsultation.objects.create(
            patient=request.user,
            service_id=service_id,
            preferred_date=preferred_date,
            preferred_time=preferred_time,
            symptoms=symptoms,
            medical_history=medical_history
        )
        messages.success(request, 'Your virtual consultation has been scheduled successfully!')
        return redirect('patient_portal')

    services = Service.objects.all()
    return render(request, 'clinic/virtual_consultation.html', {'services': services})

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
