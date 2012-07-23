import time
import cmdLineArgs
from Constants import GRASS, ZEBRA, LION
from Land import Land

class Nature:
    """
    the mother nature
    
    drive the land, then record some stats
    """
    def __init__(self):
        self.land = Land(width=400, height=300)
        if cmdLineArgs.options.debug:
            self.land.reset(2000, 2000, 500, 2500) # test, for fast init window show up
        else:
            self.land.reset(40000, 30000, 10000, 2500)
        self.day = 0
        self.timeDelta = 0
        #clear the file for stats recording
        if not cmdLineArgs.options.debug:
            open('data.log', 'w').close()
            self.recordStats()

    def newDay(self):
        """
        runs land.newDay()

        record down some stats
        """
        stamp = time.clock()
        self.day += 1
        self.land.newDay()
        self.timeDelta = time.clock() - stamp
        if self.timeDelta < 0:
            self.timeDelta = -1
        self.recordStats()

    def recordStats(self):
        """
        record the stats to a file
        """
        if cmdLineArgs.options.debug:
            return
        dataFile = open('data.log', 'a')
        print >> dataFile, ' '.join(map(str, self.getStats()))       


    def getStats(self):
        species = self.land.species
        longestDays = []
        for lifeClass in [ZEBRA, LION]:
            animal = self.land.livingLongest[lifeClass]
            if animal:
                days = animal.livingDays 
            else:
                days = 0
            longestDays.append(days)
        return (self.day
                , len(species[GRASS]) 
                , len(species[ZEBRA]) 
                , len(species[LION])
                , self.timeDelta
                , longestDays[0]
                , longestDays[1]
                )
    
