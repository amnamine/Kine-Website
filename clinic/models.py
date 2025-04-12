from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    detailed_description = models.TextField(blank=True)
    benefits = models.TextField(blank=True)
    what_to_expect = models.TextField(blank=True)
    price_calculator = models.JSONField(blank=True, null=True, help_text="JSON configuration for price calculator")

    def __str__(self):
        return self.name

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"

class Appointment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    preferred_date = models.DateField()
    preferred_time = models.TimeField()
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled')
    ], default='pending')

    def __str__(self):
        return f"Appointment for {self.name} on {self.preferred_date}"

class Testimonial(models.Model):
    patient_name = models.CharField(max_length=100)
    service_received = models.ForeignKey(Service, on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Testimonial from {self.patient_name}"

class FAQ(models.Model):
    question = models.CharField(max_length=200)
    answer = models.TextField()
    category = models.CharField(max_length=50, choices=[
        ('general', 'General Questions'),
        ('treatment', 'Treatment Related'),
        ('appointment', 'Appointment Related'),
        ('insurance', 'Insurance & Payment')
    ])
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'question']

    def __str__(self):
        return self.question

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.CharField(max_length=100)
    published_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class VirtualConsultation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    symptoms = models.TextField()
    medical_history = models.TextField(blank=True)
    current_medications = models.TextField(blank=True)
    preferred_date = models.DateField()
    preferred_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    doctor_notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"Virtual Consultation - {self.patient.username} - {self.preferred_date}"

class PatientPortal(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    medical_history = models.TextField(blank=True)
    treatment_history = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Patient Portal for {self.user.username}"

class TreatmentRecord(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.DateField()
    notes = models.TextField()
    follow_up_instructions = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Treatment record for {self.patient.username} on {self.date}"
