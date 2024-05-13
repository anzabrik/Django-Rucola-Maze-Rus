# Generated by Django 5.0.2 on 2024-05-13 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0014_alter_ingredient_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='unit_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6, verbose_name='Стоимость, руб.'),
        ),
    ]
