from .models import Application ,PinCode,State,District,Customer
from django.contrib import admin
# Register your models here.


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('id',  'customer',)
    search_fields = ('id',  'customer__name',)


@admin.register(PinCode)
class PincodeAdmin(admin.ModelAdmin):
    list_display = ('id',  'value','district',)
    search_fields = ('id',  'value','district',)


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('id',  'name',)
    search_fields = ('id',  'name',)


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ('id',  'name',)
    search_fields = ('id',  'name',)
