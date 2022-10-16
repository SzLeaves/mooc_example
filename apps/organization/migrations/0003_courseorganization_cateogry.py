# Generated by Django 3.2.15 on 2022-09-09 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0002_auto_20220907_0825'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseorganization',
            name='cateogry',
            field=models.CharField(choices=[('train_org', '培训机构'), ('personal', '个人'), ('university', '高校')], default='train_org', max_length=20, verbose_name='机构类别'),
        ),
    ]
