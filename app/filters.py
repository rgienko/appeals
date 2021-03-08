from .models import *
import django_filters


class CriticalDateFilter(django_filters.FilterSet):
    date_between = django_filters.DateFromToRangeFilter(field_name='dueDate', label='Date (Between)')

    class Meta:
        model = CriticalDatesMaster
        fields = ['caseNumber', 'actionID', 'progress',]
