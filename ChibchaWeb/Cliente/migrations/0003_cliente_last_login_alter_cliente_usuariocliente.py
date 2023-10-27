# Generated by Django 4.2.6 on 2023-10-27 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Cliente', '0002_alter_cliente_options_alter_paquetehosting_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='usuarioCliente',
            field=models.CharField(max_length=20, null=True, verbose_name='Usuario'),
        ),
    ]