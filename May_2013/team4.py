#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Mark
#
# Created:     21/05/2013
# Copyright:   (c) Mark 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import cells, random, math

class AgentMind:
    def __init__(self, *args):
        self.target_range = 50
        self.prevx = 0
        self.prevy = 0
        self.moved = False
        # self.dirx, self.diry = (1,0)
        self.set_random_target()

    def act(self, view, msg):
        me = view.get_me() # gets my info
        # Current position
        (mx, my) = me.get_pos()
        # If we have less energy then we are hungry
        hungry = (me.energy < self.target_range)
        full = (me.energy > 1000)
        energy_here = view.get_energy().get(mx, my)
        food = (energy_here > 0)
        if hungry and food or (energy_here > 100 and not full):
            self.moved = False
            return cells.Action(cells.ACT_EAT)

        # Check whether we are stuck!
        if self.is_stuck(me):
            # Change direction
            # self.dirx, self.diry = (self.diry, -self.dirx)
            self.set_random_target()

        # Move somewhere.
        # New position
        newx = mx
        newy = my
        # Move towards target
        if self.targetx > newx:
            newx += 1
        if self.targetx < newx:
            newx -= 1
        if self.targety > newy:
            newy += 1
        if self.targety < newy:
            newy -= 1
        if (self.targetx, self.targety) == (newx, newy):
            # Reached destination
            return cells.Action(cells.ACT_SPAWN, (self.prevx, self.prevy))

        # Rememeber that we tried to move, and our prev coords.
        self.moved = True
        self.prevx, self.prevy = mx, my
        return cells.Action(cells.ACT_MOVE, (newx, newy))

    def is_stuck(self, me):
        return (me.get_pos() == (self.prevx, self.prevy) and self.moved)

    def set_random_target(self):
        self.targetx = random.randrange(0,300)
        self.targety = random.randrange(0,300)
