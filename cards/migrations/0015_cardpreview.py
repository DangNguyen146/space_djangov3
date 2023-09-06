# Generated by Django 3.1.13 on 2021-11-16 07:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0014_auto_20211116_0016'),
    ]

    operations = [
        migrations.CreateModel(
            name='CardPreview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('name', models.CharField(max_length=250)),
                ('link', models.CharField(max_length=250)),
                ('imageTruoc', models.ImageField(blank=True, default=None, null=True, upload_to='cards/%Y/%m')),
                ('imageSau', models.ImageField(blank=True, default=None, null=True, upload_to='cards/%Y/%m')),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cards.card')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]