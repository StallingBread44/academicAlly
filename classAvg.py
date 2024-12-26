
#doesn't work 

def classAvg(gradeslist):
    grades = {}
    for class_vr in gradeslist:
        grade = []
        print(class_vr)
        if gradeslist[class_vr] != None:
            for assignments in class_vr:
                temp = class_vr[assignments]
                if temp[1] == "Assessment of Learning":
                    grade.append(class_vr[assignments][2])
        return grade