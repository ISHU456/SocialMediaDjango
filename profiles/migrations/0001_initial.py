# Generated by Django 5.2.4 on 2025-07-06 14:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True, max_length=500)),
                ('profile_picture', models.ImageField(blank=True, default='profile_pics/default.jpg', null=True, upload_to='profile_pics/')),
                ('cover_photo', models.ImageField(blank=True, null=True, upload_to='cover_photos/')),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('location', models.CharField(blank=True, max_length=100)),
                ('website', models.URLField(blank=True)),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('following', models.ManyToManyField(blank=True, related_name='followers', to='profiles.profile')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
