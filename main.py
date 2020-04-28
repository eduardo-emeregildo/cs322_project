from kivy.app import App
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.graphics.context_instructions import Color
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
#import pyrebase
import requests


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

class HomeWindow(Screen):
	pass

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
    	auth = firebase.auth()
    	try:
    		auth.create_user_with_email_and_password(self.email.text,self.password.text)
    		print("data added to authentication")
    		db.child("users").push(data)
    		print("data added to db")
    		self.email.text = ""
    		self.password.text = ""
    		self.dob.text = ""
    		self.interests.text = ""
    		self.prev_projects.text = ""
    	except requests.exceptions.HTTPError: # can do a popup here
    		print("Invalid email or password.(Passwords must be at least 6 characters long)")


class GroupWindow(Screen):
	pass

class CreateGroupWindow(Screen):
	pass

class HomeOUWindow(Screen):
	pass

class ProfileWindow(Screen):
	pass

class NotificationPage(Screen):
    pass

class DescriptionWindow(Screen):
    pass

class ComplimentPage(Screen):
    pass

class WarningPage(Screen):
    pass

class GroupNotificationSU(Screen):
    pass

kv = Builder.load_file("main.kv")

class MyMainApp(App):
    def build(self):
        return kv

if __name__ == "__main__":
    MyMainApp().run()



