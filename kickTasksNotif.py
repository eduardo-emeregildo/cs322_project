from signingDetails import Store, show_popup
from groupPageFunctions import *

class KickNotifications(Screen):

    def on_pre_enter(self):
        email = "jin@aol.com"
        db = firebase.database()

        notifTypeList, groupIdList, notifUserList = [], [], []

        groupReqDb = db.child('groupRequests').order_by_child('email').equal_to(email).get()
        for sect in groupReqDb:
            groupReqs = sect.val()['notifications']

        for key in groupReqs.keys():
            groupIdList.append(groupReqs[key]['groupId'])
            notifTypeList.append(groupReqs[key]['notifType'])
            if groupReqs[key]['notifType'] == "Member":
                notifUserList.append(groupReqs[key]['notifUser'])
            else:
                notifUserList.append(" ")

        titleLblGroup = "Group Close Vote: "
        titleLblMember = "Kick Member from Group Vote: "
        titleLblJoin = "Request to Join Group: "

        # Update Label 1
        if len(notifTypeList) >= 1:
            self.btnAce1.disable = False
            self.btnRej1.disable = False

            groupDb = db.child('group').order_by_child('groupId').equal_to(groupIdList[0]).get()
            for section in groupDb:
                groupInfo = section.val()
                groupUsers = section.val()['groupUsers']

            if notifTypeList[0] == "Group":
                for i in range(1, len(groupUsers)):
                    if groupUsers[i]['email'] == email:
                        groupInfoAsn = groupUsers[i]['taskAssign']
                        groupInfoCom = groupUsers[i]['taskComplete']

                self.titleLabel1.text = titleLblGroup + groupInfo['groupName']
                self.detailLbl1.text = "[ DETAILS ]   " + groupInfo['groupDesc'] + \
                                       "\n[ PERSONAL TASKS ]   Assigned: " + str(groupInfoAsn) + \
                                       " // Completed: " + str(groupInfoCom)

            elif notifTypeList[0] == "Member":

                for i in range(1, len(groupUsers)):
                    if groupUsers[i]['email'] == notifUserList[0]:
                        groupInfoAsn = groupUsers[i]['taskAssign']
                        groupInfoCom = groupUsers[i]['taskComplete']

                self.titleLabel1.text = titleLblMember + groupInfo['groupName']
                self.detailLbl1.text = "[ DETAILS ]   Email: " + notifUserList[0] + \
                                       "\n[ TASKS ]   Assigned: " + str(groupInfoAsn) + \
                                       " // Completed: " + str(groupInfoCom)

            elif notifTypeList[0] == "Join":
                groupMemList = ""
                for i in range(1, len(groupUsers)):
                    groupMemList = groupMemList + groupUsers[i]['email'] + " / "
                    if i == 2:
                        groupMemList = groupMemList + "\n"

                self.titleLabel1.text = titleLblJoin + groupInfo['groupName']
                self.detailLbl1.text = "[ DETAILS ]   Description: " + groupInfo['groupDesc'] + \
                                       "\n[ MEMBERS ]   " + groupMemList

        # Update Label 2
        if len(notifTypeList) >= 2:
            self.btnAce2.disable = False
            self.btnRej2.disable = False

            groupDb = db.child('group').order_by_child('groupId').equal_to(groupIdList[1]).get()
            for section in groupDb:
                groupInfo = section.val()
                groupUsers = section.val()['groupUsers']

            if notifTypeList[1] == "Group":
                for i in range(1, len(groupUsers)):
                    if groupUsers[i]['email'] == email:
                        groupInfoAsn = groupUsers[i]['taskAssign']
                        groupInfoCom = groupUsers[i]['taskComplete']

                self.titleLabel2.text = titleLblGroup + groupInfo['groupName']
                self.detailLbl2.text = "[ DETAILS ]   " + groupInfo['groupDesc'] + \
                                       "\n[ PERSONAL TASKS ]   Assigned: " + str(groupInfoAsn) + \
                                       " // Completed: " + str(groupInfoCom)

            elif notifTypeList[1] == "Member":

                for i in range(1, len(groupUsers)):
                    if groupUsers[i]['email'] == notifUserList[1]:
                        groupInfoAsn = groupUsers[i]['taskAssign']
                        groupInfoCom = groupUsers[i]['taskComplete']

                self.titleLabel2.text = titleLblMember + groupInfo['groupName']
                self.detailLbl2.text = "[ DETAILS ]   Email: " + notifUserList[1] + \
                                       "\n[ TASKS ]   Assigned: " + str(groupInfoAsn) + \
                                       " // Completed: " + str(groupInfoCom)

            elif notifTypeList[1] == "Join":
                groupMemList = ""
                for i in range(1, len(groupUsers)):
                    groupMemList = groupMemList + groupUsers[i]['email'] + " / "
                    if i == 2:
                        groupMemList = groupMemList + "\n"

                self.titleLabel2.text = titleLblJoin + groupInfo['groupName']
                self.detailLbl2.text = "[ DETAILS ]   Description: " + groupInfo['groupDesc'] + \
                                       "\n[ MEMBERS ]   " + groupMemList

        # Update Label 3
        if len(notifTypeList) >= 3:
            self.btnAce3.disable = False
            self.btnRej3.disable = False

            groupDb = db.child('group').order_by_child('groupId').equal_to(groupIdList[2]).get()
            for section in groupDb:
                groupInfo = section.val()
                groupUsers = section.val()['groupUsers']

            if notifTypeList[2] == "Group":
                for i in range(1, len(groupUsers)):
                    if groupUsers[i]['email'] == email:
                        groupInfoAsn = groupUsers[i]['taskAssign']
                        groupInfoCom = groupUsers[i]['taskComplete']

                self.titleLabel3.text = titleLblGroup + groupInfo['groupName']
                self.detailLbl3.text = "[ DETAILS ]   " + groupInfo['groupDesc'] + \
                                       "\n[ PERSONAL TASKS ]   Assigned: " + str(groupInfoAsn) + \
                                       " // Completed: " + str(groupInfoCom)

            elif notifTypeList[2] == "Member":

                for i in range(1, len(groupUsers)):
                    if groupUsers[i]['email'] == notifUserList[2]:
                        groupInfoAsn = groupUsers[i]['taskAssign']
                        groupInfoCom = groupUsers[i]['taskComplete']

                self.titleLabel3.text = titleLblMember + groupInfo['groupName']
                self.detailLbl3.text = "[ DETAILS ]   Email: " + notifUserList[2] + \
                                       "\n[ TASKS ]   Assigned: " + str(groupInfoAsn) + \
                                       " // Completed: " + str(groupInfoCom)

            elif notifTypeList[2] == "Join":
                groupMemList = ""
                for i in range(1, len(groupUsers)):
                    groupMemList = groupMemList + groupUsers[i]['email'] + " / "
                    if i == 2:
                        groupMemList = groupMemList + "\n"

                self.titleLabel3.text = titleLblJoin + groupInfo['groupName']
                self.detailLbl3.text = "[ DETAILS ]   Description: " + groupInfo['groupDesc'] + \
                                       "\n[ MEMBERS ]   " + groupMemList

        # Update Label 4
        if len(notifTypeList) >= 4:
            self.btnAce4.disable = False
            self.btnRej4.disable = False

            groupDb = db.child('group').order_by_child('groupId').equal_to(groupIdList[3]).get()
            for section in groupDb:
                groupInfo = section.val()
                groupUsers = section.val()['groupUsers']

            if notifTypeList[3] == "Group":
                for i in range(1, len(groupUsers)):
                    if groupUsers[i]['email'] == email:
                        groupInfoAsn = groupUsers[i]['taskAssign']
                        groupInfoCom = groupUsers[i]['taskComplete']

                self.titleLabel4.text = titleLblGroup + groupInfo['groupName']
                self.detailLbl4.text = "[ DETAILS ]   " + groupInfo['groupDesc'] + \
                                       "\n[ PERSONAL TASKS ]   Assigned: " + str(groupInfoAsn) + \
                                       " // Completed: " + str(groupInfoCom)

            elif notifTypeList[3] == "Member":

                for i in range(1, len(groupUsers)):
                    if groupUsers[i]['email'] == notifUserList[3]:
                        groupInfoAsn = groupUsers[i]['taskAssign']
                        groupInfoCom = groupUsers[i]['taskComplete']

                self.titleLabel4.text = titleLblMember + groupInfo['groupName']
                self.detailLbl4.text = "[ DETAILS ]   Email: " + notifUserList[3] + \
                                       "\n[ TASKS ]   Assigned: " + str(groupInfoAsn) + \
                                       " // Completed: " + str(groupInfoCom)

            elif notifTypeList[3] == "Join":
                groupMemList = ""
                for i in range(1, len(groupUsers)):
                    groupMemList = groupMemList + groupUsers[i]['email'] + " / "
                    if i == 2:
                        groupMemList = groupMemList + "\n"

                self.titleLabel4.text = titleLblJoin + groupInfo['groupName']
                self.detailLbl4.text = "[ DETAILS ]   Description: " + groupInfo['groupDesc'] + \
                                       "\n[ MEMBERS ]   " + groupMemList

    def kick_reject(self, btnNum, accept):
        db = firebase.database()
        email = "jin@aol.com"

        if btnNum == 4:
            self.btnAce4.disabled = True
            self.btnRej4.disabled = True

        elif btnNum == 3:
            self.btnAce3.disabled = True
            self.btnRej3.disabled = True

        elif btnNum == 2:
            self.btnAce2.disabled = True
            self.btnRej2.disabled = True

        elif btnNum == 1:
            self.btnAce1.disabled = True
            self.btnRej1.disabled = True

        groupReqDb = db.child('groupRequests').order_by_child('email').equal_to(email).get()
        for sect in groupReqDb:
            groupReqs = sect.val()['notifications']
            if sect.val()['email'] == email:
                saveUserKey = sect.key()

        groupId = ""
        count = 1
        for key in groupReqs.keys():
            if count == btnNum:
                groupId = groupReqs[key]['groupId']
                notifType = groupReqs[key]['notifType']
                kickKey = key
                if notifType == 'Member':
                    notifUser = groupReqs[key]['notifUser']
                else:
                    notifUser = ""
                break
            count += 1

        if groupId == "":
            return

        db.child('groupRequests').child(saveUserKey).child('notifications').child(kickKey).remove()

        if notifType == 'Group' or notifType == 'Member':
            kickDb = db.child('groupKick').order_by_child('groupId').equal_to(groupId).get()
            for sector in kickDb:
                if sector.val()['kickType'] == 'Group' and notifType == 'Group':
                    saveGroKickKey = sector.key()
                    groKickAce = sector.val()['accept']
                    groKickRej = sector.val()['reject']
                    groKickVot = sector.val()['votes']
                    break
                if sector.val()['groupUser'] == notifUser and notifType == 'Member':
                    saveGroKickKey = sector.key()
                    groKickAce = sector.val()['accept']
                    groKickRej = sector.val()['reject']
                    groKickVot = sector.val()['votes']
                    break

            if accept:
                groKickAce = groKickAce + 1
            else:
                groKickRej = groKickRej + 1

            data = {
                "groupId": groupId,
                "groupUser": notifUser,
                "kickType": notifType,
                "accept": groKickAce,
                "reject": groKickRej,
                "votes": groKickVot
            }

            db.child('groupKick').child(saveGroKickKey).update(data)
            self.kick_checkVote(data, saveGroKickKey)

        if notifType == 'Join':
            groupDb = db.child('group').order_by_child('groupId').equal_to(groupId).get()
            for sector in groupDb:
                groupUsers = sector.val()['groupUsers']
                saveJoinGKey = sector.key()

            for i in range(1, len(groupUsers)):
                if groupUsers[i]['email'] == email:
                    saveJoinKey = i
                    break

            if accept:
                data = {
                    "email": email,
                    "taskAssign": 0,
                    "taskComplete": 0
                }
                db.child('group').child(saveJoinGKey).child('groupUsers').child(i).update(data)
            else:
                pass
                db.child('group').child(saveJoinGKey).child('groupUsers').child(i).remove()

    def kick_checkVote(self, data, groupKickKey):
        db = firebase.database()

        if data['kickType'] == 'Member':
            if data['votes'] == data['accept']:
                remove_group_user(data['groupUser'], data['groupId'])
                db.child('groupKick').child(groupKickKey).remove()
            elif data['votes'] == data['accept'] + data['reject']:
                db.child('groupKick').child(groupKickKey).remove()
            else:
                return

        if data['kickType'] == 'Group':
            if data['votes'] <= data['accept'] + data['reject']:
                if data['accept'] > data['reject']:
                    # do not remove group yet, make sure to pass to SU first
                    groupDb = db.child('group').order_by_child('groupId').equal_to(data['groupId']).get()
                    for section in groupDb:
                        groupUsers = section.val()['groupUsers']

                    for i in range(1, len(groupUsers)):
                        dated = {
                            "desc": "closegroup",
                            "group": data['groupId'],
                            "priority": 1,
                            "user": groupUsers[i]['email']
                        }
                        db.child('groupNotification').push(dated)

                db.child('groupKick').child(groupKickKey).remove()
            else:
                return


class TasksNotifications(Screen):

    def on_pre_enter(self, *args):
        email = "jin@aol.com"
        db = firebase.database()

        groupIdList, taskDetList, taskIdList, groupNameList = [], [], [], []

        groupReqDb = db.child('posts').order_by_child('claimBy').equal_to(email).get()
        for sector in groupReqDb:
            if sector.val()['postType'] == "Task":
                groupIdList.append(sector.val()['groupId'])
                taskDetList.append(sector.val()['postContent'])
                taskIdList.append(sector.val()['taskId'])

        for i in range(len(groupIdList)):
            groupDb = db.child('group').order_by_child('groupId').equal_to(groupIdList[i]).get()
            for section in groupDb:
                groupNameList.append(section.val()['groupName'])

        # Update Labels
        if len(groupIdList) >= 1:
            self.titleLabel1.text = "Task: " + taskDetList[0]
            self.detailLbl1.text = "[ GROUP NAME ]   " + groupNameList[0]

        if len(groupIdList) >= 2:
            self.titleLabel2.text = "Task: " + taskDetList[1]
            self.detailLbl2.text = "[ GROUP NAME ]   " + groupNameList[1]

        if len(groupIdList) >= 3:
            self.titleLabel3.text = "Task: " + taskDetList[2]
            self.detailLbl3.text = "[ GROUP NAME ]   " + groupNameList[2]

        if len(groupIdList) >= 4:
            self.titleLabel4.text = "Task: " + taskDetList[3]
            self.detailLbl4.text = "[ GROUP NAME ]   " + groupNameList[3]

    def task_complete(self, btnNum):
        # when user clicks complete from their request page
        email = 'jin@aol.com'
        db = firebase.database()

        groupIdList, taskDetList, taskIdList, groupNameList = [], [], [], []

        groupReqDb = db.child('posts').order_by_child('claimBy').equal_to(email).get()
        for sector in groupReqDb:
            if sector.val()['postType'] == "Task":
                groupIdList.append(sector.val()['groupId'])
                taskIdList.append(sector.val()['taskId'])

        if btnNum+1 == 1:
            self.btnAce1.disabled = True
        if btnNum+1 == 2:
            self.btnAce2.disabled = True
        if btnNum+1 == 3:
            self.btnAce3.disabled = True
        if btnNum+1 == 4:
            self.btnAce4.disabled = True

        if btnNum+1 > len(groupIdList):
            show_popup("Error", "No Task Exists")
            return

        #search through group DB to increase task complete and task assign
        groupDb = db.child("group").order_by_child("groupId").equal_to(groupIdList[btnNum]).get()
        for sect in groupDb.each():
            groupKey = sect.key()
        for sections in groupDb.each():
            groupUsers = sections.val()['groupUsers']
        for i in range(1, len(groupUsers)):
            if email in groupUsers[i].values():
                taskFound = groupUsers[i]['taskAssign'] - 1
                taskComplete = groupUsers[i]['taskComplete'] + 1

                if taskFound < 0:
                    taskFound = 0

        #search through post DB
        postDb = db.child("posts").order_by_child("groupId").equal_to(groupIdList[btnNum]).get()

        #deletes post in post db and updates count
        for sect in postDb:
            if sect.val()['postType'] == "Task":
                if email == sect.val()['claimBy'] and taskIdList[btnNum] == sect.val()['taskId']:
                    postKey = sect.key()
                    db.child("posts").child(postKey).remove()
                    db.child("group").child(groupKey).child("groupUsers").child(i) \
                        .update({"taskAssign": taskFound, "taskComplete": taskComplete})
                else:
                    show_popup("Error", "No Task Found")


class VipNotifications(Screen):
    def on_pre_enter(self, *args):
        email = "jin@aol.com"
        db = firebase.database()

        groupNameList, groupUserList = [], []

        #finds all assignVIP for email, only looks at where ticket = 0
        groupReqDb = db.child('assignVIP').order_by_child('email').equal_to(email).get()
        for sector in groupReqDb:
            if sector.val()['ticket'] == 0:
                groupNameList.append(sector.val()['groupname assigned'])

        # gets info for all the groups assigned above
        for i in range(len(groupNameList)):
            groupDb = db.child('group').order_by_child('groupName').equal_to(groupNameList[i]).get()
            for section in groupDb:
                groupUserList.append(section.val()['groupUsers'])

        #creates member list
        memList1, memList2, memList3= "", "", ""
        for i in range(len(groupUserList)):
            for j in range(1, len(groupUserList[i])):
                if i == 0:
                    memList1 += "[ " + groupUserList[i][j]['email'] + " ]     Assigned: " + \
                                str(groupUserList[i][j]['taskAssign']) + " // Completed: " + \
                                str(groupUserList[i][j]['taskComplete']) + "\n"
                elif i == 1:
                    memList2 += "[ " + groupUserList[i][j]['email'] + " ]     Assigned: " + \
                                str(groupUserList[i][j]['taskAssign']) + " // Completed: " + \
                                str(groupUserList[i][j]['taskComplete']) + "\n"
                elif i == 2:
                    memList3 += "[ " + groupUserList[i][j]['email'] + " ]     Assigned: " + \
                                str(groupUserList[i][j]['taskAssign']) + " // Completed: " + \
                                str(groupUserList[i][j]['taskComplete']) + "\n"

        # Update Labels
        if len(groupNameList) >= 1:
            self.titleLabel1.text = "Assign Score to Group: " + groupNameList[0]
            self.detailLbl1.text = memList1

        if len(groupNameList) >= 2:
            self.titleLabel2.text = "Assign Score to Group: " + groupNameList[1]
            self.detailLbl2.text = memList2

        if len(groupNameList) >= 3:
            self.titleLabel3.text = "Assign Score to Group: " + groupNameList[2]
            self.detailLbl3.text = memList3

    def assign_score(self, btnNum):
        email = "jin@aol.com"
        db = firebase.database()

        groupKeyList, groupNameList = [], []

        # finds all assignVIP for email, only looks at where ticket = 0
        groupReqDb = db.child('assignVIP').order_by_child('email').equal_to(email).get()
        for sector in groupReqDb:
            if sector.val()['ticket'] == 0:
                groupKeyList.append(sector.key())
                groupNameList.append(sector.val()['groupname assigned'])


        if btnNum == 1:
            if self.inpScore1.text == "":
                show_popup("Error", "Enter a score")
                return
            scoreAssigned = self.inpScore1.text
            self.btnAce1.disabled = True
            self.inpScore1.disabled = True

        if btnNum == 2:
            if self.inpScore2.text == "":
                show_popup("Error", "Enter a score")
                return
            scoreAssigned = self.inpScore2.text
            self.btnAce2.disabled = True
            self.inpScore2.disabled = True

        if btnNum == 3:
            if self.inpScore3.text == "":
                show_popup("Error", "Enter a score")
                return
            scoreAssigned = self.inpScore3.text
            self.btnAce3.disabled = True
            self.inpScore3.disabled = True

        if btnNum > len(groupKeyList):
            show_popup("Error", "No Request Found")
            return

        db.child('assignVIP').child(groupKeyList[btnNum - 1]).update({"ticket": 1, "point": int(scoreAssigned)})

        self.apply_score(groupNameList[btnNum - 1], scoreAssigned)

    def apply_score(self, groupName, score):
        db = firebase.database()

        groupUserList, pointsList = [], []
        groupUser = {}

        #find group members
        groupDb = db.child('group').order_by_child('groupName').equal_to(groupName).get()
        for section in groupDb:
            groupUser = section.val()['groupUsers']

        #find all members in user table
        for i in range(1, len(groupUser)):
            userDb = db.child('users').order_by_child('email').equal_to(groupUser[i]['email']).get()
            for sect in userDb:
                groupUserList.append(sect.key())
                pointsList.append(sect.val()['points'])

        #change member's scores
        for i in range(len(groupUserList)):
            db.child('users').child(groupUserList[i]).update({"points": int(pointsList[i])+int(score)})

