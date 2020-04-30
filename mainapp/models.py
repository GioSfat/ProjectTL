from django.db import models
from enum import Enum


# Create your models here.

class Users(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=60)
    email = models.EmailField(max_length=70)
    birthDate = models.DateField()

    class Admin:
        name = models.AutoField()

    class Customer:
        customerName = models.AutoField()
        username = models.CharField(max_length=80, primary_key=True, editable=True)

    class Owner:
        busName = models.CharField(max_length=100)
        username = models.CharField(max_length=80, primary_key=True, editable=True)


class Coordinates(models.Model):
    long = models.FloatField()
    lat = models.BigIntegerField()
    add = models.CharField(max_length=70)
    city = models.CharField(max_length=70)
    coord_id = models.AutoField(primary_key=True, editable=False)  # na koitaksoyme an kanei swsto crossing
    # coordID = models.CharField(max_length=70)


class Preferences(Enum):
    bar = "Bar"
    res = "Restaurant"
    cs = "Coffee Shop"


class Schedule(Enum):
    morning = "07:00 - 12:00"
    noon = "13:00 - 18:00"
    night = "19:00 - 24:00"


class Business(models.Model):
    busName = models.CharField(max_length=100)
    busID = models.AutoField(primary_key=True, editable=False)
    phoneNum = models.IntegerField(max_length=10, )
    busEmail = models.EmailField(max_length=150)
    busSite = models.CharField(max_length=100)
    bsuSchedule = models.CharField(max_length=10,
                            choices=[(tag, tag.value) for tag in Schedule])
    multimedia = models.FileField(editable=True)  # stin parenthesi tha valoume (upload_to="fakelos gia photos")
    coordID = models.ForeignKey(Coordinates.coord_id,
                                on_delete=models.CASCADE)  # na koitaksoyme an kanei swsto crossing
    resID = models.ForeignKey()
    ownerID = models.ForeignKey(Users.Owner.username, on_delete=models.CASCADE)
    tags = models.CharField(max_length=10,
                            choices=[(tag, tag.value) for tag in Preferences])
