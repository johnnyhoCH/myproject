from django.db import models

# Create your models here.

class Player(models.Model):
    name = models.CharField(max_length=50)
    zodiac = models.CharField(max_length=20)
    height = models.CharField(max_length=10)
    weight = models.CharField(max_length=10)
    photos = models.CharField(max_length=255)
    
    class Meta:
        db_table = "player"
    
