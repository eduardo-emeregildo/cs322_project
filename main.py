from kivy.app import App
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.graphics.context_instructions import Color
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
import pyrebase
import requests
import re

# to connect to firebase
config = {
    "apiKey": "AIzaSyA3jmvr2W79q49qKP3-Meya2U6yMb9Prtk",
    "authDomain": "csc322-project.firebaseapp.com",
    "databaseURL": "https://csc322-project.firebaseio.com",
    "projectId": "csc322-project",
    "storageBucket": "csc322-project.appspot.com",
    "messagingSenderId": "1010821296449",
    "appId": "1:1010821296449:web:3bb6c7c6fd51f0024631c0",
    "measurementId": "G-B97101DQ0C"
}


# for when person is signing up
def check_email_format(email):
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if (re.search(regex, email)):
        return True
    else:
        return False


# title of the popup and what you want the label to say are input
def show_popup(title_popup, text_label):
    layout = FloatLayout()
    label = Label(text=text_label, size_hint=(0.6, 0.2), pos_hint={"x": 0.2, "top": 1})
    layout.add_widget(label)
    button = Button(text="close", size_hint=(0.8, 0.1), pos_hint={"x": 0.1, "y": 0.1})
    layout.add_widget(button)
    popup = Popup(title=title_popup, content=layout, size_hint=(None, None), size=(400, 400), auto_dismiss=False)
    button.bind(on_press=popup.dismiss)
    popup.open()


class HomeWindow(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def log_in(self):

        firebase = pyrebase.initialize_app(config)
        auth = firebase.auth()
        try:
            auth.sign_in_with_email_and_password(self.email.text, self.password.text)
            self.parent.current = "homeOU"  # how you switch screens in python code

        except:
            show_popup("Error", "wrong combination of email and password")
        self.email.text = ""
        self.password.text = ""

    def check_user(self):
        firebase = pyrebase.initialize_app(config)
        db = firebase.database()
        user = db.child("users").order_by_child("email").equal_to("ggukr@aol.com").limit_to_first(1).get()
        try:
            for emailed in user.each():
                print(emailed.val()['email'])
                if emailed.val()['email'] is not "":
                    print("User Exists")
                    return True
        except Exception:
            print("User DNE")
            return False


class SignupWindow(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)
    dob = ObjectProperty(None)
    interests = ObjectProperty(None)
    prev_projects = ObjectProperty(None)

    def sign_up(self):
        priv = 0
        data = {
            "email": self.email.text,
            "password": self.password.text,
            "priviledge": priv,
            "date of birth": self.dob.text,
            "interests": self.interests.text,
            "previous projects": self.prev_projects.text
        }
        firebase = pyrebase.initialize_app(config)
        db = firebase.database()

        if (check_email_format(self.email.text) == True) and (len(self.password.text) >= 6):
            db.child("pending_users").push(data)
            show_popup("Submit", "Application received")
            self.email.text = ""
            self.password.text = ""
            self.dob.text = ""
            self.interests.text = ""
            self.prev_projects.text = ""

        else:
            show_popup("Reject", "An error occurred")


class NotificationPage(Screen):
    pass


class DescriptionWindow(Screen):
    pass


class PopupWindow(Popup):
    input_text = ObjectProperty()

    def __init__(self, text='', **kwargs):
        super(PopupWindow, self).__init__(**kwargs)
        self.input_text.text = text
        self.auto_dismiss = False

    def Cancel(self):
        self.dismiss()


class ComplimentPage(Screen):
    def show_popup(self):
        popup = PopupWindow(title="Increase Reputation Score")
        popup.open()


class WarningPage(Screen):
    def show_popup(self):
        popup = PopupWindow(title="Decrease Reputation Score")
        popup.open()


class GroupNotificationSU(Screen):
    pass


class GroupWindow(Screen):

    def show_info(self, *args): #change to on_enter later
        firebase = pyrebase.initialize_app(config)
        db = firebase.database()

        #specify group to pull info from
        info = db.child("group").order_by_child("groupId").equal_to(3).get()
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
            elif i == 4:
                self.user4_info.text = "Assigned: " + str(userAs) + "\nCompleted: " + str(userCo)
            elif i == 5:
                self.user5_info.text = "Assigned: " + str(userAs) + "\nCompleted: " + str(userCo)

    def create_post(self, postType):

        if self.postContent.text.replace(" ", "") == "":
            show_popup("Group Post", "Cannot have empty post")
            return

        if postType == "Task":
            data = {
                "groupId": 999,
                "postContent": self.postContent.text,
                "postType": postType,
                "claimBy": 999
            }

        if postType == "Poll":
            popup = PopupWindow(title="Enter a deadline for the poll MM/DD/YYYY")
            popup.open()
            data = {
                "groupId": 999,
                "postContent": self.postContent.text,
                "postType": postType,
                "postDeadline": "05/14/2020",
                "pollOptions": 3
            }
            #have pop up specify deadline AND the options

        else:
            firebase = pyrebase.initialize_app(config)
            db = firebase.database()
            db.child("posts").push(data)
            show_popup("Group Post", "Posted!")
            self.postContent.text = ""

        #Shows post on page

    def remove_group(self):
        firebase = pyrebase.initialize_app(config)
        db = firebase.database()
        groupDb = db.child("group").order_by_child("groupId").equal_to(4).get()
        for sect in groupDb.each():
            groupKey = sect.key()

        db.child("group").child(groupKey).remove()

    def remove_group_user(self, email):
        firebase = pyrebase.initialize_app(config)
        db = firebase.database()
        groupDb = db.child("group").order_by_child("groupId").equal_to(5).get()
        for sect in groupDb.each():
            groupKey = sect.key()
        for sections in groupDb.each():
            groupUsers = sections.val()['groupUsers']
        for i in range(1, len(groupUsers)):
            if email in groupUsers[i].values():
                db.child("group").child(groupKey).child("groupUsers").child(i).remove()
                break

    def task_claim(self, email):
        #when user clicks claim button send postContent to user's request page
        #DB updates with post 'claimBy'
        firebase = pyrebase.initialize_app(config)
        db = firebase.database()
        groupDb = db.child("group").order_by_child("groupId").equal_to(5).get()
        for sect in groupDb.each():
            groupKey = sect.key()
        for sections in groupDb.each():
            groupUsers = sections.val()['groupUsers']
        for i in range(1, len(groupUsers)):
            if email in groupUsers[i].values():
                taskFound = groupUsers[i]['taskAssign'] + 1
                db.child("group").child(groupKey).child("groupUsers").child(i)\
                    .update({"taskAssign": taskFound})

        #DB also updates user's taskAssign


class CreateGroupWindow(Screen):
    def create_group(self):
        firebase = pyrebase.initialize_app(config)
        db = firebase.database()

        groupTotal = 1
        groupDb = db.child("group").get()
        for sect in groupDb.each():
            if sect is not "":
                groupTotal += 1

        groupUsers = self.userList.text.replace(" ", "").split(',')

        data = {  # change to +ref.generate_key()
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


class HomeOUWindow(Screen):
    pass


class ProfileWindow(Screen):
    pass


kv = Builder.load_file("main.kv")

class MyMainApp(App):
    def build(self):
        return kv


if __name__ == "__main__":
    MyMainApp().run()
