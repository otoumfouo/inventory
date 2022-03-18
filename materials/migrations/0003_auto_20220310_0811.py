# Generated by Django 3.2.5 on 2022-03-10 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0002_auto_20220310_0809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicule',
            name='num_chassi',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Numero de Chassi Vehicule'),
        ),
        migrations.AlterField(
            model_name='vehicule',
            name='puissance_fiscal',
            field=models.IntegerField(blank=True, null=True, verbose_name='Puissance'),
        ),
    ]
