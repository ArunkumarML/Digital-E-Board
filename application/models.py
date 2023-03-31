from django.db import models
from django.utils.translation import gettext as _

from core.models import Audit
from core.utils.date_time import transform_date_query
from eboard import settings


# Create your models here.


class ValidMixin(models.Model):
    valid = models.BooleanField(default=True)

    class Meta:
        abstract = True


class AbstractLocationMixin(ValidMixin):
    name = models.CharField(max_length=64)
    slug = models.SlugField(max_length=5, null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class State(AbstractLocationMixin):
    is_union_territory = models.BooleanField(default=False)


class District(AbstractLocationMixin):
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name="%(class)s")


class PinCode(ValidMixin):
    value = models.PositiveIntegerField(null=True, blank=True, default=0, verbose_name=_('Pin Code'))
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name="%(class)s")

    def __str__(self):
        return f'{self.value}'


class Customer(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )

    GOVERNMENT_ID_CHOICES = (
        ('aadhar', 'Aadhar'),
        ('pan', 'PAN'),
        ('passport', 'Passport'),
        ('voter_id', 'Voter ID'),
        ('driving_license', 'Driving License'),
    )

    class OwnerShipType(models.TextChoices):
        JOINT = 1, _('Joint')
        INDIVIDUAL = 2, _('Individual')

    name = models.CharField(max_length=128)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    government_id_type = models.CharField(max_length=15, choices=GOVERNMENT_ID_CHOICES)
    government_id_number = models.CharField(max_length=20)
    district = models.ForeignKey(District, on_delete=models.PROTECT, verbose_name=_('District'), null=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.PROTECT, verbose_name=_('State'))
    pin_code = models.ForeignKey(PinCode, on_delete=models.PROTECT, verbose_name=_('Pin Code'), null=True, blank=True,
                                 default=None)
    ownership = models.IntegerField(choices=OwnerShipType.choices, null=False, blank=False)


class Application(Audit):
    status_choices = [
        ('Approved', 'Approved'),
        ('Pending', 'Pending'),
        ('Cancelled', 'Cancelled'),
        ('Connection Released', 'Connection Released'),
    ]

    class CategoryType(models.TextChoices):
        COMMERCIAL = 1, _('Commercial')
        RESIDENTIAL = 2, _('Residential')

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    category = models.IntegerField(choices=CategoryType.choices, null=False, blank=False)
    approved_date = models.DateTimeField(blank=True, null=True)
    load = models.DecimalField(max_digits=10, decimal_places=3)
    status = models.CharField(default='Pending', blank=False, null=False, max_length=20,
                              choices=status_choices)
    status_changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                                          related_name="changed_status", blank=True)
    remarks = models.TextField(null=True, blank=True)

    @staticmethod
    def apply_filters(request, filter_params):
        if request.GET.get('start_date'):
            filter_params['created_at__range'] = transform_date_query(request)
        return filter_params
