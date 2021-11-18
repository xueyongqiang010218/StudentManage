from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    nick_name = models.CharField(max_length=20, verbose_name='昵称')


class Student(models.Model):
    name = models.CharField(max_length=20, verbose_name='姓名')
    gender = models.CharField(max_length=4, verbose_name='性别')
    school = models.CharField(max_length=20, verbose_name='学院')
    class_name = models.CharField(max_length=20, verbose_name='班级')
    class_position = models.CharField(max_length=20, verbose_name='班级职务')
    phone = models.CharField(max_length=11, verbose_name='手机')
    admission = models.DateTimeField(verbose_name='入学时间')
