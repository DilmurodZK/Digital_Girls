from django.db import models
from phone_field import PhoneField


class Info(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='info/')
    instagram = models.URLField()
    telegram = models.URLField()
    youtube = models.URLField()
    facebook = models.URLField()

    def __str__(self):
        return self.name


class Slider(models.Model):
    title = models.CharField(max_length=255)
    text_uz = models.TextField(null=True)
    text_ru = models.TextField(null=True)
    image = models.ImageField(upload_to='slider/')

    def __str__(self):
        return self.name


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


class Course(models.Model):
    title_uz = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255)
    text_uz = models.TextField(null=True)
    text_ru = models.TextField(null=True)

    def __str__(self):
        return self.title_uz


class CourseItem(models.Model):
    text_uz = models.TextField(null=True)
    text_ru = models.TextField(null=True)
    icon = models.ImageField(upload_to='course/')


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


class Contact(models.Model):
    website = models.URLField()
    phone = PhoneField(help_text='Contact phone number')
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
    phone = PhoneField(help_text='Contact phone number', unique=True)

    def __str__(self):
        return self.last_name