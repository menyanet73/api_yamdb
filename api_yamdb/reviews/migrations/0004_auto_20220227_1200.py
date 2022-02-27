# Generated by Django 2.2.16 on 2022-02-27 09:00

from django.db import migrations, models
import reviews.validators


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_auto_20220226_1533'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='title',
            name='year_lte_now',
        ),
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.IntegerField(validators=[reviews.validators.less_then_now_year_validator]),
        ),
    ]
