from kivy.app import App
from kivy.uix.widget import Widget
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
from kivymd.uix.button import MDRoundFlatIconButton,MDRectangleFlatButton
from kivymd.app import MDApp
from kivymd.uix.progressbar import MDProgressBar
from kivy.properties import StringProperty
from kivymd.toast import toast
from kivymd.uix.bottomsheet import MDGridBottomSheet
from kivymd.uix.chip import MDChip
from kivymd.uix.filemanager import MDFileManager
from kivy.core.window import Window
from kivymd.uix.taptargetview import MDTapTargetView
from kivymd.uix.textfield import MDTextField
from ..cloud import Cloud
from screens import cloud
from kivymd.uix.label import MDLabel
import sqlite3
import time    
from datetime import timedelta
from kivy.clock import Clock
from datetime import datetime
from datetime import date
from kivy.uix.switch import Switch
import glob
import shutil
import os
from kivymd.utils.fitimage import FitImage
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.image import Image, AsyncImage


class Mainpage(MDScreen):
    state = StringProperty("stop")
    def __init__(self,**kwargs):
        super(Mainpage,self).__init__(**kwargs)
        self.now = datetime.now()
        today = date.today()
        Clock.schedule_interval(self.update_clock, 1)
        self.layout=MDFloatLayout()
        self.add_widget(self.layout)
        self.cloud=cloud.Cloud()
        self.label=Label()
        Window.bind(on_keyboard=self.events)
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            ext=[".py", "kv",".vmem",".jpg",".jpeg",".png"],
        )
        self.time=MDLabel(text= self.now.strftime('%H:%M:%S'),size_hint=(.05,.1),pos_hint={'x':.91,'y':.89},color=(1,1,1,1))
        self.layout.add_widget(self.time)
        self.date=MDLabel(text=str(today),size_hint=(.1,.2),pos_hint={'x':.90,'y':.88},color=(1,1,1,1))
        self.layout.add_widget(self.date)
        self.person=MDRoundFlatIconButton(text_color=(1, 0, 0, 1),line_color=(1, 1, 1, 1),icon_color=(1, 0, 0, 1),icon="account",pos_hint={'x':.17,'y':.93})
        self.person.bind(on_press=self.profile)
        self.layout.add_widget(self.person)
        self.image=FitImage(size_hint=(.03,.05),pos_hint={'x':.12,'y':.93},radius=[30,])
        self.add_widget(self.image)
        self.img = Image(source ='data/images/front.jpg')
        self.img.allow_stretch = True
        self.img.keep_ratio = False


        self.img.size_hint_x = .87
        self.img.size_hint_y = .6
        self.img.pos = (100, 100)
        self.img.opacity = 1
   
        self.layout.add_widget(self.img)
        


    def exitMessage(self):
        layout = GridLayout(cols = 1, padding = 10) 
        popupLabel = Label(text="are you sure you want to exit app")
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
        confirm.bind(on_press=self.exit)

    def exit(self,instance):
        MDApp.get_running_app().stop()

       

    def update_clock(self, *args):
        self.now = self.now + timedelta(seconds = 1)
        self.time.text = self.now.strftime('%H:%M:%S')

    def profile(self,instance):
        MDApp.get_running_app().progress()
        MDApp.get_running_app().click_sound
        MDApp.get_running_app().switch_screen('profile')

    def file_manager_open(self):
        self.file_manager.show('/')  
        self.manager_open = True
    

    def select_path(self, path):
        global selected
        self.exit_manager()
        toast(path)
        selectedfile = str(path)
        try:
            mydir="data/profile/"+str(self.person.text)
            shutil.rmtree(mydir)
        except :
            pass
        directory="data/profile/"+str(self.person.text)

        filename=path.split("\\")
        selected=(filename[-1])

        extention=selected.split(".")
        extentionname=(extention[1])

        if not os.path.exists(directory):
            os.makedirs(directory)
        shutil.copy(selectedfile, mydir)
        for count,filename in enumerate(os.listdir("data/profile/"+str(self.person.text))): 
            try:
                dst ="data/profile/"+str(self.person.text)+"/"+str(self.person.text) + str(count) + "."+str(extentionname)
                src ="data/profile/"+str(self.person.text)+ "/"+filename
                os.rename(src, dst)
                MDApp.get_running_app().profile.image.source="data/profile/"+str(self.person.text)+"/"+str(self.person.text) + str(count) + "."+str(extentionname) 
                MDApp.get_running_app().mainpage.image.source="data/profile/"+str(self.person.text)+"/"+str(self.person.text) + str(count) + "."+str(extentionname) 
                MDApp.get_running_app().profile.image.reload()
                MDApp.get_running_app().mainpage.image.reload()
                
            except :
                pass       

    def exit_manager(self, *args):
        self.manager_open = False
        self.file_manager.close()
    def events(self, instance, keyboard, keycode, text, modifiers):
        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
        return True

    def fetch(self, chip_instance):
        if chip_instance.check == True:
            print("True")
        else:
            print("False")

    def callback_for_menu_items(self, *args):
        toast(args[0])

    def show_example_grid_bottom_sheet(self):
        bottom_sheet_menu = MDGridBottomSheet()
        data = {
            "Facebook": "facebook-box",
            "YouTube": "youtube",
            "Cloud": "cloud-upload",
            "Camera": "camera",
        }
        for item in data.items():
            bottom_sheet_menu.add_item(
                item[0],
                lambda x, y=item[0]: self.callback_for_menu_items(y),
                icon_src=item[1],
            )
        bottom_sheet_menu.open()
        


    def on_state(self, instance, value):
        self.progressbar=MDProgressBar(pos_hint={"center_y": .6},type="indeterminate",running_duration= 1)

        self.layout.add_widget(self.progressbar)
        {
            "start": self.progressbar.start,
            "stop": self.progressbar.stop,

        }.get(value)()
        
 

       

      


    


Builder.load_file('mainpage.kv')
