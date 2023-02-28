from django.db import models
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
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(null=True)

    def __str__(self):
        return self.title
class Student(BaseModel):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    courses = models.ManyToManyField(Course)

    def __str__(self):
        return self.name

