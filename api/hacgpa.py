from bs4 import BeautifulSoup


def _hacgpa(session):
    # using BeautifulSoup library
    # using requests library
    transcriptpagecontent = session.get('https://hac.friscoisd.org/HomeAccess/Content/Student/Transcript.aspx').text
    soup = BeautifulSoup(transcriptpagecontent, 'html.parser')
    weightedgpa = soup.find('span', attrs={'id': 'plnMain_rpTranscriptGroup_lblGPACum1'}).text
    unweightedgpa = soup.find('span', attrs={'id': 'plnMain_rpTranscriptGroup_lblGPACum2'}).text
    data = f'\nHAC Details - \n\nWeighted GPA: {weightedgpa} \nUnweighted GPA: {unweightedgpa}'
    return data