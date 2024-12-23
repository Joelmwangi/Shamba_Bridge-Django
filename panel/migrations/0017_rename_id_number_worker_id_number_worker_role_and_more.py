# Generated by Django 5.0.7 on 2024-12-07 22:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0016_alter_worker_id_number_alter_worker_mode_payment_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='worker',
            old_name='id_number',
            new_name='Id_number',
        ),
        migrations.AddField(
            model_name='worker',
            name='role',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='worker',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='worker',
            name='mode_payment',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='worker',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
