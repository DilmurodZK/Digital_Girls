from django.db import models
from phone_field import PhoneField


class Info(models.Model):
    name_uz = models.CharField(max_length=255)
    name_ru = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='info/')
    instagram = models.URLField()
    telegram = models.URLField()
    youtube = models.URLField()
    facebook = models.URLField()

    def __str__(self):
        return self.name_uz


class Slider(models.Model):
    title_uz = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255)
    text_uz = models.TextField(null=True)
    text_ru = models.TextField(null=True)
    image = models.ImageField(upload_to='slider/')
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.title_uz


class About(models.Model):
    title_uz = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255)
    text_uz = models.TextField(null=True)
    text_ru = models.TextField(null=True)

    def __str__(self):
        return self.title_uz


class AboutItem(models.Model):
    text_uz = models.TextField(null=True)
    text_ru = models.TextField(null=True)
    image = models.ImageField(upload_to='about/')
    status = models.BooleanField(default=False)


class Course(models.Model):
    title_uz = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255)
    text_uz = models.TextField(null=True)
    text_ru = models.TextField(null=True)

    def __str__(self):
        return self.title_uz


class CourseItem(models.Model):
    title_uz = models.TextField(null=True)
    title_ru = models.TextField(null=True)
    icon = models.ImageField(upload_to='course/')
    status = models.BooleanField(default=False)


class Task(models.Model):
    title_uz = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255)
    text_uz = models.TextField(null=True)
    text_ru = models.TextField(null=True)

    def __str__(self):
        return self.title_uz


class TaskItem(models.Model):
    title_uz = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.title_uz


class Result(models.Model):
    title_uz = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255)
    text_uz = models.TextField(null=True)
    text_ru = models.TextField(null=True)

    def __str__(self):
        return self.title_uz


class ResultItem(models.Model):
    text_uz = models.TextField(null=True)
    text_ru = models.TextField(null=True)
    icon = models.ImageField(upload_to='result/')
    status = models.BooleanField(default=False)


class Contact(models.Model):
    website = models.URLField()
    phone = models.CharField(max_length=13, default="+")
    email = models.EmailField()
    address = models.CharField(max_length=255)
    long = models.FloatField()
    lat = models.FloatField()


class Application(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    birthday = models.DateField()
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=13, unique=True, default="+")
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.last_name