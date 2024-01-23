from django.db import models
from simpleapp.resources import ITEM, article
from datetime import datetime

from django import template

    
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name.title()

class Post(models.Model):
    author = models.CharField(max_length=255)
    item = models.CharField(max_length=3, choices=ITEM, default=article)
    date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, related_name='posts')
    heading = models.CharField(max_length=255)
    text = models.TextField(default = "Текст не введен")

    def __str__(self):
        return f'{self.heading.title()} {self.date} {self.text.title()}'
    

