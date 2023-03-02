from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.core.exceptions import ValidationError

# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")
    deleted = models.BooleanField(default=False, verbose_name="Deleted")

    def delete(self, *args, **kwargs):
        self.deleted = True
        self.save()


class Course(BaseModel):
    pass


class Student(AbstractBaseUser):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=254, unique=True)
    phone = models.IntegerField(max_length=10, blank=True, null=True)
    courses = models.ManyToManyField(Course)
    favorite_courses = models.ForeignKey(Course, null=True, blank=True)
    certificate = models.FileField(upload_to='certificates/', null=True, blank=True)


