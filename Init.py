# -*- coding: utf-8 -*-
from kivy.lang import Builder
from kivy.support import install_twisted_reactor
install_twisted_reactor()
from twisted.internet import reactor, protocol
from twisted.internet.protocol import ReconnectingClientFactory
from twisted.spread import pb

import mysql.connector
from kivy.uix.widget import Widget
import kivy
from kivy.uix.screenmanager import Screen
import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.properties import NumericProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
import os
os.environ['KIVY_GL_BACKEND'] = 'gl'
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition, CardTransition
from kivy.core.text import LabelBase
from threading import Thread
import time
from time import sleep
import schedule
from gtts import gTTS
from kivy.uix.popup import Popup
from kivy.garden.circulardatetimepicker import CircularTimePicker
from kivy.uix.carousel import Carousel


from kivy.clock import Clock
import datetime
from datetime import timedelta
from kivy.core.window import Window
from kivy.uix.behaviors import ButtonBehavior
from google.cloud import texttospeech
#Window.size = (720, 1280)


Builder.load_string("""
<MainScreen>:
    RelativeLayout:
        canvas:
            Color:
                rgb:0 ,0 , 0
            Rectangle:    
                size: self.size
                pos: self.pos


        Label:
            text:"MEMENTO OS"
            font_size: self.height*0.09
            pos_hint:{"x":0,"y":.40}
            font_name:"Anurati" 



        Button:
        
            size_hint:.7,.7
            pos_hint:{'center_x':.5,'center_y':.6}
            background_color: 0,0,0,0
            on_press:root.manager.current='menu'
            Image:
                source: 'main.zip'
                y: self.parent.y
                x: self.parent.x
                size: self.parent.size
                allow_stretch: True
                anim_delay:0.05 
        Label:
            
            id:timer
            text:self.text
            pos_hint:{'center_x':.5,"center_y":.35}
            font_name:"Calibri"
            font_size: self.height*0.09
        Label:
            text:'Temperatura'
            font_name:"Calibri"
            font_size: self.height*0.03
            pos_hint:{'center_x':.2,"center_y":.25}
        WeatherLabel:
            id:temp
            pos_hint:{'center_x':.2,"center_y":.12}
            text:self.text
            font_name:"Calibri"
            font_size: self.height*0.09
            on_touch_down: self.on_touch_down
            size_hint: .3,.3
            canvas:
                Color:
                    rgb: 1,0,1
                Line:
                    circle:self.center_x, self.center_y,70, 0, 360
                    width: 3
                
        Label:
            text:'Wilgotność'
            font_name:"Calibri"
            font_size: self.height*0.03
            pos_hint:{'center_x':.5,"center_y":.25}
        WeatherLabel:
            id:humidity
            pos_hint:{'center_x':.5,"center_y":.12}
            text:self.text
            font_name:"Calibri"
            font_size: self.height*0.09
            on_touch_down: self.on_touch_down
            size_hint: .3,.3
            canvas:
                Color:
                    rgb: 1,0,1
                Line:
                    circle:self.center_x, self.center_y,70, 0, 360
                    width: 3
        Label:
            text:'Powietrze'
            font_name:"Calibri"
            font_size: self.height*0.03
            pos_hint:{'center_x':.8,"center_y":.25}
        WeatherLabel:
            id:dust
            pos_hint:{'center_x':.8,"center_y":.12}
            text:self.text
            font_name:"Calibri"
            font_size: self.height*0.09
            on_touch_down: self.on_touch_down
            size_hint: .3,.3
            canvas:
                Color:
                    rgb: 1,0,1
                Line:
                    circle:self.center_x, self.center_y,70, 0, 360
                    width: 3
            
        
<Menu>:
    RelativeLayout:
        canvas:
            Color:
                rgb:0 ,0 , 0
            Rectangle:    
                size: self.size
                pos: self.pos
        Label:
            text:"MENU"
            font_size: self.height*0.09
            pos_hint:{"x":0,"y":.40}
            font_name:"Anurati"
        ImageButton:  
            source:'img/hexagon1b.png'  
            size_hint: .2, .2 
            pos_hint:{'center_x':.5,'center_y':.6}
            on_press:root.manager.current='main'
            
            MenuLabel:
                font_name:"Anurati"
                text:"M"
                
        ImageButton:  
            source:'img/hexagon1bl.png'  
            size_hint: .2, .2 
            pos_hint:{'center_x':.63,'center_y':.73}
            on_press:root.manager.current='lights'
            MenuLabel:
                
                text:u'\uf0eb'
        ImageButton:  
            source:'img/hexagon1s.png'  
            size_hint: .2, .2 
            pos_hint:{'center_x':.37,'center_y':.73}
            MenuLabel:
                
                text:u'\uf023'
        ImageButton:  
            source:'img/hexagon1br.png'  
            size_hint: .2, .2 
            pos_hint:{'center_x':.73,'center_y':.6}
            on_press:root.manager.current='wake'
            MenuLabel:
                
                text:u'\uf017'
        ImageButton:  
            source:'img/hexagon1gr.png'  
            size_hint: .2, .2 
            pos_hint:{'center_x':.27,'center_y':.6}
            on_press:app.sys_suspend()
            MenuLabel:
                
                text:u'\uf236'
        ImageButton:  
            source:'img/hexagon1g.png'  
            size_hint: .2, .2 
            pos_hint:{'center_x':.37,'center_y':.47}
            on_press:root.manager.current='cam'
            on_press:root.manager.get_screen('cam').ids.camera.play=True
            MenuLabel:
                
                text:u'\uf03d'
        ImageButton:  
            source:'img/hexagon1p.png'  
            size_hint: .2, .2 
            pos_hint:{'center_x':.63,'center_y':.47}
            MenuLabel:
                
                text:u'\uf128'
<Lights>:
    RelativeLayout:
    RelativeLayout:
        canvas:
            Color:
                rgb:0 ,0 , 0
            Rectangle:    
                size: self.size
                pos: self.pos
        Label:
            text:"LIGHTS"
            font_size: self.height*0.09
            pos_hint:{"x":0,"y":.40}
            font_name:"Anurati"
            
        Label:
            text:"GÓRA"
            font_size: self.height*0.1
            pos_hint:{"center_x":.5,"center_y":.7}
            font_name:"Calibri"
        Button:
            id:1
            text:u'\uf011'
            
            font_size: self.height*0.4
            size_hint:.1,.2
            pos_hint:{"center_x":.5,"center_y":.55}
            font_name:"awesome"
            background_color: 0,0,0,0
            on_press:root.switch(3)
        
            
        Label:
            text:"DÓL"
            font_size: self.height*0.1
            pos_hint:{"center_x":.5,"center_y":.4}
            font_name:"Calibri"
        Button:
            id:2
            text:u'\uf011'
            
            font_size: self.height*0.4
            size_hint:.1,.2
            pos_hint:{"center_x":.5,"center_y":.30}
            font_name:"awesome"
            background_color: 0,0,0,0
            on_press:root.switch(2)
        Button:
            id:1
            text:u'\uf0a8'
            
            font_size: self.height*0.4
            size_hint:.1,.2
            pos_hint:{"center_x":.5,"center_y":.1}
            font_name:"awesome"
            background_color: 0,0,0,0
            on_press:root.manager.current='menu'
            on_press:app.mainscreen()
<Cam>:
    RelativeLayout:
        canvas:
            Color:
                rgb:0 ,0 , 0
            Rectangle:    
                size: self.size
                pos: self.pos
        Label:
            text:"CAMERA"
            font_size: self.height*0.09
            pos_hint:{"x":0,"y":.40}
            font_name:"Anurati"
        BoxLayout:
            pos_hint:{"center_x":.5,"center_y":.6}
            size_hint:1,.3
            Camera:
                id: camera
                resolution: (640, 480)
                play: False
                
        Button:
            id:1
            text:u'\uf0a8'
            
            font_size: self.height*0.4
            size_hint:.1,.2
            pos_hint:{"center_x":.5,"center_y":.1}
            font_name:"awesome"
            background_color: 0,0,0,0
            on_press:root.manager.current='menu'
            on_press: camera.play = False
            on_press:app.mainscreen()
<WakeUp>:
    RelativeLayout:
        
        Button:
            id:1
            text:u'\uf0a8'
            
            font_size: self.height*0.4
            size_hint:.1,.2
            pos_hint:{"center_x":.5,"center_y":.1}
            font_name:"awesome"
            background_color: 0,0,0,0
            on_press:root.manager.current='menu'
            on_press:root.get_time()
            on_press:app.mainscreen()
    
    
<MenuLabel@Label>:
    pos: self.parent.x+10,self.parent.y+45
    font_name:"awesome"
    font_size: self.height*0.7
    
    
            
        
        
    
        
        

            
            
        
    
        
    
            
            
                    """)
LabelBase.register(name="Anurati",fn_regular="Anurati-Regular.otf")
LabelBase.register(name="Calibri",fn_regular="calibril.ttf")
LabelBase.register(name="awesome",fn_regular="fontawesome-webfont.ttf")
tts=texttospeech.TextToSpeechClient()
voice=texttospeech.types.VoiceSelectionParams(language_code='pl-PL', name='pl-PL-Wavenet-C')
audio_config = texttospeech.types.AudioConfig(audio_encoding=texttospeech.enums.AudioEncoding.MP3)
class Eva(object):
    def __init__(self,text=''):


        self.text=text

    def talk(self,text):
        pass
        synthesis_input = texttospeech.types.SynthesisInput(text=text)
        response = tts.synthesize_speech(synthesis_input, voice, audio_config)
        with open('output.mp3', 'wb') as out:
            out.write(response.audio_content)
        os.system('play output.mp3')



eva=Eva()

class WeatherLabel(Label):
    def __init__(self,**kwargs):
        super(WeatherLabel, self).__init__(**kwargs)
    def on_touch_down(self,touch):
        if self.collide_point(touch.x, touch.y):
            if "C" in self.text:
                App.get_running_app().say_weather('1')
            elif "%" in self.text:
                App.get_running_app().say_weather('2')
            else:
                App.get_running_app().say_weather('3')





class Mainscreen(Screen):
    def __init__(self,**kwargs):
        super(Mainscreen,self).__init__(**kwargs)
        Clock.schedule_interval(self.update,1)

    def update(self,inst):
        self.ids.timer.text=str(time.strftime("%H:%M", time.localtime()))


class Menu(Screen):
    pass
class ImageButton(ButtonBehavior, Image):
    pass
class Cam(Screen):
    pass
class WakeUp(Screen):
    def __init__(self,**kwargs):
        self.identifier=1
        super(WakeUp,self).__init__(**kwargs)
        self.c=CircularTimePicker()
        self.c.size_hint=[.8,.8]
        self.c.pos_hint={'center_x':.5,'center_y':.6}
        self.c.color=[1,1,1,1]
        self.add_widget(self.c)
        self.c.hours=6
        self.c.minutes=30
    def get_time(self):

        self.hour = str(self.c.hours) + ':' + str(self.c.minutes)

        if self.hour[1]==':':
            self.hour='0'+self.hour
        if self.hour[3]=='0':
            self.hour=self.hour+'0'
        App.get_running_app().wake_up_setter(self.hour)
        os.system("play time.mp3")
class Lights(Screen):
    def __init__(self,**kwargs):
        super(Lights,self).__init__(**kwargs)
    def switch(self,id):
        requests.post('http://192.168.0.2{}/cm?cmnd=Power%20TOGGLE'.format(str(id)))





sm=ScreenManager(transition=CardTransition())
sm.add_widget(Mainscreen(name='main'))
sm.add_widget(Menu(name='menu'))
sm.add_widget(Lights(name='lights'))
sm.add_widget(WakeUp(name='wake'))
sm.add_widget(Cam(name='cam'))
sm.current='main'
class ClientFunctions(protocol.Protocol):
    def connectionMade(self):
        self.factory.app.on_connection(self.transport)
    def dataReceived(self, data):
        data=data.decode('utf-8')

class ClientBuilder(ReconnectingClientFactory):
    protocol = ClientFunctions

    def __init__(self, app):
        self.app = app


def mainscreen(inst):
    sm.current='main'
    sm.get_screen('cam').ids.camera.play=False
class My_app(App):
   temp=None
   humidity=None
   dust=None
   db=None
   cursor=None
   connection=None
   factory=None
   def db_connect(self):
       self.db=mysql.connector.connect(
  host="localhost",
  user="memento",
  passwd="memento",
  database="sensors"
)

   def sensor_database_query(self,inst=''):
       self.cursor = self.db.cursor()
       sql='SELECT * FROM sensor_data'
       self.cursor.execute(sql)
       result=self.cursor.fetchone()
       print(result)
       self.update_sensors(result[1],result[2],result[3])
       self.cursor.close()
       self.db.commit()


   def update_sensors(self,temp,humidity,dust):
       self.dust=dust
       self.humidity=humidity
       self.temp=temp
       celcius=u"\u2070"+'C'
       dust_meter=u"\u1d58"+u"\u1d4d"
       sm.get_screen('main').ids.temp.text=str(temp)+celcius
       sm.get_screen('main').ids.humidity.text = str(humidity)+'%'
       sm.get_screen('main').ids.dust.text = str(dust)+dust_meter
   def mainscreen(self):
       event = Clock.create_trigger(mainscreen,60)
       event()
   def build(self):
       self.db_connect()

       #self.connect_to_server()


       self.wake_up_setter()

       Clock.schedule_interval(lambda x: schedule.run_pending(), 60)
       Clock.schedule_interval(self.sensor_database_query, 300)
       self.sensor_database_query()
       #os.system("play hello.mp3")
       #self.say_weather()
       return sm


   def say_weather(self,cursor=''):
       if cursor=='1':
           eva.talk("Temperatura wynosi %s stopni Celsjusza" % self.temp)
       elif cursor=='2':
           eva.talk("Wilgotność jest na poziomie %s procent" % self.humidity)
       elif cursor == '3':
           if self.dust == 0:
               eva.talk("Powietrze jest czyste")
           else:
               eva.talk("W powietrzu mogą pojawić się zanieczyszczenia")
       else:
           eva.talk("Temperatura wynosi %s stopni Celsjusza" % self.temp)
           eva.talk("Wilgotność jest na poziomie %s procent" % self.humidity)
           if self.dust == 0:
               eva.talk("Powietrze jest czyste")
           else:
               eva.talk("W powietrzu mogą pojawić się zanieczyszczenia")

   def wake_up_setter(self,hour='06:30'):
       schedule.clear()
       schedule.every().day.at('23:30').do(self.sys_suspend)
       schedule.every().day.at(hour).do(self.sys_wakeup)
       print(hour)
   def sys_suspend(self):
       os.system('vcgencmd display_power 0')

       requests.post('http://192.168.0.22/cm?cmnd=Power%20Off')
       requests.post('http://192.168.0.23/cm?cmnd=Power%20Off')
       eva.talk("Usypiam system Memento")
   def sys_wakeup(self):

        os.system('vcgencmd display_power 1')
        eva.talk("Wybudzam system Memento")
        self.say_weather()

        #requests.post('http://192.168.0.22/cm?cmnd=Power%20On')
   def connect_to_server(self):
       reactor.connectTCP('localhost', 8000, ClientBuilder(self))

   def send_data(self,id,msg):
       msg=str(id)+str(msg)
       self.connection.write(msg.encode('utf-8'))
       print('data send!')

   def on_connection(self, connection):
       print("Connected successfully!")
       self.connection = connection









if __name__ == '__main__':

    My_app().run()