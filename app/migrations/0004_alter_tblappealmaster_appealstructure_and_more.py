# Generated by Django 4.2.7 on 2023-12-05 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0003_alter_tblappealmaster_appealstructure_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tblappealmaster",
            name="appealStructure",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Individual", "Individual"),
                    ("Optional", "Optional"),
                    ("CIRP", "CIRP"),
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
                    ("RNPR", "RNPR"),
                    ("NPR", "NPR"),
                    ("FR", "FR"),
                    ("Other", "Other"),
                ],
                max_length=5,
                null=True,
            ),
        ),
        migrations.DeleteModel(name="TblHospContactMaster",),
    ]
