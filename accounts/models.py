from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model): #회원가입 할때 회원 정보들
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=10,null=True)
    major = models.CharField(max_length=10,null=True)
    ad_year = models.CharField(max_length=10,null=True)

    def __str__(self):
        return self.name or ''


class Guest(models.Model):
    major = models.CharField(max_length=50,null=True)
    ad_year = models.CharField(max_length=50,null=True)

    def __str__(self):
        return self.major

class Lesson(models.Model): #User 객체에 수강한 과목들을 저장함.
    classname = models.CharField(max_length=50,null=True)
    classchoice = (
        ('전공선택','전공선택'),
        ('전공필수','전공필수'),
        ('균형교양','균형교양'),
        ('특화교양','특화교양'),
        ('기초교양','기초교양'),
        ('대학별교양','대학별교양'),
        ('자유선택','자유선택'),
    )
    classkind = models.TextField(max_length=10,null=True,choices=classchoice)
    classcredits = models.IntegerField(null=True)
    link = models.ForeignKey(User,on_delete=models.CASCADE,blank=True, null=True)
    #guest_link = models.ForeignKey(Guest,on_delete=models.CASCADE,blank=True, null=True)
    def __str__(self):
        return self.classkind