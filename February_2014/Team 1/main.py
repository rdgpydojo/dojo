import pygame
import random
import lair

SCREEN_SIZE = [1000, 500]

WIDTH=50
HEIGHT=5

TILE_WIDTH = 20
TILE_HEIGHT = 100

EMPTY_OUTSIDE = 1
EMPTY_INSIDE  = 2
WALL = 100
OCCUPIED_OUTSIDE = 101
OCCUPIED_INSIDE = 102

building_grid = []

colours = dict()

colours[EMPTY_OUTSIDE] = ( 0, 0, 0)
colours[EMPTY_INSIDE] = ( 160, 160, 160)
colours[WALL] = ( 160, 80, 0)
colours[OCCUPIED_OUTSIDE] = ( 0, 0, 0)
colours[OCCUPIED_INSIDE] = ( 160, 160, 160)

def generate_grid():
	global building_grid
	building_grid = [
		[ EMPTY_OUTSIDE ] * WIDTH # row 
		for y in range(HEIGHT)
		]

def generate_floor(y, minx, maxx):
	global building_grid
	# pick the left-hand and right-hand side
	lh = random.randint(minx, 17)
	rh = random.randint(30,maxx)
	building_grid[y][lh] = WALL # lh wal
	for x in range(lh+1,rh):
		building_grid[y][x] = EMPTY_INSIDE
	building_grid[y][rh] = WALL # rh wall
	
	return lh, rh

def draw_scene():
	pygame.init()

	screen = pygame.display.set_mode(SCREEN_SIZE)
	
	black = (0,0,0)
	white = (255,255,255)
	screen.fill(black)
	
	sprites = list(lair.get_rooms())
	
	for rect_y in range(HEIGHT):
		for rect_x in range(WIDTH):
			tile = building_grid[rect_y][rect_x]
			colour = colours[tile]
			screenx = rect_x * TILE_WIDTH
			screeny = SCREEN_SIZE[1] - (rect_y * TILE_HEIGHT)
			pygame.draw.rect(screen, colour, [screenx, screeny, TILE_WIDTH, TILE_HEIGHT])
			
			if tile in [ EMPTY_INSIDE, OCCUPIED_INSIDE]:
				#draw a floor on this tile
				tbot = screeny + TILE_HEIGHT - 1
				#ceiling
				ttop = screeny
				for lineh in [ttop, tbot]:
					pygame.draw.line(screen, white, (screenx, lineh), (screenx + TILE_WIDTH, lineh) )
	
	room = sprites[2][0]
	
	screen.blit(room, [0, 0]) 
	
	pygame.display.flip()
	
	done = False
	
	while done == False:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True

	pygame.quit()

def main():
	generate_grid()
	minx, maxx = 3,48
	for floor in range(5):
		minx, maxx = generate_floor(floor, minx, maxx)
		print repr(building_grid[floor])
	draw_scene()

if __name__ == '__main__':
	main()
