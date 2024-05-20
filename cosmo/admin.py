from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Plan)
admin.site.register(Booking)
admin.site.register(PaymentReminder)
admin.site.register(Transaction)
admin.site.register(Account)