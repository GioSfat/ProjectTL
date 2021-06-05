from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import MaxValueValidator, MinValueValidator
from enum import Enum
from polymorphic.models import PolymorphicModel


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

    def create_superuser(self, email, username, first_name, last_name, password):  # einai o Reviewer?
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
    lat = models.FloatField(blank=False)
    address = models.CharField(max_length=70, null=True)
    city = models.CharField(max_length=70, null=True)
    coord_id = models.AutoField(primary_key=True, editable=False)  # na koitaksoyme an kanei swsto crossing

    def set_lat(self, new_lat):
        self.lat = new_lat

    def set_long(self, new_long):
        self.long = new_long

    def set_address(self, new_address):
        self.address = new_address

    def set_city(self, new_city):
        self.city = new_city

    def get_coord_id(self):
        return self.coord_id

    def get_lat(self):
        return self.lat

    def get_long(self):
        return self.long

    def get_address(self):
        return self.address

    def get_city(self):
        return self.city


class Preferences(Enum):
    bar = "Bar"
    res = "Restaurant"
    cs = "Coffee Shop"


class Schedule(Enum):
    morning = "07:00 - 12:00"
    noon = "13:00 - 18:00"
    night = "19:00 - 24:00"


class Business(PolymorphicModel):
    bus_Name = models.CharField(max_length=100)
    busID = models.AutoField(primary_key=True, editable=False)
    phoneNum = models.IntegerField(null=True, blank=True)
    busEmail = User.email
    busSite = models.CharField(max_length=100)
    busSchedule = models.CharField(max_length=10,
                                   choices=[(tag, tag.value) for tag in Schedule])
    multimedia = models.FileField(editable=True)  # stin parenthesi tha valoume (upload_to="fakelos gia photos")
    coordID = models.ForeignKey(Coordinates,
                                on_delete=models.CASCADE)  # na koitaksoyme an kanei swsto crossing
    ownerID = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.CharField(max_length=10,
                            choices=[(tag, tag.value) for tag in Preferences])

    def set_business_name(self, new_bus_name):
        self.bus_Name = new_bus_name

    def set_phone(self, new_phone):
        self.phoneNum = new_phone

    def set_bus_email(self, new_email):
        self.busEmail = new_email

    def set_bus_site(self, new_site):
        self.busSite = new_site

    def set_bus_schedule(self, new_schedule):
        self.busSchedule = new_schedule

    def set_multimedia(self, new_multimedia):
        self.multimedia = new_multimedia

    def get_bus_id(self):
        return self.busID

    def get_bus_name(self):
        return self.bus_Name

    def get_phone(self):
        return self.phoneNum

    def get_bus_email(self):
        return self.busEmail

    def get_bus_site(self):
        return self.busSite

    def get_bus_schedule(self):
        return self.busSchedule

    def get_multimedia(self):
        return self.multimedia


class Owner(models.Model):

    owner_id = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    bus_id = models.ForeignKey(Business, on_delete=models.CASCADE)


class Customer(models.Model):
    cusID = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    phoneNumber = models.PositiveIntegerField(null=True, blank=True, help_text='Write Your Phone Number',
                                              validators=[MaxValueValidator(10)])


class Reviewer(models.Model):
    revID = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)


class Restaurant(Business):
    dayDishes = models.CharField(max_length=100, null=True, blank=False)


class CoffeeShop(Business):
    pass


class Bar(Business):
    pass


class Reviews(PolymorphicModel):
    review_id = models.AutoField(primary_key=True, editable=False)
    cus_id = models.ForeignKey(Customer, null=False, blank=False, editable=False, on_delete=models.CASCADE)
    busID = models.ForeignKey(Business, null=False, blank=False, editable=False, on_delete=models.CASCADE)

    def get_review_id(self):
        return self.review_id


class Comments(Reviews):
    com = models.TextField(null=False, blank=True, help_text='Write a comment from 1 to 300 words',
                           validators=[MinValueValidator(1), MaxValueValidator(300)])

    def set_edit_com(self, new_com):
        self.com = new_com

    def get_com(self):
        return self.com

    def snippet(self):  # an einai megalo to comment tha deixnei mono ta 20 prwta grammata
        return self.com[:20]


class Rating(Reviews):
    rate = models.PositiveSmallIntegerField(help_text='Choose from 1 to 5 stars', validators=[MinValueValidator(1),
                                                                                              MaxValueValidator(5)])

    def set_rate(self, new_rate):
        self.rate = new_rate

    def get_rate(self):
        return self.rate


class Reservations(models.Model):
    day = models.DateTimeField(auto_now=False, auto_now_add=False)
    resID = models.AutoField(primary_key=True, editable=False)
    busID = models.ForeignKey(Business, on_delete=models.CASCADE)
    customerID = models.ForeignKey(User, on_delete=models.CASCADE)

    def set_day(self, day_time):
        self.day = day_time

    def get_res(self):
        return self.resID

    def get_bus(self):
        return self.busID

    def get_customer(self):
        return self.customerID

class Tags(models.Model):
        tag = models.CharField(max_length=50)


def get_all_tag():
    Tags.objects.all()
#
#     @classmethod
#     def book_res(cls, day):
#         pass

#
#
#
#
#
#
#
#
#
#
#
#
#
