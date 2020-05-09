from signingDetails import *
from otherWindows import *
from kivy.graphics.vertex_instructions import Rectangle



class GroupWindow(Screen):

    def on_start(self, *args): #change to on_enter later
        email = 'jin@aol.com'
        groupId = 1
        pollId = 1
        taskId = 4


        #specify group to pull info from
        info = db.child("group").order_by_child("groupId").equal_to(groupId).get()
        for sections in info.each():
            group_desc = sections.val()['groupDesc']
            groupName = sections.val()['groupName']
            groupUsers = sections.val()['groupUsers']

        self.groupDesc.text = "Group Name: " + groupName + "\nDescription: " + group_desc

        for i in range(1, len(groupUsers)):
            userAs = groupUsers[i]['taskAssign']
            userCo = groupUsers[i]['taskComplete']
            if i == 1:
                self.user1_info.text = "Assigned: " + str(userAs) + "\nCompleted: " + str(userCo)
            elif i == 2:
                self.user2_info.text = "Assigned: " + str(userAs) + "\nCompleted: " + str(userCo)
            elif i == 3:
                self.user3_info.text = "Assigned: " + str(userAs) + "\nCompleted: " + str(userCo)
            elif i == 4 :
                self.user4_info.text = "Assigned: " + str(userAs) + "\nCompleted: " + str(userCo)
            elif i == 5:
                self.user5_info.text = "Assigned: " + str(userAs) + "\nCompleted: " + str(userCo)

        groupPostTasks = []
        groupPostPolls = []
        postDb = db.child("posts").order_by_child("groupId").equal_to(groupId).get()
        for sect in postDb.each():
            if sect.val()['postType'] == 'Task':
                groupPostTasks.append(sect.val())
            if sect.val()['postType'] == 'Poll':
                groupPostPolls.append(sect.val())

        pollVoted1 = groupPostPolls[0]['postVoted'].split(',')

        self.postTask1.text = "Function Name: " + groupPostTasks[0]['postContent'] + "\nDetails:                          "
        self.postPoll1.text = "Poll: " + groupPostPolls[0]['postContent']
        self.postPollVote1.text = "[ " + str(len(pollVoted1)) + "/5 members have voted ] "
        self.btnPoll1.text = groupPostPolls[0]['option1']['content']
        self.btnPoll2.text = groupPostPolls[0]['option2']['content']

    def create_post_task(self, postContent, taskId):
        email = 'jin@aol.com'
        groupId = 1
        lastPostX = 190

        with self.canvas:
            Color(.2, .5, .4, 1)  # set the colour
            # Seting the size and position of canvas
            self.rect = Rectangle(pos = (20, lastPostX-100),
                                  size = (500, 80))

        self.add_widget(
            Label(
                text = "Task: " + postContent,
                size_hint = (.5, .5),
                pos_hint = {"center_y": .24, "center_x": .215},
                id ='postTask2'
            )
        )

        btnClaim2 = Button(
                text = "Claim",
                size_hint =(0.07, 0.07),
                pos_hint ={"x": .57, "y": .18},
                background_color = (.2, .5, .4, 1),
                disabled = False,
                id ='btnClaim2',
                on_press = lambda *args: self.task_claim(email, groupId, taskId, 2)
        )
        btnClaim2.bind(on_release=partial(self.foo, btnClaim2))
        self.add_widget(btnClaim2)

    def create_post_poll(self, postContent, option1, option2, pollId):
        email = 'jin@aol.com'
        groupId = 1
        lastPostX = 190

        with self.canvas:
            Color(.2, .5, .4, 1)  # set the colour
            # Seting the size and position of canvas
            self.rect = Rectangle(pos = (20, lastPostX-150),
                                  size = (500, 130))

        self.add_widget(
            Label(
                text = "Task: " + postContent,
                size_hint = (.5, .5),
                pos_hint = {"center_y": .25, "center_x": .215},
                id ='postTask2'
            )
        )

        self.add_widget(
            Label(
                text="[ 0/5 members have voted ]",
                color= (0.5, 0.8, 0.6, 1),
                pos_hint={"center_y": .22, "center_x": .215},
                id='postTask2'
            )
        )

        btnOpt1 = Button(
                    text = option1,
                    background_color = (.2, .5, .4, 1),
                    disabled = False,
                    size_hint=(0.295, 0.1),
                    pos_hint={"top": .18, "x": 0.036}
                    #on_press = root.poll_vote('chungha@aol.com', 5, 1, 1)
                    )
        btnOpt2 = Button(
                    text= option2,
                    background_color=(.2, .5, .4, 1),
                    disabled=False,
                    size_hint=(0.295, 0.1),
                    pos_hint={"top": .18, "x": 0.342}
                    # on_press = root.poll_vote('chungha@aol.com', 5, 1, 1)
                    )

        btnOpt1.bind(on_release=partial(self.foo, btnOpt1))
        btnOpt1.bind(on_release=partial(self.foo, btnOpt2))
        btnOpt2.bind(on_release=partial(self.foo, btnOpt1))
        btnOpt2.bind(on_release=partial(self.foo, btnOpt2))

        self.add_widget(btnOpt1)
        self.add_widget(btnOpt2)

    def foo(self, instance, *args):
        instance.disabled = True

    #make sure to add pollType
    def create_post(self, postType, groupId):

        if self.postContent.text.replace(" ", "") == "":
            show_popup("Group Post", "Cannot have empty post")
            return

        if postType == "Task":
            taskIdList = []
            postDb = db.child("posts").order_by_child("groupId").equal_to(groupId).get()
            for sector in postDb.each():
                if 'Task' == sector.val()['postType']:
                    postsInfo = sector.val()['taskId']
                    taskIdList.append(postsInfo)
            taskId = max(taskIdList) + 1

            data = {
                "groupId": groupId,
                "postContent": self.postContent.text,
                "claimBy": 999,
                "taskId": taskId,
                "postType": postType
            }

            self.create_post_task(self.postContent.text, taskId)

        if postType == "Poll":
            pollIdList = []
            postDb = db.child("posts").order_by_child("groupId").equal_to(groupId).get()
            for sect in postDb.each():
                pollInfo = sect.val()['postId']
                pollIdList.append(pollInfo)
            pollId = max(pollIdList) + 1

            popup = PopupWindow(title="Enter a deadline for the poll MM/DD/YYYY")
            popup.open()
            popup = PopupWindow(title="Enter two options for the poll, separated by a comma. EX: 12:45PM, 3:45PM")
            popup.open()
            data = {
                "groupId": groupId,
                "postContent": self.postContent.text,
                "postDeadline": "05/14/2020",
                "pollId": pollId,
                "postVoted": "",
                "postType": postType,
                "option1": {
                    "content": "text",
                    "vote": 0
                },
                "option2": {
                    "content": "text",
                    "vote": 0
                }
            }
            #have pop up specify deadline AND the options

        db.child("posts").push(data)
        show_popup("Group Post", "Posted!")
        self.postContent.text = ""

    def remove_group(self, groupId):
        groupId = 5

        firebase = pyrebase.initialize_app(config)
        db = firebase.database()
        groupDb = db.child("group").order_by_child("groupId").equal_to(groupId).get()
        for sect in groupDb.each():
            groupKey = sect.key()

        db.child("group").child(groupKey).remove()

    def remove_group_user(self, email, groupId):
        groupId = 5

        groupDb = db.child("group").order_by_child("groupId").equal_to(groupId).get()
        for sect in groupDb.each():
            groupKey = sect.key()
        for sections in groupDb.each():
            groupUsers = sections.val()['groupUsers']
        for i in range(1, len(groupUsers)):
            if email in groupUsers[i].values():
                db.child("group").child(groupKey).child("groupUsers").child(i).remove()
                break

    def task_claim(self, email, groupId, taskId, btnClaimNum):
        groupId = 1
        #email = ""
        #when user clicks claim button send postContent to user's request page

        if btnClaimNum == 1:
            self.btnClaim.disabled = 'True'

        groupDb = db.child("group").order_by_child("groupId").equal_to(groupId).get()
        for sect in groupDb.each():
            groupKey = sect.key()
        for sections in groupDb.each():
            groupUsers = sections.val()['groupUsers']
        for i in range(1, len(groupUsers)):
            if email in groupUsers[i].values():
                taskFound = groupUsers[i]['taskAssign'] + 1
                db.child("group").child(groupKey).child("groupUsers").child(i)\
                    .update({"taskAssign": taskFound})

        postDb = db.child("posts").order_by_child("groupId").equal_to(groupId).get()
        for sect in postDb.each():
            if 'Task' == sect.val()['postType']:
                if 999 == sect.val()['claimBy'] and taskId == sect.val()['taskId']:
                    postKey = sect.key()
                    db.child("posts").child(postKey).update({"claimBy": email})

    def task_complete(self, email, groupId, taskId):
        #when user clicks compelte from their request page

        taskId = 1
        groupId = 5

        groupDb = db.child("group").order_by_child("groupId").equal_to(groupId).get()
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

        postDb = db.child("posts").order_by_child("groupId").equal_to(groupId).get()

        for sect in postDb.each():
            if email == sect.val()['claimBy'] and taskId == sect.val()['taskId']:
                postKey = sect.key()
                print(postKey)
                db.child("posts").child(postKey).remove()
                db.child("group").child(groupKey).child("groupUsers").child(i) \
                    .update({"taskAssign": taskFound, "taskComplete": taskComplete})
            else:
                print("No Post Found")

    def poll_vote(self, email, groupId, pollId, optionNum):
        email = 'jihyo@aol.com'
        groupId = 2
        pollId = 1

        #user clicks option
        firebase = pyrebase.initialize_app(config)
        db = firebase.database()
        postDb = db.child("posts").order_by_child("groupId").equal_to(groupId).get()
        for sect in postDb.each():
            if sect.val()['pollId'] == pollId:
                postInfo = sect.val()
                postKey = sect.key()
                option1Count = sect.val()['option1']['vote'] + 1
                option1Content = sect.val()['option1']['content']
                option2Count = sect.val()['option2']['vote'] + 1
                option2Content = sect.val()['option2']['content']

        votedMems = postInfo['postVoted'] + ", " + email

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
        self.btnPoll1.disabled = 'True'
        self.btnPoll2.disabled = 'True'

        #if everyone voted, delete post and send notifications to everyone


class CreateGroupWindow(Screen):

    def create_group(self):

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
                    "email": groupUsers[0],
                    "taskAssign": 0,
                    "taskComplete": 0
                },
                "2": {
                    "email": groupUsers[1],
                    "taskAssign": 0,
                    "taskComplete": 0
                },
                "3": {
                    "email": groupUsers[2],
                    "taskAssign": 0,
                    "taskComplete": 0
                },
                "4": {
                    "email": groupUsers[3],
                    "taskAssign": 0,
                    "taskComplete": 0
                },
                "5": {
                    "email": groupUsers[4],
                    "taskAssign": 0,
                    "taskComplete": 0
                }
            }
        }

        checkEmailCount = 0
        for i in range(len(groupUsers)):
            if check_email_format(groupUsers[i]) == True:
                checkEmailCount += 1

        if checkEmailCount == len(groupUsers):
            db.child("group").push(data)
            show_popup("Submit", "Group Created!")
            self.groupName.text = ""
            self.groupDesc.text = ""
            self.userList.text = ""
        else:
            show_popup("Error", "An error occurred")



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
