from logging import  root

from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.screen import MDScreen

from kivy.properties import NumericProperty, StringProperty
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.clock import Clock
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.button import MDFillRoundFlatButton

from kivymd.app import MDApp
from kivy.uix.button import Button

from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput

import os
from kivy.animation import Animation
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import NumericProperty
from kivy.uix.behaviors import ButtonBehavior

from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.behaviors import RectangularRippleBehavior
from . database import *
from kivy.uix.gridlayout import GridLayout
import bcrypt
import re 
import smtplib 

class Login(MDScreen):
    open_field_box = 0
    increment_width = NumericProperty(0)
    increment_height = NumericProperty(0)
    def __init__(self,**kwargs):
        super(Login,self).__init__(**kwargs)
        self.layout=MDFloatLayout()
        self.add_widget(self.layout)

    def Newregister(self,instance):
        layout = GridLayout(cols = 2, padding = 10) 
        popupLabel = Label(text='name')
        layout.add_widget(popupLabel)
        self.textinput1=TextInput()
        layout.add_widget(self.textinput1)
        popupLabel1 = Label(text='email')
        layout.add_widget(popupLabel1)
        self.textinput2=TextInput()
        layout.add_widget(self.textinput2)
        popupLabel2 = Label(text='password')
        layout.add_widget(popupLabel2)
        self.textinput3=TextInput(password=True)
        layout.add_widget(self.textinput3)
        popupLabel2 = Label(text='confirm password')
        layout.add_widget(popupLabel2)
        self.textinput4=TextInput(password=True)
        layout.add_widget(self.textinput4)
        registerButton = Button(text = "register") 
        layout.add_widget(registerButton) 
        closeButton = Button(text = "Close") 
        layout.add_widget(closeButton)   
        self.popup = Popup(title='register',
    content=layout,
    size_hint=(None, None), size=(700, 700))
        self.popup.open()
        registerButton.bind(on_press=self.Registeruser)
        closeButton.bind(on_press = self.popup.dismiss)




    def Registeruser(self,instance):
        name=self.textinput1.text
        email=self.textinput2.text
        password=self.textinput3.text
        password2=self.textinput4.text
        if name!="" and password!="":
            if password==password2:
                if self.check(email)==True:
                    conn = sqlite3.connect(r'screens\user\db.sqlite3', check_same_thread=False)
                    c = conn.cursor()
                    sql = 'SELECT * FROM userregister WHERE name=?'
                    c.execute(sql, (name,))
                    conn.commit()
                    myresult =c.fetchall()
                    if (len(myresult)) == 0:
                        password = bytes(password, 'utf-8')
                        password = bcrypt.hashpw(password, bcrypt.gensalt(14))
                        c.execute("""INSERT INTO userregister (name, email,password) values (?,?,?)""",(name,email,password))
                        conn.commit()
                        self.popup.dismiss()
                        self.textinput1.text=""
                        self.textinput2.text=""
                        self.textinput3.text=""
                        self.textinput4.text="" 
                        new=('created new user: '+str(name))
                        MDApp.get_running_app().Message(new)
                    else:
                        self.textinput1.text=""
                        self.textinput2.text=""
                        self.textinput3.text=""
                        self.textinput4.text=""
                        MDApp.get_running_app().Message('user already exists') 
                else:
                    MDApp.get_running_app().Message('please enter a valid email address') 
            else:
                MDApp.get_running_app().Message('password does not match')    
        else:
            MDApp.get_running_app().Message('invalid please try again')

    def check(self,email):   
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$' 
        if(re.search(regex,email)):   
            return True  
        else:   
            return False

    # def Admin_login(self,instance):   
    #     from datetime import date
    #     from datetime import datetime
    #     today = date.today()
    #     now = datetime.now()
    #     current_time = now.strftime("%H:%M:%S")
    #     name=self.field1.text
    #     password=self.field2.text 
    #     if name=='admin' and password=='admin':
    #         MDApp.get_running_app().progress()
    #         MDApp.get_running_app().click_sound
    #         MDApp.get_running_app().Admin()
    #         MDApp.get_running_app().Username(name,'admin')
    #         MDApp.get_running_app().switch_screen('mainpage')
    #         self.field1.text=""
    #         self.field2.text=""
    #     password = bytes(password, 'utf-8')
    #     conn = sqlite3.connect(r'screens\admin\db.sqlite3', check_same_thread=False)
    #     c = conn.cursor()
    #     sql="SELECT * FROM adminregister WHERE name=?"
    #     c.execute(sql, (name,))
    #     conn.commit()
    #     myresult =c.fetchall()
    #     for x in range(0,len(myresult)):
    #         hashed=myresult[x][2]
    #         if bcrypt.checkpw(password, hashed):
    #             c.close
    #             conn = sqlite3.connect(r'screens\cloud\db.sqlite3', check_same_thread=False)
    #             c = conn.cursor()
    #             c.execute("""INSERT INTO history (name, date,time) values (?,?,?)""",("admin "+name,today,current_time))
    #             conn.commit()
    #             MDApp.get_running_app().progress()
    #             MDApp.get_running_app().click_sound
    #             MDApp.get_running_app().Admin()
    #             MDApp.get_running_app().Username(name,'admin')
    #             welcome=('welcome: '+str(name))
    #             MDApp.get_running_app().Message(welcome)
    #             MDApp.get_running_app().switch_screen('mainpage')
    #             self.field1.text=""
    #             self.field2.text=""
    #         else:
    #             msg=('incorrect username or password')
    #             MDApp.get_running_app().Message(msg) 
    #             self.field1.text=""
    #             self.field2.text="" 
    #     self.field1.text=""
    #     self.field2.text="" 



    def User_login(self,instance):
        from datetime import date
        from datetime import datetime
        today = date.today()
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        name=self.field1.text
        password=self.field2.text 
        if name=='admin' and password=='admin':
            MDApp.get_running_app().progress()
            MDApp.get_running_app().click_sound
            MDApp.get_running_app().Admin()
            MDApp.get_running_app().Username(name,'admin')
            MDApp.get_running_app().switch_screen('mainpage')
            self.field1.text=""
            self.field2.text=""
        password = bytes(password, 'utf-8')
        conn = sqlite3.connect(r'screens\user\db.sqlite3', check_same_thread=False)
        c = conn.cursor()
        sql = 'SELECT * FROM userregister WHERE name=?'
        c.execute(sql, (name,))
        conn.commit()
        myresult =c.fetchall()
        for x in range(0,len(myresult)):
            hashed=myresult[x][2]
            if bcrypt.checkpw(password, hashed):
                c.close
                conn = sqlite3.connect(r'screens\cloud\db.sqlite3', check_same_thread=False)
                c = conn.cursor()
                c.execute("""INSERT INTO history (name, date,time) values (?,?,?)""",("user "+name,today,current_time))
                conn.commit()
                MDApp.get_running_app().progress()
                MDApp.get_running_app().click_sound
                MDApp.get_running_app().User()
                self.field1.text=""
                self.field2.text=""
                MDApp.get_running_app().Username(name,'user')
                welcome=('welcome: '+str(name))
                MDApp.get_running_app().Message(welcome)
                MDApp.get_running_app().switch_screen('mainpage')
            else:
                self.field1.text=""
                self.field2.text="" 
                msg=('incorrect username or password')
                MDApp.get_running_app().Message(msg) 
        self.field1.text=""
        self.field2.text="" 

    def register(self,instance):
        MDApp.get_running_app().switch_screen('register')
        MDApp.get_running_app().click_sound



    def on_size(self, *args):
        if self.open_field_box:
            self.ids.signin_button.width = self.width - dp(0)

    def on_enter(self):
        Animation(x=-dp(300), d=30).start(self.ids.bg_image)

    def stopanimation(self):
        self.ids.signin_button.size=(100,100)
        self.ids.signin_button.pos_hint={'x':.25,'y':.2}
    

    def start_animation(self):
        self.butt1=MDFillRoundFlatButton(pos_hint={'x':.42,'y':.14},size_hint=(.2,.05),text="LOGIN")
        self.butt1.bind(on_press=self.User_login)
        self.add_widget(self.butt1)

        self.forgetbutton=MDFillRoundFlatButton(pos_hint={'x':.47,'y':.11},size_hint=(.1,.02),text="forgot password")
        self.forgetbutton.bind(on_press=self.verifyemail)
        self.add_widget(self.forgetbutton)
        
        self.butt3=MDFillRoundFlatButton(pos_hint={'x':.42,'y':.05},size_hint=(.2,.05),text="REGISTER")
        self.butt3.bind(on_press=self.Newregister)
        self.add_widget(self.butt3)

        Animation(opacity=0, d=0.8).start(self.ids.check_box)
        Animation(opacity=0, d=0.8).start(self.ids.point_box)
        Animation(opacity=0, d=0.8).start(self.ids.login_button)
        Animation(opacity=0, d=0.8).start(self.ids.signin_label)

        self.anim_transform_button = Animation(
            increment_width=dp(140),
            increment_height=dp(270),
            d=1.2,
            t="out_quart",
        )
        self.anim_transform_button.bind(on_progress=self.anim_transform_button_progress)
        self.anim_transform_button.start(self)
        self.f=Animation(
            y=self.height - dp(486),
            d=2.2,
            t="out_quart",
        ).start(self.ids.signin_button)

    def anim_transform_button_progress(self, animation, instance, value):
        def set_focus(*args):
            self.ids.signin_button.children[-2].focus = True

        if value > 0.5 and not self.open_field_box:
            self.open_field_box = True
            height = 14
            duration = 0.8
            pos_x = 0

            height += 84
            duration += 0.2
            pos_x -= 0
            self.field1 = MDTextField(
                x=dp(pos_x),
                hint_text="name",
                size_hint_x=None,
                y=self.ids.signin_button.height - dp(height),
                width=self.ids.signin_button.width - dp(72),
                opacity=0,
            )
            self.field2 = MDTextField(
                x=dp(pos_x),
                hint_text="password",
                 password=True,
                size_hint_x=None,
                y=dp(102),
                width=self.ids.signin_button.width - dp(72),
                opacity=0,
            )
            self.field1.color_mode = "accent"
            self.ids.signin_button.add_widget(self.field1)
            self.ids.signin_button.add_widget(self.field2)

            self.animation = Animation(x=dp(66), opacity=1, t="out_quart", d=duration)
            if duration > 1.5:
                self.animation.bind(on_complete=set_focus)
            self.animation.start(self.field1)
            self.animation.start(self.field2)

    def Createuser(self,instance):
        MDApp.get_running_app().switch_screen('user')


    def verifyemail(self,instance):
        layout = GridLayout(cols = 2, padding = 10) 
        email = Label(text='email')
        layout.add_widget(email)
        self.email=TextInput()
        layout.add_widget(self.email)
        registerButton = Button(text = "confirm email") 
        layout.add_widget(registerButton) 
        closeButton = Button(text = "Close") 
        layout.add_widget(closeButton)   
        self.popup = Popup(title='email',
    content=layout,
    size_hint=(None, None), size=(700, 300))
        self.popup.open()
        registerButton.bind(on_press=self.checkemailexists)
        closeButton.bind(on_press = self.popup.dismiss)

    def checkemailexists(self,instance):
        conn = sqlite3.connect(r'screens\user\db.sqlite3', check_same_thread=False)
        c = conn.cursor()
        sql = 'SELECT * FROM userregister WHERE email=?'
        c.execute(sql, (self.email.text,))
        conn.commit()
        myresult =c.fetchall()
        if (len(myresult)) == 0:
            MDApp.get_running_app().Message("account not found")
        else:
            
            from numpy import random
            global x
            x = random.randint(10000)
            self.popup.dismiss()
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls() 
            s.login("anomalydetection123@gmail.com", "anomaly@123") 
            SUBJECT = "kivy"   
            TEXT = ("hello"+str(" reset your password"))
            message='Subject: {}\n\n{}'.format(SUBJECT, x)
            s.sendmail("anomalydetection123@gmail.com", self.email.text, message) 
            s.quit() 
            
    
            layout = GridLayout(cols = 2, padding = 10) 
            code = Label(text='Code')
            layout.add_widget(code)
            self.code=TextInput()
            layout.add_widget(self.code)
            registerButton = Button(text = "enter code") 
            layout.add_widget(registerButton) 
            closeButton = Button(text = "Close") 
            layout.add_widget(closeButton)   
            self.popup = Popup(title='code send to email',
        content=layout,
        size_hint=(None, None), size=(700, 300))
            self.popup.open()
            registerButton.bind(on_press=self.verifycode)
            closeButton.bind(on_press = self.popup.dismiss)

    def verifycode(self,instance):
        if int(self.code.text)==x:
            self.popup.dismiss()
            layout = GridLayout(cols = 2, padding = 10) 
            pass1 = Label(text='new password')
            layout.add_widget(pass1)
            self.pass1=TextInput(password=True)
            layout.add_widget(self.pass1)
            pass2 = Label(text='confirm password')
            layout.add_widget(pass2)
            self.pass2=TextInput(password=True)
            layout.add_widget(self.pass2)
            changepass = Button(text = "confirm") 
            layout.add_widget(changepass) 
            closeButton = Button(text = "Close") 
            layout.add_widget(closeButton)   
            self.popup = Popup(title='code',
        content=layout,
        size_hint=(None, None), size=(700, 400))
            self.popup.open()
            changepass.bind(on_press=self.changepassword)
            closeButton.bind(on_press = self.popup.dismiss)
        else:
            MDApp.get_running_app().Message("incorrect code")

    def changepassword(self,instance):
        a=self.pass1.text
        b=self.pass2.text
        if a!="" and b!="":
            if a==b:
                password = bytes(a, 'utf-8')
                password = bcrypt.hashpw(password, bcrypt.gensalt(14))
                conn = sqlite3.connect(r'screens\user\db.sqlite3', check_same_thread=False)
                c = conn.cursor()
                c.execute('''UPDATE userregister SET password = ? WHERE email = ?''', (password,self.email.text))            
                conn.commit()
                self.popup.dismiss()
                MDApp.get_running_app().Message("password changed successfully")
                MDApp.get_running_app().switch_screen('login')

            else:
                MDApp.get_running_app().Message("password dosent match")
        else:
            MDApp.get_running_app().Message("please enter fields")




class CustomButton(
    MDRelativeLayout,
    RectangularRippleBehavior,
    ButtonBehavior,
):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = [1, 1, 1, 1]
        self.ripple_color = [0.7, 0.7, 0.7, 1]
        self.radius = [8, ]



    


Builder.load_file('login.kv')
