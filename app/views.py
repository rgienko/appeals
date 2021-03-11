import os
import random
import shutil

import win32com.client
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic import CreateView
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from xhtml2pdf import pisa
from app.forms import *
from .filters import CriticalDateFilter

from django.db.models import Sum

from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.lib.pagesizes import letter, landscape, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm, mm

import locale

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
            return redirect('home')
    else:
        messages.error(request, 'Error, wrong username / password')
    return render(request, 'main/login.html', {
        'title': 'Login',
    })


@login_required
def home(request):
    allDueDates = CriticalDatesMaster.objects.all().order_by('dueDate')[:10]

    if request.user.is_authenticated:
        current_user = request.user.first_name
    else:
        current_user = ""
    if request.method == 'POST' and 'make_dir_button' not in request.POST:
        search_case = request.POST.get('search')
        return redirect('appeal-details', search_case)

    if request.method == 'POST' and 'make_dir_button' in request.POST:
        make_dir_form = CreateDirectoryForm(request.POST)

        if make_dir_form.is_valid():
            ctype = request.POST.get('ctype')
            parent = request.POST.get('parent')
            prov = request.POST.get('prov')
            issue = request.POST.get('issue')
            isFFY = request.POST.get('isFFY')
            fy = request.POST.get('fy')
            case = request.POST.get('case')

            if isFFY == 'on':
                if ctype == 'INDIVIDUAL':
                    # Goal: S:\3-AP\1-DOCS\INDIVIDUAL\IND~01-0001~2016~XX-XXXX
                    new_path = 'S:\\3-AP\\1-DOCS\\{0}\\{1}~{2}~FFY{3}~{4}'.format(
                        ctype, parent, prov, fy, case)
                else:
                    issue_abb = TblIssueMaster.objects.get(pk=issue)
                    if parent == 'IND':
                        new_path = 'S:\\3-AP\\1-DOCS\\{0}\\OPT~FFY{1}~{2}~{3}~{4}'.format(ctype, fy, case,
                                                                                          issue_abb.issueSRGID,
                                                                                          issue_abb.issueAbbreviation)
                    else:
                        new_path = 'S:\\3-AP\\1-DOCS\\{0}\\{1}~FFY{2}~{3}~{4}~{5}'.format(ctype, parent, fy, case,
                                                                                          issue_abb.issueSRGID,
                                                                                          issue_abb.issueAbbreviation)
            else:
                if ctype == 'INDIVIDUAL':
                    # Goal: S:\3-AP\1-DOCS\INDIVIDUAL\IND~01-0001~2016~XX-XXXX
                    new_path = 'S:\\3-AP\\1-DOCS\\{0}\\{1}~{2}~{3}~{4}'.format(
                        ctype, parent, prov, fy, case)
                else:
                    issue_abb = TblIssueMaster.objects.get(pk=issue)
                    if parent == 'IND':
                        new_path = 'S:\\3-AP\\1-DOCS\\{0}\\OPT~{1}~{2}~{3}~{4}'.format(ctype, fy, case,
                                                                                       issue_abb.issueSRGID,
                                                                                       issue_abb.issueAbbreviation)
                    else:
                        new_path = 'S:\\3-AP\\1-DOCS\\{0}\\{1}~{2}~{3}~{4}~{5}'.format(ctype, parent, fy, case,
                                                                                       issue_abb.issueSRGID,
                                                                                       issue_abb.issueAbbreviation)

            try:
                os.mkdir(new_path)
                os.mkdir(new_path + "\\1-FILING")
                os.mkdir(new_path + "\\1-FILING\\1-FINAL")
                os.mkdir(new_path + "\\1-FILING\\1-FINAL\\1-PRRB")
                os.mkdir(new_path + "\\1-FILING\\1-FINAL\\2-MAC")
                os.mkdir(new_path + "\\1-FILING\\2-DOCS")
                os.mkdir(new_path + "\\1-FILING\\2-DOCS\\1-FILED ISSUES")
                os.mkdir(new_path + "\\1-FILING\\2-DOCS\\1-FILED ISSUES\\Impacts")
                os.mkdir(
                    new_path + "\\1-FILING\\2-DOCS\\1-FILED ISSUES\\Issue Statements")
                os.mkdir(
                    new_path + "\\1-FILING\\2-DOCS\\1-FILED ISSUES\\NPR Package")
                os.mkdir(new_path + "\\2-CORRESPONDENCE")
                os.mkdir(new_path + "\\3-JURISDICTIONAL")
                os.mkdir(new_path + "\\3-JURISDICTIONAL\\1-PROVS")
                os.mkdir(new_path + "\\4-PRELIM-PP")
                os.mkdir(new_path + "\\4-PRELIM-PP\\1-PROV")
                os.mkdir(new_path + "\\4-PRELIM-PP\\1-PROV\\1-FINAL")
                os.mkdir(new_path + "\\4-PRELIM-PP\\1-PROV\\1-FINAL\\1-PRRB")
                os.mkdir(new_path + "\\4-PRELIM-PP\\1-PROV\\1-FINAL\\2-MAC")
                os.mkdir(new_path + "\\4-PRELIM-PP\\1-PROV\\2-DOCS")
                os.mkdir(new_path + "\\4-PRELIM-PP\\2-MAC")
                os.mkdir(new_path + "\\5-FINAL-PP")
                os.mkdir(new_path + "\\5-FINAL-PP\\1-PROV")
                os.mkdir(new_path + "\\5-FINAL-PP\\1-PROV\\1-FINAL")
                os.mkdir(new_path + "\\5-FINAL-PP\\1-PROV\\1-FINAL\\1-PRRB")
                os.mkdir(new_path + "\\5-FINAL-PP\\1-PROV\\1-FINAL\\2-MAC")
                os.mkdir(new_path + "\\5-FINAL-PP\\1-PROV\\2-DOCS")
                os.mkdir(new_path + "\\5-FINAL-PP\\2-MAC")
                os.mkdir(new_path + "\\6-TRANSFERS")
                os.mkdir(new_path + "\\6-TRANSFERS\\1-FORM")
                os.mkdir(new_path + "\\6-TRANSFERS\\2-EXIST")
                os.mkdir(new_path + "\\7-CLOSURE")
                os.mkdir(new_path + "\\8-MISCELLANEOUS")
                os.mkdir(new_path + "\\99-PRINTS")
                os.mkdir(new_path + "\\99-PRINTS\\1-FRM-A")
                os.mkdir(new_path + "\\99-PRINTS\\1-FRM-B")
                os.mkdir(new_path + "\\99-PRINTS\\1-FRM-G")

                for file in os.listdir("S:\\3-AP\\3~APPEALS TEMPLATES\\Issue Statements\\DIRECTORY"):
                    newPath = shutil.copy("S:\\3-AP\\3~APPEALS TEMPLATES\\Issue Statements\\DIRECTORY\\" + file,
                                          new_path + "\\1-FILING\\2-DOCS\\1-FILED ISSUES\\Issue Statements")

                make_dir_form = CreateDirectoryForm()
            except:
                pass

    else:
        make_dir_form = CreateDirectoryForm()

    return render(request,
                  'main/index.html',
                  {
                      'form': make_dir_form,
                      'current_user': current_user,
                      'allDueDates': allDueDates
                  })


class NewProviderView(CreateView):
    model = TblProviderNameMaster
    form_class = ProviderNameMasterCreateForm
    template_name = 'create/prov_create_form.html'
    context_object_name = 'new_provider'

    def form_valid(self, form):
        new_provider = form.save(commit=False)
        new_provider.save()
        return redirect('provider-master')

    def get(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        return render(
            request,
            self.template_name,
            {
                'form': form
            }
        )


@login_required
def providerNameUpdateView(request, pk):
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

    return render(
        request,
        'create/prov_create_form.html',
        {
            'form': form
        }
    )


@login_required
def providerMasterView(request):
    all_providers = TblProviderNameMaster.objects.all()
    return render(
        request,
        'main/providerMaster.html',
        {
            'all_providers': all_providers
        }
    )


class NewSystemView(CreateView):
    model = TblParentMaster
    form_class = ParentMasterCreateForm
    template_name = 'create/parent_create_form.html'
    context_object_name = 'new_parent'

    def form_valid(self, form):
        new_parent = form.save(commit=False)
        new_parent.save()
        return redirect('parent-master')

    def get(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        return render(
            request,
            self.template_name,
            {
                'form': form
            }
        )


@login_required
def parentMasterView(request):
    all_parents = TblParentMaster.objects.all().order_by('parentID')

    return render(
        request,
        'main/parentMaster.html',
        {
            'all_parents': all_parents
        }
    )


@login_required
def parentUpdateView(request, pk):
    parent_obj = get_object_or_404(TblParentMaster, pk=pk)

    if request.method == 'POST':
        form = ParentMasterCreateForm(request.POST, instance=parent_obj)

        if form.is_valid():
            parent_obj = form.save(commit=False)
            parent_obj.save()

            return redirect('parent-master')
    else:
        form = ParentMasterCreateForm(instance=parent_obj)

    return render(
        request,
        'create/parent_create_form.html',
        {
            'form': form
        }
    )


@login_required
def providerMasterUpdateView(request, pk):
    providerMaster_obj = get_object_or_404(TblProviderMaster, pk=pk)

    if request.method == 'POST':
        form = ProviderMasterCreateForm(request.POST, instance=providerMaster_obj)

        if form.is_valid():
            providerMaster_obj = form.save(commit=False)
            providerMaster_obj.save()

            return redirect('appeal-details', providerMaster_obj.caseNumber)

    else:
        form = ProviderMasterCreateForm(instance=providerMaster_obj)

    return render(request, 'create/create_form.html',
                  {
                      'form': form
                  })


@login_required
def issueMasterView(request):
    all_issues = TblIssueMaster.objects.order_by('issueSRGID')

    return render(request,
                  'main/issueMaster.html',
                  {
                      'all_issues': all_issues
                  })


class NewIssueView(CreateView):
    model = TblIssueMaster
    form_class = IssueMasterCreateForm
    template_name = 'create/issue_create_form.html'
    context_object_name = 'new_issue'

    def form_valid(self, form):
        new_issue = form.save(commit=False)
        new_issue.save()
        return redirect('issue-master')

    def get(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        return render(
            request,
            self.template_name,
            {
                'form': form
            }
        )


@login_required
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
    template_name = 'create/staff_create_form.html'
    context_object_name = 'new_staff'

    def form_valid(self, form):
        new_staff = form.save(commit=False)
        new_staff.save()
        return redirect('staff-master')

    def get(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        return render(
            request,
            self.template_name,
            {
                'form': form
            }
        )


@login_required
def fiMasterView(request):
    all_fis = TblFIMaster.objects.all()

    return render(request,
                  'main/fiMaster.html',
                  {
                      'all_fis': all_fis
                  }
                  )


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
        form = self.form_class(request.POST)
        return render(
            request,
            self.template_name,
            {
                'form': form,
                'formName': 'MAC'
            }
        )


@login_required
def prrbMasterView(request):
    all_prrbs = TblPRRBContactMaster.objects.all()

    return render(request,
                  'main/prrbMaster.html',
                  {
                      'all_prrbs': all_prrbs
                  })


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
        form = self.form_class(request.POST)
        return render(
            request,
            self.template_name,
            {
                'form': form,
                'formName': 'Create New Appeal'
            }
        )


@login_required
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


@login_required
def appealDetailsView(request, pk):
    caseObj = get_object_or_404(TblAppealMaster, pk=pk)
    caseIssues = TblProviderMaster.objects.filter(caseNumber=pk)
    provInfo = caseIssues.first()
    caseDueDates = CriticalDatesMaster.objects.filter(caseNumber=pk)

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

    return render(request,
                  'main/appealDetails.html',
                  {
                      'caseObj': caseObj,
                      'caseIssues': caseIssues,
                      'provInfo': provInfo,
                      'caseDueDates': caseDueDates,
                      'ack_form': ack_form,
                      'update_status_form': update_status_form
                  })


@login_required
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
                                               provMasterFromCase=str(
                                                   added_provider.caseNumber),
                                               provMasterNote=added_provider.provMasterNote)
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


@login_required
def addIssueView(request, pk):
    case_instance = get_object_or_404(TblAppealMaster, pk=pk)
    cur_case = case_instance.caseNumber
    case_issue_count = TblProviderMaster.objects.filter(
        caseNumber__caseNumber=cur_case).count()
    case_issues = TblProviderMaster.objects.filter(caseNumber=cur_case)

    if request.method == 'POST':
        form = ProviderMasterCreateForm(request.POST)

        if form.is_valid():
            new_issue = form.save(commit=False)
            new_issue.save()

            return redirect(r'appeal-details', cur_case)
    else:
        if case_issue_count > 0 and case_instance.appealStructure == 'Individual':
            form = ProviderMasterCreateForm(initial={'caseNumber': cur_case,
                                                     'providerID': case_issues.first().providerID,
                                                     })
        else:
            form = ProviderMasterCreateForm(initial={'caseNumber': cur_case})

    return render(request, 'create/create_form.html',
                  {
                      'form': form,
                      'formName': 'Add Issue / Provider to Appeal'
                  })


@login_required
def addCriticalDueView(request, pk):
    case_instance = get_object_or_404(TblAppealMaster, pk=pk)
    cur_case = case_instance.caseNumber
    case_due_dates = CriticalDatesMaster.objects.filter(caseNumber=cur_case)
    case_issues = TblProviderMaster.objects.filter(caseNumber=cur_case).first()

    if request.method == 'POST':
        form = CriticalDatesMasterCreateForm(request.POST)
        case_fy = case_issues.provMasterFiscalYear

        if form.is_valid():
            new_due_date = form.save(commit=False)
            new_due_date.save()

            action = TblActionMaster.objects.get(pk=new_due_date.actionID)
            subject = '{0}~{1}~{2}'.format(
                new_due_date.actionID, cur_case, str(case_fy.year))
            due_date = new_due_date.dueDate
            start_year = due_date.year
            start_month = due_date.month
            start_day = due_date.day

            start_time = datetime.datetime(start_year, start_month, start_day,
                                           random.randint(1, 12), random.randint(0, 59), 0)
            duration = 30
            location = 'N/A'

            outlook = win32com.client.Dispatch("Outlook.Application")
            appt = outlook.CreateItem(1)  # AppointmentItem
            appt.Start = start_time  # yyyy-MM-dd hh:mm
            appt.Subject = subject
            appt.Duration = duration  # In minutes (60 Minutes)
            appt.Location = location
            appt.Body = action.description
            appt.MeetingStatus = 1

            appt.Recipients.Add("appeals@srgroupllc.com")  # Don't end ; as delimiter

            appt.Save()
            appt.Send()

            return redirect(r'appeal-details', cur_case)
    else:
        form = CriticalDatesMasterCreateForm(initial={'caseNumber': cur_case})

    return render(request, 'create/create_form.html',
                  {
                      'form': form,
                      'case_due_dates': case_due_dates
                  })


@login_required
def transferIssueView(request, pk):
    issue_trans = get_object_or_404(TblProviderMaster, pk=pk)
    # poss_groups = TblAppealMaster.objects.filter(appealName__contains=issue_trans.fiscal_year).filter(
    #    appeal_name__contains=issue_trans.issue_id.issue).exclude(structure__exact='Individual')
    caseDeterObc = TblCaseDeterminationMaster.objects.get(
        caseNumber=issue_trans.caseNumber)

    caseFiscalYear = caseDeterObc.determinationFiscalYear.year
    caseDeterType = caseDeterObc.caseDeterminationID

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
                                               provMasterImpact=issue_trans.provMasterImpact,
                                               provMasterAuditAdjs=issue_trans.provMasterAuditAdjs,
                                               provMasterToCase='NULL',
                                               provMasterTransferDate=issue_trans.provMasterTransferDate,
                                               provMasterFromCase=str(
                                                   issue_trans.caseNumber),
                                               provMasterNote=issue_trans.provMasterNote)
            new_group_prov.save(force_insert=True)

            return redirect('appeal-details', issue_trans.caseNumber)
    else:
        propose_trans_date = datetime.date.today()
        form = TransferIssueForm(initial={'to_date': propose_trans_date})

    return render(request, 'main/transferIssue.html',
                  {
                      'issue_trans': issue_trans,
                      'caseFiscalYear': caseFiscalYear,
                      'caseDeterType': caseDeterType,
                      'form': form
                  })


@login_required
def searchCriticalDueDates(request):
    dueDates_list = CriticalDatesMaster.objects.all()
    dueDates_filter = CriticalDateFilter(request.GET, queryset=dueDates_list)

    return render(request, 'main/criticalDatesMaster.html', {'filter': dueDates_filter})


@login_required
def updateDueDateProgress(request, pk):
    dueDate_obj = get_object_or_404(CriticalDatesMaster, pk=pk)
    provMasterObj = TblProviderMaster.objects.filter(caseNumber=dueDate_obj.caseNumber)

    if request.method == 'POST':
        form = UpdateDueDateProgressForm(request.POST)

        if form.is_valid():
            dueDate_obj.progress = request.POST.get('new_progress')
            dueDate_obj.save()

            return redirect('appeal-details', dueDate_obj.caseNumber)
    else:
        form = UpdateDueDateProgressForm()

    return render(
        request,
        'create/due_date_edit.html',
        {
            'form': form,
            'dueDate_obj': dueDate_obj,
            'provMasterObj': provMasterObj
        }
    )


@login_required
def createFormG(request, pk):
    caseObj = get_object_or_404(TblAppealMaster, pk=pk)

    doc = SimpleDocTemplate("C:\\Users\\randall.gienko\\Desktop\\scheduleGCoverLetter.pdf", pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=0, bottomMargin=18)

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

    doc.build(Story)

    # Build Schedule G Issue Statement Page
    issueStatementDoc = []
    issueStatement = SimpleDocTemplate("C:\\Users\\randall.gienko\\Desktop\\scheduleGroupIssueStatement.pdf",
                                       pagesize=letter,
                                       rightMargin=72, leftMargin=72,
                                       topMargin=72, bottomMargin=18)
    ptext = '<font size="12"><b>%s</b></font>' % caseName
    issueStatementDoc.append(Paragraph(ptext, styles["Normal"]))
    issueStatementDoc.append(Spacer(1, 24))

    ptext = '<font size="12"><b>Statement of Issue:</b></font>'
    issueStatementDoc.append(Paragraph(ptext, styles["Normal"]))

    providerMaster = TblProviderMaster.objects.filter(
        caseNumber=caseNum).first()
    issueID = providerMaster.issueID

    issueInfo = TblIssueMaster.objects.get(
        issueSRGID=str(issueID).split('-')[0])

    ptext = '<font size="12"><b>%s</b></font>' % issueInfo.issueName
    issueStatementDoc.append(Paragraph(ptext, styles["Normal"]))
    issueStatementDoc.append(Spacer(1, 12))

    groupIssueStatement = issueInfo.issueLongDescription
    ptext = '<font size="12">%s</font>' % groupIssueStatement
    issueStatementDoc.append(Paragraph(ptext, styles["Normal"]))

    issueStatement.build(issueStatementDoc)

    # Build Schedule G Table of Contents

    tocStory = []

    toc = SimpleDocTemplate("C:\\Users\\randall.gienko\\Desktop\\scheduleGTOC.pdf", pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)

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

    toc.build(tocStory)

    # Build Form G Schedule of Providers

    formGDoc = SimpleDocTemplate("C:\\Users\\randall.gienko\\Desktop\\scheduleG.pdf", pagesize=[A4[1], A4[0]],
                                 leftMargin=0, rightMargin=0,
                                 topMargin=105, bottomMargin=40)

    elements = []
    styles = getSampleStyleSheet()
    styleN = styles["BodyText"]

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
    caseProviders = TblProviderMaster.objects.filter(caseNumber=caseNum)
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
        columnDataProviderInfo = Paragraph('<para align=center>' + str(provName.providerName) + '<br/>' + str(provName.providerCity) +
            str(provName.providerCounty) + str(provName.stateID) + '</para>', styles["Normal"])

        provFYE = TblCaseDeterminationMaster.objects.get(caseNumber=caseNum)
        # print(provFYE.determinationFiscalYear.strftime("%m/%d/%Y"))
        columnDataFYE = Paragraph('<para align=center>' + str(provFYE.determinationFiscalYear.strftime("%m/%d/%Y")) +
                                  '</para>', styles["Normal"])

        columnDataMAC = Paragraph('<para align=center>' + str(caseObj.fiID) + '</para>', styles["Normal"])

        columnDataA = Paragraph('<para align=center>' + str(prov.provMasterDeterminationDate.strftime("%m/%d/%Y")) +
                                '</para>', styles["Normal"])

        hrqDate = TblAppealMaster.objects.get(caseNumber=prov.provMasterFromCase)
        columnDataB = Paragraph('<para align=center>' + str(hrqDate.appealCreateDate.strftime("%m/%d/%Y")) + '</para>',
                                styles["Normal"])

        no_of_days = prov.get_no_days()
        print(str(no_of_days))
        columnDataC = Paragraph('<para align=center>' + str(no_of_days) + '</para>', styles["Normal"])
        columnDataD = Paragraph('<para align=center>' + str(prov.provMasterAuditAdjs) + '</para>', styles["Normal"])

        locale.setlocale(locale.LC_ALL, '')
        columnDataE = Paragraph('<para align=center>' + str(locale.currency(prov.provMasterImpact, grouping=True)) +
                                '</para>', styles["Normal"])

        columnDataF = Paragraph('<para align=center>' + str(prov.provMasterFromCase) + '</para>', styles["Normal"])
        columnDataG = Paragraph(
            '<para align=center>' + str(prov.provMasterTransferDate.strftime("%m/%d/%Y")) + '</para>', styles["Normal"])

        scheduleGData.append([columnDataNumber, columnDataProviderNumber, columnDataProviderInfo, columnDataFYE,
                              columnDataMAC, columnDataA, columnDataB, columnDataC, columnDataD, columnDataE,
                              columnDataF, columnDataG])

    tR = Table(scheduleGData, repeatRows=1, colWidths=[1 * cm, 2 * cm, 4.5 * cm, 2.5 * cm, 2.5 * cm, 3 * cm,
                                                       3 * cm, 1.5 * cm, 2 * cm, 2.5 * cm, 2 * cm, 2.5 * cm])

    tR.hAlign = 'CENTER'

    tblStyle = TableStyle([('BOX', (0, 0), (-1, -1), 1, colors.black),
                           ('INNERGRID', (0, 0), (-1, -1), 1, colors.black)])

    tR.setStyle(tblStyle)

    elements.append(tR)

    formGDoc.build(elements, onFirstPage=PageNumCanvas,
                   onLaterPages=PageNumCanvas, canvasmaker=PageNumCanvas)

    return redirect(r'appeal-details', caseObj.caseNumber)


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

        self.drawString(15.5 * cm, 2 * cm, groupTotalImpact)
        self.line(8.9 * inch, 1.94 * cm, 9.75 * inch, 1.94 * cm)

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
