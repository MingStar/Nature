import time, cmdLineArgs
from Constants import GRASS, ZEBRA, LION
from PyQt4 import QtGui

POS = [[0,0], [0,1], [1,0], [1,1]]

COLOURS = [QtGui.QColor(0,255,0).rgb()
           , QtGui.QColor(0,0,255).rgb()
           , QtGui.QColor(255,0,0).rgb()]

WHITE = QtGui.QColor(255, 255, 255).rgb()
        
class MapFrame(QtGui.QFrame):
    def __init__(self, nature, *args):
        QtGui.QFrame.__init__(self, *args)
        self.nature = nature
        self.land = nature.land
        self.img = QtGui.QImage(800, 600, QtGui.QImage.Format_RGB32)
    
    def paintEvent(self, _):
        """
        draw on the img, the paint it onto the widget
        """
        # draw
        self.drawImage()
        # show
        painter = QtGui.QPainter(self)        
        painter.drawImage(0, 0, self.img)

    def drawImage(self):
        self.img.fill(WHITE)
        for idx, lives in enumerate(self.land.species):
            # has assumptions that the order is grass, zebra then lion in self.land.species
            colour = COLOURS[idx]
            for life in lives:
                x, y = life.pos
                for pos in POS:
                    self.img.setPixel(x*2+pos[0], y*2+pos[1], colour)        


    def save(self):
        if cmdLineArgs.options.debug:
            return
        self.img.save(str(self.nature.day).zfill(4)+'.png', 'PNG')
