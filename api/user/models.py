from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class BaseModelManager(BaseUserManager):
    def create_user(self, username, email, password, is_student):
        if not email:
            raise ValueError("Users must have email field")
        if not username:
            raise ValueError("Users must have username field")
        if is_student:
            user = Student(
                email=self.normalize_email(email),
                username=username,)
        else:
            user = SchoolAdmin(
                email=self.normalize_email(email),
                username=username,)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, is_student=False):
        user = self.create_user(username=username,
                                email=email,
                                password=password,
                                is_student=is_student,
                                )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class BaseUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    phone = models.CharField(max_length=10, blank=True, null=True)
    # role = None
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    mail_verified_at = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_student = models.BooleanField(blank=True, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = BaseModelManager()

    class Meta:
        app_label = 'user'

class Student(BaseUser):
    # favorite_courses = models.ForeignKey(Course, null=True, blank=True, on_delete=models.CASCADE,
    #                                      related_name='favorite_courses')
    pass

class Expert(BaseUser):
    rating = models.IntegerField(null=True, blank=True)


class Curator(BaseUser):
    pass


class SchoolAdmin(BaseUser):
    pass
