from django.db import models

# Create your models here.
class Student(models.Model):
    StudentID=models.CharField(primary_key=True,max_length=20)
    Name=models.CharField(max_length=20)
    Chinese=models.FloatField(max_length=5,default=0)
    Math=models.FloatField(max_length=5,default=0)
    English=models.FloatField(max_length=5,default=0)
    Physics=models.FloatField(max_length=5,default=0)
    Chemistry=models.FloatField(max_length=5,default=0)
    password=models.CharField(max_length=20)
    sum=models.FloatField(max_length=5,default=0)
    def __str__(self):
        return self.id,self.Name

class Teacher(models.Model):
    TeacherID=models.CharField(primary_key=True,max_length=20)
    Name=models.CharField(max_length=20)
    password=models.CharField(max_length=20)
    def __str__(self):
        return self.id,self.Name