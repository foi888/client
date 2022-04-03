from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.app import MDApp


class SideBar(MDNavigationDrawer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def set_user_data(self, username, avatar):
        self.ids.avatar.source = avatar
        self.ids.username.text = username
    
    def open_profile(self):
        MDApp.get_running_app().root.get_screen('profile').profile_user_id = MDApp.get_running_app().current_user['id']
        MDApp.get_running_app().root.current = 'profile'