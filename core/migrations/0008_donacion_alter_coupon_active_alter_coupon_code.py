# Generated by Django 4.2.1 on 2023-06-20 12:43

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0007_coupon_active"),
    ]

    operations = [
        migrations.CreateModel(
            name="Donacion",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nombre", models.CharField(max_length=100)),
                ("apellido", models.CharField(max_length=100)),
                ("correo", models.EmailField(max_length=254)),
                ("monto", models.IntegerField()),
                ("codigo_pais", models.CharField(default="+56", max_length=100)),
                (
                    "telefono",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(100000000),
                            django.core.validators.MaxValueValidator(999999999),
                        ]
                    ),
                ),
                (
                    "rut",
                    models.CharField(
                        max_length=100,
                        validators=[
                            django.core.validators.RegexValidator(
                                "^\\d{1,8}-[0-9Kk]$", "RUT inválido."
                            )
                        ],
                    ),
                ),
                ("rut_cifrado", models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name="coupon",
            name="active",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="coupon",
            name="code",
            field=models.CharField(max_length=15, unique=True),
        ),
    ]
