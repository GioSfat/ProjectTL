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
        print('Write your new latitude')
        new_lat = models.FloatField(blank=False)
        return new_lat
        # mporei na xreiastei na valoyme

    def set_long(self, new_long):
        print('Write your new longitude')
        new_long = models.FloatField()
        return new_long

    def set_address(self, new_address):
        print('Write your new address')
        new_address = models.CharField(max_length=70, null=True)
        return new_address

    def set_city(self, new_city):
        print('Write your new city')
        new_city = models.CharField(max_length=70, null=True)
        return new_city

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


class Owner(models.Model):
    bus_Name = models.CharField(max_length=100)
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
        return f'The Review Id is {self.review_id}'


class Comments(Reviews):
    com = models.TextField(null=False, blank=True, help_text='Write a comment from 1 to 300 words',
                           validators=[MinValueValidator(1), MaxValueValidator(300)])

    def set_edit_com(self, new_com):
        print('You can edit your comment')
        new_com = self.com
        return new_com

    def get_com(self):
        return f'The comment for the Business is {self.com}'

    def snippet(self):  # an einai megalo to comment tha deixnei mono ta 20 prwta grammata
        return self.com[:20]


class Rating(Reviews):
    rate = models.PositiveSmallIntegerField(help_text='Choose from 1 to 5 stars', validators=[MinValueValidator(1),
                                                                                              MaxValueValidator(5)])

    def setRate(self, new_rate):
        print('You can adjust your star-rating')
        new_rate = self.rate
        return new_rate

    def getRate(self):
        return self.rate


class Reservations(models.Model):
    day = models.DateTimeField(auto_now=False, auto_now_add=False)
    resID = models.AutoField(primary_key=True, editable=False)
    busID = models.ForeignKey(Business, on_delete=models.CASCADE)
    customerID = models.ForeignKey(User, on_delete=models.CASCADE)

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
