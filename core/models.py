from django.db import models

# Create your models here.
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import UniqueConstraint
from django.utils.timezone import make_aware
from django.utils.translation import gettext as _
from datetime import datetime

from core.utils.date_time import get_current_date_time


class UserType(models.TextChoices):
    ADMIN = 'AD', 'Admin User'
    SUPER_ADMIN = 'SA', 'Super Admin'
    NORMAL = 'NU', 'Normal User'


class CustomUser(AbstractUser):
    username = models.CharField(max_length=50, blank=True, unique=True, null=True)
    user_type = models.CharField(max_length=2, choices=UserType.choices, default=UserType.NORMAL)
    email = models.EmailField(_('email address'), blank=True)
    phone_no = models.CharField(max_length=10)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return "{}".format(self.username)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['username', 'email'], name='unique_name_email'), ]


class FinancialYearQuerySet(models.QuerySet):
    def financial_year(self, start, end):
        today = get_current_date_time()
        month = today.month
        if month <= 3:
            start_year = today.year - start - 1
            end_year = today.year - end - 1
        else:
            start_year = today.year - start
            end_year = today.year - end
        start_date = make_aware(datetime(start_year, 4, 1))
        end_date = make_aware(datetime(end_year, 4, 1))
        return self.filter(created_at__range=(start_date, end_date))


class FinancialYearManager(models.Manager):
    def get_queryset(self):
        return FinancialYearQuerySet(self.model, using=self._db)

    def current(self):
        return self.get_queryset().financial_year(0, -1)

    def previous(self):
        return self.get_queryset().financial_year(0, 1)


class Audit(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="created_%(class)s")
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True,
                                   related_name="updated_%(class)s")

    objects = models.Manager()
    year = FinancialYearManager()

    class Meta:
        abstract = True
