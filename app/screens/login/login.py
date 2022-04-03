from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
import json
from kivymd.uix.label import MDLabel
from kivy.network.urlrequest import UrlRequest
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.toast import toast
from kivy.storage.jsonstore import JsonStore
from kivymd.app import MDApp


class LoginScreen(Screen):
    def login(self):
        # получаем окно
        inputed_username = self.ids['username'].text  # vasya
        inputed_password = self.ids['password'].text  # 123
        if inputed_username == '':
            self.parent.current = 'home'
        UrlRequest(f'http://127.0.0.1:5000/api/login?username={inputed_username}&password={inputed_password}',
                   on_success=self.success_login, on_failure=self.fail_login)

    def success_login(self, *args):
        current_app = MDApp.get_running_app()
        self.parent.current = 'home'
        # данные пользователя,  который залогинился
        user_data = json.loads(args[1])['user_data']
        store = JsonStore('cache.json')
        store.put(
            'user_data', id=user_data['id'], username=user_data['username'], avatar=user_data['avatar'])
        current_app.current_user = user_data
        current_app.root.get_screen('home').ids.sidebar.set_user_data(
            user_data['username'], user_data['avatar'])
        toast('Login ok!')

    def fail_login(self, *args):
        toast('login fail')
