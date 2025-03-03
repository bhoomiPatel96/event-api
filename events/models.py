from datetime import date
from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Inherit from AbstractUser. username uniqueness and password hashing is handled by User model
    """
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('User', 'User')
    ]
    role = models.CharField(max_length = 10, choices = ROLE_CHOICES, default = 'User')

    def __str__(self):
        return f'{self.username} is a {self.role}'

class Event(models.Model):
    name = models.CharField(max_length = 255)
    date = models.DateField()
    total_tickets = models.IntegerField(validators = [MinValueValidator(0)])
    tickets_sold = models.IntegerField(default = 0, validators = [MinValueValidator(0)])

    def __str__(self):
        return self.name

class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    event = models.ForeignKey(Event, on_delete = models.CASCADE)
    quantity = models.IntegerField()
    purchase_date = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f'{self.quantity} tickets by user {self.user.username} for event {self.event.name}'