from enum import Enum
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# Create your models here.


class Users(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=70)
    birthDate = models.DateField(null=True, blank=True)

    class Admin:
        name = models.AutoField()

    class Customer:
        customerName = models.AutoField()

    class Owner:
        busName = models.CharField(max_length=100)



class Coordinates(models.Model):
    long = models.FloatField(blank=False)
    lat = models.BigIntegerField(blank=False)
    add = models.CharField(max_length=70, null=True)
    city = models.CharField(max_length=70, null=True)
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
    phoneNum = models.IntegerField(max_length=10, null=True, blank=True)
    busEmail = models.EmailField(max_length=150)
    busSite = models.CharField(max_length=100)
    bsuSchedule = models.CharField(max_length=10,
                                   choices=[(tag, tag.value) for tag in Schedule])
    multimedia = models.FileField(editable=True)  # stin parenthesi tha valoume (upload_to="fakelos gia photos")
    coordID = models.ForeignKey(Coordinates.coord_id,
                                on_delete=models.CASCADE)  # na koitaksoyme an kanei swsto crossing
    # resID = models.ForeignKey()
    ownerID = models.ForeignKey(Users.username, on_delete=models.CASCADE)
    tags = models.CharField(max_length=10,
                            choices=[(tag, tag.value) for tag in Preferences])

    class Restaurant:
        pass

    class CoffeeShop:
        pass

    class Bar:
        pass




class Reviews(models.Model):
    comments = models.TextField()
    ratings = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(100)])
    busID = models.ForeignKey(Business.busID, null=False, blank=False, editable=False, on_delete=models.CASCADE)



class Reservations(models.Model):
    day = models.DateTimeField()
    resID = models.AutoField(primary_key=True, editable=False)
    busID = models.ForeignKey(Business.busID, on_delete=models.CASCADE)
    customerID = models.ForeignKey(Users.Customer, on_delete=models.CASCADE)

    @classmethod
    def book_res(cls, day):
        pass


