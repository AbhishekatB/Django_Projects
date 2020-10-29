from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_manager = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)


class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    phonenumber = models.CharField(max_length=12,default='phonenumber')
    location = models.CharField(max_length=20,default='location')

class Nursery_Manager(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    phonenumber = models.CharField(max_length=12,default='phonenumber')
    designation = models.CharField(max_length=20,default='designation')

class Plants(models.Model):
    user  = models.ForeignKey(Nursery_Manager,on_delete=models.CASCADE)
    price = models.CharField(null=False,default='15',max_length=4)

    def __str__(self):
        return "%s the uploader is  %s"% (self.user,self.price)

class Images(models.Model):
    plant = models.ForeignKey(Plants,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/',verbose_name='Image')

