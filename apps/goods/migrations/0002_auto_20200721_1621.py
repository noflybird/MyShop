# Generated by Django 3.0.3 on 2020-07-21 16:21

import DjangoUeditor.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goodscategorybrand',
            name='desc',
            field=DjangoUeditor.models.UEditorField(default='在此填写品牌描述', verbose_name='品牌描述'),
        ),
    ]