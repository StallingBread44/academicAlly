import requests
import discord
import re
import datetime

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
        response = requests.get("https://friscoisdhacapi.vercel.app/api/" + str(info_info) + "?username=" +
                                str(username_procedure) +
                                "&password=" + str(password_procedure))
    else:
        response = requests.get("https://friscoisdhacapi.vercel.app/api/" + str(info_info) + "?username=" +
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
    data = []
    for index in key:
        data.append(index[0])
    return data


def getgrades(username_procedure, password_procedure):
    grades = []
    for i in range(1, 5):
        response = accesshac(username_procedure, password_procedure, "pastclasses", i)
        data = response["pastClasses"]
        if grades:
            subname = subjectname(grades)
            for subject in data:
                if subject["name"] in subname:
                    x = int(subname.index(subject["name"]))
                    grades[x].append(subject["grade"])
                else:
                    grades.append([subject["name"], subject["grade"]])
        else:
            for subject in data:
                grades.append([subject["name"], subject["grade"]])
    return grades


def gpa(username_procedure, password_procedure):
    key = getgrades(username_procedure, password_procedure)
    data = 0
    for index in key:
        if re.search("Adv", index[0]):
            del index[0]
            x = 100 - average(index)
            x = x/10
            y = 5.5 - x
            data = data + y
        elif re.search("AP", index[0]):
            del index[0]
            x = 100 - average(index)
            x = x/10
            y = 6 - x
            data = data + y
        else:
            del index[0]
            x = 100 - average(index)
            x = x/10
            y = 5 - x
            data = data + y
    data = round(data/len(key), 8)
    return data


def average(key):
    response = 0
    i = 0
    for index in key:
        if index == "" or index == "0.00":
            break
        response = response + round(float(index), 2)
        i = i + 1
    avg = round(response/i, 2)
    return avg


def transcript(key):
    response = {}
    year = datetime.date.today()
    year = year.year
    quarter = 1
    data = key["studentTranscript"]
    for index in data:
        courses = index["courses"]
        for index_2 in courses:
            temp = {}
            if not index_2["sem1Grade"] == "":
                try:
                    response[index["yearsAttended"]][index_2["courseName"] + "_sem_1"] = index_2["sem1Grade"]
                except:
                    temp[index_2["courseName"] + "_sem_1"] = index_2["sem1Grade"]
                    response[index["yearsAttended"]] = temp

            if not index_2["sem2Grade"] == "":
                try:
                    response[index["yearsAttended"]][index_2["courseName"] + "_sem_2"] = index_2["sem2Grade"]
                except:
                    temp[index_2["courseName"] + "_sem_2"] = index_2["sem2Grade"]
                    response[index["yearsAttended"]] = temp
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
                response = accesshac(username, password, info, 0)
                data = response
                if info == "gpa":
                    try:
                        data = "Acutal GPA: " + str(gpa(username, password)) + str(hacgpa(username, password))
                    except:
                        data = str("Error, try again")
                await message.channel.send(data)
                username = ""
                password = ""
                info = ""
                return

print(transcript(accesshac("304551", "DEBA1243$", "transcript", 0)))

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run("MTIwNTUwNDgyNTY0MzYzODgyNA.GTFW-p.Ry4JfdZdomd-7fjZRnv7lLxaSgTvZNGvyhHDko")
