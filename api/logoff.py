def _logoff(session):
    # using requests library
    logoff = session.get('https://hac.friscoisd.org/HomeAccess/Account/Logoff')