# Generated by Django 3.1.13 on 2021-11-16 00:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0011_auto_20211116_0013'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='lo_nameName',
        ),
        migrations.RemoveField(
            model_name='card',
            name='lo_rgbnameName',
        ),
        migrations.RemoveField(
            model_name='card',
            name='lo_rgbtitleName',
        ),
        migrations.RemoveField(
            model_name='card',
            name='lo_titleName',
        ),
    ]