import sys

from direct.showbase.ShowBase import ShowBase
from panda3d import *


class mygame(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.cube=self.loader.loadModel("models/box")
        self.cube.reparentTo(self.render)
        self.cube.setPos(50,50,50)
        self.cube.setScale(50,50,50)
        self.ground=self.loader.loadModel("models/box")
        self.ground.setPos(10,10,10)
        self.ground.setScale(2,2,2)
        self.disable_mouse()
        self.camera.setPos(-10,-50,1)
        self.camera.lookAt(self.cube)
        self.accept("arrow_up", self.move_down)
        self.accept("arrow_left", self.move_left)
        self.accept("arrow_right", self.move_right)
    def move_up(self):
        self.cube.setY(self.cube.getY() + 1)
    def move_down(self):
        self.cube.setY(self.cube.getY() - 1)
    def move_right(self):
        self.cube.setX(self.cube.getX() + 1)
    def move_left(self):
        self.cube.setX(self.cube.getX() - 1)


game = mygame()
game.run()