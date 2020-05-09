## cs322_project
## all windows


## WelcomeScreen: (welcomeScreen.kv)
just a dummy screen to initialize the home window

## HomeWindow: (homeWindow.kv)
system home window visible to everyone

## HomeOUWindow: (homeOUWindow.kv)
when an OU logs in, this window will open, has 'notification' button

## HomeSUWindow: (homeSUWindow.kv)
when an SU logs in, this window will open, has 'profile' and 'notification' buttons

## ProfileWindow: (profileWindow.kv)
for the OU. they can see the blackbox whitebox, top three warnings, their groups and '+create group' button

# NotificationSU: (notificationsSU.kv)
SU notification page. all new join requests will appear here

## ComplimentPage: (complimentNotificationSU.kv)
SU compliments notification page, all compliments will appear here

## groupNotificationSU: (groupNotificationSU.kv)
SU group notification page. all group closing requests will appear here

## WarningPage: (warningNotificationSU.kv)
SU warning notifications page. all warnings will appear here


## groupNotificationOU: (groupNotificationOU.kv)
OU group notification page. Only the groups they are part of will appear here

## WarningPageOU: (warningNotificationOU.kv)
all warnings for the OU will appear here

## SignupWindow: (signupWindow.kv)
a visitor can signup here

## DescriptionWindow: (requestDescriptionSU.kv)
an SU can see the request details here

## CreateGroupWindow: (createGroupWindow.kv)
new groups can be created here

## GroupWindow: (groupWindow.kv)
once a group is created, this will be the group page

## VisitorView: (visitorViewProfile.kv)
a random visitor will see this view of the OU profile. they can only complain from this page

## VisitorViewLoggedIn: (visitorViewLoggedIn.kv)
a logged in OU will see this page as another OU's profile. they can complain, send compliment and rate the projects from here  
    
    
    
## Additional Files

## popupWindow.kv
popup with textinput

## main.kv
all screens are listed here (except popup)

## importModules.py
most of the modules, the database and configuration are stored here

## signingDetails.py
all functions and classes Eduardo is working on can be found here except the 'HomeWindow' class

## groupPageFunctions.py
all classes and functions Diana is working on can be found here

## homepageOUmain.py
most of the functions that can be used for both SU and OU (Maliha is working on) can be found here

## otherWindows.py
all functions and classes Maliha is working on can be found here

## main.py
the 'HomeWindow' class can be found here. also contains the main functions


## Please feel free to keep everything in the main if you want. Just copy paste everything in the main from all the .py files. Should work




    
    
    
    
    
    
    
    
    
  

