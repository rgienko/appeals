# Generated by Django 3.0 on 2021-01-21 22:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TblAppealMaster',
            fields=[
                ('caseNumber', models.CharField(db_column='caseNumber', max_length=7, primary_key=True, serialize=False)),
                ('appealName', models.TextField(blank=True, db_column='appealName', null=True)),
                ('appealNotes', models.TextField(blank=True, db_column='appealNotes', null=True)),
                ('appealStructure', models.CharField(blank=True, db_column='appealStructure', max_length=25, null=True)),
                ('appealCreateDate', models.DateField(blank=True, db_column='appealCreateDate', null=True)),
                ('appealAckDate', models.DateField(blank=True, db_column='appealAckDate', null=True)),
            ],
            options={
                'db_table': 'tblAppealMaster',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TblCategoryMaster',
            fields=[
                ('categoryID', models.AutoField(db_column='categoryID', primary_key=True, serialize=False)),
                ('categoryName', models.CharField(blank=True, db_column='categoryName', max_length=50, null=True)),
                ('categoryKey', models.CharField(blank=True, db_column='categoryKey', max_length=10, null=True, unique=True)),
                ('categoryDescription', models.CharField(blank=True, db_column='categoryDescription', max_length=150, null=True)),
            ],
            options={
                'db_table': 'tblCategoryMaster',
            },
        ),
        migrations.CreateModel(
            name='TblDeterminationType',
            fields=[
                ('determinationID', models.CharField(db_column='determinationID', max_length=15, primary_key=True, serialize=False)),
                ('determinationName', models.CharField(blank=True, db_column='determinationName', max_length=100, null=True)),
            ],
            options={
                'db_table': 'tblDeterminationType',
            },
        ),
        migrations.CreateModel(
            name='TblIssueMaster',
            fields=[
                ('issueID', models.AutoField(db_column='issueID', primary_key=True, serialize=False)),
                ('issueName', models.CharField(blank=True, db_column='issueName', max_length=100, null=True)),
                ('issueAbbreviation', models.CharField(blank=True, db_column='issueAbbreviation', max_length=25, null=True)),
                ('issueShortDescription', models.TextField(blank=True, db_column='issueShortDescription', null=True)),
                ('categoryID', models.ForeignKey(blank=True, db_column='categoryID', null=True, on_delete=django.db.models.deletion.CASCADE, to='app.TblCategoryMaster')),
            ],
            options={
                'db_table': 'tblIssueMaster',
            },
        ),
        migrations.CreateModel(
            name='TblParentMaster',
            fields=[
                ('parentID', models.CharField(db_column='parentID', max_length=50, primary_key=True, serialize=False)),
                ('parentFullName', models.TextField(blank=True, db_column='parentFullName', null=True)),
            ],
            options={
                'db_table': 'tblParentMaster',
            },
        ),
        migrations.CreateModel(
            name='TblStateMaster',
            fields=[
                ('stateID', models.CharField(db_column='stateID', max_length=2, primary_key=True, serialize=False)),
                ('stateName', models.CharField(db_column='stateName', max_length=50)),
            ],
            options={
                'db_table': 'tblStateMaster',
            },
        ),
        migrations.CreateModel(
            name='TblStatusMaster',
            fields=[
                ('statusID', models.AutoField(db_column='statusID', primary_key=True, serialize=False)),
                ('statusName', models.CharField(blank=True, db_column='statusName', max_length=50, null=True)),
                ('statusDescription', models.TextField(blank=True, db_column='statusDescription', null=True)),
            ],
            options={
                'db_table': 'tblStatusMaster',
            },
        ),
        migrations.CreateModel(
            name='TblTitleMaster',
            fields=[
                ('titleAbbreviation', models.CharField(db_column='titleAbbreviation', max_length=5, primary_key=True, serialize=False)),
                ('titleFull', models.CharField(blank=True, db_column='titleFull', max_length=50, null=True)),
            ],
            options={
                'db_table': 'tblTitleMaster',
            },
        ),
        migrations.CreateModel(
            name='TblStaffMaster',
            fields=[
                ('staffID', models.AutoField(db_column='staffID', primary_key=True, serialize=False)),
                ('staffLastName', models.CharField(blank=True, db_column='staffLastName', max_length=50, null=True)),
                ('staffFirstName', models.CharField(blank=True, db_column='staffFirstName', max_length=50, null=True)),
                ('staffEmail', models.EmailField(blank=True, db_column='staffEmail', max_length=100, null=True)),
                ('titleAbbreviation', models.ForeignKey(blank=True, db_column='titleAbbreviation', null=True, on_delete=django.db.models.deletion.CASCADE, to='app.TblTitleMaster')),
            ],
            options={
                'db_table': 'tblStaffMaster',
            },
        ),
        migrations.CreateModel(
            name='TblPRRBContactMaster',
            fields=[
                ('prrbContactID', models.AutoField(db_column='prrbContactID', primary_key=True, serialize=False)),
                ('prrbContactLastName', models.CharField(blank=True, db_column='prrbContactLastName', max_length=50, null=True)),
                ('prrbContactFirstName', models.CharField(blank=True, db_column='prrbContactFirstName', max_length=50, null=True)),
                ('prrbContactEmailAddress', models.EmailField(blank=True, db_column='prrrbContactEmailAddress', max_length=50, null=True)),
                ('prrbContactGenEmailAddress', models.EmailField(blank=True, db_column='prrbContactGenEmailAddress', max_length=100, null=True)),
                ('prrbContactPhone', models.IntegerField(blank=True, db_column='prrbContactPhone', null=True)),
                ('prrbContactStreet', models.CharField(blank=True, db_column='prrbContactStreet', max_length=50, null=True)),
                ('prrbContactStreetTwo', models.CharField(blank=True, db_column='prrbContactStreetTwo', max_length=50, null=True)),
                ('prrbContactCity', models.CharField(blank=True, db_column='prrbContactCity', max_length=50, null=True)),
                ('prrbContactZipCode', models.IntegerField(blank=True, db_column='prrbContactZipCode', null=True)),
                ('stateID', models.ForeignKey(blank=True, db_column='stateID', null=True, on_delete=django.db.models.deletion.CASCADE, to='app.TblStateMaster')),
            ],
            options={
                'db_table': 'tblPRRBContactMaster',
            },
        ),
        migrations.CreateModel(
            name='TblProviderNameMaster',
            fields=[
                ('providerID', models.CharField(db_column='providerID', max_length=7, primary_key=True, serialize=False)),
                ('providerName', models.CharField(blank=True, db_column='providerName', max_length=50, null=True)),
                ('providerFYE', models.DateField(blank=True, db_column='providerFYE', null=True)),
                ('providerCity', models.CharField(blank=True, db_column='providerCity', max_length=50, null=True)),
                ('providerCounty', models.CharField(blank=True, db_column='providerCounty', max_length=50, null=True)),
                ('parentID', models.ForeignKey(blank=True, db_column='parentID', null=True, on_delete=django.db.models.deletion.CASCADE, to='app.TblParentMaster')),
                ('stateID', models.ForeignKey(blank=True, db_column='stateID', null=True, on_delete=django.db.models.deletion.CASCADE, to='app.TblStateMaster')),
            ],
            options={
                'db_table': 'tblProviderNameMaster',
            },
        ),
        migrations.CreateModel(
            name='TblProviderMaster',
            fields=[
                ('provMasterID', models.AutoField(db_column='provMasterID', primary_key=True, serialize=False)),
                ('provMasterAuditAdjs', models.CharField(blank=True, db_column='provMasterAuditAdjs', max_length=50, null=True)),
                ('provMasterAmount', models.DecimalField(blank=True, db_column='provMasterAmount', decimal_places=4, max_digits=19, null=True)),
                ('provMasterToCase', models.CharField(blank=True, db_column='provMasterToCase', max_length=7, null=True)),
                ('provMasterTransferDate', models.DateField(blank=True, db_column='provMasterTransferDate', null=True)),
                ('provMasterFromCase', models.CharField(blank=True, db_column='provMasterFromCase', max_length=7, null=True)),
                ('provMasterNote', models.CharField(blank=True, db_column='provMasterNote', max_length=100, null=True)),
                ('caseNumber', models.ForeignKey(blank=True, db_column='caseNumber', null=True, on_delete=django.db.models.deletion.CASCADE, to='app.TblAppealMaster')),
                ('issueID', models.ForeignKey(blank=True, db_column='issueID', null=True, on_delete=django.db.models.deletion.CASCADE, to='app.TblIssueMaster')),
                ('providerID', models.ForeignKey(blank=True, db_column='providerID', null=True, on_delete=django.db.models.deletion.CASCADE, to='app.TblProviderNameMaster')),
            ],
            options={
                'db_table': 'tblProviderMaster',
            },
        ),
        migrations.CreateModel(
            name='TblProviderContactMaster',
            fields=[
                ('contactID', models.AutoField(db_column='contactID', primary_key=True, serialize=False)),
                ('contactLastName', models.CharField(blank=True, db_column='contactLastName', max_length=50, null=True)),
                ('contactFirstName', models.CharField(blank=True, db_column='contactFirstName', max_length=50, null=True)),
                ('contactTitle', models.CharField(blank=True, db_column='contactTitle', max_length=50, null=True)),
                ('contactEmail', models.EmailField(blank=True, db_column='contactEmail', max_length=50, null=True)),
                ('contactPhone', models.IntegerField(blank=True, db_column='contactPhone', null=True)),
                ('parentID', models.ForeignKey(blank=True, db_column='parentID', null=True, on_delete=django.db.models.deletion.CASCADE, to='app.TblParentMaster')),
                ('providerID', models.ForeignKey(db_column='providerID', on_delete=django.db.models.deletion.CASCADE, to='app.TblProviderNameMaster')),
            ],
            options={
                'db_table': 'tblProviderContactMaster',
            },
        ),
        migrations.AddField(
            model_name='tblissuemaster',
            name='staffID',
            field=models.ForeignKey(blank=True, db_column='staffID', null=True, on_delete=django.db.models.deletion.CASCADE, to='app.TblStaffMaster'),
        ),
        migrations.CreateModel(
            name='TblFIMaster',
            fields=[
                ('fiID', models.AutoField(db_column='fiID', primary_key=True, serialize=False)),
                ('fiLastName', models.CharField(blank=True, db_column='fiLastName', max_length=50, null=True)),
                ('fiFirstName', models.CharField(blank=True, db_column='fiFirstName', max_length=50, null=True)),
                ('fiName', models.CharField(blank=True, db_column='fiName', max_length=75, null=True)),
                ('fiTitle', models.CharField(blank=True, db_column='fiTitle', max_length=50, null=True)),
                ('fiJurisdiction', models.CharField(blank=True, db_column='fiJurisdiction', max_length=10, null=True)),
                ('fiEmail', models.EmailField(blank=True, db_column='fiEmail', max_length=50, null=True)),
                ('fiAppealsEmail', models.EmailField(blank=True, db_column='fiAppealsEmail', max_length=50, null=True)),
                ('fiPhone', models.IntegerField(blank=True, db_column='fiPhone', null=True)),
                ('fiStreet', models.CharField(blank=True, db_column='fiStreet', max_length=50, null=True)),
                ('fiStreetTwo', models.CharField(blank=True, db_column='fiStreetTwo', max_length=50, null=True)),
                ('fiCity', models.CharField(blank=True, db_column='fiCity', max_length=50, null=True)),
                ('fiZip', models.IntegerField(blank=True, db_column='fiZip', null=True)),
                ('stateID', models.ForeignKey(blank=True, db_column='stateID', null=True, on_delete=django.db.models.deletion.CASCADE, to='app.TblStateMaster')),
            ],
            options={
                'db_table': 'tblFIMaster',
            },
        ),
        migrations.CreateModel(
            name='TblCaseDeterminationMaster',
            fields=[
                ('caseDeterminationID', models.AutoField(db_column='caseDeterminationID', primary_key=True, serialize=False)),
                ('determinationDate', models.DateField(blank=True, db_column='determinationDate', null=True)),
                ('determinationDateSubs', models.DateField(blank=True, db_column='determinationDateSubs', null=True)),
                ('determinationFiscalYear', models.DateField(blank=True, db_column='determinationFiscalYear', null=True)),
                ('determinationInfo', models.CharField(blank=True, db_column='determinationInfo', max_length=50, null=True)),
                ('caseNumber', models.ForeignKey(blank=True, db_column='caseNumber', null=True, on_delete=django.db.models.deletion.CASCADE, to='app.TblAppealMaster')),
                ('determinationID', models.ForeignKey(blank=True, db_column='determinationID', null=True, on_delete=django.db.models.deletion.CASCADE, to='app.TblDeterminationType')),
            ],
            options={
                'db_table': 'tblCaseDeterminationMaster',
            },
        ),
    ]
