# Generated by Django 3.2.15 on 2022-09-10 11:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0007_remove_courseorganization_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseorganization',
            name='city',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='organization.citylist', verbose_name='机构所在城市'),
        ),
    ]
