from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from .models import *
from datetime import datetime
import datetime


class ParentMasterCreateForm(forms.ModelForm):
    class Meta:
        model = TblParentMaster

        fields = [
            'parentID',
            'parentFullName',
            'parentAddress',
            'parentCity',
            'stateID',
            'parentZIP'
        ]

        labels = {
            'parentID': _('Parent ID:'),
            'parentFullName': _('Parent Full Name:'),
            'parentAddress': _('Street Address:'),
            'parentCity': _('City:'),
            'stateID': _('State:'),
            'parentZIP': _('Zip-Code:')
        }

        widgets = {
            'parentID': forms.TextInput(attrs={'size': 50}),
            'parentFullName': forms.TextInput(attrs={'size': 50}),
            'parentAddress': forms.TextInput(attrs={'size': 50}),
            'parentCity': forms.TextInput(attrs={'size': 50}),

        }


class ProviderNameMasterCreateForm(forms.ModelForm):
    class Meta:
        model = TblProviderNameMaster

        fields = [
            'providerID',
            'providerName',
            'providerFYE',
            'providerCity',
            'providerCounty',
            'stateID',
            'parentID'
        ]

        labels = {
            'providerId': _('Provider Number:'),
            'providerName': _('Provider Name:'),
            'providerFYE': _('FYE'),
            'providerCity': _('City'),
            'providerCounty': _('County'),
            'stateID': _('State:'),
            'parentID': _('Parent:')

        }


class IssueMasterCreateForm(forms.ModelForm):
    class Meta:
        model = TblIssueMaster

        fields = [
            'issueSRGID',
            'issueName',
            'issueAbbreviation',
            'issueShortDescription',
            'issueLongDescription',
            'categoryID',
            'staffID'
        ]

        labels = {
            'issueSRGID': _('Issue #:'),
            'issueName': _('Issue Name:'),
            'issueAbbreviation': _('Abbreviation'),
            'issueShortDescription': _('Short Description:'),
            'issueLongDescription': _('Long Description:'),
            'categoryID': _('Category:'),
            'staffID': _('Staff:')

        }

        widgets = {
            'issueName': forms.TextInput(attrs={'size': 50}),
            'issueShortDescription': forms.Textarea(attrs={'cols': 90, 'rows': 5}),
            'issueLongDescription': forms.Textarea(attrs={'cols': 90, 'rows': 15}),

        }


class StaffMasterCreateForm(forms.ModelForm):
    class Meta:
        model = TblStaffMaster

        fields = [
            'staffFirstName',
            'staffLastName',
            'staffEmail',
            'titleAbbreviation'
        ]

        labels = {
            'staffFirstName': _('First Name:'),
            'staffLastName': _('Last Name:'),
            'staffEmail': _('Email:'),
            'titleAbbreviation': _('Title:')
        }

        widgets = {
            'staffFirstName': forms.TextInput(attrs={'size': 50}),
            'staffLastName': forms.TextInput(attrs={'size': 50}),
            'staffEmail': forms.TextInput(attrs={'size': 50}),
        }


class FIMasterCreateForm(forms.ModelForm):
    class Meta:
        model = TblFIMaster

        fields = [
            'fiFirstName',
            'fiLastName',
            'fiName',
            'fiTitle',
            'fiJurisdiction',
            'fiEmail',
            'fiAppealsEmail',
            'fiPhone',
            'fiStreet',
            'fiStreetTwo',
            'fiCity',
            'stateID',
            'fiZip'
        ]

        labels = {
            'fiFirstName': _('First Name:'),
            'fiLastName': _('Last Name:'),
            'fiName': _('FI Name:'),
            'fiTitle': _('Title:'),
            'fiJurisdiction': _('Jurisdiction:'),
            'fiEmail': _('Email:'),
            'fiAppealsEmail': _('Appeals Email:'),
            'fiPhone': _('Phone'),
            'fiStreet': _('Street:'),
            'fiStreetTwo': _('Suite / Unit:'),
            'fiCity': _('City:'),
            'stateID': _('State:'),
            'fiZip': _('Zip Code:')
        }


class PRRBContactMasterCreateForm(forms.ModelForm):
    class Meta:
        model = TblPRRBContactMaster

        fields = [
            'prrbContactFirstName',
            'prrbContactLastName',
            'prrbContactEmailAddress',
            'prrbContactGenEmailAddress',
            'prrbContactPhone',
            'prrbContactStreet',
            'prrbContactStreetTwo',
            'prrbContactCity',
            'stateID',
            'prrbContactZipCode'
        ]

        labels = {
            'prrbContactFirstName': _('First Name:'),
            'prrbContactLastName': _('Last Name:'),
            'prrbContactEmailAddress': _('Email:'),
            'prrbContactGenEmailAddress': _('Appeals Email:'),
            'prrbContactPhone': _('Phone:'),
            'prrbContactStreet': _('Street:'),
            'prrbContactStreetTwo': _('Suite / Unit:'),
            'prrbContactCity': _('City:'),
            'stateID': _('State:'),
            'prrbContactZipCode': _('Zip Code:')
        }


class AppealMasterCreateForm(forms.ModelForm):
    class Meta:
        model = TblAppealMaster

        fields = [
            'caseNumber',
            'staffID',
            'fiID',
            'prrbContactID',
            'statusID',
            'appealStructure',
            'appealName',
            'appealCreateDate',
            'appealAckDate',
            'appealNotes',
        ]

        labels = {
            'caseNumber': _('Case Number:'),
            'staffID': _('Representative:'),
            'fiID': _('FI Representative'),
            'prrbContactID': _('PRRB Representative:'),
            'statusID': _('Case Status:'),
            'appealStructure': _('Case Structure:'),
            'appealName': _('Case Name:'),
            'appealCreateDate': _('Create Date:'),
            'appealAckDate': _('Acknowledged:'),
            'appealNotes': _('Case Notes'),
        }

        widgets = {
            'appealName': forms.TextInput(attrs={'size': 100}),
            'appealCreateDate': forms.DateInput(),
            'appealAckDate': forms.DateInput(),
            'appealNotes': forms.Textarea(attrs={'cols': 90, 'rows': 5}),

        }


class CaseDeterminationMasterForm(forms.ModelForm):
    class Meta:
        model = TblCaseDeterminationMaster

        fields = [
            'caseNumber',
            'determinationID',
            'determinationDate',
            'determinationDateSubs',
            'determinationFiscalYear',
            'determinationInfo'
        ]

        labels = {
            'caseNumber': _('Case Number:'),
            'determinationID': _('Determination Type:'),
            'determinationDate': _('Determination Date:'),
            'determinationDateSubs': _('Determination Date Subs:'),
            'determinationFiscalYear': _('Determination Year'),
            'determinationInfo': _('Determination Info:')
        }

        widgets = {
            'determinationInfo': forms.TextInput(attrs={'size': 50})
        }


class ProviderMasterCreateForm(forms.ModelForm):
    class Meta:
        model = TblProviderMaster

        fields = [
            'caseNumber',
            'providerID',
            'issueID',
            'provMasterAuditAdjs',
            'provMasterImpact',
            'provMasterNote'
        ]

        labels = {
            'caseNumber': _('Case Number:'),
            'providerID': _('Provider Number:'),
            'issueID': _('Issue:'),
            'provMasterAuditAdjs': _('Audit Adjustments:'),
            'provMasterImpact': _('Amount:'),
            'provMasterNote': _('Note:')
        }

        widgets = {
            'provMasterNote': forms.Textarea(attrs={'cols': 75, 'rows': 5})
        }


class CriticalDatesMasterCreateForm(forms.ModelForm):
    class Meta:
        model = CriticalDatesMaster

        fields = [
            'caseNumber',
            'dueDate',
            'actionID',
            'progress'
        ]

        labels = {
            'caseNumber': _('Case Number:'),
            'dueDate': _('Due Date:'),
            'actionID': _('Action Due:'),
            'progress': _('Progress:')
        }


class TransferIssueForm(forms.Form):
    to_case = forms.ModelChoiceField(label='To Case:',
                                     queryset=TblAppealMaster.objects.exclude(appealStructure__exact='Individual').only(
                                         'caseNumber'
                                     ))
    to_date = forms.DateField(label='To Date:', widget=forms.DateInput(attrs={'size': 10}))

    def clean_to_date(self):
        date = self.cleaned_data['to_date']

        return date


class CreateDirectoryForm(forms.Form):
    types = [
        ('INDIVIDUAL', 'Individual'),
        ('GROUP', 'Group')
    ]
    ctype = forms.ChoiceField(label='Case Type:', choices=types)
    parent = forms.ModelChoiceField(label='Parent:', queryset=TblParentMaster.objects.only('parentID'))
    prov = forms.ModelChoiceField(label='Provider:', queryset=TblProviderNameMaster.objects.only('providerID'),
                                  required=False)
    issue = forms.ModelChoiceField(label='Issue:', queryset=TblIssueMaster.objects.only('issueAbbreviation'),
                                   required=False)
    fy = forms.IntegerField(label='Fiscal Year:')
    isFFY = forms.BooleanField(label='FFY:', required=False)
    case = forms.CharField(label='Case Number:', max_length=7)


class AcknowledgeCaseForm(forms.Form):
    ack_date = forms.DateField(label='Enter Date:', help_text="Date of Acknowledgement (default today).")

    def clean_ack_date(self):
        data = self.cleaned_data['ack_date']

        # Check if date is in the past
        if data < datetime.date.today():
            raise ValidationError(_('Invalid Date - Date is in the past'))

        return data


class UpdateCaseStatusForm(forms.Form):
    new_status = forms.ModelChoiceField(label='Select New Status:', queryset=TblStatusMaster.objects.only('statusName'))

    def clean_new_status(self):
        data = self.cleaned_data['new_status']

        return data


class UpdateDueDateProgressForm(forms.Form):
    new_progress = forms.ModelChoiceField(label='Update Progress:', queryset=CriticalDatesMaster.objects.only('progress'))

    def clean_new_progress(self):
        data = self.cleaned_data['new_progress']
        return data