#!/usr/bin/python

import sys, os, time

try:
    import psyco    
    psyco.full()
except ImportError:
    print >> sys.stderr, "Module `psyco' is not installed. It's recommended to speed up program"
    

import random
import cmdLineArgs
from PyQt4 import QtGui
from MainWindow import MainWindow


def main():
    random.seed()

    # change working dir
    if not cmdLineArgs.options.debug:
        dirname = 'data_'+time.strftime('%y%m%d_%H%M%S')
        os.makedirs(dirname)
        os.chdir(dirname)
    print "Current working directory:", os.getcwd() 
    
    app = QtGui.QApplication(sys.argv)
    app.setPalette(QtGui.QPalette(QtGui.QColor(204,230,255), QtGui.QColor(204,230,255)))
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__=='__main__':
    cmdLineArgs.parseArgv(sys.argv[1:])
    main()
