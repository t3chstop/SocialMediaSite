# Generated by Django 3.2.4 on 2021-06-26 15:47

import accounts.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('email', models.EmailField(max_length=60, unique=True, verbose_name='Email address')),
                ('display_name', models.CharField(max_length=30, unique=True)),
                ('time_joined', models.DateTimeField(auto_now_add=True, verbose_name='Time when account created')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='Last login')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('profile_picture', models.ImageField(blank=True, default=accounts.models.get_default_profile_picture, max_length=255, null=True, upload_to=accounts.models.get_profile_picture_filepath)),
                ('hide_email', models.BooleanField(default=True)),
                ('friends', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
