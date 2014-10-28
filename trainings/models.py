from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Training(models.Model):
    id = models.AutoField(primary_key=True)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    duration = models.IntegerField(max_length=10)
    distance = models.DecimalField(None, None, 7, 2)
    max_speed = models.DecimalField(None, None, 7, 2)
    user = models.ForeignKey(User, verbose_name="User")

class Track(models.Model):
    id = models.AutoField(primary_key=True)
    training = models.ForeignKey(Training)
    lat = models.DecimalField("Latitude", None, 17, 15)
    lng = models.DecimalField("Longitude", None, 17, 15)
    time = models.BigIntegerField(max_length=13)
