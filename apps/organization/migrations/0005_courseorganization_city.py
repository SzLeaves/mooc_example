# Generated by Django 3.2.15 on 2022-09-10 10:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0004_alter_courseorganization_images'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseorganization',
            name='city',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='organization.citylist', verbose_name='ζΊζε°ε'),
        ),
    ]
