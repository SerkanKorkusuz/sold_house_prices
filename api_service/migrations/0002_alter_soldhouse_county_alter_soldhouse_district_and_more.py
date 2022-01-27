# Generated by Django 4.0.1 on 2022-01-26 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_service', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='soldhouse',
            name='county',
            field=models.CharField(max_length=250, verbose_name='County'),
        ),
        migrations.AlterField(
            model_name='soldhouse',
            name='district',
            field=models.CharField(max_length=250, verbose_name='District'),
        ),
        migrations.AlterField(
            model_name='soldhouse',
            name='estate_type',
            field=models.CharField(max_length=250, verbose_name='Estate Type'),
        ),
        migrations.AlterField(
            model_name='soldhouse',
            name='locality',
            field=models.CharField(max_length=250, verbose_name='Locality'),
        ),
        migrations.AlterField(
            model_name='soldhouse',
            name='new_build',
            field=models.BooleanField(verbose_name='Is newly built?'),
        ),
        migrations.AlterField(
            model_name='soldhouse',
            name='paon',
            field=models.CharField(max_length=250, verbose_name='Primary Addressable Object Name'),
        ),
        migrations.AlterField(
            model_name='soldhouse',
            name='post_code',
            field=models.CharField(max_length=250, verbose_name='Postcode'),
        ),
        migrations.AlterField(
            model_name='soldhouse',
            name='price_paid',
            field=models.IntegerField(verbose_name='Paid Price'),
        ),
        migrations.AlterField(
            model_name='soldhouse',
            name='property_type',
            field=models.CharField(max_length=250, verbose_name='Property Type'),
        ),
        migrations.AlterField(
            model_name='soldhouse',
            name='record_status',
            field=models.CharField(max_length=250, verbose_name='Record Status'),
        ),
        migrations.AlterField(
            model_name='soldhouse',
            name='saon',
            field=models.CharField(max_length=250, verbose_name='Secondary Addressable Object Name'),
        ),
        migrations.AlterField(
            model_name='soldhouse',
            name='street',
            field=models.CharField(max_length=250, verbose_name='Street Name'),
        ),
        migrations.AlterField(
            model_name='soldhouse',
            name='town',
            field=models.CharField(max_length=250, verbose_name='Town'),
        ),
        migrations.AlterField(
            model_name='soldhouse',
            name='tx_date',
            field=models.DateTimeField(verbose_name='Transaction Date'),
        ),
        migrations.AlterField(
            model_name='soldhouse',
            name='tx_id',
            field=models.CharField(max_length=250, primary_key=True, serialize=False, verbose_name='Transaction ID'),
        ),
    ]