# Generated by Django 4.2.4 on 2023-11-19 19:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Cliente', '0017_alter_tarjetacredito_fechavencimientoanio_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sitioweb',
            name='nombreDominio',
        ),
        migrations.AddField(
            model_name='sitioweb',
            name='dominio',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Cliente.dominio'),
        ),
    ]
