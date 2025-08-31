from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    name = models.CharField(max_length=100)
    credit = models.DecimalField('Credit', max_digits=10, decimal_places=2)
    debit = models.DecimalField('Debit', max_digits=10, decimal_places=2)
    balance = models.DecimalField('Balance', max_digits=10, decimal_places=2)

    def update_financials(self):
        total_debit = self.spendamount_set.aggregate(
            total=Sum(
                models.F('home_rent') + models.F('eb_bill') + models.F('gas_bill') + models.F('groceries')
            )
        )['total'] or 0

        self.debit = total_debit
        self.balance = self.credit - total_debit
        self.save()
        return self.balance

    def __str__(self):
        return self.name
    
class SpendAmount(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    home_rent = models.DecimalField(max_digits=10, decimal_places=2)
    eb_bill = models.DecimalField("EB Bill", max_digits=10, decimal_places=2)
    gas_bill = models.DecimalField(max_digits=10, decimal_places=2)
    groceries = models.DecimalField("Groceries / Home Items", max_digits=10, decimal_places=2)
    
    def __str__(self):
        return  self.profile.name
    