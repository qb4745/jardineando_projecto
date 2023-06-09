# Generated by Django 4.2.1 on 2023-06-09 21:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_alter_item_category_alter_item_label"),
    ]

    operations = [
        migrations.AddField(
            model_name="item",
            name="on_sale",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="item",
            name="category",
            field=models.CharField(
                choices=[
                    ("A", "Arboles"),
                    ("AR", "Arbustos"),
                    ("M", "Macetas"),
                    ("S", "Semillas"),
                    ("H", "Herramientas"),
                ],
                max_length=2,
            ),
        ),
        migrations.AlterField(
            model_name="item",
            name="label",
            field=models.CharField(
                blank=True,
                choices=[("S", "success"), ("D", "danger"), ("W", "warning")],
                max_length=2,
                null=True,
            ),
        ),
    ]
