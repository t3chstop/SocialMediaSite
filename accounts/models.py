from PIL import Image
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from chat.models import ChatRoom

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
        useris_staff = True
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
    profile_picture = models.ImageField(blank=True, upload_to='profile_pictures', null=True, default=r'profile_pictures/default.png')
    bio = models.TextField(blank=True, max_length=700)
    hide_email = models.BooleanField(default=True)
    chatRooms = models.ManyToManyField(ChatRoom, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.profile_picture.path, 'r')
        size = (128, 128)
        img.thumbnail(size)
        img.save(self.profile_picture.path)


    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['display_name']

    def __str__(self):
        return self.display_name

    def has_perm(self, perm, obj=None):
        return self.is_admin

    @property
    def get_relative_image_path(self):   
        return '/static' + self.profile_picture.url

    def has_module_perms(self, app_label):
        return True

    def get_profile_picture_filename(self):
        return str(self.profile_picture)[str(self.profile_picture).index(f'profile_pictures/{self.pk}/'):]
        