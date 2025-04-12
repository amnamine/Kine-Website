from django.db import migrations

def add_initial_services(apps, schema_editor):
    Service = apps.get_model('clinic', 'Service')
    
    services = [
        {
            'name': 'Manual Therapy',
            'description': 'Hands-on treatment techniques to improve joint mobility and reduce pain. Includes joint mobilization, soft tissue massage, and stretching.',
            'duration': '45 minutes',
            'price': '80.00'
        },
        {
            'name': 'Sports Injury Rehabilitation',
            'description': 'Specialized treatment for sports-related injuries. Includes assessment, treatment planning, and progressive rehabilitation exercises.',
            'duration': '60 minutes',
            'price': '90.00'
        },
        {
            'name': 'Post-Surgical Rehabilitation',
            'description': 'Comprehensive rehabilitation program for post-surgical recovery. Focuses on restoring mobility, strength, and function.',
            'duration': '60 minutes',
            'price': '95.00'
        }
    ]
    
    for service in services:
        Service.objects.create(**service)

def remove_initial_services(apps, schema_editor):
    Service = apps.get_model('clinic', 'Service')
    Service.objects.all().delete()

class Migration(migrations.Migration):
    dependencies = [
        ('clinic', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_initial_services, remove_initial_services),
    ] 