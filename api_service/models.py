from django.db import models


class SoldHouse(models.Model):
    tx_id = models.CharField(max_length=250, primary_key=True, verbose_name='Transaction ID')
    price_paid = models.IntegerField(verbose_name='Paid Price')
    tx_date = models.DateField(verbose_name='Transaction Date')
    post_code = models.CharField(max_length=250, verbose_name='Postcode')
    property_type = models.CharField(max_length=250, verbose_name='Property Type')
    new_build = models.BooleanField(verbose_name='Is newly built?')
    estate_type = models.CharField(max_length=250, verbose_name='Estate Type')
    paon = models.CharField(max_length=250, verbose_name='Primary Addressable Object Name')
    saon = models.CharField(max_length=250, verbose_name='Secondary Addressable Object Name')
    street = models.CharField(max_length=250, verbose_name='Street Name')
    locality = models.CharField(max_length=250, verbose_name='Locality')
    town = models.CharField(max_length=250, verbose_name='Town')
    district = models.CharField(max_length=250, verbose_name='District')
    county = models.CharField(max_length=250, verbose_name='County')
    record_status = models.CharField(max_length=250, verbose_name='Record Status')

    def __str__(self):
        return self.tx_id
