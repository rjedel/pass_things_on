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
