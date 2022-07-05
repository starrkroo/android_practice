import sqlite3
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.image import Image

Window.clearcolor = (1, 1, 1, 1)

class MainApp(App):
    def get_values(self):
        """ gets values from sqlite3 """
        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM vhdata")
        data = cursor.fetchall()

        cursor.close()
        conn.close()
        return data

    def build(self):
        core_layout = GridLayout(cols=2, spacing=30, size_hint_y=None, row_default_height=40)
        core_layout.bind(minimum_height=core_layout.setter('height'))
        posts_data = self.get_values()

        for post in posts_data:
            sublayout = GridLayout(cols=1, spacing=5)
            title = post[0]
            description = post[1]
            price = post[2]
            image_url = post[3]

            sublayout.add_widget(Image(source=image_url, width=100, size_hint_y=None))
            sublayout.add_widget(Label(text=title, font_size=30, color="black", halign='right', valign='center'))
            sublayout.add_widget(Label(text=description, font_size=10, color="black"))
            sublayout.add_widget(Label(text=price, font_size=20, color="black"))

            core_layout.add_widget(sublayout)


        # layout.add_widget(Button(text='Hello 1', size_hint_x=None, width=300))
        # layout.add_widget(Button(text='World 1', size_hint_x=None, width=300))
        # layout.add_widget(Button(text='Hello 2', size_hint_x=None, width=300))
        # layout.add_widget(Button(text='World 2', size_hint_x=None, width=300))
        
        root = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        root.add_widget(core_layout)
        return root

if __name__ == '__main__':
    MainApp().run()