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

import os
from kivy.uix.popup import Popup
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFillRoundFlatIconButton,MDRaisedButton,MDFillRoundFlatButton,MDFlatButton
import csv
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.app import App
from kivy.graphics import Rectangle, Color ,RoundedRectangle
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField,MDTextFieldRound
from kivymd.uix.button import MDFillRoundFlatIconButton,MDRaisedButton,MDFillRoundFlatButton,MDFlatButton
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
import mysql.connector
from kivy.uix.filechooser import FileChooserListView,FileSystemAbstract
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivymd.uix.dialog import MDDialog
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import time
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.tree import DecisionTreeClassifier
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
import _thread
import re



ips=[]

import urllib, json
import urllib.request



class Home(MDScreen):
    def __init__(self,**kwargs):
        super(Home,self).__init__(**kwargs)
        global ips
        global df,popup,label2,label_test,popup_loading,progress_bar
        self.l=FloatLayout()
        self.add_widget(self.l)



        self.button3=MDRaisedButton(text= "start detecting ip",pos_hint={"center_x": .5, "center_y": 0.6})
        self.l.add_widget(self.button3)
        self.button3.bind(on_press=self.show_ip)

     
              

        
        self.label = Label(pos_hint={"center_x": .5, "center_y": 0.5},size_hint=(.8,.2))
        self.l.add_widget(self.label)

        label2 = Label(pos_hint={"center_x": .5, "center_y": 0.8},size_hint=(0,0))
        self.l.add_widget(label2)

        
        label_test= Label(pos_hint={"center_x": .82, "center_y": 0.5},size_hint=(.8,.2))
        self.l.add_widget(label_test)

        self.progress_bar = ProgressBar()
        self.popup_loading = Popup(title ='loading',content = self.progress_bar)
        self.popup_loading.bind(on_open = self.open)

    
        

    def show_ip(self,instance):
        try:
            url = "http://jithu810.pythonanywhere.com/anomaly"
            response = urllib.request.urlopen(url)        
            data = json.loads(response.read())
            c=data['ip']
            s=''
            for i in c:
                #print(i)
                s=str(s+"\n"+"                   "+i+"\n")
                y=i
                print(s)
            self.label.text=("DETECTED IP AS ATTACK AND BLOCKED:"+str(s))
            _thread.start_new_thread( self.show_ip,(instance,))
        except:
            print("not connected")

    def Log(self):
        g=(label2.text)
        try:
            if g!="":
                file1 = open(g, "r")
                pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
                #traverse through lines one by one
                count=0
                t=""
                for line in file1:
                    c=pattern.search(line.strip())[0]
                    if t==c:
                        count=count+1
                    else:
                        t=c
                        count=0
                if count>=50:
                    self.dialog2=MDDialog(size_hint=[.5,.3],text="attack detected",buttons=[MDFlatButton(text="close",on_release=self.close)])
                    self.dialog2.open()
                    print("attack deteccted")
                else:
                    self.dialog3=MDDialog(size_hint=[.5,.3],text="no attacks detected",buttons=[MDFlatButton(text="close",on_release=self.close2)])
                    self.dialog3.open()
                    print("no attack")
            else:
                print("choose file")
        except:
            print("error")

    def close(self,instance):
        self.dialog2.dismiss()
                    
    def close2(self,instance):
        self.dialog3.dismiss()


    def selected2(self,files,instance):
        global popup,label2,label_test
        print(files)

    def close_dialoge2(self,instance):
        self.dialog2.dismiss()
        
    def Upload_file(self):
        global popup
        self.button2=MDFillRoundFlatButton(text= "detect",custom_color=(0, 1, 0, 1),text_color=(0, 1, 0, 1),line_color=(0, 0, 1, 1),size_hint=(.1,.05),pos_hint={'x':.78,'y':.90})
        self.l.add_widget(self.button2)
        self.button2.bind(on_press=self.pop)

        self.boxx=FloatLayout(size_hint=(1,1))
        self.gb=(FileChooserListView(filters=(['*']),size_hint=(1,1 ),pos_hint={'x':0 , 'y':0 }))
        self.gb.bind(selection=Anomaly.selected)
        self.boxx.add_widget(self.gb)
        popup = Popup(title='Choose File',
        content=self.boxx,
        size_hint=(None, None), size=(400, 400))
        popup.open()

    def Next(self,instance):
        self.manager.current="test"
        
    def pop(self, instance):
        global label2
        c=label2.text
        if c!="":
            self.progress_bar.value = 1
            self.popup_loading.open()
        else:
            self.dialog=MDDialog(size_hint=[.5,.3],text="choose file for detection",buttons=[MDFlatButton(text="close",on_release=self.close_dialoge)])
            self.dialog.open()
    def close_dialoge(self,instance):
        self.dialog.dismiss()
        

    def open(self, instance):
        Clock.schedule_interval(self.next, 1 / 25)

    def next(self, dt):
        if self.progress_bar.value>= 100:
            self.popup_loading.dismiss()
            Anomaly.shows(self)
        self.progress_bar.value += 1

    
        
class Anomaly():     
    def selected(self,files):
        global popup,label2,label_test
        global popup,label2,label_test
        label2.text=(files[0])
        
        popup.dismiss()
        try:
            cols ="""duration,
            protocol_type,
            service,
            flag,
            src_bytes,
            dst_bytes,
            land,
            wrong_fragment,
            urgent,
            hot,
            num_failed_logins,
            logged_in,
            num_compromised,
            root_shell,
            su_attempted,
            num_root,
            num_file_creations,
            num_shells,
            num_access_files,
            num_outbound_cmds,
            is_host_login,
            is_guest_login,
            count,
            srv_count,
            serror_rate,
            srv_serror_rate,
            rerror_rate,
            srv_rerror_rate,
            same_srv_rate,
            diff_srv_rate,
            srv_diff_host_rate,
            dst_host_count,
            dst_host_srv_count,
            dst_host_same_srv_rate,
            dst_host_diff_srv_rate,
            dst_host_same_src_port_rate,
            dst_host_srv_diff_host_rate,
            dst_host_serror_rate,
            dst_host_srv_serror_rate,
            dst_host_rerror_rate,
            dst_host_srv_rerror_rate"""

            columns =[]
            i=0
            for c in cols.split(','):
                #c = c.replace(',', '')
                columns.append(c)
            columns.append('target')



            attacks_types = {
                    'normal': 'normal',
            'back': 'dos',
            'buffer_overflow': 'u2r',
            'ftp_write': 'r2l',
            'guess_passwd': 'r2l',
            'imap': 'r2l',
            'ipsweep': 'probe',
            'land': 'dos',
            'loadmodule': 'u2r',
            'multihop': 'r2l',
            'neptune': 'dos',
            'nmap': 'probe',
            'perl': 'u2r',
            'phf': 'r2l',
            'pod': 'dos',
            'portsweep': 'probe',
            'rootkit': 'u2r',
            'satan': 'probe',
            'smurf': 'dos',
            'spy': 'r2l',
            'teardrop': 'dos',
            'warezclient': 'r2l',
            'warezmaster': 'r2l',
            }
            path =(files[0])
            global df
            df = pd.read_csv(path, names = columns)
            #print(df['num_root'])
            #print(df['\nnum_root'])
            # Adding Attack Type column
            df['Attack Type'] =df.target.apply(lambda r:attacks_types[r[:-1]])
            print(df['Attack Type'])
            
            # # This variable is highly correlated with num_compromised and should be ignored for analysis.
            # #(Correlation = 0.9938277978738366)
            # df.drop('\nnum_root', axis = 1, inplace = True)
            # # This variable is highly correlated with serror_rate and should be ignored for analysis.
            # #(Correlation = 0.9983615072725952)
            # df.drop('srv_serror_rate', axis = 1, inplace = True)
            
            # # This variable is highly correlated with rerror_rate and should be ignored for analysis.
            # #(Correlation = 0.9947309539817937)
            # df.drop('srv_rerror_rate', axis = 1, inplace = True)
            
            # # This variable is highly correlated with srv_serror_rate and should be ignored for analysis.
            # #(Correlation = 0.9993041091850098)
            # df.drop('dst_host_srv_serror_rate', axis = 1, inplace = True)
            
            # # This variable is highly correlated with rerror_rate and should be ignored for analysis.
            # #(Correlation = 0.9869947924956001)
            # df.drop('dst_host_serror_rate', axis = 1, inplace = True)
            
            # # This variable is highly correlated with srv_rerror_rate and should be ignored for analysis.
            # #(Correlation = 0.9821663427308375)
            # df.drop('dst_host_rerror_rate', axis = 1, inplace = True)
            
            # # This variable is highly correlated with rerror_rate and should be ignored for analysis.
            # #(Correlation = 0.9851995540751249)
            # df.drop('dst_host_srv_rerror_rate', axis = 1, inplace = True)
            
            # # This variable is highly correlated with srv_rerror_rate and should be ignored for analysis.
            # #(Correlation = 0.9865705438845669)
            # df.drop('dst_host_same_srv_rate', axis = 1, inplace = True)
            

            # Target variable and train set
            y = df[['Attack Type']]
            print(y)
            X = df.drop(['Attack Type', ], axis = 1)

            sc = MinMaxScaler()
            X = sc.fit_transform(X)

            # Split test and train data
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.33, random_state = 42)

            clfd = DecisionTreeClassifier(criterion ="entropy", max_depth = 4)
            start_time = time.time()
            clfd.fit(X_train, y_train.values.ravel())
            end_time = time.time()
            print("Training time: ", end_time-start_time)


            start_time = time.time()
            y_test_pred = clfd.predict(X_train)
            end_time = time.time()
            print("Testing time: ", end_time-start_time)



            print("Train score is:", clfd.score(X_train, y_train))
            print("Test score is:", clfd.score(X_test, y_test))

        except:
            print("error")



        




        
        #df.isnull().sum()

    def shows(self):
        global label,label_text
        mm=df['target'].value_counts()
        label_test.text=str(mm)

    def Data(self):
        print(df.head())
        


    
    


Builder.load_file('dashboard.kv')
