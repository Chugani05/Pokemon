from django.db import models


class Creature(models.Model):
    name = models.CharField(unique=True, max_length=100)
    slug = models.SlugField(unique=True)
    type1 = models.CharField(max_length=100)
    attack = models.IntegerField(default=0)
    defense = models.IntegerField(default=0)
    speed = models.IntegerField(default=0)
    generation = models.IntegerField(default=1)

    def __str__(self):
        return self.name
