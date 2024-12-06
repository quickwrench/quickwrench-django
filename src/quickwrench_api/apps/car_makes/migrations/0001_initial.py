# Generated by Django 5.1.3 on 2024-12-06 21:11

from django.db import migrations, models


def populate_carmake(apps, schema_editor):
    CarMake = apps.get_model("car_makes", "CarMake")
    car_makes = ["Toyota", "Honda", "Ford", "BMW", "Mercedes"]
    for make in car_makes:
        obj = CarMake(name=make)
        obj.save()


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CarMake",
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
                ("name", models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.RunPython(populate_carmake),
    ]
