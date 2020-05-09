from importModules import *


screenToken = 0


# to retrieve top projects based on score from the database for OU and the System

def get_top_projects(self, name, username, tok, database):

    projectList = []
    groupName = []
    projectDesc = []

    if tok == 1:
        projects = database.child("projects").order_by_child(name).limit_to_first(3).get()
        
    else:
        projects = database.child("projects").order_by_child(name).equal_to(username).get()

    cnt = 0


    if projects.val() != None: 
        for project in projects.each():
            projectList.append(project.val()["name"])
            groupName.append(project.val()["group"])
            projectDesc.append(project.val()["desc"])
            cnt+=1

    while cnt < 3:
        projectList.append("")
        groupName.append("")
        projectDesc.append("")
        cnt +=1

    self.project1.text = projectList[0] + "  " + groupName[0]
    self.project2.text = projectList[1] + "  " + groupName[1]
    self.project3.text = projectList[2] + "  " + groupName[2]

    self.desc1.text = projectDesc[0]
    self.desc2.text = projectDesc[1]
    self.desc3.text = projectDesc[2]


# to get the top users based on score from the database for the system

def get_top_users(self, name, database):

    userList = []
    users = database.child("new_users").order_by_child("privilege").equal_to(1).limit_to_first(4).get()

    users_su = database.child("new_users").order_by_child("privilege").equal_to(2).limit_to_first(2).get()

    cnt = 0

    if users.val() != None:
        for user in users.each():
            userList.append(user.val()["name"])
            cnt+=1

    while cnt < 4:
        userList.append("")
        cnt +=1

    if users_su.val() != None:
        for user_su in users_su.each():
            userList.append(user_su.val()["name"])
            cnt+=1

    while cnt < 6:
        userList.append("")
        cnt +=1



    self.user2.text = userList[0]
    self.user3.text = userList[1]
    self.user4.text = userList[2]
    self.user5.text = userList[3]
    
    self.user1.text = userList[4]
    self.user6.text = userList[5]


# to get all warnings from the databse for OU and SU

def get_warnings(self, database, tok, name):

    warningList = []
    groupList = []

    if tok == 1:
        warnings = database.child("warnings").order_by_key().limit_to_last(7).get()
    
    else:
        warnings = database.child("warnings").order_by_child("user").equal_to(name).limit_to_last(7).get()
    
    
    cnt = 0

    if warnings.val() != None:
        for warning in warnings.each():
            warningList.append(warning.val()["desc"])
            groupList.append(warning.val()["group"])
            cnt = cnt + 1

    while cnt < 7:
        warningList.append("")
        groupList.append("")
        cnt += 1


    self.w1.text = warningList[0] + "  " + groupList[0]
    self.w2.text = warningList[1] + "  " + groupList[1]
    self.w3.text = warningList[2] + "  " + groupList[2]
    self.w4.text = warningList[3] + "  " + groupList[3]
    self.w5.text = warningList[4] + "  " + groupList[4]
    self.w6.text = warningList[5] + "  " + groupList[5]
    self.w7.text = warningList[6] + "  " + groupList[6]


# to retrive notifications from the database for OU and SU

def get_group_notifications(self, database, tok, name):

    notificationList = []
    groupList = []

    if tok == 1:
        notifications = database.child("groupNotification").order_by_key().limit_to_last(7).get()
    else:
        notifications = database.child("groupNotification").order_by_child("user").equal_to(name).limit_to_last(7).get()

    cnt = 0

    #print(notifications.val())

    if notifications.val() != None:
        for notification in notifications.each():
            notificationList.append(notification.val()["desc"])
            groupList.append(notification.val()["group"])
            cnt = cnt + 1

    while cnt < 7:
        notificationList.append("")
        groupList.append("")
        cnt += 1


    self.g1.text = notificationList[0] + "  " + groupList[0]
    self.g2.text = notificationList[1] + "  " + groupList[1]
    self.g3.text = notificationList[2] + "  " + groupList[2]
    self.g4.text = notificationList[3] + "  " + groupList[3]
    self.g5.text = notificationList[4] + "  " + groupList[4]
    self.g6.text = notificationList[5] + "  " + groupList[5]
    self.g7.text = notificationList[6] + "  " + groupList[6]




# the keys have timestamps on them
#########################################################################################




