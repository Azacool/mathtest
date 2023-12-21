from django.db import models

class Avto(models.Model):
    owner = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    model = models.CharField(max_length=50)
    year = models.PositiveIntegerField()

    def __str__(self):
        return self.owner
