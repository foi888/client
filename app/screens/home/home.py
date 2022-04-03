from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
import json
from kivymd.uix.label import MDLabel
from kivy.network.urlrequest import UrlRequest
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.toast import toast
from kivymd.uix.list import ThreeLineAvatarListItem, ImageLeftWidget, ThreeLineAvatarIconListItem, IconRightWidget
from kivymd.uix.textfield import MDTextField
from kivy.properties import NumericProperty, StringProperty, BooleanProperty
from kivy.storage.jsonstore import JsonStore
from kivymd.app import MDApp
from kivymd.uix.behaviors import RoundedRectangularElevationBehavior
from kivymd.uix.card import MDCardSwipeFrontBox, MDCardSwipe, MDCard
from kivy.animation import Animation
from kivy.clock import Clock
import components


class HomeScreen(Screen):
    dialog = None
    page = 0
    user_id = None

    def show_posts_on_screen(self, *args):
        posts = json.loads(args[1])
        scroll_list = self.ids['posts_scroll_list']
        # scroll_list.clear_widgets()
        if scroll_list.children:
            scroll_list.remove_widget(scroll_list.children[0])
        for post in posts:
            post_item = Post(
                post_id=post['post_id'],
                author_username=post['author_user_name'],
                post_text=post['text'],
                avatar=post['author_avatar'],
                author_id=post['author_id'],
                likes_count=str(post['likes_count']),
                is_liked=post['is_liked']
            )
            if self.user_id == post['author_id']:
                post_item.add_widget(
                    IconRightWidget(
                        icon='delete',
                        on_release=post_item.delete_post
                    )
                )
            scroll_list.add_widget(post_item)
        scroll_list.add_widget(MDRaisedButton(text='Load more posts', pos_hint={"center_x": 0.5}, on_release=self.load_posts))

    def load_posts(self, *args):
        self.page += 1
        UrlRequest(f'http://127.0.0.1:5000/api/get_posts?user_id={self.user_id}&page={self.page}&qty={3}',
                   on_success=self.show_posts_on_screen)

    def on_pre_enter(self):
        store = JsonStore('cache.json')
        self.user_id = store.get('user_data')['id']
        self.load_posts()

    def success_added_post(self, *args):
        toast('Post added')
        self.load_posts()

    def send_post(self, *args):
        post_text = self.dialog.content_cls.text
        UrlRequest(f'http://127.0.0.1:5000/api/add_post', on_success=self.success_added_post,
                   req_body=json.dumps({'text': post_text, 'user_id': self.user_id}))
        self.close_dialog()

    def open_dialog(self):
        self.dialog = MDDialog(
            title="add post",
            type="custom",
            content_cls=MDTextField(
                hint_text='post text',
                multiline=True,
                pos_hint={'center_y': 0.2},
                max_height="110dp"
            ),
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    theme_text_color="Custom",
                    on_release=self.close_dialog
                ),
                MDFlatButton(
                    text="send post",
                    theme_text_color="Custom",
                    on_release=self.send_post
                ),
            ]
        )
        self.dialog.open()

    def close_dialog(self, *args):
        self.dialog.dismiss()
    
    def reload_posts(self):
        def reload_posts(interval):
            self.page = 0
            scroll_list = self.ids['posts_scroll_list']
            scroll_list.clear_widgets()
            self.load_posts()
            self.ids.refresh_layout.refresh_done()
            self.tick = 0
        Clock.schedule_once(reload_posts, 1)



class Post(MDCard, RoundedRectangularElevationBehavior):
    post_id = NumericProperty()
    post_text = StringProperty()
    author_username = StringProperty()
    author_id = NumericProperty()
    avatar = StringProperty()
    likes_count = StringProperty()
    is_liked = BooleanProperty()

    def show_full_post(self):
        print(self.post_id)
        MDDialog(
            title="Post",
            text=f"[color=#000]{self.post_text}[/color]"
        ).open()

    def success_deleting(self, *args):
        toast('Post deleted')
        scroll_list = MDApp.get_running_app().root.get_screen('home').ids.posts_scroll_list
        scroll_list.remove_widget(self)

    def fail_deleting(self, *args):
        toast('Post deleting error')

    def delete_post(self, *args):
        anim = Animation(x=1000, duration=0.2)
        anim.start(self)
        home_screen = MDApp.get_running_app().root.get_screen('home')
        UrlRequest('http://127.0.0.1:5000/api/del_post', on_failure=self.fail_deleting,
                   on_success=self.success_deleting, req_body=json.dumps({'post_id': self.post_id, 'user_id': home_screen.user_id}))

    def open_profile(self):
        MDApp.get_running_app().root.get_screen(
            'profile').profile_user_id = self.author_id
        MDApp.get_running_app().root.current = 'profile'

    def like_post(self):
        UrlRequest('http://127.0.0.1:5000/api/like', on_success=self.update_likes, req_body=json.dumps(
            {'post_id': self.post_id, 'user_id': MDApp.get_running_app().current_user['id']}))

    def update_likes(self, *args):
        post_likes_data = json.loads(args[1])
        self.ids.likes_count.text = str(post_likes_data['likes_count'])
        self.ids.heart.icon = 'heart' if post_likes_data['is_liked'] else 'heart-outline'
