import requests
import discord
import re
import datetime
import maskpass
from api.login import _login
from api.hacgpa import _hacgpa
from api.getSession import _getsession
from api.getGrades import _getgrades
from api.logoff import _logoff
from api.transcript import _transcript
from flask import Flask, render_template, request, url_for, redirect

"""

year = datetime.date.today()
year = str(year.year)
username = ""
password = ""
info = ""


def matchstr(key):
    words = ["info", "gpa", "schedule", "transcript", "currentclasses", "pastclasses"]
    for i in words:
        if re.search(i, key):
            return True
    return False


def findstr(key):
    words = ["info", "gpa", "schedule", "transcript", "currentclasses", "pastclasses", "hacgpa"]
    for i in words:
        if re.search(i, key):
            return i
    return



def accesshac(username_procedure, password_procedure, info_info, quarter_procedure):
    if quarter_procedure == 0:
        response = requests.post("https://friscoisdhacapi.vercel.app/api/" + str(info_info) + "?username=" +
                                str(username_procedure) +
                                "&password=" + str(password_procedure))
    else:
        response = requests.post("https://friscoisdhacapi.vercel.app/api/" + str(info_info) + "?username=" +
                                str(username_procedure) +
                                "&password=" + str(password_procedure) + "&quarter=" + str(quarter_procedure))
    data = response.json()
    return data

def hacgpa(username_procedure, password_procedure):
    key = accesshac(username_procedure, password_procedure, "gpa", 0)
    if key["rank"] == "":
        data = ("\nHAC Details - \nWeighted GPA: " + key["weightedGPA"] + "\nUnweighted(college) GPA: " +
                key["unweightedGPA"] + "\nRank: Unranked")
        return data
    else:
        data = ("\nHAC Details -  \nWeighted GPA: " + key["weightedGPA"] + "\nUnweighted(college) GPA: " +
                key["unweightedGPA"] + "\nRank: " + key["rank"])
        return data

def subjectname(key):
    response = []
    for index in key:
        response.append(index)
    return response


def getgrades(username_procedure, password_procedure):
    try:
        grades = transcript(accesshac(username_procedure, password_procedure, "transcript", 0))
    except:
        grades = {}
    a = int(grades["sem"])
    grades.pop("sem", None)

    for i in range(a, 5):
        data = accesshac(username_procedure, password_procedure, "pastclasses", i)
        data = data["pastClasses"]

        if grades:
            subname = subjectname(grades)
            for subject in data:
                if subject["name"] in subname:
                    grades[subject["name"]].append(subject["grade"])
                else:
                    grades[subject["name"]] = [subject["grade"]]

        else:
            for subject in data:
                grades[subject["name"]] = [(subject["grade"])]
    return grades


def gpa(username_procedure, password_procedure):
    key = _getgrades(username_procedure, password_procedure)
    hac = _hacgpa(username_procedure, password_procedure)
    a = 0
    data = 0
    for index in key:
        if not index == "sem":
            if re.search("Adv", index):
                z = average(key[index])
                if not (z is None):
                    x = 100 - z
                    x = x/10
                    y = 5.5 - x
                    data = data + y
                    a = a + 1
            elif re.search("AP", index):
                z = average(key[index])
                if not (z is None):
                    x = 100 - z
                    x = x/10
                    y = 6 - x
                    data = data + y
                    a = a + 1
            else:
                z = average(key[index])
                if not (z is None):
                    x = 100 - z
                    x = x/10
                    y = 5 - x
                    data = data + y
                    a = a + 1
    data = round(data/a, 8)
    data = "Acutal GPA:" + str(data) + hac
    return data


def average(key):
    response = 0
    i = 0
    try:
        for index in key:
            temp = float(index)
            if not (temp == 0 or temp == 0.00 or temp == .00):
                response = temp + response
                i += 1
        avg = round(float(response/i))
        return avg
    except ZeroDivisionError:
        return None
    except ValueError:
        return None


def transcript(key):
    sem_1 = True
    response = {}
    data = key["studentTranscript"]
    response["sem"] = 1

    for index in data:
        courses = index["courses"]
        for index_2 in courses:
            if index_2["sem1Grade"] == "":
                if re.search(year, str(index["yearsAttended"])):
                    if sem_1:
                        response["sem"] = 1
                    else:
                        response["sem"] = 3
            else:
                try:
                    response[index_2["courseName"]].append(index_2["sem1Grade"])
                except KeyError:
                    response[index_2["courseName"]] = [index_2["sem1Grade"]]
            if index_2["sem2Grade"] == "":
                if re.search(year, str(index["yearsAttended"])):
                    if sem_1:
                        response["sem"] = 1
                    else:
                        response["sem"] = 3
            else:
                sem_1 = False
                try:
                    response[index_2["courseName"]].append(index_2["sem2Grade"])
                except KeyError:
                    response[index_2["courseName"]] = [index_2["sem2Grade"]]
    return response


class MyClient(discord.Client):

    async def on_ready(self):
        print(f"Logged in as {self.user}")
        channel = client.get_channel(1205508296916865034)
        await channel.send("Enter objective")

    async def on_message(self, message):
        global username, password, info
        if not message.author == client.user:
            if info == "":
                if matchstr(message.content):
                    await message.channel.send("Enter Username: ")
                    info = findstr(message.content)
                    return
                else:
                    await message.channel.send("Additional information not available")
                    return
            elif username == "" and not info == "":
                await message.channel.send("Enter password: ")
                username = message.content
                return
            elif password == "" and not username == "":
                await message.channel.send("Please wait")
                password = message.content
                response = _accesshac(username, password, info, 0)
                data = response
                if info == "gpa":
                    try:
                        data = "Acutal GPA: " + str(_gpa(username, password)) + str(_hacgpa(username, password))
                    except:
                        data = str("Error, try again")
                await message.channel.send(data)
                username = ""
                password = ""
                info = ""
                return


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run("MTIwNTUwNDgyNTY0MzYzODgyNA.GTFW-p.Ry4JfdZdomd-7fjZRnv7lLxaSgTvZNGvyhHDko")


def _run():
    run = True
    while run:
        input_user = input("Calculate gpa(Y/N): ")
        if input_user == "n" or input_user == "N":
            run = False
        elif input_user == "y" or input_user == "Y":
            username = maskpass.askpass(prompt="Enter username: ", mask="*")
            password = maskpass.askpass(prompt="Enter password: ", mask="*")
            print(transcript(accesshac(username, password, 'transcript', 0)))
        else:
            print("Invalid input")
    print("Program stopped")

s = _request_session()
_login('304551', 'DEBA1243$', s)
print(_hacgpa(s))

            
"""

session = _getsession()
if _login('304551', 'DEBA1243$', session):
	_transcript(session)
else:
	print("Error")
_logoff(session)

