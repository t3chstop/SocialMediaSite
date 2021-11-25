from django.db import models
from PIL import Image
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

#Account manager to match the custom account model
class CustomAccountManager(BaseUserManager):  #Account manager
    def create_user(self, email, displayName, password=None):
        if not email:
            raise ValueError("User must have valid email address")
        if not displayName:
            raise ValueError("User must have valid display name")

        user = self.model(
            email = self.normalize_email(email),
            displayName = displayName
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, displayName, password):
        user = self.create_user(
            email = self.normalize_email(email),
            displayName = displayName,
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    #In this model, email is used to login and display name is what people use to view
    email = models.EmailField(verbose_name='Email address', max_length=60, unique=True)
    displayName = models.CharField(max_length=30, unique=True, primary_key=True)
    time_joined = models.DateTimeField(verbose_name='Time when account created', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='Last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    profile_picture = models.ImageField(blank=True, upload_to='profile_pictures', null=True, default=r'profile_pictures/default.png')
    bio = models.TextField(blank=True, max_length=700)
    hide_email = models.BooleanField(default=True)
    #Add chatroom model soon

    #Save their profile picture
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.profile_picture.path, 'r')
        size = (128, 128)
        img.thumbnail(size)
        img.save(self.profile_picture.path)


    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['displayName']

    def __str__(self):
        return self.displayName