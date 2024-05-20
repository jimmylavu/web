from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here



class Plan(models.Model):
    img = models.ImageField(upload_to='images/', null=True)
    price =models.IntegerField()
    name  = models.CharField(max_length=255, null=True)
    description  = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f"{self.name} {self.img}"

class PaymentReminder(models.Model):
    next_payment_date = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.next_payment_date} - {self.created_at}" 
    
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    mop = models.CharField(max_length=255, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    reminder = models.ForeignKey(PaymentReminder, on_delete=models.CASCADE, null=True)
    
    def calculate_balance(self):
        self.balance = self.balance - self.total
        self.save()

    def __str__(self):
        return f"{self.id} - {self.user.username} - {self.plan}"


class Transaction(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    amount = models.FloatField(max_length=200)
    date = models.DateTimeField(null=True)

    def __str__(self):
        if self.booking:
            return f"{self.booking.user} - {self.title} - {self.date}" 
        else:
            return f"No associated booking - {self.title}"

    
class Account(models.Model):
    firstname = models.CharField(null=True, max_length=255)
    lastname = models.CharField(null=True, max_length=255)
    address = models.CharField(null=True, max_length=255)
    contact = models.CharField(null=True, max_length=255)
    birthday = models.CharField(null=True, max_length=255)
    auth_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.firstname}  {self.lastname}"