# Generated by Django 3.0 on 2021-03-30 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_auto_20210325_1619'),
    ]

    operations = [
        migrations.AddField(
            model_name='tblprovidermaster',
            name='provMasterDateStamp',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tblprovidermaster',
            name='provMasterWasAdded',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='tblappealmaster',
            name='appealStructure',
            field=models.CharField(blank=True, choices=[('CIRP', 'CIRP'), ('Individual', 'Individual'), ('Optional', 'Optional')], db_column='appealStructure', max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='tblprovidermaster',
            name='provMasterDeterminationType',
            field=models.CharField(blank=True, choices=[('NPR', 'NPR'), ('RNPR', 'RNPR'), ('FR', 'FR')], max_length=4, null=True),
        ),
    ]
