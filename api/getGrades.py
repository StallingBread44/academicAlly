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
    data = {
        'ctl00$plnMain$ddlClasses': 'ALL',
        'ctl00$plnMain$ddlCompetencies': 'ALL',
        'ctl00$plnMain$ddlOrderBy': 'Class',
        '__EVENTARGUMENT': '',
        '__EVENTTARGET': 'ctl00$plnMain$btnRefreshView',
        'ctl00$plnMain$ddlReportCardRuns': 'ALL',
    }
    data.update(hiddendata)
    response = session.post(
        'https://hac.friscoisd.org/HomeAccess/Content/Student/Assignments.aspx', data=data).text
    soup = BeautifulSoup(response, 'html.parser')
    response = soup.find_all('div', class_="AssignmentClass")
    for subject in response:
        assignmentlist = soup.find_all('tr', class_='sg-asp-table-data-row')
        for assignment in assignmentlist:
            print(assignment)


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


