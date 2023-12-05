from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django_filters.views import FilterView
from app import views
from app.models import TblProviderMaster

urlpatterns = [
    # path(r'', views.login, name='login'),
    path(r'', views.home, name='home'),
    path('signin', views.sign_in, name='signin'),
    path('signout', views.sign_out, name='signout'),
    path('callback', views.callback, name='callback'),
    path(r'main/', views.main, name='main'),
    path(r'<pk>/details', views.appealDetailsView, name='appeal-details'),
    path(r'<pk>/details/add-issue', views.addIssueView, name='add-issue'),
    path(r'<pk>/details/add-prov', views.addProviderToGroup, name='add-prov'),
    path(r'edit/details/issue/<pk>', views.providerMasterUpdateView, name='edit-case-issue'),
    path(r'edit/details/due-dates/<pk>', views.updateDueDateProgress, name='update-due-progress'),
    path(r'edit/npr-due-date/<pk>', views.updateNPRDueDateProgress, name='update-npr-progress'),
    path(r'<pk>/details/add-due-dates/', views.addCriticalDueView, name='add-due'),
    path(r'<pk>/transfer-issue/', views.transferIssueView, name='transfer-issue'),
    path(r'<pk>/withdraw-issue/', views.withdrawFromCase, name='withdraw-from-case'),
    path(r'<pk>/ScheduleG/cover-letter/', views.createFormGCoverLetter, name='form-g-cover-letter'),
    path(r'<pk>/ScheduleG/issue-statement/', views.createFormGIssueState, name='form-g-issue-state'),
    path(r'<pk>/ScheduleG/toc/', views.createFormGToc, name='form-g-toc'),
    path(r'<pk>/ScheduleG/exhibits/', views.createFormGExhibits, name='form-g-exhibits'),
    path(r'<pk>/ScheduleG/form-g/', views.createFormG, name='form-g'),
    path(r'new/appeal/', views.NewAppealMasterView.as_view(), name='new-appeal'),
    path(r'parent-master/', views.parentMasterView, name='parent-master'),
    path(r'new/parent/', views.NewSystemView.as_view(), name='new-parent'),
    path(r'edit/parent/<pk>/', views.parentUpdateView, name='update-parent'),
    path(r'new/hosp-contact/<pk>', views.NewHospContactView, name='new-hosp-contact'),
    path(r'provider-master/', views.providerMasterView, name='provider-master'),
    path(r'new/provider/', views.NewProviderView.as_view(), name='new-provider'),
    path(r'edit/prov/<pk>', views.providerNameUpdateView, name='update-provider'),
    path(r'issue-master/', views.issueMasterView, name='issue-master'),
    path(r'issue-master/detail/<pk>', views.issueDetailView, name='issue-detail'),
    path(r'new-issue/', views.NewIssueView.as_view(), name='new-issue'),
    path(r'edit/issue/<pk>/', views.issueEditView, name='edit-issue'),
    path(r'staff-master/', views.staffMasterView, name='staff-master'),
    path(r'new/staff/', views.NewStaffView.as_view(), name='new-staff'),
    path(r'mac-master/', views.fiMasterView, name='mac-master'),
    path(r'mac-master/<pk>/edit', views.editFI, name='edit-mac'),
    path(r'new/mac/', views.NewFIView.as_view(), name='new-mac'),
    path(r'prrb-master/', views.prrbMasterView, name='prrb-master'),
    path(r'new/prrb/', views.NewPRRBContactView.as_view(), name='new-prrb'),
    path(r'prrb-master/<pk>/edit', views.editPRRB, name='edit-prrb'),
    path(r'^search/$', views.searchCriticalDueDates, name='due-master'),
    path(r'search-two', views.searchCriticalDueDatesTwo, name='due-master-two'),
    path(r'provmaster-filter', views.providerAppealDetails, name='prov-appeal-details'),
    path(r'provmaster-filter', FilterView.as_view(model=TblProviderMaster), name='prov-appeal-details'),
    path(r'group-report/', views.groupReport, name='group-report'),
    path(r'provider-report/', views.providerReport, name='provider-report')

]
