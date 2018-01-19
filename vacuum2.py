from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import  Label
from kivy.uix.widget import Widget
from kivy.graphics import Line
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from  kivy.graphics import Rectangle, Canvas, Color
from kivy.graphics.instructions import  InstructionGroup

# global set
GRID_SIZE = 10

presentation = Builder.load_file("grid.kv")

class Root(Widget):
    pass
class Dirty(Rectangle):
    def __init__(self, **kwargs):
        super(Dirty, self).__init__(**kwargs)
        value = []
        for key, val in kwargs.items():
            value.append(val)
        print(value)
        self.pos = (value[0] + 100, value[1]+100)
        self.size = (38, 38)

    pass

class Grid(Widget):
    def __init__(self, **kwargs):
        super(Grid, self).__init__(**kwargs)
        Builder.load_file("grid.kv")
        gridGroup = []
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                current = InstructionGroup()
                current.add(Dirty(x= i * 40, y = j * 40))
                self.canvas.add(current)

    pass




class VacuumApp(App):
    def build(self):
        presentation
        return Root()
        # return Vacuum()


if __name__ == '__main__':
    # MyApp().run()
    VacuumApp().run()
    # SimpleKivy().run()
# class Grid(Widget):
#      def __init__(self):
#          # Builder.load_file("grid.kv")
#          with self.canvas:
#              Rectangle(pos=(2* 10, 2 * 10))
#              # for i in range(GRID_SIZE):
#              #     for j in range(GRID_SIZE):
#              #         Rectangle(pos=(i * 10, j*10))
#
# class Vacuum():
#     def __init__(self, **kwargs):
#         super(Vacuum, self).__init__(**kwargs)
#         # Builder.load_file("grid.kv")
#         # self.cols = 2
#         # self.add_widget(Label(text='Begin'))
#         # with self.canvas:
#         #
#         #     for i in range(GRID_SIZE):
#         #         for j in range(GRID_SIZE):
#         #             Rectangle(pos=(i * 10, j*10),size=(7,7))
#         # self.add_widget(Grid())
#         # self.username = Grid()
#         # self.add_widget(self.username)
#
#
#     pass

# class Grid(Widget):
#     pass
    # def __init__(self):
    #     with self.canvas:
    #
    #         for i in range(GRID_SIZE):
    #             for j in range(GRID_SIZE):
    #                 Rectangle(pos=(i * 10, j*10),size=(7,7))
#
#  class Vacuum(GridLayout):
#     def __init__(self, **kwargs):
#         super(Vacuum, self).__init__(**kwargs)
#
#         self.cols = 2
#         self.add_widget(Label(text='Begin'))
#         with self.canvas:
#
#             for i in range(GRID_SIZE):
#                 for j in range(GRID_SIZE):
#                     Rectangle(pos=(i * 10, j*10),size=(7,7))
#         # self.add_widget(Grid())
#         # self.username = Grid()
#         # self.add_widget(self.username)
#
#
#     pass