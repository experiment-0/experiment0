from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError

# Create your models here.
class BaseUser(AbstractBaseUser):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    phone = models.CharField(max_length=10, blank=True, null=True)
    role = None
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class Expert(BaseUser):
    pass


class Curator(BaseUser):
    pass


class ScoolAdmin(BaseUser):
    pass


class BaseModelManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError("Users must have email field")
        if not username:
            raise ValueError("Users must have username field")
        user = self.model(
            email=self.normalize_email(email),
            username=username, )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(username=username,
                                email=email,
                                password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class BaseContent(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")
    deleted = models.BooleanField(default=False, verbose_name="Deleted")

    def delete(self, *args, **kwargs):
        self.deleted = True
        self.save()


class School(BaseContent):
    pass


class Course(BaseContent):
    pass


class Lesson(BaseContent):
    pass


class Student(BaseUser):
    courses = models.ManyToManyField(Course, related_name="courses")
    favorite_courses = models.ForeignKey(Course, null=True, blank=True, on_delete=models.CASCADE, related_name="fav_courses")
    certificate = models.FileField(upload_to='certificates/', null=True, blank=True)
