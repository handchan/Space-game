"""
   Author: Hengcheng Yu
   Date: May 27, 2016
   
   Description: This program runs a 2 player space invaders game where players
   face off against eachother, trying to reduce the opponent's health to 0.
   The program begins with a menu where the players can choose to start or 
   view instructions. If they start the game they will have an unlimited amount
   of time to clear their aliens and try to attack the opponent. periodically 
   a neutral alien will spawn in the centre, killing it will grant the killer
   a huge advantage.

"""


# I - IMPORT AND INITIALIZE
import pygame, spaceSprites, random
pygame.init()
     
def game():
    """This function defines the game logic of my program"""
      
    # DISPLAY
    screen = pygame.display.set_mode((1280, 980))
    pygame.display.set_caption("Space Wars!")
    
    # ENTITIES
    
    # Background Music and Sound Effects
    pygame.mixer.music.load("Sounds/background_music.wav")
    pygame.mixer.music.set_volume(0.05)
    pygame.mixer.music.play(-1)
    shoot_sound = pygame.mixer.Sound("Sounds/laser.wav")
    shoot_sound.set_volume(0.1)
    alien_shoot_sound = pygame.mixer.Sound("Sounds/shoot.wav")
    alien_shoot_sound.set_volume(0.02)
    explode_sound= pygame.mixer.Sound("Sounds/player_explode.wav")
    explode_sound.set_volume(0.1)
    victory_sound= pygame.mixer.Sound("Sounds/cheering.wav")
    victory_sound.set_volume(1)
    
    neutral_taunts=[]
    for sounds in range(5):
        sound=pygame.mixer.Sound("Sounds/battle_cry"+str(sounds+1)+".wav")
        sound.set_volume(0.1)
        neutral_taunts.append(sound)
    
    neutral_death_noise=pygame.mixer.Sound("Sounds/neutral_death.wav")
    neutral_death_noise.set_volume(0.2)
    invader_killed_sound=pygame.mixer.Sound("Sounds/invaderkilled.wav")
    invader_killed_sound.set_volume(0.2)
    power_up_sound=pygame.mixer.Sound("Sounds/power_up.wav")
    power_up_sound.set_volume(0.1)
    
    
    
    #creates sprites for the background, players, players' health, and empty
    #list of power ups
    background = spaceSprites.Background()

    power_ups=[]
    power_group=pygame.sprite.Group(power_ups)

    player1=spaceSprites.Player(screen,1)
    player2=spaceSprites.Player(screen,2)
    
    player1_health=spaceSprites.LifeTracker(1,3)
    player2_health=spaceSprites.LifeTracker(2,3)
 
    #creates sprites for the endzones and empty lists for the neutral aliens,
    #bullets, and explosions
    bottom_end_zone = spaceSprites.EndZone(screen,940)
    top_end_zone = spaceSprites.EndZone(screen,40)
    end_zones=pygame.sprite.Group(bottom_end_zone,top_end_zone)
    
    neutral_alien=[]
    neutral_alien_group=pygame.sprite.Group(neutral_alien)
    
    explosions=[]
    bullets=[]
    player2_bullets=[]
    bullet_group= pygame.sprite.Group(bullets)
    bullet_group2= pygame.sprite.Group(player2_bullets)
    all_bullets=pygame.sprite.Group(bullets,player2_bullets)
    
    #creats each players walls
    blocker_wall=[]
    brick_y = 885
    for up in range(3):
        brick_x=-200
        brick_y+=13
        for bricks in range(35):
            blocker_wall.append( spaceSprites.Wall((brick_x,brick_y),1))
            brick_x+=16
            if brick_x%60==0:
                brick_x+=260
    blocker_group=pygame.sprite.Group(blocker_wall)  
                
    blocker_wall2=[]
    brick_y2 = 57
    for up in range(3):
        brick_x2=-200
        brick_y2+=13
        for bricks in range(35):
            blocker_wall2.append( spaceSprites.Wall((brick_x2,brick_y2),2))
            brick_x2+=16
            if brick_x2%60==0:
                brick_x2+=260    
    blocker_group2=pygame.sprite.Group(blocker_wall2)        

    #creates each players alien horde
    wall=[]
    alien_y = 524
    colour=5
    for up in range(5):
        alien_x=180
        alien_y+=37
        colour-=1
        for aliens in range(17):
            wall.append( spaceSprites.Alien(1,screen,(alien_x,alien_y),colour))
            alien_x+=55
    alien_group = pygame.sprite.Group(wall)
    
    wall2=[]
    alien_y2=263
    colour2=-1
    for up in range(5):
        alien_x2=166.25
        alien_y2+=37
        colour2+=1
        for aliens in range(17):
            wall2.append( spaceSprites.Alien(2,screen,(alien_x2,alien_y2),colour2))
            alien_x2+=55
    alien_group2 = pygame.sprite.Group(wall2)
    
    
    allSprites = pygame.sprite.OrderedUpdates(end_zones,background, player1_health,player2_health, blocker_group,blocker_group2,bullet_group,player1,player2,neutral_alien_group,alien_group,alien_group2,explosions,power_group)
    
    # ASSIGN 
    clock = pygame.time.Clock()
    keepGoing = True
    #create timers for reloading,exploding, and aliens pulsing
    shot_timer=120
    shot_timer2=120
    game_timer=0
    alien_pulse=0
    
    # Hide the mouse pointer
    pygame.mouse.set_visible(False)
    
    
 
    # LOOP
    while keepGoing:
  
        # TIME
        clock.tick(60)

        shot_timer+=1
        shot_timer2+=1
        alien_pulse+=1
        game_timer+=1
        
      
       # EVENT HANDLING
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                return keepGoing
                
            keys=pygame.key.get_pressed()
            
            #player 1 controls
            if keys[pygame.K_KP0] and (shot_timer>=player1.get_fire_rate()):
                shoot_sound.play()
                if player1.get_double()==True:
                    bullets.append(spaceSprites.Bullet(1,(player1.get_pos(1)[0]-25,player1.get_pos(1)[1]),False))
                    bullets.append(spaceSprites.Bullet(1,(player1.get_pos(1)[0]+25,player1.get_pos(1)[1]),False))
                
                else:   
                    bullets.append(spaceSprites.Bullet(1,player1.get_pos(1),False))
                bullet_group= pygame.sprite.Group(bullets)
                shot_timer=0
                
            if keys[pygame.K_LEFT]:
                player1.change_direction((1,0))
                    
            elif keys[pygame.K_RIGHT]:
                player1.change_direction((-1,0))
                 
            else:    
                player1.stop()
            
            #player 2 controls
            if keys[pygame.K_SPACE] and (shot_timer2>=player2.get_fire_rate()):
                shoot_sound.play()
                if player2.get_double()==True:
                    player2_bullets.append(spaceSprites.Bullet(2,(player2.get_pos(2)[0]-25,player2.get_pos(2)[1]),False))
                    player2_bullets.append(spaceSprites.Bullet(2,(player2.get_pos(2)[0]+25,player2.get_pos(2)[1]),False))
                    
                else:    
                    player2_bullets.append(spaceSprites.Bullet(2,player2.get_pos(2),False))
                
                bullet_group2= pygame.sprite.Group(player2_bullets)
                shot_timer2=0
            
            if keys[pygame.K_a]:
                player2.change_direction((1,0))
                                                
            elif keys[pygame.K_d]:
                player2.change_direction((-1,0))
                    
            else:    
                player2.stop()
        
        #checks to see if the game has ended, if it has, it returns an
        #integer which changes the background of the introduction screen 
        #displaying the winner
        past_line=pygame.sprite.groupcollide(alien_group, end_zones,False,False)
        past_line2=pygame.sprite.groupcollide(alien_group2, end_zones,False,False)
        if past_line and past_line2:
            victory_sound.play()
            return 4
                
        elif past_line:
            victory_sound.play()
            return 3
        elif past_line2:
            victory_sound.play()
            return 2
        
        
        if player1_health.show_life()==0:
            victory_sound.play()
            return 3
        if player2_health.show_life()==0:
            victory_sound.play()
            return 2
        
        #checks if player1 hit a power up, if so it checks which power up
        #it was and makes the appropriate changes reflecting the power up
        player1_power= pygame.sprite.spritecollide(player1,power_group,False)
        if player1_power:
            for power_up in player1_power:
                power_up_sound.play()
                
                if power_up.get_powerup()==0:
                    player1.speed_up()
                
                if power_up.get_powerup()==1:
                    player1_health.gain_life()
                    
                if power_up.get_powerup()==2:
                    player1.speed_fire()
               
                if power_up.get_powerup()==3:
                    player1.double_bullets()
                    
                power_ups.remove(power_up)
                power_up.kill()
                
        #checks if player2 hit a power up, if so it checks which power up
        #it was and makes the appropriate changes reflecting the power up        
        player2_power= pygame.sprite.spritecollide(player2,power_group,False)
        if player2_power:
            for power_up in player2_power:
                power_up_sound.play()
                
                if power_up.get_powerup()==0:
                    player2.speed_up()
                
                if power_up.get_powerup()==1:
                    player2_health.gain_life()
                            
                if power_up.get_powerup()==2:
                    player2.speed_fire()
                               
                if power_up.get_powerup()==3:
                    player2.double_bullets()
                
                power_ups.remove(power_up)
                power_up.kill()
        
        #spawns the neutral alien with a random power up either left or
        #right(chosen randomly).
        spawn=random.randint(1,800)
        if spawn==17:
            side=random.randint(1,2)
            sound=random.randint(0,4)
            neutral_taunts[sound].play()
            neutral=spaceSprites.NeutralAlien(screen,side)
            neutral_alien.append(neutral)
            neutral_alien_group=pygame.sprite.Group(neutral_alien)
        
        #checks to see if player 2 is hit
        player2_hit = pygame.sprite.spritecollide(player2, bullet_group, False)  
        
        if player2_hit:
            explode_sound.play()
            for bullet in player2_hit:
                bullets.remove(bullet)
                bullet.kill()
                explosion=spaceSprites.Explosion(player2.rect.center,game_timer,0,-1)
                explosions.append(explosion)
                player2_health.lose_life()
                           
        #checks to see if player 1 is hit        
        player1_hit = pygame.sprite.spritecollide(player1,bullet_group2, False)
        
        if player1_hit:
            for bullet in player1_hit:
                explode_sound.play()
                player2_bullets.remove(bullet)
                bullet.kill()
                explosion=spaceSprites.Explosion(player1.rect.center,game_timer,0,-1)
                explosions.append(explosion)
                player1_health.lose_life()
        
        
        # determines if the aliens for player1 will shoot and to move down if 
        # any alien in the horde hits a wall
        for aliens in wall:
            shoot=random.randint(1,6000)
            if shoot==11:
                alien_shoot_sound.play()
                player2_bullets.append(spaceSprites.Bullet(2, aliens.rect.center,True))
                bullet_group2= pygame.sprite.Group(player2_bullets)
            
            if aliens.get_pos()[0]>=1230 or aliens.get_pos()[0]<=0:
                for alien in wall:
                    alien.y_move()
       
        # determines if the aliens for player2 will shoot and to move down if 
        # any alien in the horde hits a wall        
        for aliens2 in wall2:
            shoot=random.randint(1,6000)
            if shoot==11:
                alien_shoot_sound.play()
                bullets.append(spaceSprites.Bullet(1,aliens2.rect.center,True))
                bullet_group=pygame.sprite.Group(bullets)
            
            if aliens2.get_pos()[0]>=1230 or aliens2.get_pos()[0]<=0:
                for alien2 in wall2:
                    alien2.y_move()
        
        # moves the aliens left or right every 1/2 a second
        if alien_pulse%30==0:
            for alien in wall:
                alien.x_move()
                alien.change_stance()
            
            for alien2 in wall2:
                alien2.x_move()
                alien2.change_stance()
        
        
                
        #checks to see if any aliens on player1's side is hit and creates
        #an explosion animation if any aliens are hit
        aliens_hit=pygame.sprite.groupcollide(alien_group,bullet_group, False, False)
        bullets_hit=pygame.sprite.groupcollide(bullet_group,alien_group, False, False)
        
        if aliens_hit:

            for bullet in bullets_hit:
                bullet.kill()
                bullets.remove(bullet)
           
            for aliens in aliens_hit:
                invader_killed_sound.play()
                aliens.kill()
                wall.remove(aliens)
                explosion=spaceSprites.Explosion(aliens.rect.center,game_timer,aliens.get_colour(),1)
                explosions.append(explosion)
                
        #checks to see if any aliens on player2's side is hit and creates
        #an explosion animation if any aliens are hit       
        aliens_hit2=pygame.sprite.groupcollide(alien_group2,bullet_group2, False, False)
        bullets_hit2=pygame.sprite.groupcollide(bullet_group2,alien_group2, False, False)
        
        if aliens_hit2:
            for bullet in bullets_hit2:
                bullet.kill()
                player2_bullets.remove(bullet)
        
                                   
            for aliens in aliens_hit2:
                invader_killed_sound.play()
                aliens.kill()
                wall2.remove(aliens)
                explosion=spaceSprites.Explosion(aliens.rect.center,game_timer,aliens.get_colour(),2)
                explosions.append(explosion)                                
                
        
                        
                
        # checks if player 1's blockers are hit and kills the ones that are hit
        blocker_hit=pygame.sprite.groupcollide(blocker_group,bullet_group, False, False)
        bullets_hit=pygame.sprite.groupcollide(bullet_group,blocker_group, False, False)

        if blocker_hit:
            for bullet in bullets_hit:
                bullet.kill()
                bullets.remove(bullet)
            for blocker in blocker_hit:
                blocker.kill()
                blocker_wall.remove(blocker)
                
        blocker_hit2=pygame.sprite.groupcollide(blocker_group,bullet_group2, False, False)
        bullets_hit2=pygame.sprite.groupcollide(bullet_group2,blocker_group, False, False)        
        
        if blocker_hit2:
            for bullet in bullets_hit2:
                bullet.kill()
                player2_bullets.remove(bullet)
            
            for blocker in blocker_hit2:
                blocker.kill()
                blocker_wall.remove(blocker)            
                
        
        # checks if player 2's blockers are hit and kills the ones that are hit        
        p2_blocker_hit=pygame.sprite.groupcollide(blocker_group2,bullet_group2, False, False)
        p2_bullets_hit=pygame.sprite.groupcollide(bullet_group2,blocker_group2, False, False)        
        
        if p2_blocker_hit:
            for bullet in p2_bullets_hit:
                bullet.kill()
                player2_bullets.remove(bullet)
            for blocker in p2_blocker_hit:
                blocker.kill()
                blocker_wall2.remove(blocker)
                
        p2_blocker_hit2=pygame.sprite.groupcollide(blocker_group2,bullet_group, False, False)
        p2_bullets_hit2=pygame.sprite.groupcollide(bullet_group,blocker_group2, False, False)        
        
        if p2_blocker_hit2:
            for bullet in p2_bullets_hit2:
                bullet.kill()
                bullets.remove(bullet)
                            
            for blocker in p2_blocker_hit2:
                blocker.kill()
                blocker_wall2.remove(blocker)            
                
        #checks to see if player1 killed the neutral alien, if so an explosion
        #is created and a power up is dropped
        neutral_aliens_hit=pygame.sprite.groupcollide(neutral_alien_group,bullet_group, False, False)
        bullets_neutral=pygame.sprite.groupcollide(bullet_group,neutral_alien_group, False, False)
        if neutral_aliens_hit:
            neutral_death_noise.play()
            for bullet in bullets_neutral:
                bullet.kill()
                bullets.remove(bullet)
                bullet_group=pygame.sprite.Group(bullets)
            for neutral in neutral_aliens_hit:
                random_power=random.randrange(4)
                neutral.kill()
                neutral_alien.remove(neutral)
                neutral_alien_group=pygame.sprite.Group(neutral_alien)
                explosion=spaceSprites.Explosion(neutral.rect.center,game_timer,0,-2)
                explosions.append(explosion)
                power_up=spaceSprites.PowerUp(1,random_power,neutral.rect.center)
                power_ups.append(power_up)
                power_group=pygame.sprite.Group(power_ups)
        
        #checks to see if player1 killed the neutral alien, if so an explosion
        #is created and a power up is dropped        
        neutral_aliens_hit2=pygame.sprite.groupcollide(neutral_alien_group,bullet_group2, False, False)
        bullets_neutral2=pygame.sprite.groupcollide(bullet_group2,neutral_alien_group, False, False)
        if neutral_aliens_hit2:
            neutral_death_noise.play()
            for bullet in bullets_neutral2:
                bullet.kill()
                player2_bullets.remove(bullet)
                bullet_group2=pygame.sprite.Group(player2_bullets)
            
            for neutral in neutral_aliens_hit2:
                random_power=random.randrange(4)
                neutral.kill()
                neutral_alien.remove(neutral)
                neutral_alien_group=pygame.sprite.Group(neutral_alien)
                explosion=spaceSprites.Explosion(neutral.rect.center,game_timer,0,-2)
                explosions.append(explosion) 
                power_up=spaceSprites.PowerUp(2,random_power,neutral.rect.center)
                power_ups.append(power_up)
                power_group=pygame.sprite.Group(power_ups)
        
        #removes explosions when they are done
        for explosion in explosions:
            if explosion.get_life()==True:
                explosions.remove(explosion) 
        
        #removes unkilled neutral aliens        
        for neutrals in neutral_alien:
            if neutrals.get_x()>1400 or neutrals.get_x()<-200:
                neutral_alien.remove(neutrals)
                neutral_alien_group=pygame.sprite.Group(neutral_alien)

        allSprites = pygame.sprite.OrderedUpdates(end_zones,background,player1_health,player2_health, blocker_group,blocker_group2,bullet_group,bullet_group2,player1,player2, neutral_alien_group,alien_group,alien_group2,explosions,power_group)
                     
        # REFRESH SCREEN 

        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)       
        pygame.display.flip()
         
    #  unhide the mouse pointer
    pygame.mouse.set_visible(True)
    
    
def intro_screen(result):
    """This function defines the introduction screen of my program. it accepts
    a result from the game as a parameter and chooses the appropriate background
    image"""
    # DISPLAY
    screen = pygame.display.set_mode((1280, 980))
    pygame.display.set_caption("Space Wars!")
    pygame.display.flip()
         
    # ENTITIES
    #creates a list of images
    background_list=[]
    for image in range(5):
        background_list.append(pygame.image.load("Images/background"+str(image+2)+".jpg"))
    background=background_list[result-1]
    screen.blit(background,(0,0))
    pygame.display.flip()
    allSprites = pygame.sprite.OrderedUpdates()
     
    # ASSIGN 
    game_start=False
    
    #Loop
    while not game_start:
        # EVENT HANDLING
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return game_start

            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_u:
                    game_start=True
                    return game_start
                
                elif event.key==pygame.K_i:
                    background=background_list[4]
                    screen.blit(background,(0,0))
                    pygame.display.flip()                      
        
        # REFRESH SCREEN 
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)       


def main():
    """This function defines the mainline logic of my space game program"""
    go=True
    while go: 
        if intro_screen(go):
            go = game()
            
        else:
            go = False
    pygame.quit()
    

# Call the main function
main()