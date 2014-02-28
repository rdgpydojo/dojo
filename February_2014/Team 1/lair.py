import pygame.image

F_INSIDE = 1
F_OUTSIDE = 2
F_BOTH = F_INSIDE | F_OUTSIDE

IMG_PATH = 'sprites/'

ROOMS = (
	# Filename, W, Flags, 
	('dish.png', 8, F_OUTSIDE),
	('shark-tank.png', 7, F_INSIDE),
	('bunks.png', 5, F_INSIDE),
	('cafeteria.png', 7, F_INSIDE),
	('elevator.png', 3, F_INSIDE),
)


def get_rooms():
	for filename, width, flags in ROOMS:
		sprite = pygame.image.load(IMG_PATH + filename)
		yield sprite, width, flags


if __name__ == '__main__':
	for n in get_rooms():
		pass