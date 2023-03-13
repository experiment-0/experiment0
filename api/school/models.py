from django.db import models


class BaseContent(models.Model):
    title = models.CharField(max_length=255, verbose_name="Title")
    description = models.TextField(verbose_name="Description")
    video = models.FileField(upload_to='videos/', verbose_name="Video")
    image = models.ImageField(upload_to='images/', verbose_name="Image")
    rating = models.IntegerField(verbose_name="Rating")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")
    deleted = models.BooleanField(default=False, verbose_name="Deleted")

    def delete(self, *args, **kwargs):
        self.deleted = True
        self.save()


class School(BaseContent):
    pass


class Course(BaseContent):
    is_active = models.BooleanField(default=True)


class Lesson(BaseContent):
    pass


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Name")
    courses = models.ManyToManyField(Course, verbose_name="Courses")
