#coding:utf-8
from django.db import models

class hzpy(models.Model):
    hz = models.CharField(max_length=2)
    py = models.CharField(max_length=2)
