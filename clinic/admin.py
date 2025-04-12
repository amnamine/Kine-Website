from django.contrib import admin
from .models import Service, ContactMessage, Appointment, Testimonial, FAQ, BlogPost, VirtualConsultation, PatientPortal, TreatmentRecord

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration', 'price')
    search_fields = ('name', 'description')

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('created_at',)

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'service', 'preferred_date', 'preferred_time', 'status', 'created_at')
    list_filter = ('service', 'preferred_date', 'status', 'created_at')
    search_fields = ('name', 'email', 'phone', 'message')
    readonly_fields = ('created_at',)
    list_editable = ('status',)

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('patient_name', 'service_received', 'rating', 'is_approved', 'created_at')
    list_filter = ('service_received', 'rating', 'is_approved', 'created_at')
    search_fields = ('patient_name', 'content')
    list_editable = ('is_approved',)

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'category', 'order')
    list_filter = ('category',)
    search_fields = ('question', 'answer')
    list_editable = ('order',)

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date', 'is_published')
    list_filter = ('is_published', 'published_date')
    search_fields = ('title', 'content', 'author')
    list_editable = ('is_published',)

@admin.register(VirtualConsultation)
class VirtualConsultationAdmin(admin.ModelAdmin):
    list_display = ('patient', 'preferred_date', 'preferred_time', 'status', 'created_at')
    list_filter = ('status', 'preferred_date')
    search_fields = ('patient__username', 'symptoms', 'medical_history')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Patient Information', {
            'fields': ('patient',)
        }),
        ('Consultation Details', {
            'fields': ('symptoms', 'medical_history', 'current_medications')
        }),
        ('Scheduling', {
            'fields': ('preferred_date', 'preferred_time')
        }),
        ('Status and Notes', {
            'fields': ('status', 'doctor_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(PatientPortal)
class PatientPortalAdmin(admin.ModelAdmin):
    list_display = ('user', 'last_updated')
    search_fields = ('user__username', 'medical_history', 'treatment_history')
    readonly_fields = ('last_updated',)

@admin.register(TreatmentRecord)
class TreatmentRecordAdmin(admin.ModelAdmin):
    list_display = ('patient', 'service', 'date', 'created_at')
    list_filter = ('service', 'date', 'created_at')
    search_fields = ('patient__username', 'notes', 'follow_up_instructions')
    readonly_fields = ('created_at',)
