from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField
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
    

class GoodReadsImport(models.Model):
    pass



class BooksDisplayed(models.Model):

    title = models.CharField(max_length=100)
    author_first = models.CharField(max_length=100)
    author_last = models.CharField(max_length=100)
    classify_ISBN = models.CharField(max_length=13)
    classify_DDC = models.DecimalField(max_digits=8, decimal_places=3)
    pages = models.IntegerField()
    publish_date = models.IntegerField()
    country = models.CharField(max_length=100)
    tags = ArrayField(
        models.CharField(max_length = 10, null=True, blank=True),
        size = 20,
        default=list,
        null=True)
    date_added = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # content = models.TextField()

    def __str__(self):
        return self.title