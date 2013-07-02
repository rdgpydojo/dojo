import pygame
from pygame.locals import *

pygame.init()
fpsClock = pygame.time.Clock()

id=0
cars=[]

moveSize = 5 # Must be the same width as the car
screenWidth = 1024
screenHeight = 640
screen = pygame.display.set_mode((screenWidth,screenHeight))
pygame.display.set_caption("rdgpydojo traffic simulator")

black = pygame.Color("black")

def update():
	screen.fill(black)
	for car in cars:
		x=car[1];y=car[2];carpng=car[4]
		screen.blit(carpng,(x,y))

def moveCars():
	for icar in cars:
		direction=icar[0]
		ix=icar[1];iy=icar[2];iid=icar[3];icarpng=icar[4]
		if direction==K_RIGHT:
			# We don't move if the car will collide with another
			l=[]
			for jcar in cars:
				jx=jcar[1];jy=jcar[2];jid=jcar[3];jcarpng=jcar[4]
				jcarrect=jcarpng.get_rect()
				if jid!=iid:
					l.append([jx,jy,jcarrect.width,jcarrect.height])
			print jcar,l
			res=icarpng.get_rect().collidelist(l)
			if res!=-1:
				print "Collision of %d with %d!" % (iid,jid)
			else:
				icar[1]+=moveSize				
		elif direction==K_DOWN:
			icar[2]+=moveSize
			# We don't move if the car now collides with another
	

def addCar(direction):
	''' Add a car from the provided direction '''
	print "addCar"
	global id,cars
	if direction==K_RIGHT:
		carpng = pygame.image.load("car-left.png")
		carrect = carpng.get_rect()
		carX=carrect.width;carY=carrect.height
		screen.blit(carpng,(0,screenHeight/2-carY/2))
		cars.append([K_RIGHT,0,screenHeight/2-carY/2,id,carpng])
	elif direction==K_DOWN:
		carpng = pygame.image.load("car-down.png")
		carrect = carpng.get_rect()
		carX=carrect.width;carY=carrect.height
		screen.blit(carpng,(screenWidth/2-carX/2,0))
		cars.append([K_DOWN,screenWidth/2-carX/2,0,id,carpng])
	id+=1
	
def doInput():
	for event in pygame.event.get():
		if event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				exit()
			elif event.key == K_RIGHT:
				addCar(K_RIGHT)
			elif event.key == K_DOWN:
				addCar(K_DOWN)
	
while True:
	fpsClock.tick(30)
	doInput()
	moveCars()
	update()
	pygame.display.flip()
