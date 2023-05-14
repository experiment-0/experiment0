from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class BaseModelManager(BaseUserManager):
    def create_user(self, username, email, password, role=None):
        if not email:
            raise ValueError("Users must have email field")
        if not username:
            raise ValueError("Users must have username field")
        user = BaseUser(email=self.normalize_email(email),
                        username=username,
                        role=role)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, role=None):
        user = self.create_user(username=username,
                                email=email,
                                password=password,
                                role=role)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class BaseUser(AbstractBaseUser, PermissionsMixin):
    ROLES_LIST = [('St', 'Student'), ('SA', 'School Admin'), ('SC', 'Curator'),
                  ('SE', 'Expert')]
    role = models.CharField(max_length=2, choices=ROLES_LIST, null=True,
                            blank=True)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    phone = models.CharField(max_length=10, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    mail_verified_at = models.DateTimeField(blank=True, null=True)
    # rated_lessons = models.ManyToManyField('school.Lesson', through='school.UserLessonRating', related_name='ratings')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = BaseModelManager()

    class Meta:
        app_label = 'user'
