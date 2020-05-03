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
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
import pyrebase
import requests
import re


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

#for when person is signing up
def check_email_format(email):
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if(re.search(regex,email)):
        return True
    else:
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
		
		firebase = pyrebase.initialize_app(config)
		auth = firebase.auth()
		try:
			auth.sign_in_with_email_and_password(self.email.text,self.password.text)
			self.parent.current = "homeOU" #how you switch screens in python code
			
		except:
			show_popup("Error","wrong combination of email and password")
		self.email.text = ""
		self.password.text = ""






class SignupWindow(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None) 
    dob = ObjectProperty(None) 
    interests = ObjectProperty(None) 
    prev_projects = ObjectProperty(None)

    def sign_up(self):
        priv = 0
        data ={
        "email":self.email.text,
        "password":self.password.text,
        "priviledge":priv,
        "date of birth":self.dob.text,
        "interests":self.interests.text,
        "previous projects":self.prev_projects.text
        }
        firebase = pyrebase.initialize_app(config)
        db = firebase.database()
        

        if (check_email_format(self.email.text)==True) and (len(self.password.text) >=6): 
            db.child("pending_users").push(data)
            show_popup("Submit","Application received")
            
        else:
            show_popup("Reject","An error occured")

        self.email.text = ""
        self.password.text = ""
        self.dob.text = ""
        self.interests.text = ""
        self.prev_projects.text = ""



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
	pass

class ProfileWindow(Screen):
	pass



kv = Builder.load_file("main.kv")

class MyMainApp(App):
    def build(self):
        return kv

if __name__ == "__main__":
    MyMainApp().run()



