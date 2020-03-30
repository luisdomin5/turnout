# Generated by Django 2.2.11 on 2020-03-18 22:08

import common.enums
from django.db import migrations
import enumfields.fields


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0002_nullstate_status_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='registration',
            name='previous_title',
            field=enumfields.fields.EnumField(blank=True, enum=common.enums.PersonTitle, max_length=10, null=True),
        ),
    ]
