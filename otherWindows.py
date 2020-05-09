from homepageOUmain import *
from signingDetails import Store


class WelcomeScreen(Screen):
    pass

# Needs working

token = 0
screenToken = 0

class PopupWindow(Popup):
    input_text = ObjectProperty()

    def __init__(self, text='', **kwargs):
        super(PopupWindow, self).__init__(**kwargs)
        self.input_text.text = text
        self.auto_dismiss = False

    def store(self):
    #    print(token)
        if token == 1:
            data = {
                "desc" : self.input_text.text
            }
            db.child("complaints").push(data)
            self.dismiss()
        elif token == 2:
            data = {
                "desc": self.input_text.text
            }
            db.child("compliments").push(data)
            self.dismiss()

        else:
            data = {
                "point": self.input_text.text
            }
            db.child("Ratings").push(data)
            self.dismiss()

class VisitorViewLoggedIn(Screen):
    def show_popup0(self):
        global token
        token = 1
        popup = PopupWindow(title= "File a Complaint")        
        popup.open()
    
        #self.complaint()

    def show_popup1(self):
        global token
        token = 2
        popup = PopupWindow(title= "Send a Compliment")        
        popup.open()
    
    def show_popup2(self):
        global token
        token = 3
        popup = PopupWindow(title= "Rate the Project: (1-20)")        
        popup.open()


    def initialize_page(self, username):
        self.username.text = "Chris"
        get_top_projects(self, "user", username, 0, db)


    

class ComplimentPage(Screen):
    def show_popup0(self):
        popup = PopupWindow(title= "Increase Reputation Score")
        popup.open()


class WarningPage(Screen):
    def update(self):
        get_warnings(self, db, 1, "")

    def show_popup0(self):
        popup = PopupWindow(title= "Decrease Reputation Score")
        popup.open()

    


class VisitorView(Screen):

    def show_popup0(self):
        global token
        token = 1
        popup = PopupWindow(title= "File a Complaint")        
        popup.open()
        

    def initialize_page(self):
        print(self.username.text)
        get_top_projects(self, "user", "Chris", 0, db)
    
    def complaint(self):
        description = db.child("popups").get()
        arr = []

        for r in description.each():
            arr.append(r.val()["desc"])
            print(r.val()["desc"])

        data = {"desc": arr[0]}
        db.child("complaints").push(data)
    
    def prev_screen(self):
        if screenToken == 1:
            self.parent.current = "homeSU"
        else:
            self.parent.current = "home"




class HomeOUWindow(Screen):
     #clearing information of person that was logged in
    def log_out_btn(self):
        Store.button = 40
        Store.points = 0
        Store.priv = ""
        Store.email = ""
        
    def initialize_page(self):
        #print(self.username.text)        
        get_top_projects(self, "user", self.username.text, 0, db)
        get_top_users(self, "name", db)



class HomeSUWindow(Screen):

        def initialize_page(self):
                global screenToken 
                screenToken = 1
                get_top_projects(self, "score", "", 1, db)
                get_top_users(self, "name", db)

    
        def switch_screen(self, username):

            #print(username)
            
            userinfo = db.child("new_users").order_by_child("name").equal_to(username).limit_to_first(1).get()

            for info in userinfo.each():
                self.manager.screens[15].ids.priv.text = str(info.val()["privilege"])

            self.manager.screens[15].ids.username.text = username
            self.manager.current = "VisitorView"



class ProfileWindow(Screen):
	pass

class groupNotificationSU(Screen):
    def update_notification(self):
        get_group_notifications(self, db, 1, "")


class groupNotificationOU(Screen):
    def update_notification(self):
        get_group_notifications(self, db, 0, "Emily")

class WarningPageOU(Screen):
    def update(self):
        get_warnings(self, db, 0, "Emily")