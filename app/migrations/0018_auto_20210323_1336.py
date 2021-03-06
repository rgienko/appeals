# Generated by Django 3.0 on 2021-03-23 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_auto_20210310_1054'),
    ]

    operations = [
        migrations.AddField(
            model_name='tblprovidernamemaster',
            name='providerIsClient',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tblappealmaster',
            name='appealStructure',
            field=models.CharField(blank=True, choices=[('Optional', 'Optional'), ('CIRP', 'CIRP'), ('Individual', 'Individual')], db_column='appealStructure', max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='tblprovidermaster',
            name='provMasterDeterminationType',
            field=models.CharField(blank=True, choices=[('NPR', 'NPR'), ('FR', 'FR'), ('RNPR', 'RNPR')], max_length=4, null=True),
        ),
    ]
