import requests
from bs4 import BeautifulSoup
import re
from api.getSession import _getsession
from api.login import _login
from api.logoff import _logoff


def _transcript(session):
    response = session.get('https://hac.friscoisd.org/HomeAccess/Content/Student/Transcript.aspx').text
    soup = BeautifulSoup(response, 'html.parser')
    data = {}
    data_2 = []
    x = 0

    d1 = soup.find('table', attrs={'id': f'plnMain_rpTranscriptGroup_dgCourses_1'})
    d2 = d1.find_all('tr', attrs={'class': 'sg-asp-table-data-row'})

    for cell in d2:
        d3 = cell.find_all('td')
        x = 0
        temp = 0
        for td in d3:
            if x == 0:
                temp = td.get_text()
                t1, t2, t3 = temp.partition(' ')
            if x == 2 or x == 3:
                try:
                    temp_2 = data[t1]
                    temp_2.append(td.get_text())
                    data[t1] = temp_2
                except:
                    data[t1] = [td.get_text()]
            x += 1

    """ 
    while True:
        index = soup.find('table', attrs={'id': f'plnMain_rpTranscriptGroup_dgCourses_{x}'})
        if index is not None:
            for item in index:
                if item.find('tr'):
                    data.append(item)

#                if item.find('class', attrs={'class': 'tr class="sg-asp-table-data-row'}):
 #                   print(item)
                #data.append(item.find_all('tr', attrs={'class': 'sg-asp-table-data-row'}))
        else:
            break
        x = x + 1
        """
    return data
