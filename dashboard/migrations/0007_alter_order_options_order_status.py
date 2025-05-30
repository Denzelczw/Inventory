# Generated by Django 5.1.7 on 2025-05-10 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_alter_order_staff'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['-date'], 'verbose_name_plural': 'Order'},
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected'), ('in_progress', 'In Progress'), ('completed', 'Completed')], default='pending', max_length=20),
        ),
    ]
