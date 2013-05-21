import cells
import random
import math


directions = [
    (-1, 0),
    (1, 0),
    (0, 1),
    (0, -1),
]

class AgentMind:

    def __init__(self, *args):
        self.target = None
        self.act = self.scout
    
    def scout(self, view, msg):
        me = view.get_me()
        if me.energy < 20:
            return self.search(view, msg)
        
        if self.target is None:
            ang = random.random() * 2 * math.pi
            tx = me.x + int(100 * math.sin(ang))
            ty = me.y + int(100 * math.cos(ang))
            self.target = tx, ty
            #print "New target", self.target
        else:
            tx, ty = self.target
        
        dx, dy = tx - me.x, ty - me.y
        
        if not dx or dy:
            self.target = None
            return self.search(view, msg)
        if abs(dx) > abs(dy):
            return cells.Action(cells.ACT_MOVE, (dx / abs(dx), 0))
        return cells.Action(cells.ACT_MOVE, (0, dy / abs(dy)))

    def search(self, view, msg):
        action, action_pos = self.searchArea(view)
        if action == "attack":
            return cells.Action(cells.ACT_ATTACK, action_pos)
        elif action == "move":
            return cells.Action(cells.ACT_MOVE, action_pos)
        else:
            return self.act_random(view, msg)
    
    def act_random(self, view, msg):
        op = random.randint(0, 2)
        me = view.get_me()            
        if op == 0:
            return cells.Action(cells.ACT_MOVE, self.getDirection(me))
        elif op == 1 and me.energy > 50:
            return cells.Action(cells.ACT_SPAWN, self.getDirection(me))
        return cells.Action(cells.ACT_EAT)
    
    def getDirection(self, me):
        dx, dy = random.choice(directions)
        return me.x + dx, me.y + dy

    def searchArea(self, view):
        agents = view.get_agents()
        for agent in agents:
            if agent.get_team() != view.get_me().get_team():
                return "attack", agent.get_pos()
            else:
                ax, ay = agent.get_pos()
                me = view.get_me()
                return 'move', (me.x - (ax - me.x), me.y - (ay - me.y))
        return None, None
        
                        
        