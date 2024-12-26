from bs4 import BeautifulSoup
import requests


def _login(username_procedure, password_procedure, session):
    # using BeautifulSoup library
    # using requests library
    response = session.get('https://hac.friscoisd.org/HomeAccess/Account/LogOn?ReturnUrl=%2fHomeAccess%2f')
    soup = BeautifulSoup(response.text, 'html.parser')
    token = soup.find('input', attrs={'name': '__RequestVerificationToken'})['value']

    data = {
        '__RequestVerificationToken': token,
        'VerificationOption': 'UsernamePassword',
        'database': '10',
        'LogOnDetails.UserName': username_procedure,
        'LogOnDetails.Password': password_procedure,
        'SCKTY00328510CustomEnabled': False,
        'SCKTY00436568CustomEnabled': False,
    }

    log = session.post('https://hac.friscoisd.org/HomeAccess/Account/LogOn?ReturnUrl=%2fHomeAccess%2f', data=data,)

    logsoup = BeautifulSoup(log.text, 'html.parser')

    if logsoup.find('div', class_='sg-login-container'):
        return False
    else:
        return True
    