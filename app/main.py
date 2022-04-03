from atexit import register
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen
from kivy.network.urlrequest import UrlRequest
from kivymd.toast import toast
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDFlatButton
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.navigationdrawer import MDNavigationDrawer
import json

import screens.home.home as home, screens.login.login as login, screens.register.register as register, screens.profile.profile as profile
#from components.sidebar import SideBar


class MainApp(MDApp):

    current_user = {}

    def build(self):
        self.load_kv('screens/home/home.kv')
        self.load_kv('screens/register/register.kv')
        self.load_kv('screens/login/login.kv')
        self.load_kv('screens/profile/profile.kv')
        return Builder.load_file('main.kv')


app = MainApp()
app.run()

# token = jwt.encode({'name': 'Vasya'}, 'my-secret', algorithm='HS256')
# jwt.decode(token, 'my-secret', algorithms=['HS256'])
#call venv/scripts/activate
# set FLASK_DEBUG=1
# pip install https://github.com/kivymd/KivyMD/archive/master.zip

# return json.dumps({'likes_count': post.likes_count, 'is_liked': })