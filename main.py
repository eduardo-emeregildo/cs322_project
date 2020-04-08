from kivy.app import App
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.graphics.context_instructions import Color
from kivy.uix.screenmanager import ScreenManager, Screen

class HomeWindow(Screen):
	pass

class SignupWindow(Screen):
    pass

kv = Builder.load_file("main.kv")

class MyMainApp(App):
    def build(self):
        return kv

if __name__ == "__main__":
    MyMainApp().run()





#----------------------------------------------------------------------------------------

#class main_kv(GridLayout):
 #   pass



#class MainApp(App):
#   def build(self):
#        return main_kv()


#MainApp().run()
