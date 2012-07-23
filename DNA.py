import sys
sys.setrecursionlimit(10000)

import random
from copy import copy, deepcopy
from Constants import MAX_RANGE, STATUS_MAX_LEN

class Node:
    """
    a node in the dna
    """
    def __init__(self, sub=[]):
        self.sub = sub
        self.count = 1 + sum(sub.count for sub in self.sub)

    def eval(self, data):
        raise NotImplementedError()

    def _replaceSubtree(self, point, tree):
        """
        replace this tree at a point with a new tree

        return a copy of this new tree
        """
        if point == 0:
            return tree
        point -= 1
        newSelf = copy(self) # shallow copy
        newSelf.sub = copy(self.sub) #shallow copy
        for idx, sub in enumerate(newSelf.sub):
            if point < sub.count:
                break
            point -= sub.count
        newSub = sub._replaceSubtree(point, tree)
        if newSub == None:
            return None
        if isinstance(sub, ActionNode) == isinstance(newSub, ActionNode):
            newSelf.sub[idx] = newSub
            newSelf.count += newSub.count - sub.count
            return newSelf
        return None

    def _pickSubtree(self, point):
        """
        pick a subtree using BFS order
        """
        if point == 0:
            return deepcopy(self)
        point -= 1
        for sub in self.sub:
            if point < sub.count:
                return sub._pickSubtree(point)
            point -= sub.count

    def crossover(self, otherDNA):        
        newSub = otherDNA._pickSubtree(random.randrange(otherDNA.count))
        return self._replaceSubtree(random.randrange(1, self.count), newSub)



class If:
    def eval(self, data):
        if self.sub[0].eval(data):
            sub = self.sub[1]
        else:
            sub = self.sub[2]
        return sub.eval(data)       


"""
Logic nodes Def
"""

class LogicNode(Node):
    pass

class One(LogicNode):
    def __str__(self):
        return "One()"
    def eval(self, _):
        return True

class Zero(LogicNode):
    def __str__(self):
        return "Zero()"
    def eval(self, _):
        return False

class And(LogicNode):
    def __str__(self):
        return "And(%s, %s)" % tuple(self.sub)
    
    def eval(self, data):
        return self.sub[0].eval(data) and self.sub[1].eval(data)

class Or(LogicNode):
    def __str__(self):
        return "Or(%s, %s)" % tuple(self.sub)

    def eval(self, data):
        return self.sub[0].eval(data) or self.sub[1].eval(data)

class Not(LogicNode):
    def __str__(self):
        return "Not(%s)" % self.sub[0]
    def eval(self, data):
        return not self.sub[0].eval(data)

class LogicIf(If, LogicNode):
    def __str__(self):
        return "LogicIf(%s, %s, %s)" % tuple(self.sub)

class Compare(LogicNode):
    def __init__(self, sub):
        LogicNode.__init__(self, sub)
        self.range = random.randrange(-MAX_RANGE, MAX_RANGE+1)
        self.compare = random.choice([1, -1])
        self.idx = random.randrange(STATUS_MAX_LEN)
    def __str__(self):
        if self.compare == 1:
            comparator = '>'
        else:
            comparator = '<'
        return 'Compare(status[%d] %s %d)' % (self.idx, comparator, self.range)
    def eval(self, status):
        return cmp(status[self.idx], self.range) == self.compare


class Action:
    MOVE_NORTH = (0, -1)
    MOVE_EAST = (1, 0)
    MOVE_SOUTH = (0, 1)
    MOVE_WEST = (-1, 0)
    MOVE_NONE = (0, 0)
    MOVE_LIST = [MOVE_NORTH, MOVE_EAST, MOVE_SOUTH, MOVE_WEST, MOVE_NONE]


"""
Action nodes Def
"""
class ActionNode(Node):
    pass
    

class North(ActionNode):
    def __str__(self):
        return "North()"
    def eval(self, _):
        return Action.MOVE_NORTH

class East(ActionNode):
    def __str__(self):
        return "East()"
    def eval(self, _):
        return Action.MOVE_EAST

class South(ActionNode):
    def __str__(self):
        return "South()"
    def eval(self, _):
        return Action.MOVE_SOUTH

class West(ActionNode):
    def __str__(self):
        return "West()"
    def eval(self, _):
        return Action.MOVE_WEST

class NoMove(ActionNode):
    def __str__(self):
        return "NoMove()"
    def eval(self, _):
        return Action.MOVE_NONE

class Random(ActionNode):
    def __str__(self):
        return "Random()"    
    def eval(self, _):
        return random.choice(Action.MOVE_LIST)
    def crossover(self, _):
        return copy(self)

class ActionIf(If, ActionNode):
    def __str__(self):
        return "ActionIf(%s, %s, %s)" % tuple(self.sub)



ACTION_IF_WEIGHT = 4
ACTION_NODES = [ActionIf] * ACTION_IF_WEIGHT + [North(), East(), South(), West(), NoMove()] #, Random]

PURE_LOGIC_NODES = ((LogicIf, 3), (And, 2), (Or, 2), (Not, 1), (One(), 0), (Zero(), 0))

LOGIC_COMPARE_WEIGHT = 20
LOGIC_NODES = list(PURE_LOGIC_NODES) + [(Compare, 0)] * LOGIC_COMPARE_WEIGHT



class DNA(ActionIf):
    def __init__(self):
        ActionIf.__init__(self,
                          [self.randomLogicTree()
                           , self.randomActionTree()
                           , self.randomActionTree()
                           ])

    def randomActionTree(self):
        node = random.choice(ACTION_NODES)
        if node == ActionIf:
            return ActionIf([self.randomLogicTree()
                             , self.randomActionTree()
                             , self.randomActionTree()
                             ])
        else:
            return node

    def randomLogicTree(self):
        node, subNum = random.choice(LOGIC_NODES)
        if subNum != 0 or node == Compare:
            args = [self.randomLogicTree() for _ in range(subNum)]
            return node(args)
        else:
            return node
        
