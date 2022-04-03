from kivy.uix.screenmanager import Screen
from kivymd.uix.toolbar import MDToolbar
from kivymd.app import MDApp
from kivy.network.urlrequest import UrlRequest
import json
from kivy.properties import NumericProperty, StringProperty
from screens.home.home import Post

class ProfileScreen(Screen):
    profile_user_id = NumericProperty()
    def on_pre_enter(self):
        UrlRequest(f'http://127.0.0.1:5000/api/get_user?user_id={self.profile_user_id}', on_success=self.user_loaded)
    
    def user_loaded(self, *args):
        user_data = json.loads(args[1])
        self.ids.profile_image.source = user_data['avatar']
        self.ids.rounded_avatar.source = user_data['avatar']
        self.ids.username.text = user_data['user_name']
        posts = user_data['posts']        
        scroll_list = self.ids['posts']
        scroll_list.clear_widgets()
        for post in posts:
            item = Post(
                post_id=post['post_id'],
                author_username=user_data['user_name'],
                post_text=post['text'],
                avatar=user_data['avatar'],
                author_id=user_data['id']
            )
            scroll_list.add_widget(item)



class Toolbar(MDToolbar):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type_height = "medium"
        self.left_action_items = [["arrow-left", lambda x: self.switch_screen('home')]]
    
    def switch_screen(self, screen_name):
        MDApp.get_running_app().root.current = screen_name

'''

{"id": 4, "user_name": "test2", "info": null, "last_seen": "2021-12-18 14:09:26", 
"avatar": "https://www.gravatar.com/avatar/3845e939e6363d1721ff8dcc41ad1062?d=identicon&s=128", 
"posts": [{"post_id": 1 , "text": "12345", "timestamp": "2021-12-04 14:31:47.812030"}]}'''