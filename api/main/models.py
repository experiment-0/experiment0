from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError

# Create your models here.


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
    title = models.CharField(max_length=255, verbose_name="Title")
    description = models.TextField(verbose_name="Description")
    video = models.FileField(upload_to='videos/', verbose_name="Video")
    image = models.ImageField(upload_to='images/', verbose_name="Image")
    comment = models.ForeignKey(Comment, null=True, blank=True, verbose_name="Comment")
    rating = models.IntegerField(verbose_name="Rating")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")
    deleted = models.BooleanField(default=False, verbose_name="Deleted")


    def delete(self, *args, **kwargs):
        self.deleted = True
        self.save()


class School(BaseContent):
    pass


class Category(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name="Name")
    courses = models.ManyToManyField(Course, verbose_name="Courses")


class Course(BaseContent):
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, verbose_name="Category")


class Lesson(BaseContent):
    pass


class Comment(models.Model):
    text = models.TextField(verbose_name="Text")
    username = models.ForeignKey(BaseUser, verbose_name="User")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")
    deleted = models.BooleanField(default=False, verbose_name="Deleted")


class BaseUser(AbstractBaseUser):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    phone = models.CharField(max_length=10, blank=True, null=True)
    role = None
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = BaseModelManager()


class Certificate(models.Model):
    cert_file = models.FileField(upload_to='certificates/', null=True, blank=True)
    pass


class StudentStatus(models.Model):
    """
    Statuses could change, so we need to store them in DB
    """
    status_id = models.IntegerField(null=True, blank=True)
    status_name = models.CharField(max_length=255, null=True, blank=True)


class Student(BaseUser):
    courses = models.ManyToManyField(Course)
    certificate = models.ForeignKey(Certificate, null=True, blank=True)
    student_status = models.ForeignKey(StudentStatus, null=True, blank=True)
    bought_courses = models.ManyToManyField(Course)
    favorite_courses = models.ForeignKey(Course, null=True, blank=True, on_delete=models.CASCADE)


class Expert(BaseUser):
    rating = models.IntegerField(null=True, blank=True)
    courses = models.ManyToManyField(Course)


class Curator(BaseUser):
    course = models.ForeignKey(Course, null=True, blank=True)


class ScoolAdmin(BaseUser):
    school = models.ForeignKey(School, null=True, blank=True)
