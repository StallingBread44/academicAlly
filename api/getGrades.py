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
    #Get additional data required for POST
    hiddendata = (_gethiddeninput('https://hac.friscoisd.org/HomeAccess/Content/Student/Assignments.aspx', session=session))
    gradeslist = list()
    grades = {}
    #Additional data required for POST
    data = {
"__EVENTTARGET": 'ctl00$plnMain$btnRefreshView',
"__EVENTARGUMENT" : "",
'ctl00$plnMain$hdnddlClasses': '(All Classes)',
'ctl00$plnMain$ddlReportCardRuns': 'ALL',
'ctl00$plnMain$ddlClasses': 'ALL',
'ctl00$plnMain$ddlCompetencies': 'ALL',
'ctl00$plnMain$ddlOrderBy': 'Class',
    }

    data.update(hiddendata)
    #POST additional data + what data we want(which is getting every single assignments' grades in the school year)
    response = session.post(
        'https://hac.friscoisd.org/HomeAccess/Content/Student/Assignments.aspx', data=data).text
    
    #Parse html text to beautiful soup
    soup = BeautifulSoup(response, 'html.parser')

    #Parsing through beautiful soup code to isolate the class assignments and their grades
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
