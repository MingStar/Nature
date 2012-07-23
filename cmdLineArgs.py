"""
command line parsing module

$Id: cmdLineArgs.py 1620 2006-08-30 06:38:35Z wchen $
"""

import sys
from optparse import OptionParser
#from Utilities.print2stderr import *

options = None # all options (optional arguments)
positional = None # all other arguments (positional arguments)

PROG_ID = '' # program ID, set in genReport.py

class MyOptionParser(OptionParser):
    """
    class which customs the error() and print_help() behaviour from OptionParser
    """
    def error(self, msg):
        """
        print help msg before exit
        """
        self.print_help(sys.stderr)
        print >> sys.stderr
        self.exit(2, "%s: error: %s\n" % (self.get_prog_name(), msg))

    def print_help(self, file=None):
        """
        print program ID as well
        """
        OptionParser.print_help(self, file)
        print >> sys.stderr
        if PROG_ID:
            print >> sys.stderr, PROG_ID        

        
def parseArgv(args):
    """
    command line arguments handling
    """    
    parser = MyOptionParser(usage='%prog reportModule [options]')
    parser.add_option('-r', '--root', dest='root', metavar='DIRECTORY'
                      , default='.'
                      , help="specify the root DIRECTORY (default: current directory)"+\
                      ", in which to store the report(s), as well as load/save the data file.")
    parser.add_option('-m', '--mail', dest='sendMail'
                      , default=False, action='store_true'
                      , help='send out notification email(s).')
    parser.add_option('-w', '--web', dest='genWebPage'
                      , default=False, action='store_true'
                      , help='print in html format when printing to stderr, '+\
                      'i.e. add <br> at the end of each line.')
    parser.add_option('', '--load-save', dest='loadSaveData'
                      , default=False, action='store_true'
                      , help='load, process, then save program data on pre-specified file(s)')
    parser.add_option('-l', '--load', dest='loadData'
                      , default=False, action='store_true'
                      , help='only load program data from pre-specified files(s)')
    parser.add_option('-d', '--debug', dest='debug', metavar='VALUE'
                      , help='turn on debug mode, with debug VALUE specified.'
                      )
    global options, positional
    options, positional = parser.parse_args(args)
    
    #check
    if options.debug:
        notify("DEBUG flag is ON")
        notify("DEBUG Option:", options.debug, '\n')
