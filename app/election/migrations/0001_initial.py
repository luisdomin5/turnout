# Generated by Django 2.2.9 on 2019-12-20 01:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_smalluuid.models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='State',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(choices=[('AL', 'AL'), ('AK', 'AK'), ('AZ', 'AZ'), ('AR', 'AR'), ('CA', 'CA'), ('CO', 'CO'), ('CT', 'CT'), ('DE', 'DE'), ('FL', 'FL'), ('GA', 'GA'), ('HI', 'HI'), ('ID', 'ID'), ('IL', 'IL'), ('IN', 'IN'), ('IA', 'IA'), ('KS', 'KS'), ('KY', 'KY'), ('LA', 'LA'), ('ME', 'ME'), ('MD', 'MD'), ('MA', 'MA'), ('MI', 'MI'), ('MN', 'MN'), ('MS', 'MS'), ('MO', 'MO'), ('MT', 'MT'), ('NE', 'NE'), ('NV', 'NV'), ('NH', 'NH'), ('NJ', 'NJ'), ('NM', 'NM'), ('NY', 'NY'), ('NC', 'NC'), ('ND', 'ND'), ('OH', 'OH'), ('OK', 'OK'), ('OR', 'OR'), ('PA', 'PA'), ('RI', 'RI'), ('SC', 'SC'), ('SD', 'SD'), ('TN', 'TN'), ('TX', 'TX'), ('UT', 'UT'), ('VT', 'VT'), ('VA', 'VA'), ('WA', 'WA'), ('WV', 'WV'), ('WI', 'WI'), ('WY', 'WY'), ('DC', 'DC')], editable=False, max_length=2, primary_key=True, serialize=False, verbose_name='Code')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
            ],
            options={
                'ordering': ['code'],
            },
        ),
        migrations.CreateModel(
            name='StateInformationFieldType',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('uuid', django_smalluuid.models.SmallUUIDField(primary_key=True, default=django_smalluuid.models.UUIDDefault(), editable=False, unique=True)),
                ('slug', models.SlugField(verbose_name='Name', unique=True)),
                ('long_name', models.CharField(max_length=200, verbose_name='Long Name')),
            ],
            options={
                'abstract': False,
                'ordering': ['slug']
            },
        ),
        migrations.CreateModel(
            name='StateInformation',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('uuid', django_smalluuid.models.SmallUUIDField(primary_key=True, default=django_smalluuid.models.UUIDDefault(), editable=False, unique=True)),
                ('text', models.TextField(blank=True, default='')),
                ('notes', models.TextField(blank=True, default='')),
                ('field_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='election.StateInformationFieldType')),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='election.State')),
            ],
            options={
                'unique_together': {('state', 'field_type')},
                'ordering': ['field_type__slug', 'state']
            },
        ),
        migrations.AddField(
            model_name='state',
            name='state_information',
            field=models.ManyToManyField(through='election.StateInformation', to='election.StateInformationFieldType'),
        ),
    ]
