# Generated by Django 3.0 on 2021-03-10 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_auto_20210309_1624'),
    ]

    operations = [
        migrations.AddField(
            model_name='tblprovidermaster',
            name='provMasterDeterminationDate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tblprovidermaster',
            name='provMasterDeterminationType',
            field=models.CharField(blank=True, choices=[('NPR', 'NPR'), ('RNPR', 'RNPR'), ('FR', 'FR')], max_length=4, null=True),
        ),
        migrations.AlterField(
            model_name='tblappealmaster',
            name='appealStructure',
            field=models.CharField(blank=True, choices=[('Individual', 'Individual'), ('Optional', 'Optional'), ('CIRP', 'CIRP')], db_column='appealStructure', max_length=25, null=True),
        ),
    ]
