from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Institution(models.Model):
    TYPE_CHOICES = (
        (1, 'fundacja'),
        (2, 'organizacja pozarządowa'),
        (3, 'zbiórka lokalna'),
    )
    name = models.CharField(max_length=64)
    description = models.TextField()
    type = models.PositiveSmallIntegerField(choices=TYPE_CHOICES, default=1)
    categories = models.ManyToManyField('Category')


class Donation(models.Model):
    quantity = models.PositiveSmallIntegerField()
    categories = models.ManyToManyField('Category')
    institution = models.ForeignKey('Institution', on_delete=models.PROTECT, related_name='donations')
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    city = models.CharField(max_length=40)
    zip_code = models.CharField(max_length=5)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.CharField(max_length=255, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=None, related_name='donations')
