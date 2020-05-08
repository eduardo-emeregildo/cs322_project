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
from kivy.properties import ObjectProperty,StringProperty,NumericProperty,DictProperty
from kivy.uix.boxlayout import BoxLayout
import smtplib #emails
import pyrebase
import requests
import re #regex


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
def check_email_format(email):
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if(re.search(regex,email)):
        return True
    else:
        return False

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

#title of the popup and what you want the label to say are input
def show_popup(title_popup,text_label):
    layout = FloatLayout()
    label = Label(text =text_label,size_hint = (0.6,0.2),pos_hint = {"x":0.2,"top":1})
    layout.add_widget(label)
    button = Button(text = "close",size_hint =(0.8,0.1),pos_hint = {"x":0.1,"y":0.1})
    layout.add_widget(button)
    popup = Popup(title=title_popup,content =layout,size_hint=(None,None),size=(400,400),auto_dismiss = False)
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
            self.parent.current = "homeOU" #how you switch screens in python code


        except:
            show_popup("Error","wrong combination of email and password")
            self.email.text = ""
            self.password.text = ""
        return True

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


class NotificationPage(Screen):
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
                    #auth.send_email_verification(create_user['idToken']) to let them know that theyre in the system, uncomment for demo
                    db.child("pending_users").child(person_key).remove() 
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
    desc_password = StringProperty() #instead of past project
    desc_birthday = StringProperty()
    desc_interest = StringProperty()
    desc_appeal = StringProperty()
    desc_reference = StringProperty()

    
    def update(self):
        a = NotificationPage()
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
                #send email here
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
        popup = PopupWindow(title= "Increase Reputation Score")
        popup.open()


class WarningPage(Screen):
    def show_popup(self):
        popup = PopupWindow(title= "Decrease Reputation Score")
        popup.open()

class GroupNotificationSU(Screen):
    pass

class GroupWindow(Screen):
	pass

class CreateGroupWindow(Screen):
	pass

class HomeOUWindow(Screen):
    #clearing information of person that was logged in
    def log_out_btn(self):
        Store.button = 40
        Store.points = 0
        Store.priv = ""
        Store.email = ""


class ProfileWindow(Screen):
	pass



kv = Builder.load_file("main.kv")

#len(db.child("pending_users").get().val()) to get how many entries in table
class MyMainApp(App):
    
    def build(self):
        return kv

if __name__ == "__main__":
    MyMainApp().run()



