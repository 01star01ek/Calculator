from django.db import models

class Graduate(models.Model):
    major       = models.CharField(max_length=50,null=True)
    ad_year     = models.CharField(max_length=50,null=True)
    basic       = models.IntegerField(null=True)
    balance     = models.IntegerField(null=True)
    college     = models.IntegerField(null=True)
    free        = models.IntegerField(null=True)    
    needmajor   = models.IntegerField(null=True)
    choicemajor = models.IntegerField(null=True)
    deepmajor   = models.IntegerField(null=True)
    special     = models.IntegerField(null=True)
    teaching    = models.IntegerField(null=True)
    sum         = models.IntegerField(null=True)

    def __str__(self):
        return self.major +" "+ self.ad_year

class ClassList(models.Model):
    kind      = models.CharField(max_length=50,null=True)
    classname = models.CharField(max_length=50,null=True)
    credit    = models.IntegerField(null=True)

    def __str__(self):
        return self.kind + " " + self.classname