import random
from Constants import GRASS, ZEBRA, LION
from Life import Grass, Zebra, Lion

class Land:
    """
    a land remembers all lives and their locations

    also make the grass to grow

    """
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.species = [{}, {}, {}]
        self.pos = {}
        

    def reset(self, grassNum, zebraNum, lionNum, grassGrowNum=None):
        """
        reset all the lives on the land
        """
        for lifeClass in [GRASS, ZEBRA, LION]:
            self.species[lifeClass] = {}
        if grassGrowNum:
            self.grassGrowNum = grassGrowNum
        else:
            self.grassGrowNum = int(grassNum * 0.1)
        self.setLives(Grass, grassNum)
        self.setLives(Zebra, zebraNum)
        self.setLives(Lion, lionNum)
        self.livingLongest = {ZEBRA:None, LION:None, GRASS:None}

    def setLives(self, lifeClass, num):
        """
        set a number of lives on the land
        """
        for _ in xrange(num):
            pos = (random.randrange(self.width), random.randrange(self.height))
            life = lifeClass(self, pos)
            # register in this land
            self.register(life)

    def newDay(self):
        self.morning()
        self.afternoon()
        self.night()

    def morning(self):
        """
        in the morning of the day,
        some grass grows
        every animal update their status
        """
        self.setLives(Grass, self.grassGrowNum)
        for lifeClass in [ZEBRA, LION]:
            for animal in self.species[lifeClass]:
                # update status
                animal.updateStatus()
                # record which animal live the longest
                if not self.livingLongest[lifeClass] or \
                       animal.livingDays > self.livingLongest[lifeClass].livingDays:
                    self.livingLongest[lifeClass] = animal
                
                

    def afternoon(self):
        """
        in the afternoon,
        every animal is moving
        """
        for lifeClass in [ZEBRA, LION]:
            for animal in self.species[lifeClass]:
                newPos = animal.proposeMove()
                if newPos == animal.pos:
                    continue
                self.pos[animal.pos][animal.__class__.SELF_CLASS].pop(animal)
                animal.pos = self.transformPos(newPos)
                self.register(animal, posOnly=True)

    def transformPos(self, pos):
        x, y = pos
        if x < 0:
            x += self.width
        elif x >= self.width:
            x -= self.width
        if y < 0:
            y += self.height
        elif y >= self.height:
            y -= self.height
        return (x,y)
        
    def night(self):
        """
        at night time
        some lives die, some eat their food to survive, some mate as well
        """
        for life in self.species[GRASS].keys():
            life.remainingDays -= 1
            if life.remainingDays <= 0:
                self.kill(life)            
        for lifeClass in [ZEBRA, LION]:
            livingLongest = self.livingLongest[lifeClass]
            for life in self.species[lifeClass].keys():
                life.eat() # try to eat
                if random.random() > 0.5:
                    life.mate() # half chance to mate                
                life.remainingDays -= 1
                if life.remainingDays <= 0:
                    self.kill(life)
                else:
                    life.livingDays += 1



    def kill(self, life, popPos=True):
        """
        kill this life
        """
        self.species[life.__class__.SELF_CLASS].pop(life)
        if popPos:
            self.pos[life.pos][life.__class__.SELF_CLASS].pop(life)
        if self.livingLongest[life.__class__.SELF_CLASS] == life:
            self.livingLongest[life.__class__.SELF_CLASS] = None
        del life


    def register(self, life, posOnly=False):
        """
        remember this life        
        """
        if not posOnly:
            self.species[life.__class__.SELF_CLASS][life] = None
        self.pos.setdefault(life.pos, [{}, {}, {}])[life.__class__.SELF_CLASS][life] = None

