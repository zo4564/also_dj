from datetime import datetime
from django.contrib.auth.models import User
from django.db import models


class Species(models.Model):
    species_name = models.CharField(max_length=200, default="name")
    species_genome = models.CharField(max_length=500, default="genome")
    species_description = models.CharField(max_length=500, default="description")
    can_move = models.BooleanField(default=False)
    can_defend = models.BooleanField(default=False)
    pub_date = models.DateTimeField("date published", default=datetime.now())
    score = models.IntegerField(default=0)
    image = models.ImageField(upload_to='species_images/', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='added_species', null=True, blank=True)

    def __str__(self):
        return self.species_name


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    species = models.ForeignKey(Species, on_delete=models.CASCADE, related_name='votes')
    vote_date = models.DateTimeField(auto_now_add=True)

