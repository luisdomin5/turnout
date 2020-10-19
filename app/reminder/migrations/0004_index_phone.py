# Generated by Django 2.2.16 on 2020-10-19 16:01

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('reminder', '0003_smalluuid_to_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reminderrequest',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, db_index=True, max_length=128, null=True, region=None),
        ),
    ]
