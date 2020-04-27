from django.contrib import admin
from mutual_fund_track.models import MutualFund, MutualFundValue

# Register your models here.

admin.site.register(MutualFund)
admin.site.register(MutualFundValue)
