import random
from Constants import *
from DNA import DNA, Action

X = 0
Y = 1

def getRelativePos(dist):
    """
    get relative pos at this distance
    """
    dist = abs(dist)
    pos = []
    for i in xrange(-dist, dist+1):
        j = dist - abs(i)
        if j == 0:
            pos.append((i,j))
        else:
            pos.extend([(i, -j), (i, j)])
    return pos

REL_POSES = []
for i in range(0, MAX_RANGE+1):
    REL_POSES.append(getRelativePos(i))

class Life:
    """
    Base class of all living things
    """
    def __init__(self, land, pos):
        self.land = land
        self.pos = pos
    
class Grass(Life):
    SELF_CLASS = GRASS
    def __init__(self, *args):
        Life.__init__(self, *args)
        self.remainingDays = random.randrange(50) #(30, 50)

class Animal(Life):
    """
    an animal is a life which has DNA to instruct it do things
    """
    ARBITARY_LONG_DIST = [-1000, 1000]
    
    def __init__(self, land, pos, dna=None):
        Life.__init__(self, land, pos)
        self.livingDays = 0
        self.remainingDays = random.randrange(40) #(10, 20)
        self.dna = dna
        if not self.dna:
            self.dna = DNA()
    
    def updateStatus(self):
        """
        update the animal's status

        shuffle positions with equal distance
        so that it won't favour paticular ones
        """
        status = self.status = [None] * STATUS_MAX_LEN
        for poses in REL_POSES:
            random.shuffle(poses) # shuffle
            for pos in poses:
                globalPos = self.land.transformPos((pos[X]+self.pos[X], pos[Y]+self.pos[Y]))
                if not self.land.pos.has_key(globalPos):
                    continue
                lives = self.land.pos[globalPos]
                if lives[self.__class__.FOOD_CLASS] and status[0] == None:
                    status[0:2] = pos
                if lives[self.__class__.OTHER_CLASS] and status[2] == None:
                    status[2:4] = pos
                if len(lives[self.__class__.SELF_CLASS]) > 1 and status[4] == None:
                    status[4:6] = pos
                if status[0] != None and status[2] != None and status[4] != None:
                    # hope will save a bit of checking when it's very crowded
                    return
    
    def proposeMove(self):
        """
        propose to move to a new location
        """
        for i in range(STATUS_MAX_LEN):
            if self.status[i] == None:
                self.status[i] = random.choice(self.__class__.ARBITARY_LONG_DIST)
        dX, dY = self.dna.eval(self.status)
        x, y = self.pos
        return (x+dX, y+dY)
        
            
    def eat(self):
        """
        try to eat if there's any food
        """
        foodDict = self.land.pos[self.pos][self.FOOD_CLASS]
        if not foodDict:
            return
        life = random.choice(foodDict.keys()) #random choice
        self.remainingDays += life.remainingDays
        self.land.kill(life)

    def mate(self):
        """
        try to mate with the same species
        """
        mates = self.land.pos[self.pos][self.__class__.SELF_CLASS].keys()
        mates.remove(self)
        if mates:
            self._crossover(random.choice(mates)) #random choice


    def _crossover(self, life):
        if not self.remainingDays and not life.remainingDays:
            return
        newDNA = self.dna.crossover(life.dna)
        if not newDNA:
            return
        if self.remainingDays:
            r1 = random.randrange(self.remainingDays)
            self.remainingDays -= r1
        else:
            r1 = 0
        if life.remainingDays:
            r2 = random.randrange(life.remainingDays)
            life.remainingDays -= r2
        else:
            r2 = 0
        newLife = self.__class__(self.land, self.pos[:], newDNA)
        newLife.remainingDays = r1 + r2
        self.land.register(newLife)


class Zebra(Animal):
    SELF_CLASS = ZEBRA
    FOOD_CLASS = GRASS
    OTHER_CLASS = LION

class Lion(Animal):
    SELF_CLASS = LION
    FOOD_CLASS = ZEBRA
    OTHER_CLASS = GRASS
