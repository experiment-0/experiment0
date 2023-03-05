from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.core.exceptions import ValidationError

# Create your models here.
class BaseUser(AbstractBaseUser):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    phone = models.IntegerField(max_length=10, blank=True, null=True)
    role = None
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

class Student(BaseUser):
    courses = models.ManyToManyField(Course)
    favorite_courses = models.ForeignKey(Course, null=True, blank=True)
    certificate = models.FileField(upload_to='certificates/', null=True, blank=True)


class Expert(BaseUser):
    pass


class Curator(BaseUser):
    pass


class ScoolAdmin(BaseUser):
    pass


class BaseModelManager(BaseUserManager):
    pass


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

