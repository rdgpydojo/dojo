import sys
import random

# Usage: python traffic_sim.py map.txt

def read_map(f):
    grid = []
    for line in f:
        row = []
        line = line.rstrip('\n')
        for char in line:
            row.append({'type': char, 'traffic': 0})
        grid.append(row)
    return grid

def draw_map(grid):
    for row in grid:
        print ''.join( c['type'] for c in row)

def pick_poi(grid):
    ok = False
    while not ok:
        # pick x,y coords
        y = random.randrange(len(grid))
        x = random.randrange(len(grid[y]))
        # check if valid POI
        cell = grid[y][x]
        if cell['type'] in 'RIC':
            return (x,y)

def pick_pair(grid):
    '''Pick distinct start and end point
    '''
    start = end = None
    while start == end:
        start = pick_poi(grid)
        end = pick_poi(grid)
    return start, end

def valid_neighbours(grid, currentpos, endpos):
    x,y = currentpos
    possible_neighbours = [
        (x-1, y),
        (x+1, y),
        (x,y-1),
        (x,y+1),
        ]
    valid = []
    for x,y in possible_neighbours:
        # check passable
        # road OR destination.
        if grid[y][x]['type'] == '+' or ((x,y) == endpos):
            valid.append( (x,y) )
    return valid
        

def calc_route(grid, start, end):
    # dijkstra
    visited = set()
    valid = set()
    nextvalid = set()
    routes = { start: [] } # maps position to best route
    # put initial point into valid
    # to bootstrap
    valid.add( start )
    while True:
        if len(valid) == 0:
            raise Exception("No route possible! %s %s" % (start, end))
        for p in valid:
            if p == end:
                return routes[p]
            for n in valid_neighbours(grid, p, end):
                if n not in visited:
                    visited.add(n)
                    nextvalid.add(n)
                    routes[n] = routes[p] + [p]
        # prep next iteration
        valid = nextvalid
        nextvalid = set()
    

def sum_traffic(grid, route):
    pass

def output_traffic(grid):
    pass

if __name__ == '__main__':
    import sys
    f = open(sys.argv[1])
    grid = read_map(f)
    draw_map(grid)
    pair = pick_pair(grid)
    print repr(pair)
    route = calc_route(grid, *pair)
    for x,y in route:
        grid[y][x]['type'] = '#'
    draw_map(grid)
    print route
