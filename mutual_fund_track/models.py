from django.db import models

# Create your models here.

class MutualFund(models.Model):
    '''
        MutualFund model for saving mutual fund ISIN and name
    '''
    ISIN = models.CharField(max_length=15, null=False, blank=False, unique=True, primary_key=True)
    name = models.TextField(null=True, unique=True)

    def __str__(self):
        return str(self.ISIN) +" "+ str(self.name)


class MutualFundValue(models.Model):
    '''
        MutualFundValue model for saving mutual fund's value for each date.
    '''
    mutual_fund = models.ForeignKey(MutualFund, on_delete=models.CASCADE)
    date = models.BigIntegerField()
    value = models.FloatField()

    class Meta:
        unique_together = [['mutual_fund', 'date']]
        index_together = [['mutual_fund', 'date']]

    def __str__(self):
        return str(self.mutual_fund) +" "+ str(self.date) +" "+ str(self.value)
