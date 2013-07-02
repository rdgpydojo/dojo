

import pygame
import math

class light(pygame.sprite.Sprite):
    LIGHTUPDATEFREQUENCY = 3000
    def __init__(self, color, xpos, ypos):
        pygame.sprite.Sprite.__init__(self)

        #Load our player character image
        self.image_list = []
        self.image_list.append( pygame.image.load("red.jpg").convert())
        self.image_list.append( pygame.image.load("green.jpg").convert())
        self.image_list.append( pygame.image.load("amber.jpg").convert())


        #Update the size of the player
        self.rect = self.image_list[0].get_rect()
        
        self.rect.x = xpos
        self.rect.y = ypos
        self.clock = pygame.time.Clock()
        pygame.time.set_timer(pygame.USEREVENT + 1, self.LIGHTUPDATEFREQUENCY)
        self.current_color = color
        
    def get_current_light(self):
        return self.current_color
     
#    def make_me(self, screen):
#        if self.current_color == "green":#
			#screen.blit(self.image_list[1], self.rect)
		#else:
	
    def switch_light(self, screen):
        if self.current_color == "green":
            self.current_color = "red"
            screen.blit(self.image_list[0], self.rect)
        else:
            self.current_color = "green"
            screen.blit(self.image_list[1], self.rect)
