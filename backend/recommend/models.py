from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    content = models.TextField()
    ISBN = models.CharField(max_length=13)
    DDC = models.DecimalField(max_digits=8, decimal_places=3)
    date_added = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class BookClassify(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    DDC = models.DecimalField(max_digits=8, decimal_places=4)
    OWI = models.CharField(max_length=20)
    date_added = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def titleinput(self):
        pass
    
