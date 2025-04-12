from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Service
from .forms import ContactForm, AppointmentForm

def home(request):
    return render(request, 'clinic/home.html')

def services(request):
    services = Service.objects.all()
    return render(request, 'clinic/services.html', {'services': services})

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
