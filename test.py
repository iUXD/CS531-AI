from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import  Label
from kivy.uix.widget import Widget
from kivy.graphics import Line
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition




class MainScreen(Screen):
    pass


class SecondScreen(Screen):
    pass

class ScreenManagement(ScreenManager):
    pass

presentation = Builder.load_file("main.kv")

class VacuumApp(GridLayout):

    def __init__(self, **kwargs):
        super(VacuumApp, self).__init__(**kwargs)
        self.cols = 2
        self.add_widget(Label(text='User Name'))
        self.username = TextInput(multiline=False)
        self.add_widget(self.username)
        self.add_widget(Label(text='password'))
        self.password = TextInput(password=True, multiline=False)
        self.add_widget(self.password)


class MyApp(App):

    def build(self):
        return VacuumApp()

class Painter(Widget):
    def on_touch_down(self, touch):
        with self.canvas:
            touch.ud["line"] = Line(points=(touch.x, touch.y))

    def on_touch_move(self, touch):
        touch.ud["line"].points += (touch.x, touch.y)


class DrawInput(Widget):
    def on_touch_down(self, touch):
        # print(touch)
        # print("DOWN")
        with self.canvas:
            touch.ud["line"] = Line(points=(touch.x, touch.y))
        # pass
    # def on_touch_up(self, touch):
    #     # print("UP")
    #     # print(touch)
    #     pass

    def on_touch_move(self, touch):
        touch.ud["line"].points += (touch.x, touch.y)



class LoginScreen(GridLayout):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.cols = 2

        self.add_widget(Label(text="UserName:"))
        self.username = TextInput(multiline=False)
        self.add_widget(self.username)

        self.add_widget(Label(text="Password:"))
        self.password = TextInput(multiline=False,password=True)
        self.add_widget(self.password)



class Widgets(Widget):
    pass

class SimpleKivy1(App):
    def build(self):
        return presentation
        # return MainScreen()
        # return Widgets()

if __name__ == '__main__':
    # MyApp().run()
    SimpleKivy1().run()
