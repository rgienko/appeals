import datetime
from datetime import timedelta
from django.db import models
import uuid


# Models for Appeal Issues

class TblCategoryMaster(models.Model):
    categoryID = models.AutoField(db_column='categoryID', primary_key=True)
    categoryName = models.CharField(
        db_column='categoryName', max_length=50, blank=True, null=True)
    categoryKey = models.CharField(
        db_column='categoryKey', unique=True, max_length=10, blank=True, null=True)
    categoryDescription = models.CharField(db_column='categoryDescription', max_length=150, blank=True,
                                           null=True)

    class Meta:
        db_table = 'tblCategoryMaster'

    def __str__(self):
        return '%s - %s' % (self.categoryID, self.categoryKey)


class TblTitleMaster(models.Model):
    titleAbbreviation = models.CharField(
        db_column='titleAbbreviation', primary_key=True, max_length=5)
    titleFull = models.CharField(
        db_column='titleFull', max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'tblTitleMaster'

    def __str__(self):
        return self.titleFull


class TblStaffMaster(models.Model):
    staffID = models.AutoField(db_column='staffID', primary_key=True)
    staffLastName = models.CharField(
        db_column='staffLastName', max_length=50, blank=True, null=True)
    staffFirstName = models.CharField(
        db_column='staffFirstName', max_length=50, blank=True, null=True)
    staffEmail = models.EmailField(
        db_column='staffEmail', max_length=100, blank=True, null=True)
    titleAbbreviation = models.ForeignKey('TblTitleMaster', on_delete=models.CASCADE, db_column='titleAbbreviation',
                                          blank=True, null=True)

    class Meta:
        db_table = 'tblStaffMaster'

    def __str__(self):
        return self.staffLastName


class TblIssueMaster(models.Model):
    issueID = models.AutoField(db_column='issueID', primary_key=True)
    issueSRGID = models.IntegerField(null=True, blank=True)
    issueName = models.CharField(
        db_column='issueName', max_length=100, blank=True, null=True)
    issueAbbreviation = models.CharField(
        db_column='issueAbbreviation', max_length=25, blank=True, null=True)
    issueShortDescription = models.TextField(
        db_column='issueShortDescription', blank=True, null=True)
    issueLongDescription = models.TextField(
        db_column='issueLongDescription', blank=True, null=True)
    categoryID = models.ForeignKey('TblCategoryMaster', on_delete=models.CASCADE, db_column='categoryID',
                                   blank=True, null=True)
    staffID = models.ForeignKey('TblStaffMaster', on_delete=models.CASCADE, db_column='staffID',
                                blank=True, null=True)

    class Meta:
        db_table = 'tblIssueMaster'

    def __str__(self):
        return '{0}-{1}'.format(str(self.issueSRGID), self.issueName)


# Models for Provider Name tables


class TblStateMaster(models.Model):
    stateID = models.CharField(
        db_column='stateID', primary_key=True, max_length=2)
    stateName = models.CharField(db_column='stateName', max_length=50)

    class Meta:
        db_table = 'tblStateMaster'
        ordering = ['stateID']

    def __str__(self):
        return self.stateID


class TblParentMaster(models.Model):
    parentID = models.CharField(
        db_column='parentID', primary_key=True, max_length=50)
    parentFullName = models.CharField(
        db_column='parentFullName', max_length=255, blank=True, null=True)
    parentAddress = models.CharField(max_length=100, null=True, blank=True)
    parentCity = models.CharField(max_length=50, null=True, blank=True)
    stateID = models.ForeignKey(
        'TblStateMaster', on_delete=models.CASCADE, blank=True, null=True)
    parentZIP = models.IntegerField()

    class Meta:
        db_table = 'tblParentMaster'

    def __str__(self):
        return self.parentFullName


class TblProviderNameMaster(models.Model):
    providerID = models.CharField(
        db_column='providerID', primary_key=True, max_length=7)
    providerName = models.CharField(
        db_column='providerName', max_length=50, blank=True, null=True)
    providerFYE = models.DateField(
        db_column='providerFYE', blank=True, null=True)
    providerCity = models.CharField(
        db_column='providerCity', max_length=50, blank=True, null=True)
    providerCounty = models.CharField(
        db_column='providerCounty', max_length=50, blank=True, null=True)
    providerIsClient = models.BooleanField(blank=True, null=True)
    stateID = models.ForeignKey(
        'TblStateMaster', on_delete=models.CASCADE, db_column='stateID', blank=True, null=True)
    parentID = models.ForeignKey('TblParentMaster', on_delete=models.CASCADE, db_column='parentID', blank=True,
                                 null=True)
    fiID = models.ForeignKey('TblFIMaster', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = 'tblProviderNameMaster'

    def __str__(self):
        return self.providerID

    def getParentName(self):
        return self.parentID.parentFullName

    def properProvName(self):
        return self.providerName.title()


class TblProviderContactMaster(models.Model):
    contactID = models.AutoField(db_column='contactID', primary_key=True)
    contactLastName = models.CharField(
        db_column='contactLastName', max_length=50, blank=True, null=True)
    contactFirstName = models.CharField(
        db_column='contactFirstName', max_length=50, blank=True, null=True)
    contactTitle = models.CharField(
        db_column='contactTitle', max_length=50, blank=True, null=True)
    contactEmail = models.EmailField(
        db_column='contactEmail', max_length=50, blank=True, null=True)
    contactPhone = models.IntegerField(
        db_column='contactPhone', blank=True, null=True)
    providerID = models.ForeignKey(
        'TblProviderNameMaster', on_delete=models.CASCADE, db_column='providerID')
    parentID = models.ForeignKey('TblParentMaster', on_delete=models.CASCADE, db_column='parentID', blank=True,
                                 null=True)

    class Meta:
        db_table = 'tblProviderContactMaster'


class TblFIMaster(models.Model):
    fiID = models.AutoField(db_column='fiID', primary_key=True)
    fiLastName = models.CharField(
        db_column='fiLastName', max_length=50, blank=True, null=True)
    fiFirstName = models.CharField(
        db_column='fiFirstName', max_length=50, blank=True, null=True)
    fiName = models.CharField(
        db_column='fiName', max_length=75, blank=True, null=True)
    fiTitle = models.CharField(
        db_column='fiTitle', max_length=50, blank=True, null=True)
    fiJurisdiction = models.CharField(
        db_column='fiJurisdiction', max_length=10, blank=True, null=True)
    fiEmail = models.EmailField(
        db_column='fiEmail', max_length=50, blank=True, null=True)
    fiAppealsEmail = models.EmailField(
        db_column='fiAppealsEmail', max_length=50, blank=True, null=True)
    fiPhone = models.IntegerField(db_column='fiPhone', blank=True, null=True)
    fiStreet = models.CharField(
        db_column='fiStreet', max_length=50, blank=True, null=True)
    fiStreetTwo = models.CharField(
        db_column='fiStreetTwo', max_length=50, blank=True, null=True)
    fiCity = models.CharField(
        db_column='fiCity', max_length=50, blank=True, null=True)
    stateID = models.ForeignKey(
        'TblStateMaster', on_delete=models.CASCADE, db_column='stateID', blank=True, null=True)
    fiZip = models.IntegerField(db_column='fiZip', blank=True, null=True)

    class Meta:
        db_table = 'tblFIMaster'

    def __str__(self):
        return '{0}-{1}'.format(self.fiName, self.fiJurisdiction)

    def get_id(self):
        return self.fiID


class TblPRRBContactMaster(models.Model):
    prrbContactID = models.AutoField(
        db_column='prrbContactID', primary_key=True)
    prrbContactLastName = models.CharField(
        db_column='prrbContactLastName', max_length=50, blank=True, null=True)
    prrbContactFirstName = models.CharField(
        db_column='prrbContactFirstName', max_length=50, blank=True, null=True)
    prrbContactEmailAddress = models.EmailField(db_column='prrrbContactEmailAddress', max_length=50, blank=True,
                                                null=True)
    prrbContactGenEmailAddress = models.EmailField(db_column='prrbContactGenEmailAddress', max_length=100, blank=True,
                                                   null=True)  # Field name made lowercase.
    prrbContactPhone = models.IntegerField(
        db_column='prrbContactPhone', blank=True, null=True)
    prrbContactStreet = models.CharField(
        db_column='prrbContactStreet', max_length=50, blank=True, null=True)
    prrbContactStreetTwo = models.CharField(
        db_column='prrbContactStreetTwo', max_length=50, blank=True, null=True)
    prrbContactCity = models.CharField(
        db_column='prrbContactCity', max_length=50, blank=True, null=True)
    prrbContactZipCode = models.IntegerField(
        db_column='prrbContactZipCode', blank=True, null=True)
    stateID = models.ForeignKey(
        'TblStateMaster', on_delete=models.CASCADE, db_column='stateID', blank=True, null=True)

    class Meta:
        db_table = 'tblPRRBContactMaster'

    def __str__(self):
        return self.prrbContactLastName


class TblStatusMaster(models.Model):
    statusID = models.AutoField(db_column='statusID', primary_key=True)
    statusName = models.CharField(
        db_column='statusName', max_length=50, blank=True, null=True)
    statusDescription = models.TextField(
        db_column='statusDescription', blank=True, null=True)

    class Meta:
        db_table = 'tblStatusMaster'

    def __str__(self):
        return '{0}-{1}'.format(str(self.statusID), self.statusName)


class TblDeterminationType(models.Model):
    # Field name made lowercase.
    determinationID = models.CharField(
        db_column='determinationID', primary_key=True, max_length=15)
    # Field name made lowercase.
    determinationName = models.CharField(
        db_column='determinationName', max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'tblDeterminationType'

    def __str__(self):
        return self.determinationID


class TblAppealMaster(models.Model):
    caseNumber = models.CharField(
        db_column='caseNumber', primary_key=True, max_length=7)
    appealName = models.CharField(
        db_column='appealName', blank=True, null=True, max_length=255)
    appealNotes = models.TextField(
        db_column='appealNotes', blank=True, null=True)
    structureChoices = {
        ('Individual', 'Individual'),
        ('CIRP', 'CIRP'),
        ('Optional', 'Optional')
    }
    appealStructure = models.CharField(
        db_column='appealStructure', max_length=25, choices=structureChoices, blank=True, null=True)
    appealCreateDate = models.DateField(
        db_column='appealCreateDate', blank=True, null=True)
    appealAckDate = models.DateField(
        db_column='appealAckDate', blank=True, null=True)
    staffID = models.ForeignKey(
        'TblStaffMaster', on_delete=models.CASCADE, db_column='staffID', blank=True, null=True)
    statusID = models.ForeignKey(
        'TblStatusMaster', on_delete=models.CASCADE, db_column='statusID', blank=True, null=True)
    prrbContactID = models.ForeignKey(
        'TblPRRBContactMaster', on_delete=models.CASCADE, db_column='prrbContactID', blank=True, null=True)
    fiID = models.ForeignKey(
        'TblFIMaster', on_delete=models.CASCADE, db_column='fiID', blank=True, null=True)

    class Meta:
        db_table = 'tblAppealMaster'

    def __str__(self):
        return self.caseNumber

    def get_rep(self):
        repObj = TblStaffMaster.objects.get(staffID=self.staffID)
        return '{0} {1}'.format(repObj.staffFirstName, repObj.staffLastName)

    def get_fi(self):
        return self.fiID.fiName

    def get_deter_date(self):
        ddate = TblCaseDeterminationMaster.objects.get(
            caseNumber=self.caseNumber)
        return str(ddate.determinationDate)


class TblCaseDeterminationMaster(models.Model):
    caseDeterminationID = models.AutoField(
        db_column='caseDeterminationID', primary_key=True)
    caseNumber = models.ForeignKey(
        'TblAppealMaster', on_delete=models.CASCADE, db_column='caseNumber', blank=True, null=True)
    providerNumber = models.ForeignKey('TblProviderNameMaster', db_column='providerID',
                                       on_delete=models.CASCADE, blank=True, null=True)
    determinationID = models.ForeignKey(
        'TblDeterminationType', on_delete=models.CASCADE, db_column='determinationID', blank=True, null=True)
    determinationDate = models.DateField(
        db_column='determinationDate', blank=True, null=True)
    determinationDateSubs = models.DateField(
        db_column='determinationDateSubs', blank=True, null=True)
    determinationFiscalYear = models.DateField(
        db_column='determinationFiscalYear', blank=True, null=True)
    determinationInfo = models.CharField(
        db_column='determinationInfo', max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'tblCaseDeterminationMaster'


class TblProviderMaster(models.Model):
    # Field name made lowercase.
    provMasterID = models.AutoField(db_column='provMasterID', primary_key=True)
    caseNumber = models.ForeignKey(
        'TblAppealMaster', on_delete=models.CASCADE, db_column='caseNumber', blank=True, null=True)
    providerID = models.ForeignKey(
        'TblProviderNameMaster', on_delete=models.CASCADE, db_column='providerID', blank=True, null=True)
    provMasterDeterminationDate = models.DateField(blank=True, null=True)
    determinationTypes = {
        ('FR', 'FR'),
        ('NPR', 'NPR'),
        ('RNPR', 'RNPR'),
        ('Other', 'Other')
    }
    provMasterDeterminationType = models.CharField(max_length=4, choices=determinationTypes, blank=True, null=True)
    provMasterFiscalYear = models.DateField(blank=True, null=True)
    issueID = models.ForeignKey(
        'TblIssueMaster', on_delete=models.CASCADE, db_column='issueID', blank=True, null=True)
    provMasterAuditAdjs = models.CharField(
        db_column='provMasterAuditAdjs', max_length=50, blank=True, null=True)
    provMasterWasAdded = models.BooleanField(default=False)
    provMasterImpact = models.DecimalField(
        db_column='provMasterAmount', max_digits=19, decimal_places=0, blank=True, null=True)
    provMasterToCase = models.CharField(
        db_column='provMasterToCase', max_length=7, blank=True, null=True)
    provMasterTransferDate = models.DateField(
        db_column='provMasterTransferDate', blank=True, null=True)
    provMasterFromCase = models.CharField(
        db_column='provMasterFromCase', max_length=7, blank=True, null=True)
    provMasterNote = models.CharField(
        db_column='provMasterNote', max_length=100, blank=True, null=True)
    provMasterDateStamp = models.DateField(blank=True, null=True)
    provMasterIsActive = models.BooleanField(default=True, blank=True, null=True)

    class Meta:
        db_table = 'tblProviderMaster'

    def get_appeal_structure(self):
        caseObj = TblAppealMaster.objects.get(caseNumber=self.caseNumber)
        return caseObj.appealStructure

    def get_prov_name(self):
        return self.providerID.providerName

    def get_parent(self):
        return self.providerID.parentID.parentFullName

    def get_deter_date(self):
        ddate = TblCaseDeterminationMaster.objects.get(
            providerNumber=self.providerID)
        return ddate.determinationDate

    def get_fye(self):
        fye = TblCaseDeterminationMaster.objects.get(
            caseNumber=self.provMasterFromCase)
        return str(fye.determinationFiscalYear)

    def get_srg_id(self):
        return self.issueID.issueSRGID

    def get_issue_name(self):
        return self.issueID.issueName

    def get_issue_statement(self):
        return self.issueID.issueLongDescription

    def get_hrq_date(self):
        hrqDate = TblAppealMaster.objects.get(
            caseNumber=self.provMasterFromCase)
        return hrqDate.appealCreateDate

    def get_no_days(self):
        hrqDate = TblAppealMaster.objects.get(caseNumber=self.provMasterFromCase)
        delta = hrqDate.appealCreateDate - self.provMasterDeterminationDate
        return delta.days

    def get_ind_fi(self):
        indivCase = TblAppealMaster.objects.get(caseNumber=self.provMasterFromCase)
        fi = indivCase.fiID
        return fi


class TblActionMaster(models.Model):
    actionID = models.CharField(primary_key=True, max_length=25, default='')
    note = models.TextField(blank=True, null=True)
    description = models.TextField(max_length=3000, blank=True, null=True)
    lead_time = models.IntegerField(blank=True, null=True)
    type = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.actionID


class NPRDueDatesMaster(models.Model):
    nprID = models.AutoField(db_column='provMasterID', primary_key=True)
    parentID = models.ForeignKey('TblParentMaster', on_delete=models.CASCADE, max_length=50, blank=True, null=True)
    providerID = models.ForeignKey('TblProviderNameMaster', on_delete=models.CASCADE, blank=True, null=True)
    nprFY = models.IntegerField()
    nprDate = models.DateField()
    statuses = [
        ('Not Filed', 'Not Filed'),
        ('Not Started', 'Not Started'),
        ('Completed', 'Completed')
    ]
    status = models.CharField(max_length=20, choices=statuses, default= 'Not Started', blank=True, null=True)

    def get_prov_name(self):
        return self.providerID.providerName

    def get_prov_parent(self):
        return self.providerID.parentID

    def calc_deadline(self):
        due_date = self.nprDate + timedelta(days=180)
        return due_date


class TblCriticalDatesMaster(models.Model):
    id = models.AutoField(primary_key=True)
    caseNumber = models.ForeignKey('TblAppealMaster', on_delete=models.CASCADE)
    dueDate = models.DateField()
    actionID = models.ForeignKey(
        'TblActionMaster', on_delete=models.CASCADE, blank=True, null=True)
    # action = models.TextField(blank=True, null=True)
    response = models.TextField(blank=True, null=True)
    progress_choices = [
        ('Unknown', 'Unknown'),
        ('Not Applicable', 'Not Applicable'),
        ('Not Started', 'Not Started'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed')
    ]
    progress = models.CharField(
        max_length=20, choices=progress_choices, default='Not Started', blank=True, null=True)

    class Meta:
        ordering = ['dueDate']

    def __str__(self):
        return str(self.caseNumber)

    def due_date_status(self):
        today = datetime.datetime.strptime(
            str(datetime.date.today()), "%Y-%m-%d")
        due = datetime.datetime.strptime(str(self.dueDate), "%Y-%m-%d")
        if (due-today).days < 90:
            return "Low"
        elif (due-today).days < 60:
            return "Medium"
        elif (due-today).days < 30:
            return "Important"
        elif (due-today).days < 7:
            return "URGENT"
        else:
            return ""

    def get_action_note(self):
        return self.actionID.note

    def get_action_details(self):
        return self.actionID.description

    def get_response(self):
        return self.actionID.type

    def get_case_structure(self):
        return self.caseNumber.appealStructure

    def get_appeal_name(self):
        return self.caseNumber.appealName

    def get_provider(self):
        caseIssues = TblProviderMaster.objects.filter(
            caseNumber=self.caseNumber)
        provInfo = caseIssues.first()
        provNum = provInfo.providerID
        provName = TblProviderNameMaster.objects.get(providerID=provNum)
        provName = provName.providerName
        return '{0} - {1}'.format(provNum, provName)

    def get_fy(self):
        caseIssues = TblProviderMaster.objects.filter(
            caseNumber=self.caseNumber)
        provInfo = caseIssues.first()
        caseFY = provInfo.provMasterFiscalYear
        return caseFY


class CriticalDatesMaster(models.Model):
    id = models.AutoField(primary_key=True)
    caseNumber = models.ForeignKey(
        'TblAppealMaster', on_delete=models.CASCADE, blank=True, null=True)
    dueDate = models.DateField()
    actionID = models.ForeignKey(
        'TblActionMaster', on_delete=models.CASCADE, blank=True, null=True)
    # action = models.TextField(blank=True, null=True)
    response = models.TextField(blank=True, null=True)
    progress_choices = [
        ('Unknown', 'Unknown'),
        ('Not Applicable', 'Not Applicable'),
        ('Not Started', 'Not Started'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed')
    ]
    progress = models.CharField(
        max_length=20, choices=progress_choices, default='Not Started', blank=True, null=True)

    class Meta:
        ordering = ['dueDate']

    def __str__(self):
        return str(self.caseNumber)

    def due_date_status(self):
        today = datetime.datetime.strptime(
            str(datetime.date.today()), "%Y-%m-%d")
        due = datetime.datetime.strptime(str(self.dueDate), "%Y-%m-%d")
        if (due-today).days < 90:
            return "Low"
        elif (due-today).days < 60:
            return "Medium"
        elif (due-today).days < 30:
            return "Important"
        elif (due-today).days < 7:
            return "URGENT"
        else:
            return ""

    def get_action_note(self):
        return self.actionID.note

    def get_action_details(self):
        return self.actionID.description

    def get_response(self):
        return self.actionID.type

    def get_case_structure(self):
        return self.caseNumber.appealStructure

    def get_appeal_name(self):
        return self.caseNumber.appealName

    def get_provider(self):
        caseIssues = TblProviderMaster.objects.filter(
            caseNumber=self.caseNumber)
        provInfo = caseIssues.first()
        provNum = provInfo.providerID
        provName = TblProviderNameMaster.objects.get(providerID=provNum)
        provName = provName.providerName
        return '{0} - {1}'.format(provNum, provName)

