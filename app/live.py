from urllib import request
from kivy.factory import Factory
from kivy.core.window import Window
from kaki.app import App
from kivymd.app import MDApp
import os


class HotReload(App, MDApp):
    CLASSES = {
        'Main': 'main'
    }
    AUTORELOADER_PATHS = [
        ('.', {'recursive': True})
    ]
    KV_FILES = {
        os.path.join(os.getcwd(), 'main.kv'),
        os.path.join(os.getcwd(), 'login.kv'),
        os.path.join(os.getcwd(), 'register.kv'),
        os.path.join(os.getcwd(), 'index.kv')
    }

    def build_app(self):
        return Factory.Main()


if __name__ == '__main__':
    HotReload().run()


# set DEBUG=1 && python live.py



'''

1. Vasya
2. Misha
3. Vova
4. John
5. Steve
6. Vasya2
7. Misha2


>>>>>  All()
1. Vasya
2. Misha
3. Vova
4. John
5. Steve
6. Vasya2
7. Misha2


>>>> (1, 4)
1. Vasya
2. Misha
3. Vova
4. John
'''




