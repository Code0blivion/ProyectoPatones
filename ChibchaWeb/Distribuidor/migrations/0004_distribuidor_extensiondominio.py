# Generated by Django 4.2.4 on 2023-11-10 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Distribuidor', '0003_distribuidor_usuario'),
    ]

    operations = [
        migrations.AddField(
            model_name='distribuidor',
            name='extensionDominio',
            field=models.CharField(max_length=4, null='True', verbose_name='extensionDominio'),
            preserve_default='True',
        ),
    ]
