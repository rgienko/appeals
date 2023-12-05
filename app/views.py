import datetime
import locale
import random
import django.db.models.functions.math
from io import BytesIO

from django.contrib import auth, messages
from django.db.models import Sum, Q, Count
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak

from app.auth_helper import *
from app.forms import *
from app.graph_helper import *
from .filters import *

global title
global cnum
global case_name
global case_rep
global case_issue
global groupTotalImpact


# Create your views here.

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('main')
    else:
        messages.error(request, 'Error, wrong username / password')
    return render(request, 'main/login.html', {
        'title': 'Login',
    })


def initialize_context(request):
    context = {}

    error = request.session.pop('flash_error', None)

    if error is not None:
        context['errors'] = []
        context['errors'].append(error)

    context['user'] = request.session.get('user', {'is_authenticated': False})

    return context


def home(request):
    context = initialize_context(request)
    return render(request, 'main/click.html', context)


def sign_in(request):
    # Get the sign-in flow
    flow = get_sign_in_flow()
    # Save the expected flow so we can use it in the callback
    try:
        request.session['auth_flow'] = flow
    except Exception as e:
        print(e)
    # Redirect to the Azure sign-in page
    return HttpResponseRedirect(flow['auth_uri'])


def callback(request):
    # Make the token request
    result = get_token_from_code(request)

    # Get the user's profile
    user = get_user(result['access_token'])

    # Store user
    store_user(request, user)
    return HttpResponseRedirect(reverse('main'))


def sign_out(request):
    # Clear out the user and token
    remove_user_and_token(request)

    return HttpResponseRedirect(reverse('home'))


def main(request):
    context = initialize_context(request)

    allDueDates = TblCriticalDatesMaster.objects.all().filter(progress='Not Started').order_by('dueDate')[:20]
    nprDueDates = NPRDueDatesMaster.objects.all().order_by('nprDueDate')
    today = datetime.date.today()

    dueDates = TblCriticalDatesMaster.objects.all().filter(progress='Not Started').order_by('dueDate')
    dueDatesThirty = dueDates.filter(dueDate__lte=today + datetime.timedelta(days=30))
    dueDatesSixty = dueDates.filter(
        dueDate__range=(today + datetime.timedelta(days=30), today + datetime.timedelta(days=60)))
    dueDatesNinety = dueDates.filter(
        dueDate__range=(today + datetime.timedelta(days=60), today + datetime.timedelta(days=90)))
    dueDatesOneTwenty = dueDates.filter(
        dueDate__range=(today + datetime.timedelta(days=90), today + datetime.timedelta(days=120)))

    nprDueDatesThirty = nprDueDates.filter(nprDueDate__lte=today + datetime.timedelta(days=30))
    nprDueDatesSixty = nprDueDates.filter(
        nprDueDate__range=(today + datetime.timedelta(days=30), today + datetime.timedelta(days=60)))

    if request.method == 'POST' and 'add_npr_due_button' not in request.POST:
        search_case = request.POST.get('search')
        return redirect('appeal-details', search_case)

    elif request.method == 'POST' and 'add_npr_due_button' in request.POST:
        form = NPRDueDatesMasterCreateForm(request.POST)
        # due_date = request.POST.get('nprDate') + datetime.timedelta(days=180)

        if form.is_valid():
            new_npr_due_date = form.save(commit=False)
            new_npr_due_date.nprDueDate = new_npr_due_date.nprDate + timedelta(days=180)
            new_npr_due_date.save()

            # Create the data for outlook event
            token = get_token(request)

            # Create the subject
            parent = new_npr_due_date.parentID
            parent = TblParentMaster.objects.get(parentFullName=parent)
            subject = '{0}~{1}~FY{2}~HRQ'.format(parent.parentID,
                                                 new_npr_due_date.providerID,
                                                 str(new_npr_due_date.nprFY))

            npr_date = new_npr_due_date.nprDate
            due_date = npr_date + timedelta(days=180)
            start_year = due_date.year
            start_month = due_date.month
            start_day = due_date.day

            start_time = datetime.datetime(start_year, start_month, start_day,
                                           random.randint(1, 12), random.randint(0, 59), 0)
            end_time = start_time + timedelta(minutes=30)

            body = 'Request for Hearing Due'

            lead_time = 4 * 10080

            create_event(
                token,
                subject,
                start_time,
                end_time,
                lead_time,
                body
            )
            return redirect(r'main')
    else:
        form = NPRDueDatesMasterCreateForm()

    context['form'] = form
    context['allDueDates'] = allDueDates
    context['dueDatesThirty'] = dueDatesThirty
    context['dueDatesSixty'] = dueDatesSixty
    context['dueDatesNinety'] = dueDatesNinety
    context['dueDatesOneTwenty'] = dueDatesOneTwenty
    context['nprDueDates'] = nprDueDates
    context['nprDueDatesThirty'] = nprDueDatesThirty
    context['nprDueDatesSixty'] = nprDueDatesSixty
    context['today'] = today

    return render(request, 'main/index.html', context)


class NewProviderView(CreateView):
    model = TblProviderNameMaster
    form_class = ProviderNameMasterCreateForm
    template_name = 'create/create_form.html'
    context_object_name = 'new_provider'

    def form_valid(self, form):
        new_provider = form.save(commit=False)
        new_provider.save()
        return redirect('main')

    def get(self, request, *args, **kwargs):
        context = initialize_context(request)
        form = self.form_class(request.POST)
        context['form'] = form
        context['formName'] = 'Add Provider'
        context['today'] = datetime.datetime.now() - datetime.timedelta(hours=6)
        return render(request, self.template_name, context)


def providerNameUpdateView(request, pk):
    context = initialize_context(request)
    provider_object = get_object_or_404(TblProviderNameMaster, pk=pk)
    if request.method == 'POST':
        form = ProviderNameMasterCreateForm(
            request.POST, instance=provider_object)

        if form.is_valid():
            provider_object = form.save(commit=False)
            provider_object.save()

            return redirect('provider-master')
    else:
        form = ProviderNameMasterCreateForm(instance=provider_object)

    context['form'] = form
    context['formName'] = 'Update Provider'
    context['today'] = date.today()
    return render(request, 'create/create_form.html', context)


def providerMasterView(request):
    context = initialize_context(request)
    # all_providers = TblProviderNameMaster.objects.all()
    # all_clients = TblProviderNameMaster.objects.filter(providerIsClient=1).order_by('parentID', 'providerID')
    allProviders = (TblProviderMaster.objects.values('providerID', 'providerID__providerName',
                                                     'providerID__fiID__fiName', 'providerID__fiID__fiJurisdiction',
                                                     'providerID__parentID__parentFullName')
                    .annotate(pcount=Count('providerID')).order_by('providerID__parentID__parentFullName',
                                                                   'providerID'))
    context['allProviders'] = allProviders
    context['today'] = date.today()
    return render(request, 'main/providerMaster.html', context)


def NewHospContactView(request, pk):
    parent = get_object_or_404(TblParentMaster, pk=pk)

    if request.method == 'POST':
        form = HospContactCreateForm(request.POST, initial={'parentID': parent.parentID})

        if form.is_valid():
            new_hosp_contact = form.save(commit=False)
            new_hosp_contact.save()
            return redirect('parent-master')

    else:
        form = HospContactCreateForm(request.POST, initial={'parentID': parent.parentID})

    context = initialize_context(request)
    context['form'] = form
    context['formName'] = 'Add Hospital Contact'
    context['today'] = date.today()
    return render(request, 'create/create_form.html', context)


class NewSystemView(CreateView):
    model = TblParentMaster
    form_class = ParentMasterCreateForm
    template_name = 'create/create_form.html'
    context_object_name = 'new_parent'

    def form_valid(self, form):
        new_parent = form.save(commit=False)
        new_parent.save()
        return redirect('parent-master')

    def get(self, request, *args, **kwargs):
        context = initialize_context(request)
        form = self.form_class(request.POST)
        context['form'] = form
        context['formName'] = 'New System'
        return render(request, self.template_name, context)


def parentMasterView(request):
    context = initialize_context(request)
    all_parents = TblParentMaster.objects.all().prefetch_related('tblhospcontactmaster_set')
    print(all_parents)
    context['all_parents'] = all_parents
    context['today'] = date.today()
    return render(request, 'main/parentMaster.html', context)


def parentUpdateView(request, pk):
    context = initialize_context(request)
    parent_obj = get_object_or_404(TblParentMaster, pk=pk)

    if request.method == 'POST':
        form = ParentMasterCreateForm(request.POST, instance=parent_obj)

        if form.is_valid():
            parent_obj = form.save(commit=False)
            parent_obj.save()

            return redirect('parent-master')
    else:
        form = ParentMasterCreateForm(instance=parent_obj)

    context['form'] = form
    context['formName'] = 'Update System'
    return render(request, 'create/create_form.html', context)


def providerMasterUpdateView(request, pk):
    context = initialize_context(request)
    providerMaster_obj = get_object_or_404(TblProviderMaster, pk=pk)

    if request.method == 'POST':
        form = ProviderMasterCreateForm(request.POST, instance=providerMaster_obj)

        if form.is_valid():
            providerMaster_obj = form.save(commit=False)
            providerMaster_obj.save()

            return redirect('appeal-details', providerMaster_obj.caseNumber)

    else:
        form = ProviderMasterCreateForm(instance=providerMaster_obj)

    context['form'] = form
    context['formName'] = 'Edit Case Provider'
    return render(request, 'create/create_form.html', context)


def issueMasterView(request):
    context = initialize_context(request)
    all_issues = TblIssueMaster.objects.order_by('issueSRGID')
    context['all_issues'] = all_issues
    context['today'] = date.today()
    return render(request, 'main/issueMaster.html', context)


def issueDetailView(request, pk):
    context = initialize_context(request)
    issue = TblIssueMaster.objects.get(pk=pk)

    context['issue'] = issue
    context['today'] = date.today()
    return render(request, 'main/issueDetail.html', context)


def issueEditView(request, pk):
    context = initialize_context(request)
    issueInstance = get_object_or_404(TblIssueMaster, pk=pk)

    if request.method == 'POST':
        form = IssueMasterCreateForm(request.POST, instance=issueInstance)

        if form.is_valid():
            issueInstance = form.save(commit=False)
            issueInstance.save()

            return redirect('issue-master')
    else:
        form = IssueMasterCreateForm(instance=issueInstance)

    context['form'] = form
    context['formName'] = 'Edit Issue Form'
    return render(request, 'create/issue_create_form.html', context)


class NewIssueView(CreateView):
    model = TblIssueMaster
    form_class = IssueMasterCreateForm
    template_name = 'create/create_form.html'
    context_object_name = 'new_issue'

    def form_valid(self, form):
        new_issue = form.save(commit=False)
        new_issue.save()
        return redirect('issue-master')

    def get(self, request, *args, **kwargs):
        context = initialize_context(request)
        form = self.form_class(request.POST)
        context['form'] = form
        context['formName'] = 'Add Issue'
        return render(
            request,
            self.template_name,
            context
        )


def staffMasterView(request):
    all_staff = TblStaffMaster.objects.all()

    return render(request,
                  'main/staffMaster.html',
                  {
                      'all_staff': all_staff
                  })


class NewStaffView(CreateView):
    model = TblStaffMaster
    form_class = StaffMasterCreateForm
    template_name = 'create/create_form.html'
    context_object_name = 'new_staff'

    def form_valid(self, form):
        new_staff = form.save(commit=False)
        new_staff.save()
        return redirect('staff-master')

    def get(self, request, *args, **kwargs):
        context = initialize_context(request)
        form = self.form_class(request.POST)
        context['form'] = form
        context['formName'] = 'New Staff'
        return render(
            request,
            self.template_name,
            context
        )


def fiMasterView(request):
    context = initialize_context(request)
    all_fis = TblFIMaster.objects.all().order_by('fiName').exclude(fiID=14)

    context['all_fis'] = all_fis
    context['today'] = date.today()
    return render(request, 'main/fiMaster.html', context)


class NewFIView(CreateView):
    model = TblFIMaster
    form_class = FIMasterCreateForm
    template_name = 'create/create_form.html'
    context_object_name = 'new_mac'

    def form_valid(self, form):
        new_mac = form.save(commit=False)
        new_mac.save()
        return redirect('mac-master')

    def get(self, request, *args, **kwargs):
        context = initialize_context(request)
        form = self.form_class(request.POST)

        context['form'] = form
        context['formName'] = 'Add MAC'
        return render(request, self.template_name, context)


def editFI(request, pk):
    context = initialize_context(request)

    fiInstance = get_object_or_404(TblFIMaster, pk=pk)

    if request.method == 'POST':
        form = FIMasterCreateForm(request.POST, instance=fiInstance)

        if form.is_valid():
            fiInstance = form.save(commit=False)
            fiInstance.save()

            return redirect('mac-master')
    else:
        form = FIMasterCreateForm(instance=fiInstance)

    context['form'] = form
    context['formName'] = 'Update MAC Form'
    context['fiInstance'] = fiInstance

    return render(request, 'create/create_form.html', context)


def editPRRB(request, pk):
    context = initialize_context(request)
    prrbInstance = get_object_or_404(TblPRRBContactMaster, pk=pk)

    if request.method == 'POST':
        form = PRRBContactMasterCreateForm(request.POST, instance=prrbInstance)

        if form.is_valid():
            prrbInstance = form.save(commit=False)
            prrbInstance.save()

            return redirect('prrb-master')
    else:
        form = PRRBContactMasterCreateForm(instance=prrbInstance)

    context['form'] = form
    context['formName'] = 'Update PRRB Contact Form'
    context['prrbInstance'] = prrbInstance

    return render(request, 'create/create_form.html', context)


def prrbMasterView(request):
    context = initialize_context(request)
    all_prrbs = TblPRRBContactMaster.objects.all()

    context['all_prrbs'] = all_prrbs

    return render(request, 'main/prrbMaster.html', context)


class NewPRRBContactView(CreateView):
    model = TblPRRBContactMaster
    form_class = PRRBContactMasterCreateForm
    template_name = 'create/create_form.html'
    context_object_name = 'new_prrb'

    def form_valid(self, form):
        new_prrb = form.save(commit=False)
        new_prrb.save()
        return redirect('prrb-master')

    def get(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        return render(
            request,
            self.template_name,
            {
                'form': form,
                'formName': 'PRRB'
            }
        )


class NewAppealMasterView(CreateView):
    model = TblAppealMaster
    form_class = AppealMasterCreateForm
    template_name = 'create/create_form.html'
    context_object_name = 'new_appeal'

    def form_valid(self, form):
        new_appeal = form.save(commit=False)
        caseNum = new_appeal.caseNumber
        structure = new_appeal.appealStructure
        new_appeal.save()
        if structure == 'Individual':
            return redirect('add-issue', caseNum)
        else:
            return redirect('add-issue', caseNum)

    def get(self, request, *args, **kwargs):
        context = initialize_context(request)
        form = self.form_class(request.POST)
        context['form'] = form
        context['formName'] = 'Create New Appeal'
        return render(request, self.template_name, context)


def updateCaseStatus(request, pk):
    caseInstance = get_object_or_404(TblAppealMaster, pk=pk)

    if request.method == 'POST':
        form = UpdateCaseStatusForm(request.POST)

        if form.is_valid():
            caseInstance.statusID = form.new_status
            caseInstance.save()

            return redirect('appeal-details', caseInstance.caseNumber)
    else:
        form = UpdateCaseStatusForm()

    return render(
        request,
        'create/create_form.html',
        {
            'form': form
        }
    )


def appealDetailsView(request, pk):
    context = initialize_context(request)
    caseObj = get_object_or_404(TblAppealMaster, pk=pk)
    caseIssues = TblProviderMaster.objects.filter(caseNumber=pk).order_by('-provMasterIsActive',
                                                                          'provMasterTransferDate',
                                                                          'providerID', )

    # caseDueDates = TblCriticalDatesMaster.objects.filter(Q(caseNumber=pk, progress='Not Started') |
    #                                                     Q(caseNumber=pk, progress='In Progress')).order_by('dueDate')

    caseDueDates = TblCriticalDatesMaster.objects.filter(caseNumber=pk).order_by('-dueDate')

    if caseObj.appealStructure == 'Individual':
        provInfo = caseIssues.first()
    else:
        provInfo = caseIssues

    if request.method == 'POST' and 'ack_button' in request.POST:
        ack_form = AcknowledgeCaseForm(request.POST)
        if ack_form.is_valid():
            caseObj.appealAckDate = ack_form.cleaned_data['ack_date']
            caseObj.save()

            return redirect('appeal-details', caseObj.caseNumber)

    elif request.method == 'POST' and 'save_notes_button' in request.POST:
        updated_notes = request.POST.get('save_notes_button')
        caseObj.appealNotes = updated_notes
        caseObj.save()

        return redirect('appeal-details', caseObj.caseNumber)

    elif request.method == 'POST' and 'case_status_button' in request.POST:
        update_status_form = UpdateCaseStatusForm(request.POST)

        if update_status_form.is_valid():
            caseObj.statusID = update_status_form.cleaned_data['new_status']
            caseObj.save()

            return redirect('appeal-details', caseObj.caseNumber)

    elif request.method == 'POST':
        search_case = request.POST.get('search')
        return redirect('appeal-details', search_case)

    else:
        proposed_ack_date = datetime.date.today()
        ack_form = AcknowledgeCaseForm(initial={'ack_date': proposed_ack_date})
        update_status_form = UpdateCaseStatusForm()

    context['caseObj'] = caseObj
    context['caseIssues'] = caseIssues
    context['provInfo'] = provInfo
    context['caseDueDates'] = caseDueDates
    context['ack_form'] = ack_form
    context['update_status_form'] = update_status_form

    return render(request, 'main/appealDetails.html', context)


def addProviderToGroup(request, pk):
    case_instance = get_object_or_404(TblAppealMaster, pk=pk)
    if request.method == 'POST':
        form = ProviderMasterCreateForm(request.POST)

        if form.is_valid():
            added_provider = form.save(commit=False)

            added_provider = TblProviderMaster(caseNumber=added_provider.caseNumber,
                                               providerID=added_provider.providerID,
                                               issueID=added_provider.issueID,
                                               provMasterImpact=added_provider.provMasterImpact,
                                               provMasterAuditAdjs=added_provider.provMasterAuditAdjs,
                                               provMasterToCase='NULL',
                                               provMasterTransferDate=datetime.date.today(),
                                               provMasterFromCase='NULL',
                                               provMasterNote=added_provider.provMasterNote,
                                               provMasterDateStamp=datetime.datetime.today()
                                               )
            added_provider.save(force_insert=True)
            return redirect('appeal-details', case_instance.caseNumber)
    else:
        form = ProviderMasterCreateForm(
            initial={'caseNumber': case_instance.caseNumber})

    return render(request, 'create/create_form.html',
                  {
                      'form': form,
                      'formName': 'Add Provider to Group (Direct Add)'
                  })


def addIssueView(request, pk):
    context = initialize_context(request)
    case_instance = get_object_or_404(TblAppealMaster, pk=pk)
    cur_case = case_instance.caseNumber
    case_issue_count = TblProviderMaster.objects.filter(
        caseNumber__caseNumber=cur_case).count()
    case_issues = TblProviderMaster.objects.filter(caseNumber=cur_case)
    today = datetime.date.today()

    if request.method == 'POST':
        form = ProviderMasterCreateForm(request.POST)

        if form.is_valid():
            if case_instance.appealStructure == 'Individual':
                new_issue = form.save(commit=False)
                new_issue.save()

                return redirect(r'appeal-details', cur_case)
            else:
                added_provider = form.save(commit=False)

                added_provider = TblProviderMaster(caseNumber=added_provider.caseNumber,
                                                   providerID=added_provider.providerID,
                                                   provMasterDeterminationDate=added_provider.provMasterDeterminationDate,
                                                   provMasterDeterminationType=added_provider.provMasterDeterminationType,
                                                   provMasterFiscalYear=added_provider.provMasterFiscalYear,
                                                   issueID=added_provider.issueID,
                                                   provMasterAuditAdjs=added_provider.provMasterAuditAdjs,
                                                   provMasterWasAdded=added_provider.provMasterWasAdded,
                                                   provMasterImpact=added_provider.provMasterImpact,
                                                   provMasterToCase='NULL',
                                                   provMasterTransferDate=added_provider.provMasterTransferDate,
                                                   provMasterFromCase='NULL',
                                                   provMasterNote=added_provider.provMasterNote,
                                                   provMasterDateStamp=today,
                                                   provMasterIsActive=True,
                                                   )
                added_provider.save(force_insert=True)
                return redirect(r'appeal-details', cur_case)
    else:
        if case_issue_count > 0 and case_instance.appealStructure == 'Individual':
            form = ProviderMasterCreateForm(initial={'caseNumber': cur_case,
                                                     'providerID': case_issues.first().providerID,
                                                     'provMasterDateStamp': today
                                                     })
        else:
            form = ProviderMasterCreateForm(initial={'caseNumber': cur_case,
                                                     'provMasterWasAdded': False,
                                                     'provMasterDateStamp': today
                                                     })

    context['form'] = form
    context['formName'] = 'Add Issue / Provider (DA) to Appeal'
    return render(request, 'create/add_to_case_form.html', context)


def addCriticalDueView(request, pk):
    context = initialize_context(request)

    case_instance = get_object_or_404(TblAppealMaster, pk=pk)
    cur_case = case_instance.caseNumber
    case_due_dates = TblCriticalDatesMaster.objects.filter(caseNumber=cur_case)
    case_issues = TblProviderMaster.objects.filter(caseNumber=cur_case).first()

    if request.method == 'POST':
        form = CriticalDatesMasterCreateForm(request.POST)
        case_fy = case_issues.provMasterFiscalYear

        if form.is_valid():
            new_due_date = form.save(commit=False)
            new_due_date.save()

            # Create the due date
            token = get_token(request)

            action = TblActionMaster.objects.get(pk=new_due_date.actionID)

            # Create the subject
            if case_issues.provMasterDeterminationType == 'FR':
                subject = '{0}~{1}~FFY{2}'.format(
                    new_due_date.actionID, cur_case, str(case_fy.year))
            else:
                subject = '{0}~{1}~FY{2}'.format(
                    new_due_date.actionID, cur_case, str(case_fy.year))

            due_date = new_due_date.dueDate
            start_year = due_date.year
            start_month = due_date.month
            start_day = due_date.day

            start_time = datetime.datetime(start_year, start_month, start_day,
                                           random.randint(1, 12), random.randint(0, 59), 0)
            end_time = start_time + timedelta(minutes=30)

            body = action.description

            lead_time = action.lead_time * 10080

            create_event(
                token,
                subject,
                start_time,
                end_time,
                lead_time,
                body
            )
            return redirect(r'appeal-details', cur_case)
    else:
        form = CriticalDatesMasterCreateForm(initial={'caseNumber': cur_case})

    context['formName'] = 'Add Critical Due Date Form'
    context['form'] = form
    context['case_due_dates'] = case_due_dates

    return render(request, 'create/create_form.html', context)


def transferIssueView(request, pk):
    context = initialize_context(request)

    issue_trans = get_object_or_404(TblProviderMaster, pk=pk)
    # caseDeterObc = TblCaseDeterminationMaster.objects.get(
    #    caseNumber=issue_trans.caseNumber)

    caseFiscalYear = issue_trans.provMasterFiscalYear.year
    caseDeterType = issue_trans.provMasterDeterminationType

    poss_groups = TblAppealMaster.objects.filter(appealName__contains=caseFiscalYear).filter(
        appealName__contains=issue_trans.issueID.issueName).exclude(appealStructure__exact='Individual')

    if request.method == 'POST':
        form = TransferIssueForm(request.POST)
        if form.is_valid():
            issue_trans.provMasterToCase = request.POST.get('to_case')
            issue_trans.provMasterTransferDate = form.cleaned_data['to_date']
            issue_trans.save()

            app_instance = TblAppealMaster.objects.get(
                pk=issue_trans.provMasterToCase)

            new_group_prov = TblProviderMaster(caseNumber=app_instance,
                                               providerID=issue_trans.providerID,
                                               issueID=issue_trans.issueID,
                                               provMasterDeterminationDate=issue_trans.provMasterDeterminationDate,
                                               provMasterDeterminationType=issue_trans.provMasterDeterminationType,
                                               provMasterFiscalYear=issue_trans.provMasterFiscalYear,
                                               provMasterImpact=issue_trans.provMasterImpact,
                                               provMasterAuditAdjs=issue_trans.provMasterAuditAdjs,
                                               provMasterWasAdded=0,
                                               provMasterIsActive=True,
                                               provMasterToCase='NULL',
                                               provMasterTransferDate=issue_trans.provMasterTransferDate,
                                               provMasterFromCase=str(issue_trans.caseNumber),
                                               provMasterNote=issue_trans.provMasterNote,
                                               provMasterDateStamp=datetime.date.today())
            new_group_prov.save(force_insert=True)

            return redirect('appeal-details', issue_trans.caseNumber)
    else:
        propose_trans_date = datetime.date.today()
        form = TransferIssueForm(initial={'to_date': propose_trans_date})

    context['issue_trans'] = issue_trans
    context['caseFiscalYear'] = caseFiscalYear
    context['caseDeterType'] = caseDeterType
    context['form'] = form
    context['formName'] = 'Transfer Issue Form'
    context['poss_groups'] = poss_groups

    return render(request, 'main/transferIssue.html', context)


def withdrawFromCase(request, pk):
    context = initialize_context(request)

    provMasterInstance = get_object_or_404(TblProviderMaster, pk=pk)

    if request.method == 'POST':
        provMasterInstance.provMasterIsActive = False
        provMasterInstance.save()

        return redirect('appeal-details', provMasterInstance.caseNumber)

    context['provMasterInstance'] = provMasterInstance

    return render(request, 'main/withdrawFromCase.html', context)


def searchCriticalDueDates(request):
    dueDates_list = TblCriticalDatesMaster.objects.filter(progress='Not Started')
    dueDates_filter = CriticalDateFilter(request.GET, queryset=dueDates_list)

    return render(request, 'main/CriticalDatesMaster.html', {'filter': dueDates_filter})


def searchCriticalDueDatesTwo(request):
    context = initialize_context(request)
    dueDates_list = TblAppealMaster.objects.all().order_by('TblCriticalDatesMaster__dueDate')
    dueDates_filter = CriticalDateFilterTwo(request.GET, queryset=dueDates_list)

    context['filter'] = dueDates_filter

    return render(request, 'main/CriticalDatesMasterTwo.html', context)


def groupReport(request):
    context = initialize_context(request)
    today = date.today()
    # allGroups = TblAppealMaster.objects.exclude(appealStructure='Individual').order_by('-appealCreateDate')[:50]

    queryset = TblProviderMaster.objects.values('provMasterID', 'providerID', 'providerID__providerName',
                                                'caseNumber__statusID__statusName',
                                                'issueID__issueName', 'caseNumber', 'caseNumber__appealName',
                                                'provMasterFiscalYear',
                                                'caseNumber__appealStructure').order_by('-provMasterFiscalYear',
                                                                                        '-caseNumber',
                                                                                        '-issueID__issueSRGID')

    f = ProviderMasterFilter(request.GET, queryset=queryset)

    # context['allGroups'] = allGroups
    context['today'] = today
    context['filter'] = f
    return render(request, 'main/groupReport.html', context)


def providerReport(request):
    context = initialize_context(request)
    today = date.today()
    # allGroups = TblAppealMaster.objects.exclude(appealStructure='Individual').order_by('-appealCreateDate')[:50]

    queryset = TblProviderMaster.objects.values('provMasterID', 'providerID', 'providerID__providerName',
                                                'caseNumber__statusID__statusName',
                                                'issueID__issueName', 'caseNumber', 'caseNumber__appealName',
                                                'provMasterFiscalYear',
                                                'caseNumber__appealStructure').order_by('-provMasterFiscalYear',
                                                                                        '-caseNumber',
                                                                                        '-issueID__issueSRGID')

    f = ProviderMasterFilter(request.GET, queryset=queryset)

    # context['allGroups'] = allGroups
    context['today'] = today
    context['filter'] = f
    return render(request, 'main/providerReport.html', context)


def updateDueDateProgress(request, pk):
    context = initialize_context(request)
    dueDate_obj = get_object_or_404(TblCriticalDatesMaster, pk=pk)
    provMasterObj = TblProviderMaster.objects.filter(caseNumber=dueDate_obj.caseNumber)

    if request.method == 'POST':
        form = UpdateDueDateProgressForm(request.POST)

        if form.is_valid():
            dueDate_obj.progress = request.POST.get('new_progress')
            dueDate_obj.save()

            return redirect('appeal-details', dueDate_obj.caseNumber)
    else:
        form = UpdateDueDateProgressForm()

    context['dueDate_obj'] = dueDate_obj
    context['form'] = form
    context['provMasterObj'] = provMasterObj
    return render(request, 'create/due_date_edit.html', context)


def updateNPRDueDateProgress(request, pk):
    context = initialize_context(request)
    NPRDate_obj = get_object_or_404(NPRDueDatesMaster, pk=pk)
    provNameMasterObj = TblProviderNameMaster.objects.filter(providerID=NPRDate_obj.providerID)

    if request.method == 'POST':
        form = UpdateNPRDateProgressForm(request.POST)

        if form.is_valid():
            NPRDate_obj.status = request.POST.get('new_status')
            NPRDate_obj.save()

            return redirect('main')
    else:
        form = UpdateNPRDateProgressForm()

    context['NPRDate_obj'] = NPRDate_obj
    context['form'] = form
    context['provNameMasterObj'] = provNameMasterObj
    return render(request, 'create/npr_date_edit.html', context)


def providerAppealDetails(request):
    context = initialize_context(request)
    provMaster_list = TblProviderMaster.objects.all()
    provMaster_filter = ProviderMasterFilter(request.GET, queryset=provMaster_list)

    context['filter'] = provMaster_filter

    return render(request, 'main/providerMasterFilter.html', context)


# Begin Creation of Form G
def createFormGCoverLetter(request, pk):
    caseObj = get_object_or_404(TblAppealMaster, pk=pk)

    Story = []
    logo = "S:\\11_SRI Templates\\SRI_Letterhead - 2018 12 18.png"
    subject = "Schedule G and Jurisdictional Documents"
    caseName = caseObj.appealName
    caseNum = caseObj.caseNumber

    im = Image(logo, 8 * inch, 2 * inch)
    Story.append(im)

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    ptext = '<font size="12">%s</font>' % 'February 16, 2021'

    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 24))

    # Create Address
    addressParts = ["Chairperson", "Provider Reimbursement Review Board", "CMS Office of Hearings",
                    "7500 Security Boulevard", "Mail Stop: N2-19-25", "Baltimore, MD 21244"]

    for part in addressParts:
        ptext = '<font size="12">%s</font>' % part.strip()
        Story.append(Paragraph(ptext, styles["Normal"]))

    Story.append(Spacer(1, 24))
    ptext = '<font size="12">RE:&nbsp;&nbsp;&nbsp;&nbsp;' \
            '&nbsp;&nbsp;&nbsp;&nbsp;%s</font>' % subject
    Story.append(Paragraph(ptext))
    ptext = '<font size="12">&nbsp;&nbsp;&nbsp;&nbsp;' \
            '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' \
            '&nbsp;&nbsp;' \
            'Case Name: %s</font>' % caseName
    Story.append(Paragraph(ptext, styles["Normal"]))
    ptext = '<font size="12">&nbsp;&nbsp;&nbsp;&nbsp;' \
            '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' \
            '&nbsp;&nbsp;' \
            'Case Number: %s</font>' % caseNum
    Story.append(Paragraph(ptext, styles["Normal"]))

    Story.append(Spacer(1, 24))
    ptext = '<font size="12">Dear Sir/Madam:</font>'
    Story.append(Paragraph(ptext, styles["Normal"]))

    Story.append(Spacer(1, 12))
    ptext = '<font size="12"> Please find the enclosed Model Form G - Schedule of Providers and' \
            'supporting documentation.</font>'
    Story.append(Paragraph(ptext, styles["Normal"]))

    Story.append(Spacer(1, 12))
    ptext = '<font size="12">Should you have any questions, please contact me at (630)-530-7100.</font>'
    Story.append(Paragraph(ptext, styles["Normal"]))

    Story.append(Spacer(1, 12))
    ptext = '<font size="12">Sincerely,</font>'
    Story.append(Paragraph(ptext, styles["Normal"]))

    Story.append(Spacer(1, 48))
    addressParts = ["Randall Gienko", "Manager", "Strategic Reimbursement Group, LLC",
                    "360 W. Butterfield Road, Suite 310", "Elmhurst, IL 60126",
                    "Phone: (630) 530-7100", "Email:appeals@srgroupllc.com"]
    for part in addressParts:
        ptext = '<font size="12">%s</font>' % part.strip()
        Story.append(Paragraph(ptext, styles["Normal"]))

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=0, bottomMargin=18)
    doc.build(Story)
    pdf_value = buffer.getvalue()
    buffer.close()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="formGCoverLetter.pdf"'

    response.write(pdf_value)
    return response


def createFormGIssueState(request, pk):
    caseObj = get_object_or_404(TblAppealMaster, pk=pk)
    caseName = caseObj.appealName
    caseNum = caseObj.caseNumber

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))

    issueStatementDoc = []

    ptext = '<font size="12"><b>%s</b></font>' % caseName
    issueStatementDoc.append(Paragraph(ptext, styles["Normal"]))
    issueStatementDoc.append(Spacer(1, 24))

    ptext = '<font size="12"><b>Statement of Issue:</b></font>'
    issueStatementDoc.append(Paragraph(ptext, styles["Normal"]))
    issueStatementDoc.append(Spacer(1, 12))

    providerMaster = TblProviderMaster.objects.filter(caseNumber=caseNum).first()
    issueID = providerMaster.issueID

    issueInfo = TblIssueMaster.objects.get(issueSRGID=str(issueID).split('-')[0])

    ptext = '<font size="12"><b>%s</b></font>' % issueInfo.issueName
    issueStatementDoc.append(Paragraph(ptext, styles["Normal"]))
    issueStatementDoc.append(Spacer(1, 12))

    groupIssueStatement = issueInfo.issueLongDescription
    ptext = Paragraph('<para justifyBreaks=True>' + groupIssueStatement + '</para>', styles["Normal"])
    issueStatementDoc.append(ptext)

    buffer = BytesIO()
    issueStatement = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72,
                                       leftMargin=72, topMargin=72, bottomMargin=18)

    issueStatement.build(issueStatementDoc)
    pdf_value = buffer.getvalue()
    buffer.close()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="formGIssueStatement.pdf"'

    response.write(pdf_value)
    return response


def createFormGToc(request, pk):
    caseObj = get_object_or_404(TblAppealMaster, pk=pk)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))

    tocStory = []

    ptext = '<font size="14">Summary of Schedules and Exhibits</font>'
    tocStory.append(Paragraph(ptext, styles["Normal"]))
    tocStory.append(Spacer(1, 12))

    tocItems = ['- Tab A - Final Determinations', '- Tab B - Date of Hearings / Hearing Requests',
                '- Tab C - Number of Days', '- Tab D - Audit Adjustments & Protested Amounts',
                '- Tab E - Impact Calculations / Estimates', '- Tab F - Original Appeal Letters',
                '- Tab G - Additions & Transfers', '- Tab H - Representation Letter']

    for item in tocItems:
        ptext = '<font size="14">&nbsp;&nbsp;&nbsp;&nbsp;%s</font>' % item.strip()
        tocStory.append(Paragraph(ptext, styles["Normal"]))
        tocStory.append(Spacer(1, 12))

    buffer = BytesIO()
    toc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    toc.build(tocStory)
    pdf_value = buffer.getvalue()
    buffer.close()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="formGTOC.pdf"'

    response.write(pdf_value)
    return response


def createFormGExhibits(request, pk):
    caseObj = get_object_or_404(TblAppealMaster, pk=pk)
    caseNum = caseObj.caseNumber
    caseProviders = TblProviderMaster.objects.filter(caseNumber=caseNum).filter(provMasterIsActive='True').order_by(
        'provMasterTransferDate',
        'providerID')
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))

    exhibitsStory = []

    exhibitItems = ['Tab A - Final Determinations', 'Tab B - Date of Hearings / Hearing Requests',
                    'Tab C - Number of Days', 'Tab D - Audit Adjustments & Protested Amounts',
                    'Tab E - Impact Calculations / Estimates', 'Tab F - Original Appeal Letters',
                    'Tab G - Additions & Transfers', 'Tab H - Representation Letter']

    for count, prov in enumerate(caseProviders, start=1):
        ptext = Paragraph('<para align=center>' + str(count) + ' - ' + str(prov.providerID) + '</para>',
                          styles["Normal"])
        exhibitsStory.append(ptext)
        exhibitsStory.append(Spacer(1, 12))
        proveName = prov.get_prov_name()
        ptext = Paragraph('<para align=center>' + str(proveName) + '</para>', styles["Normal"])
        exhibitsStory.append(ptext)
        exhibitsStory.append(PageBreak())

        for exhibit in exhibitItems:
            ptext = Paragraph('<para align=center>%s</para>' % exhibit.strip(), styles["Normal"])
            exhibitsStory.append(ptext)
            exhibitsStory.append(PageBreak())

    buffer = BytesIO()
    exhibits = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    exhibits.build(exhibitsStory)
    pdf_value = buffer.getvalue()
    buffer.close()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="formGTExhibits.pdf"'

    response.write(pdf_value)
    return response


def createFormG(request, pk):
    # Build Form G Schedule of Providers
    caseObj = get_object_or_404(TblAppealMaster, pk=pk)
    caseName = caseObj.appealName
    caseNum = caseObj.caseNumber
    caseMac = caseObj.get_fi()
    providerMaster = TblProviderMaster.objects.filter(caseNumber=caseNum).first()
    issueID = providerMaster.issueID
    issueInfo = TblIssueMaster.objects.get(issueSRGID=str(issueID).split('-')[0])
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))

    elements = []
    styles = getSampleStyleSheet()

    global title
    global cnum
    global case_name
    global case_rep
    global case_issue
    repObj = TblStaffMaster.objects.get(staffLastName=caseObj.staffID)

    title = "Model Form G: Schedule of Providers in Group"
    cnum = "Case No.: {0}".format(caseNum)
    case_name = "Group Case Name: {0}".format(caseName)
    case_rep = "Group Representative: {0} {1} / Strategic Reimbursement Group , LLC".format(str(repObj.staffFirstName),
                                                                                            str(repObj.staffLastName))
    case_issue = "Issue: {0}".format(issueInfo.issueShortDescription)

    columnHeaderNumber = Paragraph(
        '<para align=center>#</para>', styles["Normal"])
    columnHeaderProviderNumber = Paragraph(
        '<para align=center>Provider <br/>Number</para>', styles["Normal"])
    columnHeaderProviderInfo = Paragraph('<para align=center>Provider Name / Location <br/>'
                                         '(city, county, state)</para>', styles["Normal"])
    columnHeaderFYE = Paragraph(
        '<para align=center>FYE</para>', styles["Normal"])
    columnHeaderMAC = Paragraph(
        '<para align=center>Intermediary / <br/> MAC</para>', styles["Normal"])
    columnHeaderA = Paragraph(
        '<para align=center>A<br/>Date of Final<br/>Determination</para>', styles["Normal"])
    columnHeaderB = Paragraph('<para align=center>B<br/>Date of<br/>Hearing<br/>Request<br/>Add '
                              'Issue<br/>Request</para>', styles["Normal"])
    columnHeaderC = Paragraph(
        '<para align=center>C<br/>No.<br/>of<br/>Days</para>', styles["Normal"])
    columnHeaderD = Paragraph(
        '<para align=center>D<br/>Audit<br/>Adj.</para>', styles["Normal"])
    columnHeaderE = Paragraph(
        '<para align=center>E<br/>Amount in<br/>Controversy</para>', styles["Normal"])
    columnHeaderF = Paragraph(
        '<para align=center>F<br/>Prior Case<br/>No(s).</para>', styles["Normal"])
    columnHeaderG = Paragraph('<para align=center>G<br/>Date of<br/>Direct Add /<br/>Transfer(s)<br/>to Group</para>',
                              styles["Normal"])

    scheduleGData = [[columnHeaderNumber, columnHeaderProviderNumber, columnHeaderProviderInfo,
                      columnHeaderFYE, columnHeaderMAC, columnHeaderA, columnHeaderB, columnHeaderC,
                      columnHeaderD, columnHeaderE, columnHeaderF, columnHeaderG]]

    # Assemble rows for Form G
    caseProviders = TblProviderMaster.objects.filter(caseNumber=caseNum).filter(provMasterIsActive='True').order_by(
        'provMasterTransferDate',
        'providerID')
    global groupTotalImpact
    groupImpact = caseProviders.aggregate(Sum('provMasterImpact'))
    groupTotalImpact = "Total Amount in Controversy for All Providers: ${0:,}".format(
        groupImpact['provMasterImpact__sum'])

    for count, prov in enumerate(caseProviders, start=1):
        columnDataNumber = Paragraph(
            '<para align=center>' + str(count) + '</para>', styles["Normal"])
        columnDataProviderNumber = Paragraph('<para align=center>' + str(prov.providerID) + '</para>',
                                             styles["Normal"])

        provName = TblProviderNameMaster.objects.get(providerID=prov.providerID)
        columnDataProviderInfo = Paragraph(
            '<para align=center>' + str(provName.providerName.title()) + '<br/>' + str(provName.providerCity) +
            ', ' + str(provName.providerCounty) + ', ' + str(provName.stateID) + '</para>', styles["Normal"])

        columnDataFYE = Paragraph('<para align=center>' + str(prov.provMasterFiscalYear.strftime("%m/%d/%Y")) +
                                  '</para>', styles["Normal"])

        # columnDataMAC = Paragraph('<para align=center>' + str(prov.get_ind_fi()) + '</para>', styles["Normal"])

        columnDataA = Paragraph('<para align=center>' + str(prov.provMasterDeterminationDate.strftime("%m/%d/%Y")) +
                                '</para>', styles["Normal"])

        if prov.provMasterWasAdded == 1:
            hrqDate = prov.provMasterDateStamp
            columnDataMAC = Paragraph('<para align=center>' + str(caseMac) + '</para>', styles["Normal"])
            columnDataB = Paragraph(
                '<para align=center> N/A - Provider Direct Added to Group</para>',
                styles["Normal"])
            columnDataC = Paragraph('<para align=center> N/A </para>', styles["Normal"])
            columnDataG = Paragraph(
                '<para align=center>' + str(hrqDate.strftime("%m/%d/%Y")) + '</para>',
                styles["Normal"])
        else:
            hrqDate = TblAppealMaster.objects.get(caseNumber=prov.provMasterFromCase)
            columnDataMAC = Paragraph('<para align=center>' + str(prov.get_ind_fi()) + '</para>', styles["Normal"])
            columnDataB = Paragraph(
                '<para align=center>' + str(hrqDate.appealCreateDate.strftime("%m/%d/%Y")) + '</para>',
                styles["Normal"])
            no_of_days = prov.get_no_days()
            columnDataC = Paragraph('<para align=center>' + str(no_of_days) + '</para>', styles["Normal"])
            columnDataG = Paragraph(
                '<para align=center>' + str(prov.provMasterTransferDate.strftime("%m/%d/%Y")) + '</para>',
                styles["Normal"])

        columnDataD = Paragraph('<para align=center>' + str(prov.provMasterAuditAdjs) + '</para>', styles["Normal"])

        locale.setlocale(locale.LC_ALL, '')
        provImpactFormatted = "${0:,}".format(prov.provMasterImpact)
        columnDataE = Paragraph('<para align=center>' + str(provImpactFormatted) +
                                '</para>', styles["Normal"])

        columnDataF = Paragraph('<para align=center>' + str(prov.provMasterFromCase) + '</para>', styles["Normal"])

        scheduleGData.append([columnDataNumber, columnDataProviderNumber, columnDataProviderInfo, columnDataFYE,
                              columnDataMAC, columnDataA, columnDataB, columnDataC, columnDataD, columnDataE,
                              columnDataF, columnDataG])

    tR = Table(scheduleGData, repeatRows=1, colWidths=[1 * cm, 2 * cm, 4.5 * cm, 2.5 * cm, 2.5 * cm, 3 * cm,
                                                       3 * cm, 1.5 * cm, 2 * cm, 2.5 * cm, 2 * cm, 2.5 * cm],
               rowHeights=1.05 * inch)

    tR.hAlign = 'CENTER'

    tblStyle = TableStyle([('BOX', (0, 0), (-1, -1), 1, colors.black),
                           ('INNERGRID', (0, 0), (-1, -1), 1, colors.black)])

    tR.setStyle(tblStyle)

    elements.append(tR)

    buffer = BytesIO()
    formGDoc = SimpleDocTemplate(buffer, pagesize=[A4[1], A4[0]], leftMargin=0, rightMargin=0, topMargin=105,
                                 bottomMargin=5)

    formGDoc.build(elements, onFirstPage=PageNumCanvas, onLaterPages=PageNumCanvas, canvasmaker=PageNumCanvas)

    pdf_value = buffer.getvalue()
    buffer.close()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="formGScheduleG.pdf"'

    response.write(pdf_value)

    # return redirect(r'appeal-details', caseObj.caseNumber)
    return response


class PageNumCanvas(canvas.Canvas):
    """
    http://code.activestate.com/recipes/546511-page-x-of-y-with-reportlab/
    http://code.activestate.com/recipes/576832/
    """

    # ----------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        """Constructor"""
        canvas.Canvas.__init__(self, *args, **kwargs)
        self.pages = []

    # ----------------------------------------------------------------------
    def showPage(self):
        """
        On a page break, add information to the list
        """
        self.pages.append(dict(self.__dict__))
        self._startPage()

    # ----------------------------------------------------------------------
    def save(self):
        """
        Add the page number to each page (page x of y)
        """
        page_count = len(self.pages)

        for page in self.pages:
            self.__dict__.update(page)
            self.draw_page_number(page_count)
            canvas.Canvas.showPage(self)

        canvas.Canvas.save(self)

    # ----------------------------------------------------------------------
    def draw_page_number(self, page_count):
        """
        Add the page number
        """

        page = "Page: %s of %s" % (self._pageNumber, page_count)
        date = "Date Prepared: %s" % datetime.datetime.today().strftime("%m/%d/%Y")
        self.setFont("Helvetica", 12)
        self.drawString(4 * inch, 8 * inch, title)
        self.setFont("Helvetica", 10)

        self.drawString(.5 * cm, 19.33 * cm, cnum)
        self.line(2.1 * cm, 19.27 * cm, 4 * cm, 19.27 * cm)

        self.drawString(.5 * cm, 18.66 * cm, case_name)
        self.line(1.40 * inch, 18.60 * cm, 5.5 * inch, 18.61 * cm)

        self.drawString(.5 * cm, 17.99 * cm, case_rep)
        self.line(1.65 * inch, 17.93 * cm, 6 * inch, 17.95 * cm)

        self.drawString(.5 * cm, 17.33 * cm, case_issue)
        self.line(.57 * inch, 17.27 * cm, 10 * inch, 17.27 * cm)

        self.drawString(15.5 * cm, .5 * cm, groupTotalImpact)
        self.line(8.9 * inch, .4 * cm, 9.75 * inch, .4 * cm)

        self.drawString(23 * cm, 19.33 * cm, page)
        self.line(9.4 * inch, 19.27 * cm, 9.9 * inch, 19.27 * cm)

        self.drawString(23 * cm, 18.66 * cm, date)
        self.line(10 * inch, 18.60 * cm, 11 * inch, 18.60 * cm)

# def generate_pdf_through_template(request, pk):
#    context = {"caseObj": get_object_or_404(TblAppealMaster, pk=pk)}

#    html = render_to_string('main/formG.html', context)
#    write_to_file = open('C:\\Users\\randall.gienko\\Desktop\\test_1.pdf', "w+b")
#    result = pisa.CreatePDF(html, dest=write_to_file)
#    write_to_file.close()
#    # return HttpResponse(result.err)
#    return render(request, 'main/formG.html')


# class NewCaseDeterminationView(CreateView):
#    model = TblCaseDeterminationMaster
#    form_class = CaseDeterminationMasterForm
#    template_name = 'create/create_form.html'
#    context_object_name = 'new_determination'

#    def form_valid(self, form):
#        new_determination = form.save(commit=False)
#        caseNum = new_determination.caseNumber
#        new_determination.save()
#        return redirect('new-deter', caseNum)

#   def get(self, request, *args, **kwargs):
#       form = self.form_class(request.POST)
#       return render(
#           request,
#           self.template_name,
#           {
#               'form': form,
#               'formName': 'Appeal Determination Info'
#           }
#       )


# def addDeterminationView(request, pk, prov):
#    case_instance = get_object_or_404(TblAppealMaster, pk=pk)
#    caseNum = case_instance.caseNumber
#    if request.method == 'POST':
#        form = CaseDeterminationMasterForm(request.POST)

#        if form.is_valid():
#            new_deter = form.save(commit=False)
#            new_deter.save()

#           return redirect('appeal-details', caseNum)

#    else:
#        form = CaseDeterminationMasterForm(initial={'caseNumber': caseNum, 'providerNumber': prov})

#    return render(request, 'create/create_form.html',
#                  {
#                      'form': form,
#                      'formName': 'Appeal Determination Info'

#                  })
