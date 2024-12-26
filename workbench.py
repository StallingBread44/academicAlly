from api.getGrades import _getgrades
from api.login import _login
from api.getSession import _getsession
from api.hacgpa import _hacgpa
from api.logoff import _logoff
import pprint
from classAvg import classAvg

#Heres where you can mess around

#Rn this code gets my grades(each and every single assignments' grades) from hac
session = _getsession()
_login("304551", "DEBA1243$", session)
x = _getgrades(session)

#Calls function to avg grades
#Right now classAvg is broken so dont expect it to work
y = classAvg(x)

#Prints class averages
print(y)

#Make sure to log off after your done with the session
_logoff(session)