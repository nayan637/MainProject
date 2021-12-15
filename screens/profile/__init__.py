from logging import RootLogger, root
from kivymd.uix.screen import MDScreen
from kivymd.uix.behaviors import HoverBehavior
from kivymd.theming import ThemableBehavior
from kivymd.uix.button import MDIconButton
from kivy.properties import NumericProperty, StringProperty
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.clock import Clock
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.button import MDRoundFlatIconButton
from kivymd.app import MDApp
from kivymd.uix.button import MDFloatingActionButtonSpeedDial
import sqlite3
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
import bcrypt
import shutil
from kivymd.utils.fitimage import FitImage
import plyer
import re

class Profile(MDScreen):
    def __init__(self,**kwargs):
        super(Profile,self).__init__(**kwargs)
        self.layout=MDFloatLayout()
        self.add_widget(self.layout)
        self.label=Label()
        self.label2=Label()
        
        self.image=FitImage(size_hint=(.05,.09),pos_hint={'x':.13,'y':.75},radius=[35,])
        self.add_widget(self.image)
        

     
    def show_notification(self):
        plyer.notification.notify(title='test', message="Notification using plyer")


    
    



        


    def Board(self,name,user):
        self.label.text=str(user)
        self.label2.text=str(name)
        if user=='user':
            c=MDApp.get_running_app().Userdata()
            sql = 'SELECT * FROM userregister WHERE name=?'
            c.execute(sql, (name,))
            myresult =c.fetchall()
            for i in myresult:
                self.ids.person.text=str(i[0])
                self.ids.email.text=str(i[1])
            

        elif user=='admin':
            c=MDApp.get_running_app().Admindata()
            sql = 'SELECT * FROM adminregister WHERE name=?'
            c.execute(sql, (name,))
            myresult =c.fetchall()
            for i in myresult:
                self.ids.person.text=str(i[0])
                self.ids.email.text=str(i[1])

    def delete_data(self,instance):
        self.popup.dismiss()
        user=self.label.text
        name=self.label2.text
        if user=='user':
            conn = sqlite3.connect(r'screens\user\db.sqlite3', check_same_thread=False)
            c = conn.cursor()
            sql = 'DELETE FROM userregister WHERE name=?'
            c.execute(sql, (name,))
            conn.commit()
            c.close()
            delete=("deleted user"+str(name))
            MDApp.get_running_app().Message(delete)
            try:
                mydir="data/profile/"+str(name)
                shutil.rmtree(mydir)
            except :
                pass
            MDApp.get_running_app().switch_screen('login')

        elif user=='admin':
            conn2 = sqlite3.connect(r'screens\admin\db.sqlite3', check_same_thread=False)
            c2 = conn2.cursor()
            sql = 'DELETE FROM adminregister WHERE name=?'
            c2.execute(sql, (name,))
            conn2.commit()
            c2.close()
            delete=("deleted admin"+str(name))
            MDApp.get_running_app().Message(delete)
            try:
                mydir="data/profile/"+str(name)
                shutil.rmtree(mydir)
            except :
                pass
            MDApp.get_running_app().switch_screen('login')

    def Message(self):
        layout = GridLayout(cols = 1, padding = 10) 
        popupLabel = Label(text="are you sure you want to delete")
        closeButton = Button(text = "Close")
        confirm=Button(text = "confirm")
        layout.add_widget(popupLabel)
        layout.add_widget(closeButton)
        layout.add_widget(confirm)
        self.popup = Popup(title='message',
    content=layout,
    size_hint=(None, None), size=(400, 400))
        self.popup.open()
        closeButton.bind(on_press = self.popup.dismiss)
        confirm.bind(on_press=self.delete_data)

    def check(self,email):   
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$' 
        if(re.search(regex,email)):   
            return True  
        else:   
            return False

            
        

    
       

        


    


Builder.load_file('profile.kv')
