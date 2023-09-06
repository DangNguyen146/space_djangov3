# Generated by Django 3.1.13 on 2021-11-24 02:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0025_auto_20211124_0204'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpublic',
            name='decripttion',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userpublic',
            name='profile_title',
            field=models.CharField(default=1, max_length=250),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='data2',
            name='link',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='data2',
            name='title',
            field=models.CharField(max_length=250, null=True),
        ),
    ]