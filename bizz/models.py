from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser

from django.utils.translation import gettext_lazy as _
from django.db import models

# Create your models here.
from django.db import models


class Archive(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    asking_price = models.CharField(max_length=255, blank=True, null=True)
    gross_revenue = models.CharField(max_length=255, blank=True, null=True)
    ebitda = models.CharField(max_length=255, blank=True, null=True)
    ff_e = models.CharField(max_length=255, blank=True, null=True)
    cash_flow = models.CharField(max_length=255, blank=True, null=True)
    inventory = models.CharField(max_length=255, blank=True, null=True)
    real_estate = models.CharField(max_length=255, blank=True, null=True)
    established = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    real_estate_from_detail = models.CharField(max_length=255, blank=True, null=True)
    building_sf = models.CharField(max_length=255, blank=True, null=True)
    employees = models.CharField(max_length=255, blank=True, null=True)
    furniture_fixture_equipment = models.CharField(max_length=255, blank=True, null=True)
    facilities = models.TextField(blank=True, null=True)
    competition = models.TextField(blank=True, null=True)
    reason_for_selling = models.CharField(max_length=255, blank=True, null=True)
    franchise = models.CharField(max_length=255, blank=True, null=True)
    business_website = models.CharField(max_length=255, blank=True, null=True)
    detail_url = models.CharField(unique=True, max_length=255, blank=True, null=True)
    google_address = models.CharField(max_length=255, blank=True, null=True)
    scraped_time = models.DateTimeField(blank=True, null=True)
    broker_name = models.CharField(max_length=255, blank=True, null=True)
    broker_business_name = models.CharField(max_length=255, blank=True, null=True)
    broker_listing_url = models.CharField(max_length=255, blank=True, null=True)
    broker_telephone = models.CharField(max_length=255, blank=True, null=True)
    sponsored_broker = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'archive'


class Scraped_data(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)
    asking_price = models.IntegerField(blank=True, null=True)
    gross_revenue = models.IntegerField(blank=True, null=True)
    ebitda = models.IntegerField(blank=True, null=True)
    ff_e = models.IntegerField(blank=True, null=True)
    cash_flow = models.IntegerField(blank=True, null=True)
    cash_flow_multiple = models.IntegerField(blank=True, null=True)
    inventory = models.BooleanField(default=False)
    real_estate = models.BooleanField(default=False)
    established = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    county = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=2, blank=True, null=True)
    real_estate_from_detail = models.CharField(max_length=255, blank=True, null=True)
    building_sf = models.IntegerField(blank=True, null=True)
    employees = models.IntegerField(blank=True, null=True)
    furniture_fixture_equipment = models.BooleanField(default=False)
    facilities = models.TextField(blank=True, null=True)
    competition = models.TextField(blank=True, null=True)
    reason_for_selling = models.CharField(max_length=255, blank=True, null=True)
    franchise = models.CharField(max_length=255, blank=True, null=True)
    business_website = models.CharField(max_length=255, blank=True, null=True)
    detail_url = models.CharField(unique=True, max_length=255, blank=True, null=True)
    google_address = models.CharField(max_length=255, blank=True, null=True)
    scraped_time = models.DateTimeField(blank=True, null=True)
    broker_name = models.CharField(max_length=255, blank=True, null=True)
    broker_business_name = models.CharField(max_length=255, blank=True, null=True)
    broker_listing_url = models.CharField(max_length=255, blank=True, null=True)
    broker_telephone = models.CharField(max_length=255, blank=True, null=True)
    sponsored_broker = models.CharField(max_length=255, blank=True, null=True)
    age_years = models.IntegerField(blank=True, null=True)
    first_scraped_time = models.DateTimeField(blank=True, null=True)
    lease_expiration_date = models.DateTimeField(blank=True, null=True)
    inventory_price = models.IntegerField(blank=True, null=True)
    rent = models.IntegerField(blank=True, null=True)
    listing_type = models.CharField(max_length=255, blank=True, null=True)
    image_url = models.TextField(blank=True, null=True)


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """User model."""

    username = None
    email = models.EmailField(_('email address'), unique=True)
    email2 = models.EmailField(blank=True, null=True)
    phone = models.CharField(blank=True, null=True, max_length=15)
    phone2 = models.CharField(blank=True, null=True, max_length=15)
    address = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    zip = models.CharField(max_length=10, blank=True, null=True)
    emailverified = models.BooleanField(default=False)

    last_updated = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.first_name


    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'


class List(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    user_filters = models.TextField(blank=True, null=True)
    filters = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email_preference = models.CharField(max_length=255, blank=True, null=True)
    last_email_sent = models.DateTimeField( blank=True, null=True)
    next_email_date = models.DateTimeField( blank=True, null=True)
    email_frequency = models.CharField(max_length=255, blank=True, null=True)
    email_active = models.BooleanField(default=False, blank=True, null=True)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Config(models.Model):
    url = models.CharField(max_length=255, blank=True, null=True)
    user = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    host = models.CharField(max_length=255, blank=True, null=True)
    port = models.IntegerField( blank=True, null=True)
    db_name = models.CharField(max_length=255, blank=True, null=True)


    def __str__(self):
        return self.url


class Script(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    short_description = models.TextField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    last_run_date = models.DateTimeField( blank=True, null=True)
    frequency = models.IntegerField(blank=True, null=True)
    total_listing_scrapped = models.IntegerField(blank=True, null=True)
    new_listing_scrapped = models.IntegerField(blank=True, null=True)
    old_listing_deleted = models.IntegerField(blank=True, null=True)
    listing_for_review = models.IntegerField(blank=True, null=True)
    fields_scraped = models.TextField(blank=True, null=True)
    schedule_active = models.BooleanField(blank=True, null=True,default=False)
    schedule_once = models.DateTimeField(blank=True, null=True)
    schedule_frequency = models.CharField(blank=True, null=True, max_length=255)
    schedule_day = models.TextField(blank=True, null=True, max_length=255)
    monthly_dates = models.TextField(blank=True, null=True, max_length=255)

    def __str__(self):
        return self.title  # this 'name' field must be exist in your model.


class Archives(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)
    asking_price = models.IntegerField(blank=True, null=True)
    gross_revenue = models.IntegerField(blank=True, null=True)
    ebitda =models.IntegerField(blank=True, null=True)
    ff_e = models.IntegerField( blank=True, null=True)
    cash_flow = models.IntegerField(blank=True, null=True)
    cash_flow_multiple = models.IntegerField(blank=True, null=True)
    inventory = models.BooleanField(default=False)
    real_estate = models.BooleanField(default=False)
    established = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    county = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=2, blank=True, null=True)
    real_estate_from_detail = models.CharField(max_length=255, blank=True, null=True)
    building_sf =  models.IntegerField(blank=True, null=True)
    employees =  models.IntegerField(blank=True, null=True)
    furniture_fixture_equipment =models.BooleanField(default=False)
    facilities = models.TextField(blank=True, null=True)
    competition = models.TextField(blank=True, null=True)
    reason_for_selling = models.CharField(max_length=255, blank=True, null=True)
    franchise = models.CharField(max_length=255, blank=True, null=True)
    business_website = models.CharField(max_length=255, blank=True, null=True)
    detail_url = models.CharField(unique=True, max_length=255, blank=True, null=True)
    google_address = models.CharField(max_length=255, blank=True, null=True)
    scraped_time = models.DateTimeField(blank=True, null=True)
    broker_name = models.CharField(max_length=255, blank=True, null=True)
    broker_business_name = models.CharField(max_length=255, blank=True, null=True)
    broker_listing_url = models.CharField(max_length=255, blank=True, null=True)
    broker_telephone = models.CharField(max_length=255, blank=True, null=True)
    sponsored_broker = models.CharField(max_length=255, blank=True, null=True)
    age_years = models.IntegerField(blank=True, null=True)
    first_scraped_time = models.DateTimeField(blank=True, null=True)
    lease_expiration_date = models.DateTimeField(blank=True, null=True)
    inventory_price = models.IntegerField(blank=True, null=True)
    rent = models.IntegerField(blank=True, null=True)
    listing_type = models.CharField(max_length=255, blank=True, null=True)
    image_url = models.TextField(blank=True, null=True)


class History(models.Model):
    record = models.ForeignKey('ScrapedData', models.DO_NOTHING, blank=True, null=True)
    id = models.AutoField(primary_key=True)
    field_changed = models.CharField(max_length=255, blank=True, null=True)
    old_value = models.TextField(blank=True, null=True)
    new_value = models.TextField(blank=True, null=True)
    changed_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'history'

class ScrapedData(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    asking_price = models.CharField(max_length=255, blank=True, null=True)
    gross_revenue = models.CharField(max_length=255, blank=True, null=True)
    ebitda = models.CharField(max_length=255, blank=True, null=True)
    ff_e = models.CharField(max_length=255, blank=True, null=True)
    cash_flow = models.CharField(max_length=255, blank=True, null=True)
    inventory = models.CharField(max_length=255, blank=True, null=True)
    real_estate = models.CharField(max_length=255, blank=True, null=True)
    established = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    real_estate_from_detail = models.CharField(max_length=255, blank=True, null=True)
    building_sf = models.CharField(max_length=255, blank=True, null=True)
    employees = models.CharField(max_length=255, blank=True, null=True)
    furniture_fixture_equipment = models.CharField(max_length=255, blank=True, null=True)
    facilities = models.TextField(blank=True, null=True)
    competition = models.TextField(blank=True, null=True)
    reason_for_selling = models.CharField(max_length=255, blank=True, null=True)
    franchise = models.CharField(max_length=255, blank=True, null=True)
    business_website = models.CharField(max_length=255, blank=True, null=True)
    detail_url = models.CharField(unique=True, max_length=255, blank=True, null=True)
    google_address = models.CharField(max_length=255, blank=True, null=True)
    scraped_time = models.DateTimeField(blank=True, null=True)
    broker_name = models.CharField(max_length=255, blank=True, null=True)
    broker_business_name = models.CharField(max_length=255, blank=True, null=True)
    broker_listing_url = models.CharField(max_length=255, blank=True, null=True)
    broker_telephone = models.CharField(max_length=255, blank=True, null=True)
    sponsored_broker = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'scraped_data'