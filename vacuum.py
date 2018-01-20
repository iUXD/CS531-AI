from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Rectangle,  Color
from kivy.graphics.instructions import InstructionGroup
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from  simple_reflex import SimpleDeterminAgent
# global set
GRID_SIZE = 10
CELL_SIZE = 30
START_X = 50
START_Y = 150
CELL_GRAP = 1
ENV1 = 0    # environment 1
ENV2 = 1    # environment 2
ENV_GAP = 400
homeSet = {(0, 0)}
dirtyCellSet = {(0, 0), (1, 1), (2, 2),
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
agant1_status = 0
agant2_status = 0
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
        self.i = value[1]
        self.j = value[0]
        self.env = value[2]

        self.direction = value[3]       # up= 0, left = 1, down = 2, right = 3
        self.pos = self.getPos()


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
            self.i += 1
        elif self.direction == 1:
            self.j += 1
        elif self.direction == 2:
            self.i -= 1
        elif self.direction == 3:
            self.j -= 1
        self.rotateFace()
        self.pos = self.getPos()
        # print(self)
        # print(self.j)

    def getPos(self):
        # used to return current pix position ,for drawing
        return (self.j * CELL_SIZE + START_X + self.env * ENV_GAP,
                self.i * CELL_SIZE + START_Y)
    def getPosIJ(self):
        return (self.j, self.i)

    def nextPos(self):
        # return next position, based on current direction
        if self.direction == 0:
            return self.j, self.i+1
        elif self.direction == 1:
            return self.j + 1, self.i
        elif self.direction == 2:
            return self.j, self.i - 1
        else: # self.direction == 3
            return self.j - 1, self.i

class Sensor():
    def __init__(self, agent):
        self.agent = agent

    def isWall_ENV1(self):
        # for env1
        return self.agent.nextPos() in outWallCellSet

    def isWall_ENV2(self):
        return self.agent.nextPos() in wallCellSet or self.agent.nextPos() in outWallCellSet

    def isHome(self):
        return self.agent.getPosIJ() in homeSet

    def isDirty(self):
        return self.agent.getPosIJ() in dirtyCellSet

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
        self.i1, self.j1, self.env1, self.direct1 = 0, 0, 0, 0
        self.visitedSet1 = set()  # record visited set
        self.i2, self.j2, self.env2, self.direct2 = 0, 0, 1, 0
        self.visitedSet2 = set()  # record visited set
        self.agent1 = Agent(x=self.i1, y=self.j1, env=self.env1, dirt=self.direct1)
        self.agent2 = Agent(x=self.i2, y=self.j2, env=self.env2, dirt=self.direct2)
        self.sensor1 = Sensor(self.agent1)
        self.sensor2 = Sensor(self.agent2)

        self.controlLimit = 50   # used to setup steps to break animation.

    pass


    def _initEnv1(self, **kwargs):
        # draw env1
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):

                if (i, j) in dirtyCellSet:                          ## draw clean cells
                    self.canvas.add(DrawDirty(x=i, y=j, z=ENV1))
                else:                                               ## draw clean cells
                    self.canvas.add(DrawClean(x=i , y=j, z = ENV1))
        for (i, j) in outWallCellSet:                               ## draw outside wall cells
            self.canvas.add(DrawWall(x=i, y=j, z=ENV1))

        pass

    def _initEnv2(self, **kwargs):
        # draw env2
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if (i, j) in wallCellSet:                           ## draw inside wall cells
                    self.canvas.add(DrawWall(x=i , y=j, z=ENV2))
                elif (i,j) in dirtyCellSet:                         ## draw dirty cells
                    self.canvas.add(DrawDirty(x=i , y=j, z=ENV2))
                else:                                               ## draw clean cells
                    self.canvas.add(DrawClean(x=i , y=j, z = ENV2))
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
        percept1 = SimpleDeterminAgent()
        agent1_percept = [self.sensor1.isWall_ENV1(), self.sensor1.isDirty(), self.sensor1.isHome()]
        agent1_location = [self.agent1.j, self.agent1.i]
        agent1_direction = self.agent1.direction
        agent1_new_location, agent1_new_direction, agent1_action = percept1.update(agent1_percept,
                                                                    agent1_location,
                                                                    agent1_direction)
        self.agent1.j = agent1_new_location[0]
        self.agent1.i = agent1_new_location[1]
        print("===============new Location %d %d " %(self.agent1.getPosIJ()))
        self.agent1.direction = agent1_new_direction
        if agent1_action == 'Clean':
            dirtyCellSet.remove(self.agent1.getPosIJ())
        if agent1_action == 'Clean' or agent1_action == 'GoHead' or agent1_action == 'TurnRight':
            self.visitedSet1.add(self.agent1.getPosIJ())
        #
        # percept2 = SimpleDeterminAgent()
        # agent2_percept = [self.sensor2.isWall_ENV1(), self.sensor2.isDirty(), self.sensor2.isHome()]
        # agent2_location = [self.agent2.i, self.agent2.j]
        # agent2_direction = self.agent2.direction
        # agent2_new_location, agent2_new_direction, agent2_action = percept2.update(agent2_percept,
        #                                                                            agent2_location,
        #                                                                            agent2_direction)
        # if agent2_action == 'clean' or agent2_action == 'gohead':
        #     self.visitedSet1.add(self.agent1.pos)
        #
        #
        #
        #
        # global agant1_status
        # global agant2_status
        '''
        if self.sensor1.isWall_ENV1() and self.sensor1.isHome():    # back to home, terminate
            agant1_status = 1
            pass
        else:
            if self.sensor1.isDirty():
                dirtyCellSet.remove(self.agent1.pos)
            elif self.agent1.nextPos() in outWallCellSet:             # agent 1 only have out wall cells
                self.agent1.turnRight()
            else:
                self.agent1.goAhead()
        
        ## Agent 2
        if self.sensor2.isWall_ENV2() and self.sensor2.isHome():    # back to home, terminate
            agant2_status = 1
            pass
        else:
            if self.agent2.nextPos() in wallCellSet or self.agent2.nextPos() in outWallCellSet:
                self.agent2.turnRight()
            else:
                self.agent2.goAhead()
        self.visitedSet1.add((self.agent1.i, self.agent1.j))
        self.visitedSet2.add((self.agent2.i, self.agent2.j))

        if (agant1_status, agant2_status) == (1, 1):                # terminate the animation
            Clock.unschedule(self.drawGrid)
        print("current direction is : %d" % self.agent2.direction)
        '''


    def update(self, *args):
        self.canvas.clear()
        self._initEnv1()
        self._initEnv2()
        self._drawGrid()                            # draw visited cells
        self._updateAgent()                         # draw current Agents

        self.canvas.add(Color(1,1,1,1))
        self.canvas.add(self.agent1)
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
        Clock.schedule_interval(self.canvasGrid.drawGrid, 2)
        pass


if __name__ == '__main__':
    # MyApp().run()
    VacuumApp().run()
