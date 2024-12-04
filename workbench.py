from api.getGrades import _getgrades
from api.login import _login
from api.getSession import _getsession
from api.hacgpa import _hacgpa


session = _getsession()
_login("304551", "DEBA1243$", session)
x = _getgrades(session)

print(x)