from functools import partial
from kivy.app import App
from kivy.graphics.vertex_instructions import Rectangle
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.graphics.context_instructions import Color
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty,StringProperty,NumericProperty,DictProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
import smtplib #emails
import pyrebase
import requests
import re #regex
import smtplib
#inside are the details of person thats logged in. Useful for loading data to the pages
class Store:
    button = 40
    priv = ""
    points = 0
    email =""
#to connect to firebase
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

firebase = pyrebase.initialize_app(config) 
#for when person is signing up

# for when person is signing up
def check_email_format(email):
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if (re.search(regex, email)):
        return True
    else:
        return False

def send_rejection_email(email):
    with smtplib.SMTP('smtp.gmail.com',587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login("cs322projectd@gmail.com","cs322s20mw")
        subject = "Rejected from teaming system"
        body = """You have been rejected from the system. If you wish to try again, you can sign
        up again. The second attempt will be your appeal."""
        msg = f'Subject: {subject}\n\n{body}'
        smtp.sendmail("cs322projectd@gmail.com",email,msg)
    
#for getting username from the email
def extract_user_from_email(email):
    count = 0
    for char in email:
        if char == '@':
            break
        else:
            count+=1
    return email[:count:]


#returns dictionary of person in the pending users table given their email
def get_info_pending(email):
	db = firebase.database()
	all_users = db.child("pending_users").get()
	for users in all_users.each():
		a = users.val()
		if a['email'] == email:
			return a
	return None
def get_info_users(email):
    db = firebase.database()
    all_users = db.child("users").get()
    for users in all_users.each():
        a = users.val()
        if a['email'] == email:
            return a
    return None

def get_key_appeal(email):
    db = firebase.database()
    all_users = db.child("possible_appeals").get()
    for users in all_users.each():
        a = users.val()
        if a['email'] == email:
            return users.key()
    return None


#returns key in db given the existing email of pending user in the system
def get_key_pending(email): 
    
    db = firebase.database()
    all_users = db.child("pending_users").get() 
    for users in all_users.each():
        a=users.val()
        
        if a['email'] == email:
            return users.key()
    return None
def get_key_group_notifs(email): 
    
    db = firebase.database()
    all_users = db.child("groupNotification").get() 
    for users in all_users.each():
        a=users.val()
        
        if a['user'] == email:
            return users.key()
    return None


def is_in_blacklist(email):
    db = firebase.database()
    all_users = db.child("blacklist").get()
    for users in all_users.each():
        a = users.val()
        if a['email'] == email:
            return True
    return False

def is_in_appeal(email):
    db = firebase.database()
    all_users = db.child("possible_appeals").get()
    for users in all_users.each():
        a = users.val()
        if a['email'] == email:
            return True
    return False


def is_in_users(email):
    db = firebase.database()
    all_users = db.child("users").get()
    for users in all_users.each():
        a = users.val()
        if a['email'] == email:
            return True
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
        auth = firebase.auth()

        try:
            auth.sign_in_with_email_and_password(self.email.text,self.password.text)
            person_info = get_info_users(self.email.text)
            Store.email = person_info['email']
            Store.points = person_info['points']

            user_priv = person_info['privilege']
            if user_priv == 0:
                Store.priv = "OU"

            elif user_priv == 1:
                Store.priv = "VIP"

            elif user_priv ==2:
                Store.priv = "SU"
        
            self.email.text=""
            self.password.text=""
            if Store.points <0:
                show_popup("Warning","""        You have a negative score. 
When you log out you will be banned""")
            if Store.priv == "OU" or Store.priv == "VIP":
                self.parent.current = "homeOU"
            elif Store.priv == "SU":
                self.parent.current = "homeSU" #how you switch screens in python code
        except:
            if is_in_blacklist(self.email.text) == True:
                show_popup("Error","This email is banned")
            else:
                show_popup("Error","wrong combination of email and password")
            self.email.text = ""
            self.password.text = ""
        return True

    def check_user(self):
        
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
    reference = ObjectProperty(None)

    def sign_up(self):

        appeal = 0
        if is_in_appeal(self.email.text) == True:
            appeal = 1

        priv = 0
        points = 0
        data ={
        "email":self.email.text,
        "password":self.password.text,
        "privilege":priv,
        "points":points,
        "appeal": appeal,
        "date of birth":self.dob.text,
        "interests":self.interests.text,
        "reference email":self.reference.text
        }
        db = firebase.database()

        if (check_email_format(self.email.text)==True) and (len(self.password.text) >=6): 
            if is_in_blacklist(self.email.text) == True:
                show_popup("Error","This email is banned from the system")

            elif is_in_users(self.email.text) == True:
                show_popup("Error","This email is already in the system")

            elif appeal == 1:

                appeal_key = get_key_appeal(self.email.text)
                db.child("possible_appeals").child(appeal_key).remove()
                db.child("pending_users").push(data)
                show_popup("Submit","Application received. This is your appeal")

            else:
                db.child("pending_users").push(data)
                show_popup("Submit","Application received")
            
        else:
            show_popup("Reject","Email or password did not meet the requirements")

        self.email.text = ""
        self.password.text = ""
        self.dob.text = ""
        self.interests.text = ""
        self.reference.text = ""
        
class NotificationOUPage(Screen):
    pass

class NotificationSUPage(Screen):
    person1 = StringProperty("")
    person2 = StringProperty("")
    person3 = StringProperty("")
    person4 = StringProperty("")
    person5 = StringProperty("")
    person6 = StringProperty("")
    person7 = StringProperty("")

    email = StringProperty()
    password = StringProperty() #instead of past project
    birthday = StringProperty()
    interest = StringProperty()
    appeal = StringProperty()
    reference = StringProperty()
    #refresh button
    def show_new_requests(self):
        db = firebase.database()
        email_requests = ["","","","","","",""]

        all_users = db.child("pending_users").get()
        count = 0
        for users in all_users.each():
            if count >=7:
                break

            a = users.val()
            email_requests[count] = a["email"]
            count+=1
        self.person1 = email_requests[0]
        self.person2 = email_requests[1]
        self.person3 = email_requests[2]
        self.person4 = email_requests[3]
        self.person5 = email_requests[4]
        self.person6 = email_requests[5]
        self.person7 = email_requests[6]
        


    def accept_btns(self,which_person_email):
        try:
            if which_person_email == "" or which_person_email == "sentinel":
                show_popup("Error","This request is empty(No email is shown). Try refreshing")
            else:

                person_info = get_info_pending(which_person_email)
                person_key = get_key_pending(which_person_email)
                db = firebase.database()
                auth = firebase.auth()
                person_password  = person_info['password']
                try:
                    create_user = auth.create_user_with_email_and_password(which_person_email,person_password)
                    db.child("pending_users").child(person_key).remove() 
                    user = extract_user_from_email(which_person_email)
                    auth.send_email_verification(create_user['idToken'])
                    person_info.update({"name":user})
                    db.child("users").push(person_info)
                    show_popup("Success","""User was successfully added to the system. 
            Refresh to get new requests""")
                    which_person_email = ""
                except:
                    show_popup("Error","This email is already in the system, has to be rejected")
        except:
            show_popup("Error","Refresh to update requests")

    def change_button(self,i,which_person_email):
        if which_person_email:
            Store.button = i

    def is_email_there(self,which_person_email):
        if which_person_email:
            return True
        return False

    


    def show_details(self,index,which_person_email):
        if which_person_email == "" or which_person_email == "sentinel":
            show_popup("Error","No details to load.(Try refreshing)")
        else:

            db = firebase.database()
            email_requests = ["","","","","","",""]
            

            all_users = db.child("pending_users").get()
            count = 0
            for users in all_users.each():
                if count >=7:
                    break

                a = users.val()
                email_requests[count] = a["email"]
                count+=1

            user_info = get_info_pending(email_requests[index])
            self.email = user_info['email']
            self.password = user_info['password']
            self.birthday = user_info['date of birth']
            self.interest = user_info['interests']
            self.appeal = str(user_info['appeal'])
            self.reference = user_info['reference email']
        


class DescriptionWindow(Screen):
    desc_email = StringProperty()
    desc_password = StringProperty() 
    desc_birthday = StringProperty()
    desc_interest = StringProperty()
    desc_appeal = StringProperty()
    desc_reference = StringProperty()

    
    def update(self):
        a = NotificationSUPage()
        a.show_details(Store.button,"not empty")
        self.desc_email = a.email
        self.desc_password = a.password
        self.desc_birthday = a.birthday
        self.desc_interest = a.interest
        self.desc_appeal = a.appeal
        self.desc_reference = a.reference

    def return_btn(self):
        self.desc_email =""
        self.desc_password =""
        self.desc_birthday =""
        self.desc_interest =""
        self.desc_appeal =""
        self.desc_reference =""

    def reject_btn(self):
        if self.desc_email == "":
            show_popup("Error","Press load info to view details before rejecting")

        
        else:
            db = firebase.database()
            person = get_info_pending(self.desc_email)
            person_key = get_key_pending(self.desc_email)
            if person['appeal'] ==0:
                
                person['appeal'] = 1
                db.child("possible_appeals").push(person)
                db.child("pending_users").child(person_key).remove()
                send_rejection_email(self.desc_email) 
                self.desc_email =""
                self.desc_password =""
                self.desc_birthday =""
                self.desc_interest =""
                self.desc_appeal =""
                self.desc_reference =""

                show_popup("Success","""User was rejected from the system.
        Refresh to get new requests""")
                self.parent.current = "requests"
            elif person['appeal'] ==1:
                db.child("pending_users").child(person_key).remove()
                db.child("blacklist").push(person)
                self.desc_email =""
                self.desc_password =""
                self.desc_birthday =""
                self.desc_interest =""
                self.desc_appeal =""
                self.desc_reference =""
                show_popup("Blacklisted","""This is the second time they have
    applied. User was added to blacklist""")
                self.parent.current = "requests"




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
    close_req1 = StringProperty()
    close_req2 = StringProperty()
    close_req3 = StringProperty()
    close_req4 = StringProperty()
    close_req5 = StringProperty()
    close_req6 = StringProperty()
    

    #loads the close group requests when you enter page
    def on_pre_enter(self):
        db = firebase.database()
        close_requests = db.child("groupNotification").order_by_child("desc").equal_to("closegroup").get()
        count = 0
        groups = ["","","","","",""]
        for request in close_requests.each():
            if count > 5:
                break
            else:
                a = request.val()
                #print(a['user'])
                groups[count] = str(a['group'])
                count+=1

        self.close_req1 = groups[0]
        self.close_req2 = groups[1]
        self.close_req3 = groups[2]
        self.close_req4 = groups[3]
        self.close_req5 = groups[4]
        self.close_req6 = groups[5]
        return groups

    def validate_email(self,email,popup,email_list,groupname):
        db = firebase.database()
        #check if a vip was assigned to this group
        try:
            is_group_assigned = len(db.child("assignVIP").order_by_child("groupname assigned").equal_to(groupname).get().val())
        except:
            is_group_assigned = 0

        if is_group_assigned > 0:
            show_popup("Error","VIP is already assigned for this group")
            popup.dismiss()
        else:
            if email == "":
                show_popup("Error","Please enter an email.")
            elif groupname == "":
                show_popup("Error","No requests here.Refresh to get new close group requests")
                popup.dismiss()
            elif email == email_list[0] or email == email_list[1] or email == email_list[2] or email == email_list[3] or email == email_list[4] or email_list[5]:
                data = {"email":email,"groupname assigned": str(groupname),"ticket":0}
                db.child("assignVIP").push(data)
                popup.dismiss()
                #self.on_pre_enter()

            else:
                show_popup("Error","Did not enter correct email")

    def assign_vip(self,index):
        
        db =firebase.database()
        
        
        vips = db.child("users").order_by_child("privilege").equal_to(1).get()
        count = 0 
        vip_emails = ["","","","","",""]
        for users in vips.each():
            if count > 5:
                break
            else:
                a = users.val()
                vip_emails[count] = a['email']
                count+=1
        layout = FloatLayout()
        title = Label(text="Choose one of the following emails to assign them to close the group", size_hint=(0.6, 0.2), pos_hint={"x": 0.2, "top": 1})
        layout.add_widget(title)
        email1 = Label(text=vip_emails[0], size_hint=(0.6, 0.2), pos_hint={"x": 0.2, "y": 0.7})
        email2 = Label(text=vip_emails[1], size_hint=(0.6, 0.2), pos_hint={"x": 0.2, "y": 0.65})
        email3 = Label(text=vip_emails[2], size_hint=(0.6, 0.2), pos_hint={"x": 0.2, "y": 0.60})
        email4 = Label(text=vip_emails[3], size_hint=(0.6, 0.2), pos_hint={"x": 0.2, "y": 0.55})
        email5 = Label(text=vip_emails[4], size_hint=(0.6, 0.2), pos_hint={"x": 0.2, "y": 0.50})
        email6 = Label(text=vip_emails[5], size_hint=(0.6, 0.2), pos_hint={"x": 0.2, "y": 0.45})
        layout.add_widget(email1)
        layout.add_widget(email2)
        layout.add_widget(email3)
        layout.add_widget(email4)
        layout.add_widget(email5)
        layout.add_widget(email6)
        textinput = TextInput(hint_text = 'Enter email of VIP you want to assign this group to',multiline = False,size_hint=(0.8,0.15),pos_hint ={"x":0.1,"y":0.35})
        layout.add_widget(textinput)

        assign_button = Button(text= "Assign the VIP", size_hint=(0.8, 0.1), pos_hint={"x": 0.1, "y": 0.20})
        close_button = Button(text="close", size_hint=(0.8, 0.1), pos_hint={"x": 0.1, "y": 0.1})
        layout.add_widget(close_button)
        layout.add_widget(assign_button)
        popup = Popup(title="Assign VIP", content=layout, size_hint=(None, None), size=(500, 500), auto_dismiss=False)
        a = self.on_pre_enter()
        assign_button.bind(on_press= lambda x: self.validate_email(textinput.text,popup,vip_emails,a[index]))
        close_button.bind(on_press=popup.dismiss)
        popup.open()
       



    
    #which_group is a StringProperty
    def close_group(self,which_group):
        
        db = firebase.database()
        vip_assigned_email = ""
        is_complete = 0
        #checking if a vip gave out a rating for the group
        try:
            did_vip_assign = db.child("assignVIP").order_by_child("groupname assigned").equal_to(which_group).get()
            for users in did_vip_assign.each():
                a = users.val()
                if a["ticket"] == 1:
                    is_complete+=1
                    vip_assigned_email = a["email"]
                    break   
        except:
            is_complete = 0

        if which_group == "":
            show_popup("Error","Can't close. Refresh to get new requests")
        
        elif is_complete == 0:
            show_popup("Error","""  VIP has not yet assigned a score
    for the members of this group""")
        elif is_complete == 1:
            #deleting assigned VIP from the assign VIP table
            for users in did_vip_assign.each():
                a = users.val()
                if a['groupname assigned'] == which_group:
                   # print(a['email'],get_key_assignVIP(a['email']))
                   key = users.key()
                   db.child("assignVIP").child(key).remove()

            #deleting all closegroup requests for the group
            groupnotif = db.child("groupNotification").order_by_child("group").equal_to(which_group).get()
            for users in groupnotif.each():
                a = users.val()
                if a['desc'] == "closegroup":
                    key = users.key()
                    db.child("groupNotification").child(key).remove()


            #deleting the group itself
            group = db.child("group").order_by_child("groupName").equal_to(which_group).get()

            for sect in group.each():
                key = sect.key()
                db.child("group").child(key).remove()
                break
            
            show_popup("Success","Group has been deleted from the system")
            self.on_pre_enter() #to update requests
       
class GroupWindow(Screen):

    def on_start(self, *args): #change to on_enter later
        email = 'jin@aol.com'
        groupId = 1
        pollId = 1
        taskId = 4

        #firebase = pyrebase.initialize_app(config)
        db = firebase.database()

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

        #firebase = pyrebase.initialize_app(config)
        db = firebase.database()

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

        #firebase = pyrebase.initialize_app(config)
        db = firebase.database()
        groupDb = db.child("group").order_by_child("groupId").equal_to(groupId).get()
        for sect in groupDb.each():
            groupKey = sect.key()

        db.child("group").child(groupKey).remove()

    def remove_group_user(self, email, groupId):
        groupId = 5

        #firebase = pyrebase.initialize_app(config)
        db = firebase.database()
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

        #firebase = pyrebase.initialize_app(config)
        db = firebase.database()
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

        #firebase = pyrebase.initialize_app(config)
        db = firebase.database()
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
        
        db = firebase.database()

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


class HomeSUWindow(Screen):
    #clearing information of person that was logged in
    def log_out_btn(self):
        Store.button = 40
        Store.points = 0
        Store.priv = ""
        Store.email = ""

class HomeOUWindow(Screen):

    def log_out_btn(self):
        if Store.points < 0:
            blacklist_info = get_info_users(Store.email)
            db = firebase.database()
            user= db.child("users").order_by_child("email").equal_to(Store.email).get()
            for person in user.each():
                key = person.key()
                db.child("users").child(key).remove()
                break
            db.child("blacklist").push(blacklist_info)

        Store.button = 40
        Store.points = 0
        Store.priv = ""
        Store.email = ""


class ProfileWindow(Screen):
    pass


kv = Builder.load_file("main.kv")



class MyMainApp(App):
    
    def build(self):
        return kv


if __name__ == "__main__":
    MyMainApp().run()
