from kickTasksNotif import *
#inside are the details of person thats logged in. Useful for loading data to the pages


def get_key_group_notifs(email): 

	db = firebase.database()
	all_users = db.child("groupNotification").get() 
	for users in all_users.each():
		a=users.val()

		if a['user'] == email:
		    return users.key()
	return None


class HomeWindow(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)


    def initialize_page(self):
        get_top_projects(self, "", "", 1, db)
        get_top_users(self, "name", db) 
	
    def log_in_auto(self):               
        userinfo = db.child("users").order_by_child("name").equal_to(self.email.text).limit_to_first(1).get()


        try:
            for info in userinfo.each():
                if info.val()["points"] > 30:
                    rank = "VIP"
                else:
                    rank = "OU"
                self.manager.screens[2].ids.points.text = rank
        except:
            pass

        text = self.email.text.split("@")

        self.manager.screens[2].ids.username.text = text[0]
        self.manager.current = "homeOU"
	
    def switch_screen(self, username):
        if username != "":
            standing_update(self, username, 16)


# Actual login function


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

            if Store.points <0:
                show_popup("Warning","""        You have a negative score. 
When you log out you will be banned""")
            if Store.priv == "OU" or Store.priv == "VIP":

                self.log_in_auto()
                
            elif Store.priv == "SU":
                self.parent.current = "homeSU" #how you switch screens in python code
        except:
            if is_in_blacklist(self.email.text) == True:
                show_popup("Error","This email is banned")
            else:
                show_popup("Error","wrong combination of email and password")
                self.email.text = ""
                self.password.text = ""
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
        
	
class DescriptionWindow(Screen):
    desc_email = StringProperty()
    desc_password = StringProperty() 
    desc_birthday = StringProperty()
    desc_interest = StringProperty()
    desc_appeal = StringProperty()
    desc_reference = StringProperty()

    
    def update(self):
        a = NotificationSU()
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
            

kv = Builder.load_file("main.kv")

class MyMainApp(App):
    def build(self):
        return kv

if __name__ == "__main__":
    MyMainApp().run()

