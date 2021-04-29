from .models import *
import django_filters


class CriticalDateFilter(django_filters.FilterSet):
    date_between = django_filters.DateFromToRangeFilter(field_name='dueDate', label='Date (Between)')

    class Meta:
        model = TblCriticalDatesMaster
        fields = ['caseNumber', 'actionID', 'progress', ]


class CriticalDateFilterTwo(django_filters.FilterSet):
    class Meta:
        model = TblAppealMaster
        fields = ['appealStructure', 'statusID']


class ProviderMasterFilter(django_filters.FilterSet):
    class Meta:
        model = TblProviderMaster
        fields = ['providerID', 'issueID']

    def __init__(self, *args, **kwargs):
        super(ProviderMasterFilter, self).__init__(*args, **kwargs)
        if self.data == {}:
            self.queryset = self.queryset.none()
