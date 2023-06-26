from django.db import models
from django.contrib.auth.models import User
from datetime import date,datetime


# Create your models here.
class Item(models.Model):
    Id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=30)
    Category = models.CharField(max_length=5)
    AuthorName = models.CharField(max_length=30)
    Quantity = models.IntegerField()
    YearOfPublished = models.IntegerField()


    def __str__(self):
        return self.Name


class ReserveItem(models.Model):
    Id = models.AutoField(primary_key=True)
    ItemId = models.ForeignKey(Item,on_delete=models.PROTECT)
    UserId = models.ForeignKey(User,on_delete=models.PROTECT)
    Category = models.CharField(max_length=5)
    DateOfIssue = models.DateField()
    DateOfReturn = models.DateField()

    def __str__(self):
        return self.ItemId