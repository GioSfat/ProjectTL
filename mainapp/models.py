from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import MaxValueValidator, MinValueValidator
from enum import Enum


class UserManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, first_name, last_name, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.username

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True

    def get_full_name(self):
        return self.first_name + " " + self.last_name

    def get_first_name(self):
        return self.first_name


class Coordinates(models.Model):
    long = models.FloatField(blank=False)
    lat = models.BigIntegerField(blank=False)
    add = models.CharField(max_length=70, null=True)
    city = models.CharField(max_length=70, null=True)
    coord_id = models.AutoField(primary_key=True, editable=False)  # na koitaksoyme an kanei swsto crossing


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
    coordID = models.ForeignKey(Coordinates,
                                on_delete=models.CASCADE)  # na koitaksoyme an kanei swsto crossing
    # resID = models.ForeignKey()
    ownerID = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.CharField(max_length=10,
                            choices=[(tag, tag.value) for tag in Preferences])


#     class Restaurant:
#         pass
#
#     class CoffeeShop:
#         pass
#
#     class Bar:
#         pass
#

class Reviews(models.Model):
    comments = models.TextField()
    ratings = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(100)])
    busID = models.ForeignKey(Business, null=False, blank=False, editable=False, on_delete=models.CASCADE)

#
# class Reservations(models.Model):
#     day = models.DateTimeField()
#     resID = models.AutoField(primary_key=True, editable=False)
#     busID = models.ForeignKey(Business.busID, on_delete=models.CASCADE)
#     customerID = models.ForeignKey(User.Customer, on_delete=models.CASCADE)
#     rating = models.PositiveIntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
#
#     @classmethod
#     def book_res(cls, day):
#         pass
