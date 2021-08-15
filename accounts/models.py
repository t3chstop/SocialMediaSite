from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.aggregates import Max

class CustomAccountManager(BaseUserManager):  #Account manager
    def create_user(self, email, display_name, password=None):
        if not email:
            raise ValueError("User must have valid email address")
        if not display_name:
            raise ValueError("User must have valid display name")

        user = self.model(
            email = self.normalize_email(email),
            display_name = display_name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, display_name, password):
        user = self.create_user(
            email = self.normalize_email(email),
            display_name = display_name,
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

def get_profile_picture_filepath(self):
    return f'profile_pictures/{self.pk}/{"profile_picture.jpg"}'

def get_default_profile_picture():
    return "static_cdn\defaults\profilepic360by360.jpg"


# Create your models here.
class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name='Email address', max_length=60, unique=True)
    display_name = models.CharField(max_length=30, unique=True, primary_key=True)
    time_joined = models.DateTimeField(verbose_name='Time when account created', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='Last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    profile_picture = models.ImageField(blank=True, upload_to='profile_pictures', null=True, default='profile_pictures/default.png')
    bio = models.TextField(blank=True, max_length=700)
    hide_email = models.BooleanField(default=True)


    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['display_name']

    def __str__(self):
        return self.display_name

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def get_profile_picture_filename(self):
        return str(self.profile_picture)[str(self.profile_picture).index(f'profile_pictures/{self.pk}/'):]