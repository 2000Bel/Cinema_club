from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

# Create your models here.
GENRES = (
  ('A', 'Action'),
  ('B', 'Biography'),
  ('C', 'Comedy'),
  ('D', 'Drama'),
  ('E', 'Western'),
  ('F', 'Fantasy'),
  ('G', 'Crime'),
  ('H', 'Horror'),
  ('I', 'Animation'),
  ('J', 'Adventure'),
  ('K', 'K-Drama'),
  ('L', 'History'), 
  ('M', 'Musical'),
  (' N', 'None'),
  ('O', 'Other'),
  ('P', 'Documentary'),
  ('R', 'Romance'),
  ('S', 'Sport'),
  ('SF', 'Sci-Fi'),
  ('T', 'Thriller'),
  ('W', 'War'),
  ('X', 'Family'),
  ('Y', 'Mystery'),
  ('Z', 'Short Film'),
)

class Actor(models.Model):
   name = models.CharField(max_length=100)
   bio = models.TextField(max_length=500)

   def __str__(self):
     return self.name

   def get_absolute_url(self):
     return reverse('actor-detail', kwargs={'pk': self.id})

class Movie(models.Model):
   title = models.CharField(max_length=100)
   genre = models.CharField(max_length=3, choices=GENRES)
   year = models.DateField('Release Year')
   description = models.TextField(max_length=500)
   poster = models.URLField()
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   actors = models.ManyToManyField(Actor)

   def __str__(self):
     return f'{self.title} ({self.id})'

   def get_absolute_url(self):
     return reverse('movie-detail', kwargs={'movie_id': self.id})
  
