from django.db import models

class User(models.Model):
    '''用户表'''

    gender = (
        ('male','男'),
        ('female','女'),
    )

    name = models.CharField(max_length=256)
    password = models.CharField(max_length=256)
    email = models.EmailField(max_length=256)
    is_driver = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Vehicle(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    vehicle_type = models.CharField(max_length=256, default='')
    license_number = models.CharField(max_length=256,  default='')
    max_number_of_passengers = models.IntegerField(default=0)
    special_request = models.CharField(max_length=256, blank=True, default='') # optional
    
    def __str__(self):
        return self.user.name


class Ride(models.Model):
    owner = models.CharField(max_length=256)
    owner_number = models.IntegerField(default = 0)
    destination = models.CharField(max_length=256)
    arrival_time_early = models.DateTimeField()
    #arrival_time_late = models.DateTimeField()
    current_passenger_num = models.IntegerField()
    vehicle_type = models.CharField(max_length=256, blank=True, default='')
    has_shared = models.BooleanField(default=False)
    is_shared = models.BooleanField(default=False)
    sharer = models.ManyToManyField(User)
    
    is_confirmed = models.BooleanField(default=False)
    driver = models.CharField(max_length=256)
    
    is_complete = models.BooleanField(default=False)

    def __str__(self):
        return self.owner