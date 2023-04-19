# Generated by Django 4.1.7 on 2023-04-15 17:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('school', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='school',
            name='school_admin',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='lesson',
            name='comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='school.comment', verbose_name='Content'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.course', verbose_name='Course'),
        ),
        migrations.AddField(
            model_name='course',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.school', verbose_name='School'),
        ),
        migrations.AddField(
            model_name='course',
            name='user',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AddField(
            model_name='category',
            name='courses',
            field=models.ManyToManyField(to='school.course', verbose_name='Courses'),
        ),
    ]