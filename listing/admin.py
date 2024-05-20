from django.contrib import admin
from .models import Region, City, Listing, Image
from import_export.admin import ImportExportModelAdmin

@admin.register(Region)
class RegionAdmin(ImportExportModelAdmin):
    list_display = ('id', 'name', 'lat', 'long')
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(City)
class CityAdmin(ImportExportModelAdmin):
    list_display = ('id', 'name', 'region', 'lat', 'long')
    search_fields = ('name', 'region__name',)
    ordering = ('name',)

@admin.register(Listing)
class ListingAdmin(ImportExportModelAdmin):
    list_display = ('id', 'address', 'l_type', 'status', 'number_of_rooms', 'price', 'price_type', 'owner', 'city', 'created_date', 'last_update')
    list_filter = ('l_type', 'status', 'owner', 'city')
    search_fields = ('address', 'owner__username', 'city__name',)
    date_hierarchy = 'created_date'


@admin.register(Image)
class ImageAdmin(ImportExportModelAdmin):
    list_display = ('id', 'image', 'listing')
