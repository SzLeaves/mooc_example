# Generated by Django 3.2.15 on 2022-09-13 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0011_auto_20220912_1044'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='images',
            field=models.ImageField(default='', null=True, upload_to='teachers/%Y/%m', verbose_name='讲师封面'),
        ),
    ]
