import pygame
from lights import light

class traffic:

    screen_width = 1024
    screen_height = 768
    
    def __init__(self):
        pygame.init()
        #Initialise the display
        self.screen = pygame.display.set_mode([self.screen_width,self.screen_height])
        
        self.car_sprites_list = pygame.sprite.RenderPlain()
        
        self.lights_sprites_list = pygame.sprite.RenderPlain()
        self.lights = []
        self.lights.append(light("green", 225, 150))
        self.lights.append(light("red", 725, 550))
        
        self.background = pygame.image.load("road.jpg")
        self.background_rect = self.background.get_rect()
        self.clock = pygame.time.Clock()
    
    def run(self):

        while(True):
            self.screen.blit(self.background, self.background_rect)
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT + 1:
					for light in self.lights:
						light.switch_light(self.screen)
            
                pygame.display.flip()
            
            self.clock.tick(30)
