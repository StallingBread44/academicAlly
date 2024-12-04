from bs4 import BeautifulSoup


# The below function is the outdated slow one
""" 
def _getgrades(session):
    # using BeautifulSoup library
    # using requests library
    # using re library
    hiddendata = (_gethiddeninput('https://hac.friscoisd.org/HomeAccess/Content/Student/Assignments.aspx'))
    gradeslist = list()
    for index in range(1, 5):
        data = {
            'ctl00$plnMain$ddlClasses': 'ALL',
            'ctl00$plnMain$ddlCompetencies': 'ALL',
            'ctl00$plnMain$ddlOrderBy': 'Class',
            '__EVENTARGUMENT': '',
            '__EVENTTARGET': 'ctl00$plnMain$btnRefreshView',
            'ctl00$plnMain$ddlReportCardRuns': f'{str(index)}-2024',
        }

        data.update(hiddendata)
        response = session.post(
            'https://hac.friscoisd.org/HomeAccess/Content/Student/Assignments.aspx', data=data).text
        soup = BeautifulSoup(response, 'html.parser')
        response = soup.find_all(class_='AssignmentClass')
        a = 0
        for i in response:
            subject = i.find(class_='sg-header-heading').text.strip()
            grade = soup.find(name='span', attrs={'id': f'plnMain_rptAssigmnetsByCourse_lblHdrAverage_'
                                                        + str(a)}).text.strip()
            grade = re.sub(r'[^0-9.]', '', grade)
            if gradeslist:
                sublist = _subjectname(gradeslist)
                if subject in sublist:
                    if grade:
                        gradeslist[sublist.index(subject)].append(grade)
                else:
                    if grade:
                        gradeslist.append([subject, grade])
                    else:
                        gradeslist.append([subject, None])
            else:
                if grade:
                    gradeslist.append([subject, grade])
                else:
                    gradeslist.append([subject, None])
            a += 1
    return gradeslist
"""


def _getgrades(session):
    hiddendata = (_gethiddeninput('https://hac.friscoisd.org/HomeAccess/Content/Student/Assignments.aspx', session=session))
    gradeslist = list()
    grades = {}
    data = {
"__EVENTTARGET": 'ctl00$plnMain$btnRefreshView',
"__EVENTARGUMENT" : "",
"ctl00$plnMain$hdnValidMHACLicense" : 'Y',
'ctl00$plnMain$hdnIsVisibleClsWrk': 'N',
'ctl00$plnMain$hdnIsVisibleCrsAvg': 'N',
'ctl00$plnMain$hdnTitle': 'Classwork',
'ctl00$plnMain$hdnLastUpdated': 'Last Updated',
'ctl00$plnMain$hdnDroppedCourse':  'This course was dropped as of',
'ctl00$plnMain$hdnddlClasses': '(All Classes)',
'ctl00$plnMain$hdnddlCompetencies': '(All Classes)',
'ctl00$plnMain$hdnCompDateDue': 'Date Due',
'ctl00$plnMain$hdnCompDateAssigned': 'Date Assigned',
'ctl00$plnMain$hdnCompCourse': 'Course',
'ctl00$plnMain$hdnCompAssignment': 'Assignment',
'ctl00$plnMain$hdnCompAssignmentLabel': 'Assignments Not Related to Any Competency',
'ctl00$plnMain$hdnCompNoAssignments': 'No assignments found',
'ctl00$plnMain$hdnCompNoClasswork': 'Classwork could not be found for this competency for the selected report card run.',
'ctl00$plnMain$hdnCompScore': 'Score',
'ctl00$plnMain$hdnCompPoints': 'Points',
'ctl00$plnMain$hdnddlReportCardRuns1': '(All Runs)',
'ctl00$plnMain$hdnddlReportCardRuns2': '(All Terms)',
'ctl00$plnMain$hdnbtnShowAverage': 'Show All Averages',
'ctl00$plnMain$hdnShowAveragesToolTip': "Show all student's averages",
'ctl00$plnMain$hdnPrintClassworkToolTip': 'Print all classwork',
'ctl00$plnMain$hdnPrintClasswork': 'Print Classwork',
'ctl00$plnMain$hdnCollapseToolTip': 'Collapse all courses',
'ctl00$plnMain$hdnCollapse': 'Collapse All',
'ctl00$plnMain$hdnFullToolTip': 'Switch courses to Full View',
'ctl00$plnMain$hdnViewFull': 'Full View',
'ctl00$plnMain$hdnQuickToolTip': 'Switch courses to Quick View',
'ctl00$plnMain$hdnViewQuick': 'Quick View',
'ctl00$plnMain$hdnExpand': 'Expand All',
'ctl00$plnMain$hdnExpandToolTip': 'Expand all courses',
'ctl00$plnMain$hdnChildCompetencyMessage': 'This competency is calculated as an average of the following competencies',
'ctl00$plnMain$hdnCompetencyScoreLabel': 'Grade',
'ctl00$plnMain$hdnAverageDetailsDialogTitle': 'Average Details',
'ctl00$plnMain$hdnAssignmentCompetency': 'Assignment Competency',
'ctl00$plnMain$hdnAssignmentCourse': 'Assignment Course',
'ctl00$plnMain$hdnTooltipTitle': 'Title',
'ctl00$plnMain$hdnCategory': 'Category',
'ctl00$plnMain$hdnDueDate': 'Due Date',
'ctl00$plnMain$hdnMaxPoints': 'Max Points',
'ctl00$plnMain$hdnCanBeDropped': 'Can Be Dropped',
'ctl00$plnMain$hdnHasAttachments': 'Has Attachments',
'ctl00$plnMain$hdnExtraCredit': 'Extra Credit',
'ctl00$plnMain$hdnType': 'Type',
'ctl00$plnMain$hdnAssignmentDataInfo': 'Information could not be found for the assignment',
'ctl00$plnMain$ddlReportCardRuns': 'ALL',
'ctl00$plnMain$ddlClasses': 'ALL',
'ctl00$plnMain$ddlCompetencies': 'ALL',
'ctl00$plnMain$ddlOrderBy': 'Class',
    }

    data.update(hiddendata)
    response = session.post(
        'https://hac.friscoisd.org/HomeAccess/Content/Student/Assignments.aspx', data=data).text
    soup = BeautifulSoup(response, 'html.parser')
    gradeslist = soup.find_all('div', class_='AssignmentClass')
    x = 0
    for class_ls in gradeslist:
        class_name = class_ls.find('a', class_='sg-header-heading').text.strip()
        class_vr = {}
        a = class_ls.find_all('tr', class_='sg-asp-table-data-row')
        for b in a:
            c = b.find_all('td')
            try:
                p1 = c[2].find('a').text.strip()
                p2 = c[3].text.strip()
                p3 = c[4].text.strip()
                class_vr[str(p1)] = (p2, p3)
            except AttributeError:
                pass
        grades[class_name] = class_vr
    return grades


def _subjectname(key):
    response = []
    for index in key:
        response.append(index[0])
    return response


def _gethiddeninput(content, session):
    # using BeautifulSoup library
    # using requests library
    tags = {}
    response = session.get(content).text
    soup = BeautifulSoup(response, 'html.parser')
    hiddentags = soup.findAll('input', attrs={'type': 'hidden'})
    for tag in hiddentags:
        tags[tag.get('name')] = tag.get('value')
    return tags
