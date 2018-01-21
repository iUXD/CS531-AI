from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Rectangle,  Color
from kivy.graphics.instructions import InstructionGroup
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from simple_determin_reflex import SimpleDeterministicAgent
from simple_random_reflex import SimpleStochasticAgent
from model_determin_reflex import ModelDeterministicAgent
# global set
AGENT_ID = 3
GRID_SIZE = 10
CELL_SIZE = 30
START_X = 50
START_Y = 150
CELL_GRAP = 1
ENV1 = 0    # environment 1
ENV2 = 1    # environment 2
ENV_GAP = 400
homeSet = {(0, 0)}
dirtyCellSet1 = {(0, 0), (1, 1), (2, 2),
                (3, 3), (4, 4), (5, 5),
                (6, 6), (7, 7), (8, 8),
                (9, 9)}
dirtyCellSet2 = {(0, 0), (1, 1), (2, 2),
                (3, 3), (4, 4), (5, 5),
                (6, 6), (7, 7), (8, 8),
                (9, 9)}
wallCellSet = {(0, 5), (1, 5), (2, 5), (3, 5), (5, 5), (7, 5), (8, 5),(9, 5),
               (5, 0), (5, 1), (5, 2), (5, 3), (5, 5), (5, 7), (5, 8),(5, 9)}
outWallCellSet = {(-1, -1), (-1, 0), (-1, 1), (-1, 2), (-1, 3), (-1, 4), (-1, 5),
                  (-1, 6), (-1, 7), (-1, 8), (-1, 9), (-1, 10),
                  (10, -1), (10, 0), (10, 1), (10, 2), (10, 3), (10, 4), (10, 5),
                  (10, 6), (10, 7), (10, 8), (10, 9),(10, 10),
                  (0, -1), (1, -1), (2, -1), (3, -1), (4, -1), (5, -1),
                  (6, -1), (7, -1), (8, -1), (9, -1), (10, -1),
                  (0, 10), (1, 10), (2, 10), (3, 10), (4, 10), (5, 10),
                  (6, 10), (7, 10), (8, 10), (9, 10)}
# presentation = Builder.load_file("grid.kv")
# global variables
agent1_status = 0
agent1_actionNum = 0
agent1_cleanedNum = 0
agent2_status = 0
agent2_actionNum = 0
agent2_cleanedNum = 0
agent31_memory = [0, 0, 0]
agent32_memory = [0, 0, 0]
class Label1(Label):
    pass
class Root(Widget):
    pass

class Start(Button):
    def __init__(self, **kwargs):
        super(Start, self).__init__(**kwargs)
        self.text = "Start"


class Agent(Rectangle):
    def __init__(self, **kwargs):
        super(Agent, self).__init__(**kwargs)
        self.source = 'img/faceUp.png'
        self.size = CELL_SIZE * 1.0, CELL_SIZE * 1.0

        value = []
        for key, val in kwargs.items():
            value.append(val)
        self.i = value[0]
        self.j = value[1]
        self.env = value[2]

        self.direction = value[3]       # up= 0, left = 1, down = 2, right = 3
        self.pos = self.getPos()
    def update(self):
        self.i, self.j = self.getPosIJ()
        self.pos = self.getPos()
        self.rotateFace()

    def rotateFace(self):
        if self.direction == 0:
            self.source = 'img/faceUp.png'
        elif self.direction == 1:
            self.source = 'img/faceRight.png'
        elif self.direction == 2:
            self.source = 'img/faceDown.png'
        elif self.direction == 3:
            self.source = 'img/faceLeft.png'

    def turnRight(self):
        self.direction += 1
        if self.direction == 4:
            self.direction = 0
        self.rotateFace()


    def turnLeft(self):
        self.direction -= 1
        if self.direction == -1:
            self.direction = 3
        self.rotateFace()

    def goAhead(self):
        if self.direction == 0:
            self.j += 1
        elif self.direction == 1:
            self.i += 1
        elif self.direction == 2:
            self.j -= 1
        elif self.direction == 3:
            self.i -= 1
        self.rotateFace()
        self.pos = self.getPos()
        # print(self)
        print(self.j)

    def getPos(self):
        # used to return current pix position ,for drawing
        return (self.i * CELL_SIZE + START_X + self.env * ENV_GAP,
                self.j * CELL_SIZE + START_Y)
    def getPosIJ(self):
        return (self.i, self.j)

    def nextPos(self):
        # return next position, based on current direction
        if self.direction == 0:
            return self.i, self.j+1
        elif self.direction == 1:
            return self.i + 1, self.j
        elif self.direction == 2:
            return self.i, self.j - 1
        else: # self.direction == 3
            return self.i - 1, self.j

class Sensor():
    def __init__(self, agent):
        self.agent = agent

    def isWall_ENV1(self):
        # for env1
        return self.agent.nextPos() in outWallCellSet

    def isWall_ENV2(self):
        return self.agent.nextPos() in wallCellSet or self.agent.nextPos() in outWallCellSet

    def isHome(self):
        return (self.agent.i, self.agent.j) in homeSet

    def isDirty1(self):
        return (self.agent.i, self.agent.j) in dirtyCellSet1

    def isDirty2(self):
        return (self.agent.i, self.agent.j) in dirtyCellSet2

class Cell(Rectangle):
    # draw one cell
    def __init__(self, **kwargs):
        super(Cell, self).__init__(**kwargs)
        value = []
        for key, val in kwargs.items():
            value.append(val)
        # x = i * cell size + env_offset + start x offset
        # y = j * cell size + start y offset
        self.pos = (value[0] * CELL_SIZE + value[2] * ENV_GAP + START_X, value[1] * CELL_SIZE +START_Y)
        self.size = (CELL_SIZE -CELL_GRAP , CELL_SIZE -CELL_GRAP)
    pass


class DrawClean(InstructionGroup):
    # draw a clean cell
    def __init__(self,**kwargs):
        super(DrawClean, self).__init__(**kwargs)
        self.add(Color(0, 0, 1, 1))
        self.add(Cell(**kwargs))

class DrawDirty(InstructionGroup):
    # draw a dirty cell
    def __init__(self,**kwargs):
        super(DrawDirty, self).__init__(**kwargs)
        self.add(Color(0, 1, 0, 1))
        self.add(Cell(**kwargs))

class DrawWall(InstructionGroup):
    # draw a wall cell
    def __init__(self,**kwargs):
        super(DrawWall, self).__init__(**kwargs)
        self.add(Color(1, 0, 0, 1))
        self.add(Cell(**kwargs))

class DrawVisited(InstructionGroup):
    # draw a visited cell
    def __init__(self,**kwargs):
        super(DrawVisited, self).__init__(**kwargs)
        self.add(Color(1, 0.5, 0.5, 1))
        self.add(Cell(**kwargs))

class Grid(Widget):

    def __init__(self, **kwargs):
        super(Grid, self).__init__(**kwargs)
        self._initEnv1(**kwargs)
        self._initEnv2(**kwargs)
        # initialize agent state: i, j, env, direction,
        #            visitedSet
        self.fileName = "agent1.txt"
        self.i1, self.j1, self.env1, self.direct1 = 0, 0, 0, 0
        self.visitedSet1 = set()  # record visited set
        self.i2, self.j2, self.env2, self.direct2 = 0, 0, 1, 0
        self.visitedSet2 = set()  # record visited set
        self.agent1 = Agent(x=self.i1, y=self.j1, env=self.env1, dirt=self.direct1)
        self.agent2 = Agent(x=self.i2, y=self.j2, env=self.env2, dirt=self.direct2)
        self.sensor1 = Sensor(self.agent1)
        self.sensor2 = Sensor(self.agent2)
        self.actionNum1 = 0
        self.cleanedNum1 = 0
        self.performancedNum1 = 0.0
        self.actionNum2 = 0
        self.cleanedNum2 = 0
        self.performancedNum2 = 0
        self.label1 = Label(text="action# :%5d"%self.actionNum1,          size=(10, 10), pos=(60, 30))
        self.label2 = Label(text="cleaned# :%4d"%self.cleanedNum1,        size=(10, 10), pos=(160, 30))
        self.label3 = Label(text="performance:%5f"%self.performancedNum1, size=(10, 10), pos=(300, 30))
        self.label4 = Label(text="action# :%5d"%self.actionNum1,          size=(10, 10), pos=(460, 30))
        self.label5 = Label(text="cleaned# :%4d"%self.cleanedNum1,        size=(10, 10), pos=(560, 30))
        self.label6 = Label(text="performance:%5f"%self.performancedNum1, size=(10, 10), pos=(700, 30))
        self._addLabels()

        self.controlLimit = 500   # used to setup steps to break animation.

    pass
    def _addLabels(self):
        # add labels to report the values
        self.actionNum1 = agent1_actionNum
        self.cleanedNum1 = agent1_cleanedNum
        self.performancedNum1 = 0.0 if agent1_actionNum == 0 else agent1_cleanedNum/agent1_actionNum
        self.actionNum2 = agent2_actionNum
        self.cleanedNum2 = agent2_cleanedNum
        self.performancedNum2 = 0.0 if agent2_actionNum == 0 else agent2_cleanedNum/agent2_actionNum
        self.label1.text = "action# :%5d"%self.actionNum1
        self.label2.text = "cleaned# :%4d"%self.cleanedNum1
        self.label3.text = "performance:%5f"%self.performancedNum1
        self.label4.text = "action# :%5d" % self.actionNum2
        self.label5.text = "cleaned# :%4d" % self.cleanedNum2
        self.label6.text = "performance:%5f" % self.performancedNum2

        self.canvas.add(Rectangle(texture=self.label1.texture, size=(80, 30),  pos=( 60, 30)))
        self.canvas.add(Rectangle(texture=self.label2.texture, size=(80, 30),  pos=(160, 30)))
        self.canvas.add(Rectangle(texture=self.label3.texture, size=(120, 30), pos=(260, 30)))
        self.canvas.add(Rectangle(texture=self.label4.texture, size=(80, 30),  pos=(460, 30)))
        self.canvas.add(Rectangle(texture=self.label5.texture, size=(80, 30),  pos=(560, 30)))
        self.canvas.add(Rectangle(texture=self.label6.texture, size=(120, 30), pos=(660, 30)))
        self._write2File()
    def _write2File(self):

        with open(self.fileName, 'a') as text_file:
            text_file.write("%5d+%4d+%5f+%5d+%4d+%5f \n" %(self.actionNum1,
                                                                     self.cleanedNum1,
                                                                     self.performancedNum1,
                                                                     self.actionNum2,
                                                                     self.cleanedNum2,
                                                                     self.performancedNum2
                                                                     ))


    def _initEnv1(self, **kwargs):
        # draw env1
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):

                if (i, j) in dirtyCellSet1:                          ## draw clean cells
                    self.canvas.add(DrawDirty(x=i, y=j, z=ENV1))
                else:                                               ## draw clean cells
                    self.canvas.add(DrawClean(x=i, y=j, z = ENV1))
        for (i, j) in outWallCellSet:                               ## draw outside wall cells
            self.canvas.add(DrawWall(x=i, y=j, z=ENV1))

        pass

    def _initEnv2(self, **kwargs):
        # draw env2
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if (i, j) in wallCellSet:                           ## draw inside wall cells
                    self.canvas.add(DrawWall(x=i, y=j, z=ENV2))
                elif (i,j) in dirtyCellSet2:                         ## draw dirty cells
                    self.canvas.add(DrawDirty(x=i, y=j, z=ENV2))
                else:                                               ## draw clean cells
                    self.canvas.add(DrawClean(x=i, y=j, z = ENV2))
        for (i, j) in outWallCellSet:                               ## draw outside wall cells
            self.canvas.add(DrawWall(x=i, y=j, z=ENV2))
        pass

    def drawGrid(self, *kwargs):
        self.controlLimit -= 1
        if self.controlLimit == 0:              # break the animation, this if clause can be modified
            Clock.unschedule(self.drawGrid)

        # print(self.controlLimit, self.agent1.j, self.agent2.i)

        self.update()


    def _updateAgent(self):
        # update information about the agent
        # update self.i1, self.j1,self.direct1  self.visitedSet1 for agent1
        #        self.i2, self.j2,self.direct2  self.visitedSet2 for agent1
        # 1. add current cell to visitedSet
        self.visitedSet1.add((self.i1, self.j1))
        self.visitedSet2.add((self.i2, self.j2))
        # 2. uppdate agent states, just try move ahead now
        # most of our code should be here!
        ######################################################################################################
        ## A. question 1: Simple agent
        global agent31_memory
        global agent32_memory
        if AGENT_ID == 1:
            percept1 = SimpleDeterministicAgent()
            percept2 = SimpleDeterministicAgent()
            self.fileName = "agent1.txt"
        elif AGENT_ID == 2:
            percept1 = SimpleStochasticAgent()
            percept2 = SimpleStochasticAgent()
            self.fileName = "agent2.txt"
        else:
            percept1 = ModelDeterministicAgent(agent31_memory)
            percept2 = ModelDeterministicAgent(agent32_memory)
            self.fileName = "agent3.txt"

        global agent1_status
        global agent1_actionNum
        global agent1_cleanedNum
        global agent2_status
        global agent2_actionNum
        global agent2_cleanedNum

        # self._updateOneAgent(percept1)
        agent1_percept = [self.sensor1.isWall_ENV1(), self.sensor1.isDirty1(), self.sensor1.isHome()]
        agent1_location = [self.agent1.i, self.agent1.j]
        agent1_direction = self.agent1.direction
        agent1_new_location, agent1_new_direction, agent1_action, agent31_memory = percept1.update(agent1_percept,
                                                                    agent1_location,
                                                                    agent1_direction)

        if agent1_action == 'Off':
            agent1_status = 1
        else:
            self.agent1.i = agent1_new_location[0]
            self.agent1.j = agent1_new_location[1]
            self.agent1.direction = agent1_new_direction
            agent1_actionNum += 1
            if agent1_action == 'Clean':
                agent1_cleanedNum += 1
                dirtyCellSet1.remove((self.agent1.i, self.agent1.j))
            if agent1_action == 'Clean' or agent1_action == 'GoHead' or agent1_action == 'TurnRight':
                self.visitedSet1.add((self.agent1.i, self.agent1.j))

        agent2_percept = [self.sensor2.isWall_ENV2(), self.sensor2.isDirty2(), self.sensor2.isHome()]
        agent2_location = [self.agent2.i, self.agent2.j]
        agent2_direction = self.agent2.direction
        agent2_new_location, agent2_new_direction, agent2_action, agent32_memory = percept2.update(agent2_percept,
                                                                                   agent2_location,
                                                                                   agent2_direction)
        if agent2_action == 'Off':
            agent2_status = 1
        else:
            self.agent2.i = agent2_new_location[0]
            self.agent2.j = agent2_new_location[1]
            print("==============agent2 at %d %d" % (self.agent2.getPosIJ()))
            self.agent2.direction = agent2_new_direction
            agent2_actionNum += 1
            if agent2_action == 'Clean':
                agent2_cleanedNum += 1
                dirtyCellSet2.remove(self.agent2.getPosIJ())
            if agent2_action == 'Clean' or agent2_action == 'GoHead' or agent2_action == 'TurnRight':
                self.visitedSet2.add(self.agent2.getPosIJ())

        if agent1_status == 1 and agent2_status == 1:
                Clock.unschedule(self.drawGrid)

    def _updateOneAgent(self, percept):

        pass


    def update(self, *args):
        self.canvas.clear()
        self._initEnv1()
        self._initEnv2()
        self._drawGrid()                            # draw visited cells
        self._updateAgent()                         # draw current Agents

        self.canvas.add(Color(1,1,1,1))
        self.agent1.update()
        self.agent2.update()
        self._addLabels()
        self.canvas.add(self.agent1)
        # print("=========**********=====agent1 at %d %d" % (self.agent1.i, self.agent1.j))
        self.canvas.add(self.agent2)


    def _drawGrid(self):
        # used to update other cells, get info from visitedSet
        for (i, j) in self.visitedSet1:
            self.canvas.add(DrawVisited(x=i, y=j, env=ENV1))
        for (i, j) in self.visitedSet2:
            self.canvas.add(DrawVisited(x=i, y=j, env=ENV2))
        pass


class VacuumApp(App):
    def build(self):
        self.canvasGrid = Grid()

        startButton = Start(on_press=self.beginRun)
        buttonLayout = BoxLayout(size_hint=(1, None), height=50)
        buttonLayout.add_widget(startButton)
        root = BoxLayout(orientation='vertical')
        root.add_widget(buttonLayout)
        root.add_widget(self.canvasGrid)

        return root

    def beginRun(self,  *kwargs):

        Clock.schedule_interval(self.canvasGrid.drawGrid, 0.05)

        # Clock.schedule_interval(self.canvasGrid.drawGrid, 7)

        pass


if __name__ == '__main__':
    # MyApp().run()
    with open('agent3.txt', 'w') as text_file:
        text_file.write("")
    VacuumApp().run()
