from django.db import models

# Create your models here.

class BondYld(models.Model):
    date = models.CharField(max_length=20)
    bond_type = models.CharField(max_length=4)
    three_month = models.CharField(max_length=4)
    six_month = models.CharField(max_length=4)
    nine_month = models.CharField(max_length=4)
    one_year = models.CharField(max_length=4)
    one_year_half = models.CharField(max_length=4)
    two_year = models.CharField(max_length=4)
    three_year = models.CharField(max_length=4)
    five_year = models.CharField(max_length=4)

    class Meta:
        db_table = 'bond_yld'


class YldDeviation(models.Model):
    bond_yld_id = models.ForeignKey(BondYld, on_delete=models.CASCADE, db_column='bond_yld_id')
    dv_value = models.CharField(max_length=25)
    int_cycle = models.CharField(max_length=10)

    class Meta:
        db_table = 'yld_deviation'
