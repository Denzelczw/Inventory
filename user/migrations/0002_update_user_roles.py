from django.db import migrations

def update_user_roles(apps, schema_editor):
    Profile = apps.get_model('user', 'Profile')
    # Update Customer to Head Of Department
    Profile.objects.filter(user_type='customer').update(user_type='head_of_department')
    # Update Supplier to ICT
    Profile.objects.filter(user_type='supplier').update(user_type='ict')

def reverse_user_roles(apps, schema_editor):
    Profile = apps.get_model('user', 'Profile')
    # Reverse Head Of Department to Customer
    Profile.objects.filter(user_type='head_of_department').update(user_type='customer')
    # Reverse ICT to Supplier
    Profile.objects.filter(user_type='ict').update(user_type='supplier')

class Migration(migrations.Migration):
    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(update_user_roles, reverse_user_roles),
    ] 