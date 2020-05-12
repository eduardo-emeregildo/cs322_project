from kickTasksNotif import *
#inside are the details of person thats logged in. Useful for loading data to the pages

class HomeWindow(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)


    def initialize_page(self):
        get_top_projects(self, "score", "", 1, db)
        get_top_users(self, "name", db) 

def get_key_group_notifs(email): 
    
    db = firebase.database()
    all_users = db.child("groupNotification").get() 
    for users in all_users.each():
        a=users.val()
        
        if a['user'] == email:
            return users.key()
    return None

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


class groupNotificationSU(Screen):
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
            

kv = Builder.load_file("main.kv")

class MyMainApp(App):
    def build(self):
        return kv

if __name__ == "__main__":
    MyMainApp().run()

