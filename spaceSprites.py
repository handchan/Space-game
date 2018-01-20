"""Author: Hengcheng Yu
   Date: April 27, 2016
   
   Description: This module defines the sprites used for my superbreakout game.
   it includes the bullet sprite, the player sprite, the alien sprite, the 
   endzone sprite, the explosion sprite, the neutral alien sprite,
   the power up sprite, the background sprite, and the life tracker sprite.
"""

import pygame
import random

            
class Player(pygame.sprite.Sprite):
    """This class defines the sprite for the player"""
    def __init__(self,screen,player_num):
        """This method initializes the attributes of the player sprite, fire
        rate, whether it has 2 bullets or 1, screen, speed,image,and position."""
        
        self.__double_bullets=False
        self.__fire_rate=35
        self.__speed=5
        self.__screen = screen
        pygame.sprite.Sprite.__init__(self)
        self.width = screen.get_width()
        if player_num==1:
            self.image=pygame.image.load("Images/tank1.gif").convert()
        
        elif player_num==2:
            self.image=pygame.image.load("Images/tank2.gif").convert() 
        
        self.rect= self.image.get_rect()
        self.rect.left= screen.get_width()/2-50
        
        if player_num==1:
            self.rect.bottom = 980
            
        elif player_num==2:
            self.rect.bottom = 45
        self.__dx = 0
        
        self.__dead=False
        
    def double_bullets(self):
        """This method changes the attribute that controls whether the player
        gets to fire 2 bullets or 1, so that the player fires 2 bullets."""
        self.__double_bullets=True
    
    def get_double(self):
        """This method returns True or False, that the player can fire 2 
        bullets."""
        return self.__double_bullets
    
    def speed_up(self):
        """This method increases the speed up to a limit."""
        if self.__speed<=10:
            self.__speed+=1
    
    def speed_fire(self):
        """This method increases the fire rate up to a limit."""
        if self.__fire_rate>15:
            self.__fire_rate-=5
            
    def get_fire_rate(self):
        """This method returns the fire rate"""
        return self.__fire_rate

        
    def change_direction(self, xy_change):
        """This method changes the direction of the player."""
        self.__dx = xy_change[0]
        

            
    def stop(self):
        """This method stops the player."""
        self.__dx = 0
    
    def get_pos(self,player_num):
        """This method returns the position of the player."""
        if player_num==1:
            return (self.rect.left+50,980)
        elif player_num==2:
            return (self.rect.left+50,20)
    

        
            
    def update(self):
        """This method makes sure that the player doesn't leave the screen."""
        if ((self.rect.left > -5) and (self.__dx > 0)) or\
            ((self.rect.right < self.__screen.get_width()) and (self.__dx < 0)):
            self.rect.left -= (self.__dx*self.__speed)
            

class Bullet(pygame.sprite.Sprite):
    """This class defines the sprite for the bullets"""
    def __init__(self,player_num, xy_pos,alien):
        """This method initializes the player number, position and whether
        it is a player or alien."""
        
        pygame.sprite.Sprite.__init__(self)                
        self.__player_num = player_num
        
        if self.__player_num==1:
            self.image=pygame.image.load("Images/rocket.gif").convert()
            if alien==True:
                self.__dy=5
            else:
                self.__dy = 12
            
        
        elif self.__player_num==2:
            self.image=pygame.image.load("Images/rocket2.gif").convert()
            if alien==True:
                self.__dy=-5
            else:
                self.__dy = -12
        

        
        self.rect = self.image.get_rect()
        self.rect.left = xy_pos[0]
        self.rect.bottom = xy_pos[1]
        
                

    
    def get_pos(self):
        """This method returns the position of the bullet."""
        return (self.rect.left,self.rect.bottom)
    

        
    def update(self):
        """This method is automatically called, it moves the bullet and 
        kills them when they are far off the screen."""
        self.rect.top -= self.__dy
        
        if (self.rect.bottom>=1100) or (self.rect.bottom<=-100):
            self.kill()
            

class NeutralAlien(pygame.sprite.Sprite):
    """This class defines the sprite for the neutral alien."""
    def __init__(self,screen,side):
        """This method initializes the screen and the side in which it spawns."""
        pygame.sprite.Sprite.__init__(self)
        self.__screen=screen
        self.image=pygame.image.load("Images/neutral.gif").convert()
        self.rect=self.image.get_rect()
        if side==1:
            self.rect.left = -40
            self.__dx = 5
            
        elif side==2:
            self.rect.left= 1320
            self.__dx = -5
            
        self.rect.bottom = screen.get_height()/2+25
    
        
    def get_power(self):
        """This method returns a random power up."""
        self.__power=random.randint(1,5)
        
    def get_x(self):
        """This method returns the x position."""
        return self.rect.left
    
    def update(self):
        """This method is automatically called to move the sprite and kills it
        when it is far off the screen."""
        
        self.rect.left+=self.__dx
        
        if self.rect.left==1400 or self.rect.left==-200:
            self.kill()
            

        


class Explosion(pygame.sprite.Sprite):
    """This class defines the sprite for the explosion."""
    
    def __init__(self,center,time,colour,player):
        """This method initializes the attributes for position, time, colour 
        of explosion, and the plays side it it for."""
        
        pygame.sprite.Sprite.__init__(self)
        self.__colour=colour
        self.__explode_list=[]
        if player==1:
            for image in range(1,5):
                self.__explode_list.append(pygame.image.load("Images/"+str(self.__colour+1)+"explode"+ str(image) + ".gif").convert())
        elif player==2:
            for image in range(1,5):
                self.__explode_list.append(pygame.image.load("Images/2P"+str(self.__colour+1)+"explode"+ str(image) + ".gif").convert())
                
        elif player==-1:
            for image in range(1,5):
                self.__explode_list.append(pygame.image.load("Images/explosion"+str(image) + ".gif").convert())
                
        elif player==-2:
            for image in range(1,5):
                self.__explode_list.append(pygame.image.load("Images/neutral_explode"+str(image) + ".gif").convert())
        
        self.image= self.__explode_list[0]
        self.rect=self.image.get_rect()
        self.rect.center= center
        self.__frame=0
        self.__time=time
        self.__last_update = self.__time
        self.__delay=3
        self.__dead=False
        self.__state=0
        
    def get_life(self):
        """This method returns the state of the explosion as True of False."""
        return self.__dead
    
    def update(self):
        """This method is called automatically to create the explosion animation."""
        self.__time+=1
        if self.__last_update+self.__delay < self.__time:
            self.__state+=1
            self.__delay+=5
            
            if self.__state>=4:
                self.kill()
                self.__dead=True
                
            elif self.__state<=4:
                self.image=self.__explode_list[self.__state]
                
        

    
class Alien(pygame.sprite.Sprite):
    """This class defines the sprite for the aliens."""
    
    def __init__(self,player,screen,xy_pos,colour):
        """This method initializes the attributes for the player's side,
        screen, position, and colour."""
        
        pygame.sprite.Sprite.__init__(self)
        self.__colour=colour
        
        self.__image_list=[]
        self.__image_list2=[]
        
        
        if player==1:
            for image in range(1,6):
                self.__image_list.append(pygame.image.load("Images/alien" + str(image) + ".gif"))
                
            for image in range(1,6):
                self.__image_list2.append(pygame.image.load("Images/stance2alien" + str(image) + ".gif"))   
            
                

            self.__dx=13.75
            self.__dy=20            
        
        elif player==2:
            for image in range(1,6):
                self.__image_list.append(pygame.image.load("Images/P2alien" + str(image) + ".gif")) 
                
            for image in range(1,6):
                self.__image_list2.append(pygame.image.load("Images/P2stance2alien" +str(image) + ".gif"))
                
                
            self.__dx=-13.75
            self.__dy=-20
            
        
        self.image=self.__image_list[self.__colour]

        
        
        self.rect=self.image.get_rect()
        self.rect.left=xy_pos[0]
        self.rect.bottom=xy_pos[1]
        self.__dead=False


    def get_pos(self):
        """This method returns the position of the alien."""
        return (self.rect.left,self.rect.bottom)
   
    def get_colour(self):
        """This method returns the colour of the alien."""
        return self.__colour
        
    def x_move(self):
        """This method moves the alien horizontally."""
        self.rect.left += self.__dx
        
    def y_move(self):
        """This method moves the alien vertically."""
        self.rect.bottom += self.__dy
        self.__dx=-self.__dx
        self.rect.left+=self.__dx
    
    def change_stance(self):
        """This method changes the image for the stance of the alien."""
        
        if self.image in self.__image_list:
            self.image=self.__image_list2[self.__colour]
        
        else:
            self.image=self.__image_list[self.__colour]
            
    


            
        
        
class EndZone(pygame.sprite.Sprite):
    """This class defines the sprite for the top and bottom end zones."""
    def __init__(self, screen, y_position):
        """This method initializes the screen, and y_position of the end zones."""
    
        pygame.sprite.Sprite.__init__(self)
         
        # The endzone sprite will be a 1 pixel wide line.
        self.image = pygame.Surface((screen.get_width(),1))
        self.image = self.image.convert()
        self.image.fill((255, 255, 255))
         
        # Set the rect attributes for the endzone
        self.rect = self.image.get_rect()
        self.rect.left = 0
        self.rect.top = y_position

class Background(pygame.sprite.Sprite):
    """This class defines the background sprite."""
    def __init__(self):
        """This method initializes the image for the background."""
        pygame.sprite.Sprite.__init__(self)
        
        self.image=pygame.image.load("Images/background.jpg").convert()
        self.rect=self.image.get_rect()
        self.rect.left=0
        self.rect.top=0
        

class Wall(pygame.sprite.Sprite):
    """This class defines the wall sprite."""
    def __init__(self,xy_pos,player):
        """This method initializes the position and the player that it belongs to."""
        
        pygame.sprite.Sprite.__init__(self)
        if player==1:
            self.image=pygame.image.load("Images/wallfrag.gif").convert()
        elif player==2:
            self.image=pygame.image.load("Images/wallfrag2.gif").convert()
            
        self.rect=self.image.get_rect()
        self.rect.left=xy_pos[0]
        self.rect.bottom=xy_pos[1]

class LifeTracker(pygame.sprite.Sprite):
    """This class defines the sprite for the life trackers."""
    
    def __init__(self,player,health):
        """This method initializes the player it belongs to and their health."""
        pygame.sprite.Sprite.__init__(self)
        self.__health=health
        self.__display_bar=[]
        self.__player=player
        for image in range(1,4):
            self.__display_bar.append(pygame.image.load("Images/"+str(image) +"health"+ ".gif").convert())
        self.image=self.__display_bar[self.__health-1]
        self.rect=self.image.get_rect()
        self.rect.left=10
        if player==1:
            self.rect.bottom=870
        elif player==2:
            self.rect.top=110
        
    def lose_life(self):
        """This method reduces the player's health by 1."""
        if self.__health>0:
            self.__health-=1
        
        if self.__health==0:
            self.image=pygame.image.load("images/dead.gif")
        
        elif self.__health>0:
            self.image=self.__display_bar[self.__health-1]
        self.rect=self.image.get_rect()
        self.rect.left=10
        
        if self.__player==1:
            self.rect.bottom=870
        
        elif self.__player==2:
            self.rect.top=110
            
    def gain_life(self):
        """This method increases the player's health by 1."""
        if self.__health<3:
            self.__health+=1
        self.image=self.__display_bar[self.__health-1]
        self.rect=self.image.get_rect()
        self.rect.left=10
                
        if self.__player==1:
            self.rect.bottom=870
        
        elif self.__player==2:
            self.rect.top=110
            
    def show_life(self):
        """This method returns the health of the player."""
        return self.__health
            
            
class PowerUp(pygame.sprite.Sprite):
    """This class defines the power up sprite."""
    
    def __init__(self,player,power,center):
        """This method initializes the player who killed to neutral alien, the 
        power up and the position."""
        
        pygame.sprite.Sprite.__init__(self)
        self.__player=player
        self.__power=power
        self.__image_list=[]
        for image in range(4):
            self.__image_list.append(pygame.image.load("Images/power_up"+str(image+1)+ ".gif").convert())
        self.image=self.__image_list[self.__power]
        self.rect=self.image.get_rect()
        self.rect.center = center
        if player==1:
            self.__dy=5
        elif player==2:
            self.__dy=-5
            
    def get_powerup(self):
        """This method returns the type of power up."""
        return self.__power
    
    
    
    
    def update(self):
        """This method moves the power up and stops it at the ends of the screen."""
        if (self.rect.bottom>=970) or (self.rect.top<=10):
            self.__dy=0        
       
        if self.__player==1:
            self.rect.top += self.__dy
        
        if self.__player==2:
            self.rect.top += self.__dy
    