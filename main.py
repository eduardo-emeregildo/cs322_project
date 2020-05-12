from kickTasksNotif import *

class HomeWindow(Screen):

    email = ObjectProperty(None)
    password = ObjectProperty(None)


    def initialize_page(self):
        get_top_projects(self, "score", "", 1, db)
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


        self.manager.screens[2].ids.username.text = self.email.text
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
        
            self.email.text=""
            self.password.text=""
            self.parent.current = "homeOU" #how you switch screens in python code
        except:
            show_popup("Error","wrong combination of email and password")
            self.email.text = ""
            self.password.text = ""
        return True

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


kv = Builder.load_file("main.kv")

class MyMainApp(App):
    def build(self):
        return kv

if __name__ == "__main__":
    MyMainApp().run()

