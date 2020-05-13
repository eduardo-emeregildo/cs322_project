from signingDetails import *
from otherWindows import *
from kivy.graphics.vertex_instructions import Rectangle


def remove_group(groupId):
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    groupDb = db.child("group").order_by_child("groupId").equal_to(groupId).get()
    for sect in groupDb.each():
        groupKey = sect.key()

    db.child("group").child(groupKey).remove()

def remove_group_user(email, groupId):
    groupDb = db.child("group").order_by_child("groupId").equal_to(groupId).get()
    for sect in groupDb:
        groupKey = sect.key()
        groupUsers = sect.val()['groupUsers']

    for i in range(1, len(groupUsers)):
        if email in groupUsers[i].values():
            db.child("group").child(groupKey).child("groupUsers").child(i).remove()
            break

# specifcally groupKick DB
def kick_vote_table(groupId, kickType, kickUser):
    db = firebase.database()
    groupKickKey = ""

    # checks if kick request is already in DB
    groupKick = db.child('groupKick').order_by_child('groupId').equal_to(groupId).get()
    for section in groupKick:
        if kickType == 'Group':
            if section.val()['kickType'] == 'Group':
                print("Request already exists")
                return
        elif kickType == 'Member':
            if section.val()['groupUser'] == kickUser:
                print("Request already exists")
                return

    groupDb = db.child('group').order_by_child('groupId').equal_to(groupId).get()
    for sect in groupDb:
        groupUsers = sect.val()['groupUsers']

    if kickType == 'Member':
        kickVotes = len(groupUsers) - 2
    if kickType == 'Group':
        kickVotes = len(groupUsers) - 1

    data = {
        "groupId": groupId,
        "groupUser": kickUser,
        "kickType": kickType,
        "accept": 0,
        "reject": 0,
        "votes": kickVotes
    }

    db.child('groupKick').push(data)

    # sends request to every user in group
    for i in range(1, len(groupUsers)):
        if kickType == 'Group':
            kick_req(groupUsers[i]['email'], groupId, kickType, "")
        elif kickType == 'Member':
            if groupUsers[i]['email'] != kickUser:
                kick_req(groupUsers[i]['email'], groupId, kickType, kickUser)

# connect requests to group page
# specifically groupRequest DB
def kick_req(email, groupId, notifType, notifUser):
    db = firebase.database()
    #notifType = "Join"
    groupReqKey = ""

    # checks if user already has groupRequest table
    while (groupReqKey == ""):
        groupRequests = db.child('groupRequests').order_by_child('email').equal_to(email).get()
        for section in groupRequests:
            if section.val()['email'] == email:
                groupReqKey = section.key()
                break

        # if no, makes new one
        if (groupReqKey) == "":
            data = {
                "email": email,
                "notifications": ""
            }
            db.child('groupRequests').push(data)

    # pushes data accordingly
    if notifType == 'Member':
        notifData = {
            "groupId": groupId,
            "notifType": "Member",
            "notifUser": notifUser
        }

    elif notifType == 'Group':
        notifData = {
            "groupId": groupId,
            "notifType": "Group"
        }

    elif notifType == 'Join':
        notifData = {
            "groupId": groupId,
            "notifType": "Join"
        }
    else:
        return

    if groupReqKey.replace(" ", "") is not "":
        db.child('groupRequests').child(groupReqKey).child('notifications').push(notifData)

class GroupWindow(Screen):
    groupId = 2
    pollId = 1
    taskId = 4

    def on_pre_enter(self, *args):
        db = firebase.database()

        # self.groupDesc.text = "Group Name: " + groupName + "\nDescription: " + group_desc
        # get self.groupDesc.text and find group ID that way and assign it above ;;

        # specify group to pull info from
        info = db.child("group").order_by_child("groupName").equal_to(self.groupDesc.text).get()
        for sections in info.each():
            group_desc = sections.val()['groupDesc']
            groupIdHere = sections.val()['groupId']
            groupUsers = sections.val()['groupUsers']

        if groupIdHere is not self.groupId:
            self.btnClaim.disabled = False
            self.btnPoll1.disabled = False
            self.btnPoll2.disabled = False
            GroupWindow.groupId = groupIdHere

        self.groupDesc2.text = group_desc

        for i in range(1, len(groupUsers)):
            userAs = groupUsers[i]['taskAssign']
            userCo = groupUsers[i]['taskComplete']
            if i == 1:
                self.user1_info.text = "Assigned: " + str(userAs) + "\nCompleted: " + str(userCo)
            elif i == 2:
                self.user2_info.text = "Assigned: " + str(userAs) + "\nCompleted: " + str(userCo)
            elif i == 3:
                self.user3_info.text = "Assigned: " + str(userAs) + "\nCompleted: " + str(userCo)
            elif i == 4:

                self.user4_info.text = "Assigned: " + str(userAs) + "\nCompleted: " + str(userCo)
            elif i == 5:
                self.user5_info.text = "Assigned: " + str(userAs) + "\nCompleted: " + str(userCo)

        groupPostTasks = []
        groupPostPolls = []
        postDb = db.child("posts").order_by_child("groupId").equal_to(self.groupId).get()
        for sect in postDb:
            if sect.val()['postType'] == 'Task':
                if sect.val()['claimBy'] == 999:
                    groupPostTasks.append(sect.val())
            if sect.val()['postType'] == 'Poll':
                groupPostPolls.append(sect.val())

        print(groupPostTasks)
        print(groupPostPolls)

        try:
            if groupPostPolls[0]['postVoted'] == "":
                pollVoted1 = []
            else:
                pollVoted1 = groupPostPolls[0]['postVoted'].split(',')

            GroupWindow.pollId = groupPostPolls[0]['pollId']

            self.postPoll1.text = "Poll: " + groupPostPolls[0]['postContent']
            self.postPollVote1.text = "[ " + str(len(pollVoted1)) + "/5 members have voted ] "
            self.btnPoll1.text = groupPostPolls[0]['option1']['content']
            self.btnPoll2.text = groupPostPolls[0]['option2']['content']
        
        except Exception:
            pass

        try:
            GroupWindow.taskId = groupPostTasks[0]['taskId']
            self.postTask1.text = "Function Name: " + groupPostTasks[0]['postContent']

        except Exception:
            pass

    def on_leave(self):
        self.postTask1.text = "No Task to Display "
        self.postPoll1.text = "No Post to Display "
        self.postPollVote1.text = "[ 0/5 members have voted ] "
        self.btnPoll1.text = "Option 1"
        self.btnPoll2.text = "Option 2"

    def req_kick(self, btnNum, kickType):
        db = firebase.database()

        if kickType == 'Member':
            info = db.child("group").order_by_child("groupId").equal_to(self.groupId).get()
            for sections in info.each():
                groupUsers = sections.val()['groupUsers']

            kick_vote_table(self.groupId, kickType, groupUsers[btnNum]['email'])

        elif kickType == 'Group':
            kick_vote_table(self.groupId, kickType, "")

    def create_post_task(self, postContent, taskId):

        lastPostX = 190

        with self.canvas:
            Color(.2, .5, .4, 1)  # set the colour
            # Seting the size and position of canvas
            self.rect = Rectangle(pos=(20, lastPostX - 100), size=(500, 80))
        self.add_widget(
            Label(
                text="Task: " + postContent,
                size_hint=(.5, .5),
                pos_hint={"center_y": .22, "center_x": .315},
                id='postTask2'
            )
        )

        btnClaim2 = Button(
            text="Claim",
            size_hint=(0.07, 0.07),
            pos_hint={"x": .57, "y": .18},
            background_color=(.2, .5, .4, 1),
            disabled=False,
            id='btnClaim2',
            on_press=lambda *args: self.task_claim(2, taskId)
        )
        btnClaim2.bind(on_release=partial(self.foo, btnClaim2))
        self.add_widget(btnClaim2)

    def create_post_poll(self, postContent, option1, option2, pollId):
        lastPostX = 190

        with self.canvas:
            Color(.2, .5, .4, 1)  # set the colour
            # Seting the size and position of canvas

            self.rect = Rectangle(pos=(20, lastPostX - 150),
                                  size=(500, 130))

        self.add_widget(
            Label(
                text="Poll: " + postContent,
                size_hint=(.5, .5),
                pos_hint={"center_y": .25, "center_x": .330},
                id='postTask2'
            )
        )

        self.add_widget(
            Label(
                text="[ 0/5 members have voted ]",
                color=(0.5, 0.8, 0.6, 1),
                pos_hint={"center_y": .22, "center_x": .215},
                id='postTask2'
            )
        )

        btnOpt1 = Button(
            text=option1,
            background_color=(.2, .5, .4, 1),
            disabled=False,
            size_hint=(0.295, 0.1),
            pos_hint={"top": .18, "x": 0.036},
            on_press=lambda *args: self.poll_vote(1, 2, pollId)
        )
        btnOpt2 = Button(
            text=option2,
            background_color=(.2, .5, .4, 1),
            disabled=False,
            size_hint=(0.295, 0.1),
            pos_hint={"top": .18, "x": 0.342},
            on_press=lambda *args: self.poll_vote(2, 2, pollId)
        )


        btnOpt1.bind(on_release=partial(self.foo, btnOpt1))
        btnOpt1.bind(on_release=partial(self.foo, btnOpt2))
        btnOpt2.bind(on_release=partial(self.foo, btnOpt1))
        btnOpt2.bind(on_release=partial(self.foo, btnOpt2))

        self.add_widget(btnOpt1)
        self.add_widget(btnOpt2)

    def foo(self, instance, *args):
        instance.disabled = True

    def create_post(self, postType):

        if self.taskInDetail.text.replace(" ", "") == "" or self.taskInTitle.text.replace(" ", "") == "":
            show_popup("Group Post", "Cannot have empty post")
            return

        db = firebase.database()

        if postType == "Task":

            taskContent = self.taskInTitle.text + ": \n" + self.taskInDetail.text
            taskIdList = []
            postDb = db.child("posts").order_by_child("groupId").equal_to(self.groupId).get()
            for sector in postDb.each():
                if 'Task' == sector.val()['postType']:
                    postsInfo = sector.val()['taskId']
                    taskIdList.append(postsInfo)

            try:
                taskId = max(taskIdList) + 1
            except Exception:
                taskId = 1

            data = {
                "groupId": self.groupId,
                "postContent": taskContent,
                "claimBy": 999,
                "taskId": taskId,
                "postType": postType
            }

            self.create_post_task(taskContent, taskId)

        if postType == "Poll":

            pollOptions = self.taskInDetail.text.split(',')

            pollIdList = []
            postDb = db.child("posts").order_by_child("groupId").equal_to(self.groupId).get()
            for sect in postDb.each():
                if 'Poll' == sect.val()['postType']:
                    pollInfo = sect.val()['pollId']
                    pollIdList.append(pollInfo)
            try:
                pollId = max(pollIdList) + 1
            except Exception:
                pollId = 1


            data = {
                "groupId": self.groupId,
                "postContent": self.taskInTitle.text,
                "postDeadline": "05/13/20",
                "pollId": pollId,
                "postVoted": "",
                "postType": postType,
                "option1": {
                    "content": pollOptions[0],
                    "vote": 0
                },
                "option2": {
                    "content": pollOptions[1],
                    "vote": 0
                }
            }

            self.create_post_poll(self.taskInTitle.text, pollOptions[0], pollOptions[1], pollId)

        db.child("posts").push(data)
        show_popup("Group Post", "Posted!")
        self.taskInDetail.text = ""
        self.taskInTitle.text = ""

    def task_claim(self, btnClaimNum, taskId):
        email = Store.email
        # when user clicks claim button send postContent to user's request page

        if btnClaimNum == 1:
            self.btnClaim.disabled = True
            taskUsed = self.taskId
        if btnClaimNum == 2:
            taskUsed = taskId

        db = firebase.database()
        groupDb = db.child("group").order_by_child("groupId").equal_to(self.groupId).get()
        for sect in groupDb.each():
            groupKey = sect.key()
        for sections in groupDb.each():
            groupUsers = sections.val()['groupUsers']
        for i in range(1, len(groupUsers)):
            if email in groupUsers[i].values():
                taskFound = groupUsers[i]['taskAssign'] + 1
                db.child("group").child(groupKey).child("groupUsers").child(i) \
                    .update({"taskAssign": taskFound})

        postDb = db.child("posts").order_by_child("groupId").equal_to(self.groupId).get()
        for sect in postDb.each():
            if 'Task' == sect.val()['postType']:
                if 999 == sect.val()['claimBy'] and taskUsed == sect.val()['taskId']:
                    postKey = sect.key()
                    db.child("posts").child(postKey).update({"claimBy": email})

    def poll_vote(self, optionNum, btnClaim, pollId):
        email = Store.email
        postInfo, votedMems = "", ""
        option1Count, option1Content, option2Count, option2Content = 0, 0, 0, 0

        if btnClaim == 1:
            pollUsed = self.pollId
            self.btnPoll1.disabled = True
            self.btnPoll2.disabled = True
        elif btnClaim == 2:
            pollUsed = pollId


        # user clicks option
        db = firebase.database()
        postDb = db.child("posts").order_by_child("groupId").equal_to(self.groupId).get()
        for sect in postDb.each():
            if sect.val()['postType'] == 'Poll':
                if sect.val()['pollId'] == pollUsed:
                    postInfo = sect.val()
                    postKey = sect.key()
                    option1Count = sect.val()['option1']['vote'] + 1
                    option1Content = sect.val()['option1']['content']
                    option2Count = sect.val()['option2']['vote'] + 1
                    option2Content = sect.val()['option2']['content']
                    if postInfo['postVoted'] == "":
                        votedMems = email
                    else:
                        votedMems = postInfo['postVoted'] + ", " + email

        if postInfo is not "":
            if optionNum == 1:
                data = {
                    "postVoted": votedMems,
                    "option1": {
                        "vote": option1Count,
                        "content": option1Content
                    }
                }
            else:
                data = {
                    "postVoted": votedMems,
                    "option2": {
                        "vote": option2Count,
                        "content": option2Content
                    }
                }

            db.child("posts").child(postKey).update(data)


        # if everyone voted, delete post and send notifications to everyone

    def show_inputs(self, postType):
        if postType == 'Poll':
            self.btnChooseInputs.opacity = 1
            self.btnCreatePoll.opacity = 1

            self.taskInTitle.disabled = False
            self.taskInDetail.disabled = False

            self.taskInTitle.hint_text = "Poll Description"
            self.taskInDetail.hint_text = "Write two options separated by comma EX: 12:30, 5:00"

            self.btnPollInputs.disabled = True
            self.btnTaskInputs.disabled = True

        elif postType == 'Task':
            self.btnChooseInputs.opacity = 1
            self.btnCreateTask.opacity = 1

            self.taskInTitle.disabled = False
            self.taskInDetail.disabled = False

            self.taskInTitle.hint_text = "Task Title"
            self.taskInDetail.hint_text = "Task Description"

            self.btnPollInputs.disabled = True
            self.btnTaskInputs.disabled = True

        elif postType == 'Back':
            self.inputsChoose.opacity = 1
            self.btnChooseInputs.opacity = 0
            self.btnCreatePoll.opacity = 0
            self.btnCreateTask.opacity = 0

            self.taskInTitle.disabled = True
            self.taskInDetail.disabled = True

            self.taskInTitle.hint_text = "Choose Poll to create a poll post"
            self.taskInDetail.hint_text = "Choose Task to create a task post"

            self.btnPollInputs.disabled = False
            self.btnTaskInputs.disabled = False

    def get_popup(self):
        group_popup()


class CreateGroupWindow(Screen):

    def create_group(self):
        db = firebase.database()

        if self.userList.text.replace(" ", "") == "" or self.groupName.text.replace(" ",
                                                                                    "") == "" or self.groupDesc.text.replace(
                " ", "") == "" or self.projName.text.replace(" ", "") == "":
            show_popup("Error", "Fields cannot be empty")
            return

        groupList = []
        groupDb = db.child("group").get()
        for sect in groupDb.each():
            groupInfo = sect.val()['groupId']
            groupList.append(groupInfo)
        groupTotal = max(groupList) + 1

        groupUsers = self.userList.text.replace(" ", "").split(',')

        data = {
            "groupName": self.groupName.text,
            "groupId": groupTotal,
            "groupDesc": self.groupDesc.text,
            "groupUsers": {
                "1": {
                    "email": Store.email,
                    "taskAssign": 0,
                    "taskComplete": 0
                },
                "2": {

                    "email": groupUsers[0],
                    "taskAssign": -1,
                    "taskComplete": -1
                },
                "3": {

                    "email": groupUsers[1],
                    "taskAssign": -1,
                    "taskComplete": -1
                },
                "4": {

                    "email": groupUsers[2],
                    "taskAssign": -1,
                    "taskComplete": -1
                },
                "5": {
                    "email": groupUsers[3],
                    "taskAssign": -1,
                    "taskComplete": -1
                }
            }
        }

        db.child("group").push(data)

        members = {Store.email, groupUsers[0], groupUsers[1], groupUsers[2], groupUsers[3]}
        add_projects(self.groupName.text, self.projName.text, self.groupDesc.text, members)

        for i in range(len(groupUsers)):
            kick_req(groupUsers[i], groupTotal, 'Join', "")

        show_popup("Submit", "Group Created!")
        self.groupName.text = ""
        self.groupDesc.text = ""
        self.userList.text = ""
        self.projName.text = ""


#add_projects( "Group8", "Lighthouse", "to motivate people", {"eduardo@gmail.com", "me1@gmail.com", "idk@gmail.com", "boi@gmail.com"})

# popup function
    def validate(self):

        if self.groupName.text == "":
            show_popup("Error", "Please include the group name")

        elif self.groupDesc.text == "":
            show_popup("Error", "Add group description")

        elif self.userList.text == "":
            show_popup("Error", "No users added")
        
        else:
            self.create_group()


