import os, sys, time, cPickle as pickle
try:
    import profile
except:
    print >> sys.stderr, 'profile module is not found!'
    
from PyQt4 import QtCore, QtGui
from Ui_MainWindow import Ui_MainWindow
from MapFrame import MapFrame
from Life import Grass, Zebra, Lion
from Nature import Nature

class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        
        # Set up the user interface from Designer.
        self.setupUi(self)      
        
        # Make some local modifications.
        # set up the nature
        self.nature = Nature()
                
        # set up the map widget
        self.map = MapFrame(self.nature, self.frame)
        self.map.setGeometry(QtCore.QRect(0,0,800,600))

        # connect
        QtCore.QObject.connect(self.btnNewDay,QtCore.SIGNAL("clicked()"), self.slotMove)
        QtCore.QObject.connect(self.btnManyDays,QtCore.SIGNAL("clicked()"), self.slotMoveMany)
        QtCore.QObject.connect(self.btnSave,QtCore.SIGNAL("clicked()"), self.slotSave)
        QtCore.QObject.connect(self.btnLoad,QtCore.SIGNAL("clicked()"), self.slotLoad)
    


    def show(self):
        QtGui.QMainWindow.show(self)
        self.showStatus()

    def slotMoveManyProfile(self):
        """
        for profiling,
        to use, rename slotMoveMany() to slotMoveManyReal()
        and rename this function to slotMoveMany()
        """
        profile.runctx('self.slotMoveManyReal()'
                       , vars(sys.modules[__name__])
                       , vars()
                       , 'profile.log')

    def slotMoveMany(self):
        """
        move many days
        """
        for _ in xrange(int(self.txtDays.text())):
            self.nature.newDay()
            self.map.drawImage()
            self.map.save()
        self.showStatus(save=False)
        os.system('eject')

    def slotMove(self):
        self.nature.newDay()
        self.showStatus()

    def showStatus(self, save=True):
        self.map.update()
        self.statusbar.showMessage('Day: %d  Grass: %d  Zebra: %d  Lion: %d  Time: %.3f' % \
                                   self.nature.getStats()[:5])
        if save:
            self.map.save()

    def slotSave(self):
        pickle.dump(self.nature, open('nature.pickle', 'w'), protocol=pickle.HIGHEST_PROTOCOL)
        self.statusbar.showMessage('Saved data!')

    def slotLoad(self):
        self.nature = pickle.load(open('nature.pickle'))
        self.showStatus(save=False)
