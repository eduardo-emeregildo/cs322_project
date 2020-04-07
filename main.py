from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
import pyrebase
import requests


#dictionary containing data to connect to firebase
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

def get_key(email): #returns key in db given the existing email of user in the system
	firebase= pyrebase.initialize_app(config)
	db = firebase.database()
	all_users = db.child("users").get() 
	for users in all_users.each():
		a=users.val()
		if a['email'] == email:
			return users.key()


def delete_record_db(key): #deletes user from db given their corresponding key
	firebase= pyrebase.initialize_app(config)
	db = firebase.database()
	db.child("users").child(key).remove() #key has to be given
	print("user removed")


class HomeWindow(Screen):
	pass
    # def log_in(self):
    # 	firebase = pyrebase.initialize_app(config)
    # 	email = input("enter email ")
    # 	password = input("enter pass ")
    # 	auth = firebase.auth()
    # 	try:
    # 		auth.sign_in_with_email_and_password(email,password)
    # 		print("Success")
    # 	except:
    # 		print("you have entered wrong email or password"
	 

class SignupWindow(Screen):
	def sign_up(self):
		firebase = pyrebase.initialize_app(config)
		name = input("Enter your name ")
		pwd = input("enter your password ")
		reference = input("Enter email of your reference ")
		priv = 0
		db = firebase.database()
		auth = firebase.auth()
		data ={
		"name":name,
		"email":email,
		"password":pwd,
		"priviledge":priv
		}
		try:
			auth.create_user_with_email_and_password(email,pwd)
			print("data added to authentication")
			db.child("users").push(data)
			print("data added to db")
		except requests.exceptions.HTTPError:
			print("Invalid email or password.(Passwords must be at least 6 characters long)")




class WindowManager(ScreenManager):
    pass



kv = Builder.load_file("main.kv")


class MyMainApp(App):
    def build(self):
        return kv



if __name__ == "__main__":
    MyMainApp().run()
