# Generated by Django 3.1.13 on 2021-11-16 00:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0012_auto_20211116_0014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='lo_rgbnameTruoc',
            field=models.TextField(blank=True, default='228,178,149', null=True),
        ),
    ]