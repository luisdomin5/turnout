# Generated by Django 2.2.14 on 2020-07-03 15:29

from django.db import migrations, models
import django_smalluuid.models


class Migration(migrations.Migration):

    dependencies = [
        ('integration', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExternalStateSite',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('uuid', django_smalluuid.models.SmallUUIDField(default=django_smalluuid.models.UUIDDefault(), editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.TextField(null=True)),
                ('description', models.TextField(null=True)),
                ('state_up', models.BooleanField(null=True)),
                ('state_changed_at', models.DateTimeField(null=True)),
                ('last_tweet_at', models.DateTimeField(null=True)),
            ],
            options={
                'ordering': ['-modified_at'],
            },
        ),
    ]
