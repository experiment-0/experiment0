from django.db import models
from user.models import BaseUser


class Comment(models.Model):
    text = models.TextField(verbose_name="Text")
    user = models.ForeignKey(BaseUser, verbose_name="User", on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")
    deleted = models.BooleanField(default=False, verbose_name="Deleted")


class BaseContent(models.Model):
    title = models.CharField(max_length=255, verbose_name="Title")
    description = models.TextField(verbose_name="Description")
    video = models.URLField(blank=True, verbose_name="Video URL")
    image = models.ImageField(blank=True, upload_to='images/', verbose_name="Image")
    # rating = models.IntegerField(verbose_name="Rating")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")
    deleted = models.BooleanField(default=False, verbose_name="Deleted")

    class Meta:
        abstract = True
        # app_label = 'content'

    def delete(self, *args, **kwargs):
        self.deleted = True
        self.save()

    def __str__(self):
        return self.title


class School(BaseContent):
    school_admin = models.ForeignKey(BaseUser, null=True, blank=True, on_delete=models.DO_NOTHING)


class Course(BaseContent):
    is_finished = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    school = models.ForeignKey(School, verbose_name="School", on_delete=models.CASCADE)
    user = models.ManyToManyField(BaseUser, blank=True)


class Lesson(BaseContent):
    is_passed = models.BooleanField(default=False)
    course = models.ForeignKey(Course, verbose_name="Course", on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, verbose_name="Comment", on_delete=models.DO_NOTHING, blank=True, null=True)


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Name")
    courses = models.ManyToManyField(Course, verbose_name="Courses")
