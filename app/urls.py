from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from app import views

urlpatterns = [
    # path(r'', views.login, name='login'),
    path(r'', views.sign_in, name='login'),
    path(r'main/', views.home, name='home'),
    path(r'<pk>/details', views.appealDetailsView, name='appeal-details'),
    path(r'<pk>/details/add-issue', views.addIssueView, name='add-issue'),
    path(r'<pk>/details/add-prov', views.addProviderToGroup, name='add-prov'),
    path(r'<pk>/details/add-due-dates/', views.addCriticalDueView, name='add-due'),
    path(r'<pk>/transfer-issue/', views.transferIssueView, name='transfer-issue'),
    path(r'<pk>/ScheduleG/', views.createFormG, name='form-g'),
    path(r'new/appeal/', views.NewAppealMasterView.as_view(), name='new-appeal'),
    path(r'new/appeal/<pk>/determination/', views.addDeterminationView, name='new-deter'),
    path(r'parent-master/', views.parentMasterView, name='parent-master'),
    path(r'new/parent/', views.NewSystemView.as_view(), name='new-parent'),
    path(r'edit/parent/<pk>/', views.parentUpdateView, name='update-parent'),
    path(r'provider-master/', views.providerMasterView, name='provider-master'),
    path(r'new/provider/', views.NewProviderView.as_view(), name='new-provider'),
    path(r'edit/prov/<pk>', views.providerNameUpdateView, name='update-provider'),
    path(r'issue-master/', views.issueMasterView, name='issue-master'),
    path(r'new/issue/', views.NewIssueView.as_view(), name='new-issue'),
    path(r'staff-master/', views.staffMasterView, name='staff-master'),
    path(r'new/staff/', views.NewStaffView.as_view(), name='new-staff'),
    path(r'mac-master/', views.fiMasterView, name='mac-master'),
    path(r'new/mac/', views.NewFIView.as_view(), name='new-mac'),
    path(r'prrb-master/', views.prrbMasterView, name='prrb-master'),
    path(r'new/prrb/', views. NewPRRBContactView.as_view(), name='new-prrb'),
    path(r'^search/$', views.searchCriticalDueDates, name='due-master')

]
