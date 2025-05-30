# Generated by Django 5.1.7 on 2025-05-10 11:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_merge_20250510_1254'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='user_company',
        ),
        migrations.AlterField(
            model_name='profile',
            name='staff',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user_type',
            field=models.CharField(choices=[('admin', 'Admin'), ('staff', 'Staff'), ('head_of_department', 'Head Of Department'), ('ict', 'ICT')], default='staff', max_length=20),
        ),
    ]
