# Generated by Django 5.0.7 on 2024-12-07 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0018_worker_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worker',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Active', 'Active')], default='Pending', max_length=20),
        ),
    ]