# Generated by Django 3.0 on 2021-04-12 19:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0032_auto_20210412_1421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tblappealmaster',
            name='appealStructure',
            field=models.CharField(blank=True, choices=[('CIRP', 'CIRP'), ('Optional', 'Optional'), ('Individual', 'Individual')], db_column='appealStructure', max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='tblcriticaldatesmaster',
            name='caseNumber',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='app.TblAppealMaster'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tblprovidermaster',
            name='provMasterDeterminationType',
            field=models.CharField(blank=True, choices=[('FR', 'FR'), ('RNPR', 'RNPR'), ('NPR', 'NPR')], max_length=4, null=True),
        ),
    ]
