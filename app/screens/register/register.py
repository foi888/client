from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
import json
from kivymd.uix.label import MDLabel
from kivy.network.urlrequest import UrlRequest
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.toast import toast



class RegisterScreen(Screen):
    def register(self):
        screen = self.root.get_screen('register')
        inputed_username = screen.ids['username'].text  
        inputed_password = screen.ids['password'].text
        inputed_email = screen.ids['email'].text
        UrlRequest(f'http://127.0.0.1:5000/api/register?username={inputed_username}&password={inputed_password}&email={inputed_email}', on_success=self.success_register)

    def success_register(self, *args):
        app.root.current = 'login'  # меняем экран на login
        toast('register ok')