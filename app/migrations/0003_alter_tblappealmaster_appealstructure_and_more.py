# Generated by Django 4.2.7 on 2023-12-05 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0002_alter_tblappealmaster_appealstructure_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tblappealmaster",
            name="appealStructure",
            field=models.CharField(
                blank=True,
                choices=[
                    ("CIRP", "CIRP"),
                    ("Optional", "Optional"),
                    ("Individual", "Individual"),
                ],
                db_column="appealStructure",
                max_length=25,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="tblprovidermaster",
            name="provMasterDeterminationType",
            field=models.CharField(
                blank=True,
                choices=[
                    ("FR", "FR"),
                    ("NPR", "NPR"),
                    ("RNPR", "RNPR"),
                    ("Other", "Other"),
                ],
                max_length=5,
                null=True,
            ),
        ),
    ]