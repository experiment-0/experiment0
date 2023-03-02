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
    slug = models.SlugField(max_length=255, unique=True, verbose_name="Short label for URL")
    description = models.TextField(null=True)

    def __str__(self):
        return self.title
class Student(BaseModel):
    name = models.CharField(max_length=255, blank=False, null=False)
    email = models.EmailField(max_length=254, unique=True, blank=False, null=False)
    password = models.CharField(max_length=50, blank=False, null=False)
    phone = models.IntegerField(max_length=10, blank=True, null=True)  # CharField? (+, spaces, () etc.)
    courses = models.ManyToManyField(Course)
    favorite_courses = models.ForeignKey(Course, null=True, blank=True)
    certificate = models.FileField(upload_to='certificates/', null=True, blank=True)

    def __str__(self):
        return self.name

