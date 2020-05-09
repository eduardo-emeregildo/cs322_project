from functools import partial

from kivy.app import App
from kivy.graphics.vertex_instructions import Rectangle
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.graphics.context_instructions import Color
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty,StringProperty,NumericProperty,DictProperty
from kivy.uix.boxlayout import BoxLayout
import smtplib #emails
import pyrebase
import requests
import re #regex


#from populateDatabase import *

# to connect to firebase, project database cs322
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

firebase = pyrebase.initialize_app(config) 
db = firebase.database()