def createFormG(request, pk):
    caseObj = get_object_or_404(TblAppealMaster, pk=pk)

    # doc = SimpleDocTemplate("C:\\Users\\randall.gienko\\Desktop\\scheduleGCoverLetter.pdf", pagesize=letter,
    #                        rightMargin=72, leftMargin=72,
    #                        topMargin=0, bottomMargin=18)

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
        columnDataProviderInfo = Paragraph(
            '<para align=center>' + str(provName.providerName) + '<br/>' + str(provName.providerCity) +
            str(provName.providerCounty) + str(provName.stateID) + '</para>', styles["Normal"])

        columnDataFYE = Paragraph('<para align=center>' + str(prov.provMasterFiscalYear.strftime("%m/%d/%Y")) +
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

    # return redirect(r'appeal-details', caseObj.caseNumber)
    return response