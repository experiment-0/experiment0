from django.db import models


class BaseContent(models.Model):
    title = models.CharField(max_length=255, verbose_name="Title")
    description = models.TextField(verbose_name="Description")
    video = models.URLField(verbose_name="Video URL")
    image = models.ImageField(upload_to='images/', verbose_name="Image")
    # rating = models.IntegerField(verbose_name="Rating")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")
    deleted = models.BooleanField(default=False, verbose_name="Deleted")

    def delete(self, *args, **kwargs):
        self.deleted = True
        self.save()


class School(BaseContent):
    pass


class Course(BaseContent):
    is_finished = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    school = models.ForeignKey(School, verbose_name="School", on_delete=models.DO_NOTHING)


class Lesson(BaseContent):
    is_passed = models.BooleanField(default=False)
    course = models.ForeignKey(Course, verbose_name="Course", on_delete=models.DO_NOTHING)


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Name")
    courses = models.ManyToManyField(Course, verbose_name="Courses")
