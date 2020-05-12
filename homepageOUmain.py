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

    try:
        if projects.val() != None: 
            for project in projects.each():
                projectList.append(project.val()["name"])
                groupName.append(project.val()["group"])
                projectDesc.append(project.val()["desc"])
                cnt+=1
    except:
        pass

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
    users = database.child("users").order_by_child("points").limit_to_last(4).get()

    users_su = database.child("users").order_by_child("privilege").equal_to(2).limit_to_first(2).get()

    cnt = 0

    try:
        if users.val() != None:
            for user in users.each():
                userList.append(user.val()["name"])
                cnt+=1
    except:
        pass

    while cnt < 4:
        userList.append("")
        cnt +=1

    try:
        if users_su.val() != None:
            for user_su in users_su.each():
                userList.append(user_su.val()["name"])
                cnt+=1
    except:
        pass

    while cnt < 6:
        userList.append("")
        cnt +=1

    self.user2.text = userList[0]
    self.user3.text = userList[1]
    self.user4.text = userList[2]
    self.user5.text = userList[3]
    
    self.user1.text = userList[4]
    self.user6.text = userList[5]

# to get reference notification 

def get_reference_notifications(self, db, name):
        notificationList = []
        notifications = db.child("references").order_by_child("user").equal_to(name).limit_to_last(7).get()
        cnt = 0

        try:
            if notifications.val() != None:
                for notification in notifications.each():
                    notificationList.append(notification.val()["desc"])
                    cnt = cnt + 1
        except:
            pass

        while cnt < 7:
            notificationList.append("")
            cnt += 1

        self.g1.text = notificationList[0] 
        self.g2.text = notificationList[1]
        self.g3.text = notificationList[2] 
        self.g4.text = notificationList[3] 
        self.g5.text = notificationList[4]
        self.g6.text = notificationList[5] 
        self.g7.text = notificationList[6] 


# get all information of a user to display 

def standing_update(self, username, index):
        userinfo = db.child("users").order_by_child("name").equal_to(username).limit_to_first(1).get()
        standing = ""

        try:
            if userinfo.val()!= None:
                for info in userinfo.each():
                    val = info.val()["privilege"]
                
                if val == 0:
                    standing = "OU"
                elif val == 1:
                    standing = "VIP"
                else: standing = "SU"
        except:
            pass

        self.manager.screens[index].ids.priv.text = standing
        self.manager.screens[index].ids.username.text = username            
        if index == 16:
            self.manager.current = "VisitorView"
        elif index == 4:
            self.manager.current = "profile"
        else:
            self.manager.current = "VisitorViewLoggedIn"


def get_compliments(self, database):

    complimentList = []
    userName = []
    users = database.child("users").get()

    compliment_cnt = []

    try:
        if users.val() != None:
            for user in users.each():
                comp_count = database.child("compliments").order_by_child("user").equal_to(user.val()["name"]).get()

                cnt_num = 0
                for comp in comp_count.each():
                    cnt_num = cnt_num + 1   

                if cnt_num >= 3:
                    compliment_cnt.append("(3 compliments, increase score)")
                else:
                    compliment_cnt.append("")
    except:
        pass
        
    while len(compliment_cnt) < 7:
        compliment_cnt.append("")
    compliments = database.child("compliments").order_by_key().limit_to_last(7).get()    
    
    cnt = 0

    try:
        if compliments.val() != None:
            for compliment in compliments.each():
                complimentList.append(compliment.val()["desc"])
                userName.append(compliment.val()["user"])
                cnt = cnt + 1
    except:
        pass

    while cnt < 7:
        complimentList.append("")
        userName.append("")
        cnt += 1


    self.c1.text = userName[0] + " " + complimentList[0] + "\n" + compliment_cnt[0] 
    self.c2.text = userName[1] + " " + complimentList[1] + "\n" + compliment_cnt[1] 
    self.c3.text = userName[2] + " " + complimentList[2] + "\n" + compliment_cnt[2] 
    self.c4.text = userName[3] + " " + complimentList[3] + "\n" + compliment_cnt[3] 
    self.c5.text = userName[4] + " " + complimentList[4] + "\n" + compliment_cnt[4] 
    self.c6.text = userName[5] + " " + complimentList[5] + "\n" + compliment_cnt[5] 
    self.c7.text = userName[6] + " " + complimentList[6] + "\n" + compliment_cnt[6] 


def get_groups(self, username):

    groupList = []

    groups = db.child("projects").order_by_child("user").equal_to(username).get()  
    
    cnt = 0
    try:
        if groups.val() != None:
            for group in groups.each():
                groupList.append(group.val()["group"])
                cnt = cnt + 1
    except:
        pass

    while cnt < 5:
        groupList.append("")
        cnt += 1


    self.g1.text = groupList[0]
    self.g2.text = groupList[1]
    self.g3.text = groupList[2]
    self.g4.text = groupList[3]
    self.g5.text = groupList[4]



# to get all warnings from the databse for OU and SU

def get_warnings(self, database, tok, name, callerId):

    warningList = []
    groupList = []
    userName = []

    if tok == 1:
        warnings = database.child("warnings").order_by_key().limit_to_last(7).get()    
    else:
        warnings = database.child("warnings").order_by_child("user").equal_to(name).limit_to_last(7).get()
    
    
    cnt = 0

    try:
        if warnings.val() != None:
            for warning in warnings.each():
                warningList.append(warning.val()["desc"])
                groupList.append(warning.val()["group"])
                userName.append(warning.val()["user"])
                cnt = cnt + 1
    except:
        pass
    
    while cnt < 7:
        warningList.append("")
        groupList.append("")
        userName.append("")
        cnt += 1

    if callerId == 1:
        self.w1.text = userName[0] + " " + warningList[0] + "  " + groupList[0]
        self.w2.text = userName[1] + " " + warningList[1] + "  " + groupList[1]
        self.w3.text = userName[2] + " " + warningList[2] + "  " + groupList[2]
        self.w4.text = userName[3] + " " + warningList[3] + "  " + groupList[3]
        self.w5.text = userName[4] + " " + warningList[4] + "  " + groupList[4]
        self.w6.text = userName[5] + " " + warningList[5] + "  " + groupList[5]
        self.w7.text = userName[6] + " " + warningList[6] + "  " + groupList[6]

    else:
        t1 = userName[0] + " " + warningList[0] + "  " + groupList[0] 
        t2 = userName[1] + " " + warningList[1] + "  " + groupList[1] 
        t3 = userName[2] + " " + warningList[2] + "  " + groupList[2]

        self.w1.text = "1. " + t1 + "\n2. " + t2 + "\n3. " + t3

# to retrive notifications from the database for OU and SU

def get_group_notifications(self, database, tok, name):

    notificationList = []
    groupList = []

    if tok == 1:
        notifications = database.child("groupNotification").order_by_key().limit_to_last(7).get()
    else:
        notifications = database.child("groupNotification").order_by_child("user").equal_to(name).limit_to_last(7).get()

    cnt = 0

    try:
        if notifications.val() != None:
            for notification in notifications.each():
                notificationList.append(notification.val()["desc"])
                groupList.append(notification.val()["group"])
                cnt = cnt + 1
    except:
        pass

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


# to get all warnings from the databse for OU and SU

def get_complaints(self, database, tok, name, callerId):

    complaintList = []
    userName = []

    if tok == 1:
        complaints = database.child("complaints").order_by_key().limit_to_last(7).get()    
    else:
        complaints = database.child("complaints").order_by_child("user").equal_to(name).limit_to_last(7).get()
    
    
    cnt = 0

    try:
        if complaints.val() != None:
            for complaint in complaints.each():
                complaintList.append(complaint.val()["desc"])
                userName.append(complaint.val()["user"])
                cnt = cnt + 1
    except:
        pass

    while cnt < 7:
        complaintList.append("")
        userName.append("")
        cnt += 1

    if callerId == 1:
        self.w1.text = userName[0] + " " + complaintList[0] 
        self.w2.text = userName[1] + " " + complaintList[1] 
        self.w3.text = userName[2] + " " + complaintList[2] 
        self.w4.text = userName[3] + " " + complaintList[3] 
        self.w5.text = userName[4] + " " + complaintList[4] 
        self.w6.text = userName[5] + " " + complaintList[5] 
        self.w7.text = userName[6] + " " + complaintList[6] 

    else:
        t1 = userName[0] + " " + complaintList[0] 
        t2 = userName[1] + " " + complaintList[1] 
        t3 = userName[2] + " " + complaintList[2] 

        self.w1.text = "1. " + t1 + "\n2. " + t2 + "\n3. " + t3


#########################################################################################
# add project information for each user in projects table


def add_projects(groupName, projectName, groupDesc, groupUsers):
    for groupUser in groupUsers:
        userNames = db.child("users").order_by_child("email").equal_to(groupUser).limit_to_first(1).get()
        
        try:
               for u in userNames.each():
                name = u.val()["name"]
        except:
            pass

        data = {
            "desc": groupDesc,
            "group": groupName,
            "name": projectName,
            "score": 0,
            "user": name
        }
        db.child("projects").push(data)

#add_projects( "Group8", "Lighthouse", "to motivate people", {"eduardo@gmail.com", "me1@gmail.com", "idk@gmail.com", "boi@gmail.com"})
