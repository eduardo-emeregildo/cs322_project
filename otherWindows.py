from homepageOUmain import *
from signingDetails import Store, add_ref, get_info_users, show_popup




# to take actions from popup class
token = 0
userCallingPopup = ""

# for loading homeOU page with username
userOUNotifications = ""

# to return to homeSU or homepage depending on log in status
screenToken = 0


# taboo words

tabooWords = {"idiot", "useless", "stupid"}

# taboo word remove function

def remove_taboo_words(line):
    for word in tabooWords:
        line = line.replace(word, "*****")
    return line

# check whether the info exists in the database

def data_exist(self, tableName, name):
    all_data = db.child(tableName).get()
    try:
        for data in all_data.each():
            if data.val()["name"] == name:
                return True
    except:
        return False

    return False

def data_exist2(self, tableName, name):
    all_data = db.child(tableName).get()
    try:
        for data in all_data.each():
            if data.val()["listed"] == name:
                return True
    except:
        return False

    return False

# check if the popup input text format is correct

def check_valid_format(self, num, text):
    if num == 1:
        if text == "":
            return False

    elif num == 2:
        textList = self.input_text.text.replace(" ", "").split(',')

        if len(textList) < 2:
            return False
        elif textList[0] == "" or textList[1].isnumeric() == False:
            return False

    return True

# initiate a button that has a link

def check_button_active(username):
    if username != "":
        return True
    return False


def group_popup():
        global token 
        token = 6

        popup = PopupWindow(title= "File a Complaint\nFormat:name, group name, complaint")        
        popup.open()


        
class PopupWindow(Popup):
    input_text = ObjectProperty()

    def __init__(self, text='', **kwargs):
        super(PopupWindow, self).__init__(**kwargs)
        self.input_text.text = text
        self.auto_dismiss = False

    def change_score(self, username, score):
        if data_exist(self, "users", username):
            userinfo = db.child("users").order_by_child("name").equal_to(username).get()           
            for user in userinfo.each():
                s = user.val()["points"]
                p = user.key()
            s = s + score
            db.child("users").child(p).update({"points": s })
        
        else:
            show_popup("Error", "User doesn't exist")

    def change_project_score(self, projectName, score):
        if data_exist(self, "projects", projectName):
            projectinfo = db.child("projects").order_by_child("name").equal_to(projectName).get()
            for project in projectinfo.each():
                s = project.val()["score"]
                p = project.key()
                s = s + score
                db.child("projects").child(p).update({"score": s })
        else:
            show_popup("Error", "Project doesn't exist")

    def store(self):
        if check_valid_format(self, 1, self.input_text.text) == False:
            show_popup("Error", "Please use the correct format\n and make sure the value exists")
            self.dismiss()
        
        elif token == 1:    
            text = remove_taboo_words(self.input_text.text)   
            data = {
                "user" : userCallingPopup,
                "desc" : text
            }
            db.child("complaints").push(data)

        elif token == 2:
            text = remove_taboo_words(self.input_text.text)
            data = {
                "user" : userCallingPopup,
                "desc" : text
            }
            db.child("compliments").push(data)
        
        elif token == 6:
            text = self.input_text.text.split(',', 3)
            if len(text)<3:
                show_popup("Error", "Please use the correct format")
            else:
                data = {
                    "user": text[0],
                    "group": text[1],
                    "desc": text[2] 
                }
                db.child("warnings").push(data)

        else:
            if check_valid_format(self, 2, self.input_text.text):                
                text = self.input_text.text.replace(" ", "").split(',')
                name = text[0]
                score = text[1]
                if token == 3:
                    score = int(score)
                    self.change_project_score(name, score)
                elif token == 4:
                    score = int(score)
                    self.change_score(name, score)               
                elif token == 5:
                    score = int(score)
                    self.change_score(name, -score)
            else:
                    show_popup("Error", "Please use the correct format\n and make sure the value exists")

        self.dismiss()
    
        
###########################################################################

class VisitorView(Screen):
    def show_popup0(self):
        global token 
        token = 1

        global userCallingPopup
        userCallingPopup = self.username.text

        popup = PopupWindow(title= "File a Complaint")        
        popup.open()
        
    def initialize_page(self):
        get_top_projects(self, "user", self.username.text, 0, db)
       
    def prev_screen(self):
        if screenToken == 1:
            self.parent.current = "homeSU"
        else:
            self.parent.current = "home"


class HomeOUWindow(Screen):
     #clearing information of person that was logged in
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

        
    def initialize_page(self):
        global userOUNotifications
        userOUNotifications = self.username.text

        get_top_projects(self, "user", self.username.text, 0, db)
        get_top_users(self, "name", db)

    def switch_screen(self, username):
        if username != "":
            standing_update(self, username, 17)

    def go_to_profile(self):
        standing_update(self, self.username.text, 4)



class HomeSUWindow(Screen):

        def log_out_btn(self):
            Store.button = 40
            Store.points = 0
            Store.priv = ""
            Store.email = ""

        def initialize_page(self):
                global screenToken 
                screenToken = 1
                get_top_projects(self, "score", "", 1, db)
                get_top_users(self, "name", db)
    
        def switch_screen(self, username):
            if username != "":
                standing_update(self, username, 16)



class groupNotificationSU(Screen):
    def update_notification(self):
        get_group_notifications(self, db, 1, "")


class ComplimentPage(Screen):
    def show_popup0(self):
        global token 
        token = 4

        popup = PopupWindow(title= "Increase Reputation Score\nFormat: Name, Score(must be an integer)")
        popup.open()
    
    def update(self):
        get_compliments(self, db)


class WelcomeScreen(Screen):
    pass



class ReferenceOU(Screen):
    def show_popup2(self):
        global token 
        token = 4

        popup = PopupWindow(title= "Give a Score:\nFormat: Name, Score(must be an integer)")        
        popup.open()

    def update_notification(self):
        get_reference_notifications(self, db, userOUNotifications)


class WarningPage(Screen):
    def update(self):
        get_complaints(self, db, 1, "", 1)

    def show_popup0(self):
        global token
        token = 5

        popup = PopupWindow(title= "Decrease Score:\nFormat: Name, Score(must be an integer)")
        popup.open()




class VisitorViewLoggedIn(Screen):
    def show_popup0(self):
        global token
        token = 1
        global userCallingPopup
        userCallingPopup = self.username.text
        popup = PopupWindow(title= "File a Complaint")        
        popup.open()
       
    def show_popup1(self):
        global token 
        token = 2
        global userCallingPopup
        userCallingPopup = self. username.text
        popup = PopupWindow(title= "Send a Compliment")        
        popup.open()
   
    def show_popup2(self):
        global token
        token = 3
        popup = PopupWindow(title= "Rate a Project:\nFormat: Project Name, Score(must be an integer)")        
        popup.open()

    def initialize_page(self):
        get_top_projects(self, "user", self.username.text, 0, db)


# Needs working, check if user exist, do blackbox

class ProfileWindow(Screen):
        def update(self):
                get_warnings(self, db, 0, userOUNotifications, 0)
                get_groups(self, self.username.text)
                self.update_whitebox()
                self.update_blackbox()
                
        def get_groupname(self, name):
            self.manager.screens[8].ids.groupDesc.text = name
            self.parent.current = "grouppage"
        
        def add_toList(self, user, addUser, priv):
            
            if priv == 1:
                name = self.text_input2.text
                self.text_input2.text = ""
            else:
                name = self.input_text.text
                self.input_text.text =""
            
            if data_exist(self, "users", addUser):
                if data_exist2(self, "whitebox_blackbox", addUser) == False:
                    data = {
                        "name": self.username.text,
                        "listed": name,
                        "priv": priv
                    }
                    db.child("whitebox_blackbox").push(data)
                    self.update()
            else:
                show_popup("Error", "User doesn't exist")



# privilege 2 for whitebox, 1 for blackbox
            
        def update_whitebox(self):
            newList = []            
            boxedUser = db.child("whitebox_blackbox").order_by_key().get()


            try:
                if boxedUser.val() != None: 
                    for user in boxedUser.each():
                        if user.val()["name"] == self.username.text:
                            if user.val()["priv"] == 2:
                                newList.append(user.val()["listed"])
            except:
                pass


            newList.reverse()
            while(len(newList) < 4):
                newList.append("")

            self.b1.text = newList[0]
            self.b2.text = newList[1]
            self.b3.text = newList[2]
            self.b4.text = newList[3]


        def update_blackbox(self):
            newList = []            
            boxedUser = db.child("whitebox_blackbox").order_by_key().get()

            try:
                if boxedUser.val() != None: 
                    for user in boxedUser.each():
                        if user.val()["name"] == self.username.text:
                            if user.val()["priv"] == 1:
                                newList.append(user.val()["listed"])
            except:
                pass


            newList.reverse()
            while(len(newList) < 4):
                newList.append("")

            self.b5.text = newList[0]
            self.b6.text = newList[1]
            self.b7.text = newList[2]
            self.b8.text = newList[3]

        def remove_last(self, name):
            userinfo = db.child("whitebox_blackbox").get() 
            p = ""      
            try:   
                for user in userinfo.each():
                    if user.val()["listed"] != "don't delete":
                        if user.val()["listed"] == name:
                            p = user.key()
                
                db.child("whitebox_blackbox").child(p).remove()
                #db.child("whitebox_blackbox").child(p).update({"priv": 0})

            except:
                pass
            self.update()


#add_ref("mm@gmail.com", "ss@ymm.com", 1)
