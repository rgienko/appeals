from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(TblParentMaster)
class TblParentMasterAdmin(admin.ModelAdmin):
    list_display = ('parentID', 'parentFullName', 'parentAddress',
                    'parentCity', 'stateID', 'parentZIP')


@admin.register(TblStateMaster)
class TblStateMasterAdmin(admin.ModelAdmin):
    list_display = ('stateID', 'stateName')


@admin.register(TblCategoryMaster)
class TblCategoryMasterAdmin(admin.ModelAdmin):
    list_display = ('categoryID', 'categoryName', 'categoryKey', 'categoryDescription')


@admin.register(TblIssueMaster)
class TblIssueMasterAdmin(admin.ModelAdmin):
    list_display = ('issueID', 'issueName', 'issueAbbreviation', 'issueShortDescription',
                    'issueLongDescription', 'categoryID', 'staffID')


@admin.register(TblStaffMaster)
class TblStaffMasterAdmin(admin.ModelAdmin):
    list_display = ('staffID', 'staffLastName', 'staffFirstName',
                    'staffEmail', 'titleAbbreviation')


@admin.register(TblTitleMaster)
class TblTitleMasterAdmin(admin.ModelAdmin):
    list_display = ('titleAbbreviation', 'titleFull')


@admin.register(TblStatusMaster)
class TblStatusMasterAdmin(admin.ModelAdmin):
    list_display = ('statusName', 'statusDescription')


@admin.register(TblDeterminationType)
class TblDeterminationAdmin(admin.ModelAdmin):
    list_display = ('determinationID', 'determinationName')


@admin.register(TblActionMaster)
class TblActionMasterAdmin(admin.ModelAdmin):
    list_display = ('actionID', 'note', 'description', 'lead_time', 'type')


