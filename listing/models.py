from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse


class Region(models.Model):
    name = models.CharField(max_length=255)
    lat = models.FloatField(blank=True, null=True)
    long = models.FloatField(blank=True, null=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=255)
    region = models.ForeignKey(Region, models.CASCADE, related_name="region_city")
    lat = models.FloatField(blank=True, null=True)
    long = models.FloatField(blank=True, null=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['region']),
        ]

    def __str__(self):
        return self.name


class Listing(models.Model):

    class Type(models.TextChoices):
        HOUSE = "HS", "House"
        APARTMENT = "AP", "Apartment"

    class Status(models.TextChoices):
        SALE = "SL", "Sale"
        RENT = "RN", "Rent"
        DONE = "DN", "Done"
    
    class PriceType(models.TextChoices):
        s = "$", "$"
        sum ="Sum", "Sum"

    address = models.CharField(max_length=255)
    lat = models.FloatField(blank=True, null=True)
    long = models.FloatField(blank=True, null=True)
    about = models.TextField()
    l_type = models.CharField(max_length=2, choices=Type.choices, default=Type.APARTMENT)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.RENT)
    number_of_rooms = models.PositiveIntegerField()
    price = models.FloatField()
    price_type = models.CharField(max_length=10, choices=PriceType.choices, default=PriceType.sum)
    owner = models.ForeignKey(get_user_model(), models.CASCADE, related_name="user_listing")
    area = models.CharField(max_length=255)
    city = models.ForeignKey(City, models.CASCADE, related_name="city_listing")
    created_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_date']
        indexes = [
            models.Index(fields=['address']),
            models.Index(fields=['city']),
            models.Index(fields=['created_date']),
        ]

    def __str__(self):
        return self.address

    def get_absolute_url(self):
        return reverse("listing_app:property_detail", args=[str(self.pk)])


class Image(models.Model):
    image = models.ImageField(upload_to="photos/")
    listing = models.ForeignKey(Listing, models.CASCADE, related_name="listing_images")

    class Meta:
        indexes = [
            models.Index(fields=['listing']),
        ]

    def __str__(self):
        return self.image.name[:-5]