# Generated by Django 3.0.3 on 2020-07-23 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20200723_1329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verifycode',
            name='email',
            field=models.EmailField(max_length=100, verbose_name='电子邮箱'),
        ),
    ]