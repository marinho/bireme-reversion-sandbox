import datetime

from django.db import models

from reversion_relations.fields import ReversionForeignKey

class Supplier(models.Model):
    name = models.CharField(max_length=100)
    location = models.TextField(blank=True)
    salary = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    starred = models.BooleanField(default=False, blank=True)
    points = models.IntegerField(default=0, blank=True)
    date_foundation = models.DateField(blank=True, null=True)

    def __unicode__(self):
        return self.name

class Purchase(models.Model):
    date = models.DateTimeField(blank=True, default=datetime.datetime.now)
    supplier = ReversionForeignKey(Supplier, null=True, blank=True)

