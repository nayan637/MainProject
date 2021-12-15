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
from kivymd.app import MDApp
from . database import *
import bcrypt
import re

class User(MDScreen):
    def __init__(self,**kwargs):
        super(User,self).__init__(**kwargs)
        self.layout=MDFloatLayout()
        self.add_widget(self.layout)
        self.label=Label()
        self.label2=Label()

    def Clean(self):
        self.ids.usename.text=""
        self.ids.email.text=""
        self.ids.password.text=""
        self.ids.password2.text=""
        
    def Updateprofile(self):
        name=self.ids.usename.text
        email=self.ids.email.text
        password=self.ids.password.text
        password2=self.ids.password2.text
        if name!="" and password!="":
            if password==password2:
                if self.check(email)==True:
                    c=MDApp.get_running_app().Userdata()
                    conn.execute('''UPDATE userregister SET name = ? ,email = ? ,password = ? WHERE name = ?''', (name,email,password,name))            
                    conn.commit()
                    self.ids.usename.text=""
                    self.ids.email.text=""
                    self.ids.password.text=""
                    self.ids.password2.text="" 
                    MDApp.get_running_app().Message('updated successfully') 
                    MDApp.get_running_app().switch_screen('profile')
                else:
                    MDApp.get_running_app().Message('please enter a valid email address') 
            else:
                MDApp.get_running_app().Message('password does not match')    
        else:      
            MDApp.get_running_app().Message('invalid please try again')





    def submit(self):
        name=self.ids.usename.text
        email=self.ids.email.text
        password=self.ids.password.text 
        password2=self.ids.password2.text
        if name!="" and password!="":
            if password==password2:
                if self.check(email)==True:
                    password = bytes(password, 'utf-8')
                    password = bcrypt.hashpw(password, bcrypt.gensalt(14))
                    conn = sqlite3.connect(r'screens\user\db.sqlite3', check_same_thread=False)
                    c = conn.cursor()
                    sql = 'SELECT * FROM userregister WHERE name=?'
                    c.execute(sql, (name,))
                    conn.commit()
                    myresult =c.fetchall()
                    if (len(myresult)) == 0:
                        c.execute("""INSERT INTO userregister (name, email,password) values (?,?,?)""",(name,email,password))
                        conn.commit()
                        self.ids.usename.text=""
                        self.ids.email.text=""
                        self.ids.password.text=""
                        self.ids.password2.text="" 
                        new=('created new user: '+str(name))
                        MDApp.get_running_app().Message(new)
                    else:
                        self.ids.usename.text=""
                        self.ids.email.text=""
                        self.ids.password.text=""
                        self.ids.password2.text=""
                        MDApp.get_running_app().Message('user already exists')
                else:
                    MDApp.get_running_app().Message('please enter a valid email address') 
            else:
                MDApp.get_running_app().Message('password does not match')    
        else:
            MDApp.get_running_app().Message('invalid please try again')


    def display_name(self,name):
        c=MDApp.get_running_app().Userdata()
        sql = 'SELECT * FROM userregister WHERE name=?'
        c.execute(sql, (name,))
        conn.commit()
        myresult =c.fetchall()
        for i in myresult:
            self.ids.usename.text=i[0]
            self.ids.email.text=i[1]

    def check(self,email):   
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$' 
        if(re.search(regex,email)):   
            return True  
        else:   
            return False
                
            
            

        



        




       

        


    


Builder.load_file('user.kv')
