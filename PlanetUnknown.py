# -*- coding: utf-8 -*-
"""
Created on Tue May 17 13:33:57 2022

@author: LENOVO
"""

import pygame
import sys
import time
import random
pygame.init()

win = pygame.display.set_mode((1280,720))
pygame.display.set_caption("First Game")

walkRight = [pygame.image.load('sprites/right1.png'), 
             pygame.image.load('sprites/right2.png'), 
             pygame.image.load('sprites/right3.png'), 
             pygame.image.load('sprites/right4.png'), 
             pygame.image.load('sprites/right1.png'), 
             pygame.image.load('sprites/right2.png'), 
             pygame.image.load('sprites/right3.png'),
             pygame.image.load('sprites/right4.png'), 
             pygame.image.load('sprites/right3.png')]
walkLeft = [pygame.image.load('sprites/left1.png'), 
            pygame.image.load('sprites/left2.png'), 
            pygame.image.load('sprites/left3.png'), 
            pygame.image.load('sprites/left4.png'), 
            pygame.image.load('sprites/left1.png'), 
            pygame.image.load('sprites/left2.png'), 
            pygame.image.load('sprites/left3.png'), 
            pygame.image.load('sprites/left4.png'), 
            pygame.image.load('sprites/left3.png')]
bg = pygame.image.load('sprites/BackgroundV2.0.png')
char = pygame.image.load('sprites/standing.png')

clock = pygame.time.Clock()

bulletsound=pygame.mixer.Sound('sounds/Kido.wav')
hitsound=pygame.mixer.Sound('sounds/Hit.wav')
gameovermusic=pygame.mixer.Sound('sounds/GameOver.wav')

cynmusic=pygame.mixer.music.load('sounds/cynmusic.mp3')

pygame.mixer.music.play(-1)

score = 0

invaderImage = []
invader_X = []
invader_Xchange = []
no_of_invaders = 8

class player(object):
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.jumpCount =10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True
        self.hitbox = (self.x+20, self.y, 28,70)
        self.health=10
        self.visible=True
        
    def draw(self,win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0
        
        if not(self.standing):
            if self.left:  
                win.blit(walkLeft[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1                          
            elif self.right:
                win.blit(walkRight[cyn.walkCount//3], (self.x,self.y))
                self.walkCount += 1
        else:
            if self.right:
                win.blit(walkRight[0],(self.x,self.y))
            else:
                win.blit(walkLeft[0],(self.x,self.y))
            
        pygame.draw.rect(win,(255,0,0),(self.hitbox[0]-20,self.hitbox[1]-20,52,10))
        pygame.draw.rect(win,(0,255,0),(self.hitbox[0]-20,self.hitbox[1]-20,50 + 2-(5*(10-self.health)),10))
        self.hitbox = (self.x+20, self.y+10, 35,60)
  #     pygame.draw.rect(win, (0,255,0),self.hitbox,2)
    
    def hit(self):
        self.x=0
        self.y=650
        self.walkCount=0
        self.isJump=False
        self.jumpCount=10
        
        font1=pygame.font.SysFont('comicsans',30)
        text=font1.render('-5',1,(100,0,0))
        win.blit(text,(1100,50))
        pygame.display.update()
        
        i=0
        while i<100:
            pygame.time.delay(5)
            i+=1
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    i=301
                    pygame.quit()  
                
        if self.health>0:
            self.health-=1
        else:
            self.visible=False
            self.hitbox=(0,0,0,0)
            
        if self.visible:
            pass
        else:
            font1=pygame.font.SysFont('comicsans',100)
            text=font1.render('Game Over',1,(255,0,0))
            win.blit(text,(1280/2 - (text.get_width()/2),200))
            pygame.display.update()
            gameovermusic.play()
            time.sleep(7)
            pygame.quit()
            


class projectile(object):
    def __init__(self,x,y,radius,color,facing):
        self.x=x
        self.y=y
        self.radius=radius
        self.color=color
        self.facing=facing
        self.vel=20*facing
    
    def draw(self,win):
        pygame.draw.circle(win,self.color,(self.x,self.y),self.radius)
        
class enemy1(object):
    walkRight =  [pygame.image.load('sprites/ar1.png'), 
                 pygame.image.load('sprites/ar2.png'), 
                 pygame.image.load('sprites/ar3.png'), 
                 pygame.image.load('sprites/ar4.png'), 
                 pygame.image.load('sprites/ar1.png'), 
                 pygame.image.load('sprites/ar2.png'), 
                 pygame.image.load('sprites/ar3.png'), 
                 pygame.image.load('sprites/ar4.png'), 
                 pygame.image.load('sprites/ar1.png'), 
                 pygame.image.load('sprites/ar2.png'), 
                 pygame.image.load('sprites/ar3.png')]
    walkLeft = [pygame.image.load('sprites/al1.png'), 
                pygame.image.load('sprites/al2.png'), 
                pygame.image.load('sprites/al3.png'), 
                pygame.image.load('sprites/al4.png'), 
                pygame.image.load('sprites/al1.png'), 
                pygame.image.load('sprites/al2.png'), 
                pygame.image.load('sprites/al3.png'), 
                pygame.image.load('sprites/al4.png'), 
                pygame.image.load('sprites/al1.png'), 
                pygame.image.load('sprites/al2.png'), 
                pygame.image.load('sprites/al3.png')]
    
    def __init__(self,x,y,width,height,end):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.end=end
        self.walkCount=0
        self.vel=3
        self.path=[self.x,self.end]
        self.hitbox = (self.x+20, self.y+25, 28,35)
        self.health=10
        self.visible= True
             
    def draw(self,win):
        self.move()
        if self.visible:
            if self.walkCount +1>=33:
                self.walkCount=0
                
            if self.vel>0:
                win.blit(self.walkRight[self.walkCount//3],(self.x,self.y))
                self.walkCount+=1
            else:
                win.blit(self.walkLeft[self.walkCount//3],(self.x,self.y))
                self.walkCount+=1
                
            pygame.draw.rect(win,(255,0,0),(self.hitbox[0],self.hitbox[1]-20,52,10))
            pygame.draw.rect(win,(0,100,0),(self.hitbox[0],self.hitbox[1]-20,50 + 2-(5*(10-self.health)),10))
            self.hitbox = (self.x+20, self.y+25, 28,35)
     #      pygame.draw.rect(win,(255,0,0),self.hitbox,2)
    
    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x+=self.vel
            else:
                self.vel=self.vel*-1
                self.walkCount=0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel=self.vel*-1
                self.walkCount=0
                
    def hit(self):
        if self.health>0:
            self.health-=5
        else:
            self.visible=False
            self.hitbox=(0,0,0,0)
        print('hit')

class enemy2(object):
    walkRight =  [pygame.image.load('sprites/mr1.png'), 
                 pygame.image.load('sprites/mr2.png'), 
                 pygame.image.load('sprites/mr3.png'), 
                 pygame.image.load('sprites/mr4.png'), 
                 pygame.image.load('sprites/mr1.png'), 
                 pygame.image.load('sprites/mr2.png'), 
                 pygame.image.load('sprites/mr3.png'), 
                 pygame.image.load('sprites/mr4.png'), 
                 pygame.image.load('sprites/mr1.png'), 
                 pygame.image.load('sprites/mr2.png'), 
                 pygame.image.load('sprites/mr3.png')]
    walkLeft = [pygame.image.load('sprites/ml1.png'), 
                pygame.image.load('sprites/ml2.png'), 
                pygame.image.load('sprites/ml3.png'), 
                pygame.image.load('sprites/ml4.png'), 
                pygame.image.load('sprites/ml1.png'), 
                pygame.image.load('sprites/ml2.png'), 
                pygame.image.load('sprites/ml3.png'), 
                pygame.image.load('sprites/ml4.png'), 
                pygame.image.load('sprites/ml1.png'), 
                pygame.image.load('sprites/ml2.png'), 
                pygame.image.load('sprites/ml3.png')]
    
    def __init__(self,x,y,width,height,end):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.end=end
        self.walkCount=0
        self.vel=8
        self.path=[self.x,self.end]
        self.hitbox = (self.x+20, self.y+10, 28,50)
        self.health=10
        self.visible= True
             
    def draw(self,win):
        self.move()
        if self.visible:
            if self.walkCount +1>=33:
                self.walkCount=0
                
            if self.vel>0:
                win.blit(self.walkRight[self.walkCount//3],(self.x,self.y))
                self.walkCount+=1
            else:
                win.blit(self.walkLeft[self.walkCount//3],(self.x,self.y))
                self.walkCount+=1
                
            pygame.draw.rect(win,(255,0,0),(self.hitbox[0],self.hitbox[1]-20,52,10))
            pygame.draw.rect(win,(0,100,0),(self.hitbox[0],self.hitbox[1]-20,50 + 2-(5*(10-self.health)),10))
            self.hitbox = (self.x+20, self.y+10, 28,50)
            #pygame.draw.rect(win,(255,0,0),self.hitbox,2)
    
    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x+=self.vel
            else:
                self.vel=self.vel*-1
                self.walkCount=0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel=self.vel*-1
                self.walkCount=0
                
    def hit(self):
        if self.health>0:
            self.health-=2
        else:
            self.visible=False
            self.hitbox=(0,0,0,0)
        print('hit')

class boss1(object):
    walkRight =  [pygame.image.load('sprites/bnr1.png'), 
                 pygame.image.load('sprites/bnr2.png'), 
                 pygame.image.load('sprites/bnr1.png'), 
                 pygame.image.load('sprites/bnr2.png'), 
                 pygame.image.load('sprites/bnr1.png'), 
                 pygame.image.load('sprites/bnr2.png'), 
                 pygame.image.load('sprites/bnr1.png'), 
                 pygame.image.load('sprites/bnr2.png'), 
                 pygame.image.load('sprites/bnr1.png'), 
                 pygame.image.load('sprites/bnr2.png'), 
                 pygame.image.load('sprites/bnr1.png')]
    walkLeft = [pygame.image.load('sprites/bnl1.png'), 
                pygame.image.load('sprites/bnl2.png'), 
                pygame.image.load('sprites/bnl1.png'), 
                pygame.image.load('sprites/bnl2.png'), 
                pygame.image.load('sprites/bnl1.png'), 
                pygame.image.load('sprites/bnl2.png'), 
                pygame.image.load('sprites/bnl1.png'), 
                pygame.image.load('sprites/bnl2.png'), 
                pygame.image.load('sprites/bnl1.png'), 
                pygame.image.load('sprites/bnl2.png'), 
                pygame.image.load('sprites/bnl1.png')]
    
    def __init__(self,x,y,width,height,end):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.end=end
        self.walkCount=0
        self.vel=24
        self.path=[self.x,self.end]
        self.hitbox = (self.x+20, self.y+10, 28,50)
        self.health=10
        self.visible= True
             
    def draw(self,win):
        self.move()
        if self.visible:
            if self.walkCount +1>=33:
                self.walkCount=0
                
            if self.vel>0:
                win.blit(self.walkRight[self.walkCount//3],(self.x,self.y))
                self.walkCount+=1
            else:
                win.blit(self.walkLeft[self.walkCount//3],(self.x,self.y))
                self.walkCount+=1
                
            pygame.draw.rect(win,(255,0,0),(self.hitbox[0],self.hitbox[1]-20,52,10))
            pygame.draw.rect(win,(0,100,0),(self.hitbox[0],self.hitbox[1]-20,50 + 2-(5*(10-self.health)),10))
            self.hitbox = (self.x+20, self.y+10, 28,50)
            #pygame.draw.rect(win,(255,0,0),self.hitbox,2)
    
    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x+=self.vel
            else:
                self.vel=self.vel*-1
                self.walkCount=0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel=self.vel*-1
                self.walkCount=0
                
    def hit(self):
        if self.health>0:
            self.health-=2
        else:
            self.visible=False
            self.hitbox=(0,0,0,0)
        print('hit')
        
class boss2(object):
    walkRight =  [pygame.image.load('sprites/bar1.png'), 
                 pygame.image.load('sprites/bar2.png'), 
                 pygame.image.load('sprites/bar1.png'), 
                 pygame.image.load('sprites/bar2.png'), 
                 pygame.image.load('sprites/bar1.png'), 
                 pygame.image.load('sprites/bar2.png'), 
                 pygame.image.load('sprites/bar1.png'), 
                 pygame.image.load('sprites/bar2.png'), 
                 pygame.image.load('sprites/bar1.png'), 
                 pygame.image.load('sprites/bar2.png'), 
                 pygame.image.load('sprites/bar1.png')]
    walkLeft = [pygame.image.load('sprites/bal1.png'), 
                pygame.image.load('sprites/bal2.png'), 
                pygame.image.load('sprites/bal1.png'), 
                pygame.image.load('sprites/bal2.png'), 
                pygame.image.load('sprites/bal1.png'), 
                pygame.image.load('sprites/bal2.png'), 
                pygame.image.load('sprites/bal1.png'), 
                pygame.image.load('sprites/bal2.png'), 
                pygame.image.load('sprites/bal1.png'), 
                pygame.image.load('sprites/bal2.png'), 
                pygame.image.load('sprites/bal1.png')]
    
    def __init__(self,x,y,width,height,end):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.end=end
        self.walkCount=0
        self.vel=30
        self.path=[self.x,self.end]
        self.hitbox = (self.x+20, self.y+10, 28,50)
        self.health=10
        self.visible= True
             
    def draw(self,win):
        self.move()
        if self.visible:
            if self.walkCount +1>=33:
                self.walkCount=0
                
            if self.vel>0:
                win.blit(self.walkRight[self.walkCount//3],(self.x,self.y))
                self.walkCount+=1
            else:
                win.blit(self.walkLeft[self.walkCount//3],(self.x,self.y))
                self.walkCount+=1
                
            pygame.draw.rect(win,(255,0,0),(self.hitbox[0],self.hitbox[1]-20,52,10))
            pygame.draw.rect(win,(0,100,0),(self.hitbox[0],self.hitbox[1]-20,50 + 2-(5*(10-self.health)),10))
            self.hitbox = (self.x+20, self.y+10, 28,50)
            #pygame.draw.rect(win,(255,0,0),self.hitbox,2)
    
    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x+=self.vel
            else:
                self.vel=self.vel*-1
                self.walkCount=0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel=self.vel*-1
                self.walkCount=0
                
    def hit(self):
        if self.health>0:
            self.health-=2
        else:
            self.visible=False
            self.hitbox=(0,0,0,0)
        print('hit')
        
class boss3(object):
    walkRight =  [pygame.image.load('sprites/bdr1.png'), 
                 pygame.image.load('sprites/bdr2.png'), 
                 pygame.image.load('sprites/bdr1.png'), 
                 pygame.image.load('sprites/bdr2.png'), 
                 pygame.image.load('sprites/bdr1.png'), 
                 pygame.image.load('sprites/bdr2.png'), 
                 pygame.image.load('sprites/bdr1.png'), 
                 pygame.image.load('sprites/bdr2.png'), 
                 pygame.image.load('sprites/bdr1.png'), 
                 pygame.image.load('sprites/bdr2.png'), 
                 pygame.image.load('sprites/bdr1.png')]
    walkLeft = [pygame.image.load('sprites/bdl1.png'), 
                pygame.image.load('sprites/bdl2.png'), 
                pygame.image.load('sprites/bdl1.png'), 
                pygame.image.load('sprites/bdl2.png'), 
                pygame.image.load('sprites/bdl1.png'), 
                pygame.image.load('sprites/bdl2.png'), 
                pygame.image.load('sprites/bdl1.png'), 
                pygame.image.load('sprites/bdl2.png'), 
                pygame.image.load('sprites/bdl1.png'), 
                pygame.image.load('sprites/bdl2.png'), 
                pygame.image.load('sprites/bdl1.png')]
    
    def __init__(self,x,y,width,height,end):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.end=end
        self.walkCount=0
        self.vel=20
        self.path=[self.x,self.end]
        self.hitbox = (self.x+20, self.y+10, 28,50)
        self.health=10
        self.visible= True
             
    def draw(self,win):
        self.move()
        if self.visible:
            if self.walkCount +1>=33:
                self.walkCount=0
                
            if self.vel>0:
                win.blit(self.walkRight[self.walkCount//3],(self.x,self.y))
                self.walkCount+=1
            else:
                win.blit(self.walkLeft[self.walkCount//3],(self.x,self.y))
                self.walkCount+=1
                
            pygame.draw.rect(win,(255,0,0),(self.hitbox[0],self.hitbox[1]-20,52,10))
            pygame.draw.rect(win,(0,100,0),(self.hitbox[0],self.hitbox[1]-20,50 + 2-(5*(10-self.health)),10))
            self.hitbox = (self.x+20, self.y+10, 28,50)
            #pygame.draw.rect(win,(255,0,0),self.hitbox,2)
    
    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x+=self.vel
            else:
                self.vel=self.vel*-1
                self.walkCount=0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel=self.vel*-1
                self.walkCount=0
                
    def hit(self):
        if self.health>0:
            self.health-=1
        else:
            self.visible=False
            self.hitbox=(0,0,0,0)
        print('hit')
        
class boss4(object):
    walkRight =  [pygame.image.load('sprites/bsr1.png'), 
                 pygame.image.load('sprites/bsr2.png'), 
                 pygame.image.load('sprites/bsr1.png'), 
                 pygame.image.load('sprites/bsr2.png'), 
                 pygame.image.load('sprites/bsr1.png'), 
                 pygame.image.load('sprites/bsr2.png'), 
                 pygame.image.load('sprites/bsr1.png'), 
                 pygame.image.load('sprites/bsr2.png'), 
                 pygame.image.load('sprites/bsr1.png'), 
                 pygame.image.load('sprites/bsr2.png'), 
                 pygame.image.load('sprites/bsr1.png')]
    walkLeft = [pygame.image.load('sprites/bsl1.png'), 
                pygame.image.load('sprites/bsl2.png'), 
                pygame.image.load('sprites/bsl1.png'), 
                pygame.image.load('sprites/bsl2.png'), 
                pygame.image.load('sprites/bsl1.png'), 
                pygame.image.load('sprites/bsl2.png'), 
                pygame.image.load('sprites/bsl1.png'), 
                pygame.image.load('sprites/bsl2.png'), 
                pygame.image.load('sprites/bsl1.png'), 
                pygame.image.load('sprites/bsl2.png'), 
                pygame.image.load('sprites/bsl1.png')]
    
    def __init__(self,x,y,width,height,end):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.end=end
        self.walkCount=0
        self.vel=40
        self.path=[self.x,self.end]
        self.hitbox = (self.x+20, self.y+10, 28,50)
        self.health=10
        self.visible= True
             
    def draw(self,win):
        self.move()
        if self.visible:
            if self.walkCount +1>=33:
                self.walkCount=0
                
            if self.vel>0:
                win.blit(self.walkRight[self.walkCount//3],(self.x,self.y))
                self.walkCount+=1
            else:
                win.blit(self.walkLeft[self.walkCount//3],(self.x,self.y))
                self.walkCount+=1
                
            pygame.draw.rect(win,(255,0,0),(self.hitbox[0],self.hitbox[1]-20,52,10))
            pygame.draw.rect(win,(0,100,0),(self.hitbox[0],self.hitbox[1]-20,50 + 2-(5*(10-self.health)),10))
            self.hitbox = (self.x+20, self.y+10, 28,50)
            #pygame.draw.rect(win,(255,0,0),self.hitbox,2)
    
    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x+=self.vel
            else:
                self.vel=self.vel*-1
                self.walkCount=0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel=self.vel*-1
                self.walkCount=0
                
    def hit(self):
        if self.health>0:
            self.health-=2
        else:
            self.visible=False
            self.hitbox=(0,0,0,0)
        print('hit')

def redrawGameWindow(z,y,q):
    win.blit(bg, (0,0))
    text=font.render('Score: '+str(score),1,(255,255,255))
    win.blit(text,(1000,10))
    cyn.draw(win)
    alien[0].draw(win)
    if alien[0].visible:
        pass
    else:
        alien[1].draw(win)
        if alien[1].visible:
            pass
        else:
            alien[2].draw(win)
            alien[3].draw(win)
            alien[4].draw(win)
            alien[5].draw(win)
            alien[6].draw(win)
            alien[7].draw(win)
            alien[8].draw(win)
            alien[9].draw(win)
            alien[10].draw(win)
            alien[11].draw(win)
            alien[12].draw(win)
            
            if alien[z].visible:
                pass
            else:
                alien[13].draw(win)
                alien[14].draw(win)
                alien[15].draw(win)
                alien[16].draw(win)
                alien[17].draw(win)
                alien[18].draw(win)
                alien[19].draw(win)
                alien[20].draw(win)
                alien[21].draw(win)
                alien[22].draw(win)
                alien[23].draw(win)
                alien[24].draw(win)
                alien[25].draw(win)
                if alien[y].visible:
                    pass
                else:
                    alien[0].draw(win)
                    alien[1].draw(win)
                    alien[2].draw(win)
                    alien[3].draw(win)
                    alien[4].draw(win)
                    alien[5].draw(win)
                    alien[6].draw(win)
                    alien[7].draw(win)
                    alien[8].draw(win)
                    alien[9].draw(win)
                    alien[10].draw(win)
                    alien[11].draw(win)
                    alien[12].draw(win)
                    if alien[q].visible:
                        pass
                    else:
                        alien[13].draw(win)
                        alien[14].draw(win)
                        alien[15].draw(win)
                        alien[16].draw(win)
                        alien[17].draw(win)
                        alien[18].draw(win)
                        alien[19].draw(win)
                        alien[20].draw(win)
                        alien[21].draw(win)
                        alien[22].draw(win)
                        alien[23].draw(win)
                        alien[24].draw(win)
                        alien[25].draw(win)
                        
                        if alien[0].visible or alien[1].visible or alien[2].visible or alien[3].visible or alien[4].visible or alien[5].visible or alien[6].visible or alien[7].visible or alien[8].visible or alien[9].visible or alien[10].visible or alien[11].visible or alien[12].visible or alien[13].visible or alien[14].visible or alien[15].visible or alien[16].visible or alien[17].visible or alien[18].visible or alien[19].visible or alien[20].visible or alien[21].visible or alien[22].visible or alien[23].visible or alien[24].visible or alien[25].visible:
                            pass
                        else:
                            alien[26].draw(win)
                            alien[27].draw(win)
                            alien[28].draw(win)
                            alien[29].draw(win)
                            
                            if alien[26].visible or alien[27].visible or alien[28].visible or alien[29].visible:
                                pass
                            else:
                                text2=font.render('You win',1,(255,255,255))
                                win.blit(text2,(500,300))
                                
                
    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update() 
    
#main
cyn= player(0, 650, 68,72)   #x,y,width,height
s=[]
e=[]
c=0
for i in range(30):
    a=random.randint(40,1080)
    s.append(a)
    b=random.randint(a+10,1280)
    e.append(b)
    
alien=[enemy1(s[0],650,64,64,e[0]),
       enemy2(s[1] ,500,64,64,e[1]),
       enemy1(s[2],650,64,64,e[2]),
       enemy2(s[3] ,500,64,64,e[3]),
       enemy1(s[4],650,64,64,e[4]),
       enemy2(0 ,500,64,64,e[5]),
       enemy1(s[6],650,64,64,e[6]),
       enemy2(s[7] ,500,64,64,e[7]),
       enemy1(s[8],650,64,64,e[8]),
       enemy2(s[9] ,500,64,64,e[9]),
       enemy1(s[10],650,64,64,e[10]),
       enemy2(s[11] ,500,64,64,e[11]),
       enemy1(s[12],650,64,64,e[12]),
       enemy1(25,650,64,64,e[13]),
       enemy2(s[14] ,500,64,64,e[14]),
       enemy1(s[15],650,64,64,e[15]),
       enemy2(s[16] ,500,64,64,e[16]),
       enemy1(s[17],650,64,64,e[17]),
       enemy2(25 ,500,64,64,e[18]),
       enemy1(s[19],650,64,64,e[19]),
       enemy2(s[20] ,500,64,64,e[20]),
       enemy1(s[21],650,64,64,e[21]),
       enemy2(s[22] ,500,64,64,e[22]),
       enemy1(s[23],650,64,64,e[23]),
       enemy2(s[24] ,500,64,64,e[24]),
       enemy1(s[25],650,64,64,e[25]),
       boss1(0,575,64,64,1280),
       boss2(0,600,64,64,1280),
       boss3(0,625,64,64,1280),
       boss4(0,650,64,64,1280)
       ]

bullets=[]
run = True
shootLoop = 0
font=pygame.font.SysFont('comicsans',30, True, True)        #font,size,bold,italic
z=random.randint(2,13)
y=random.randint(13,26)
q=random.randint(0,13)

while run:
    clock.tick(27)
    if cyn.hitbox[1] < alien[0].hitbox[1] + alien[0].hitbox[3] and cyn.hitbox[1] + cyn.hitbox[3] > alien[0].hitbox[1]:
        if cyn.hitbox[0] + cyn.hitbox[2] > alien[0].hitbox[0] and cyn.hitbox[0] < alien[0].hitbox[0] + alien[0].hitbox[2]:
                cyn.hit() 
                score-=5
                
    for bullet in bullets:
        if bullet.y - bullet.radius < alien[0].hitbox[1] + alien[0].hitbox[3] and bullet.y - bullet.radius > alien[0].hitbox[1]:
            if bullet.x + bullet.radius > alien[0].hitbox[0] and bullet.x - bullet.radius < alien[0].hitbox[0] + alien[0].hitbox[2]:
                alien[0].hit() 
                hitsound.play()
                score+=1
                bullets.pop(bullets.index(bullet))
                 
         
        if bullet.x<1280 and bullet.x>0:
            bullet.x += bullet.vel
        else:
             bullets.pop(bullets.index(bullet))
    if alien[0].visible:
        pass
    else:        
        if cyn.hitbox[1] < alien[1].hitbox[1] + alien[1].hitbox[3] and cyn.hitbox[1] + cyn.hitbox[3] > alien[1].hitbox[1]:
            if cyn.hitbox[0] + cyn.hitbox[2] > alien[1].hitbox[0] and cyn.hitbox[0] < alien[1].hitbox[0] + alien[1].hitbox[2]:
                    cyn.hit() 
                    score-=5
         
        for bullet in bullets:
            if bullet.y - bullet.radius < alien[1].hitbox[1] + alien[1].hitbox[3] and bullet.y - bullet.radius > alien[1].hitbox[1]:
                if bullet.x + bullet.radius > alien[1].hitbox[0] and bullet.x - bullet.radius < alien[1].hitbox[0] + alien[1].hitbox[2]:
                    alien[1].hit() 
                    hitsound.play()
                    score+=1
                    bullets.pop(bullets.index(bullet))
                    
            
            if bullet.x<1280 and bullet.x>0:
                bullet.x += bullet.vel
            else:
                bullets.pop(bullets.index(bullet))  
      
        if alien[1].visible:
            pass
        else:
            for i in range(2,13):
                if cyn.hitbox[1] < alien[i].hitbox[1] + alien[i].hitbox[3] and cyn.hitbox[1] + cyn.hitbox[3] > alien[i].hitbox[1]:
                    if cyn.hitbox[0] + cyn.hitbox[2] > alien[i].hitbox[0] and cyn.hitbox[0] < alien[i].hitbox[0] + alien[i].hitbox[2]:
                            cyn.hit() 
                            score-=5
                for bullet in bullets:
                    if bullet.y - bullet.radius < alien[i].hitbox[1] + alien[i].hitbox[3] and bullet.y - bullet.radius > alien[i].hitbox[1]:
                        if bullet.x + bullet.radius > alien[i].hitbox[0] and bullet.x - bullet.radius < alien[i].hitbox[0] + alien[i].hitbox[2]:
                            alien[i].hit() 
                            hitsound.play()
                            score+=1
                            bullets.pop(bullets.index(bullet))
                
            if alien[z].visible:
                pass
            else:
                for j in range(13,26):
                    if cyn.hitbox[1] < alien[j].hitbox[1] + alien[j].hitbox[3] and cyn.hitbox[1] + cyn.hitbox[3] > alien[j].hitbox[1]:
                        if cyn.hitbox[0] + cyn.hitbox[2] > alien[j].hitbox[0] and cyn.hitbox[0] < alien[j].hitbox[0] + alien[j].hitbox[2]:
                            cyn.hit() 
                            score-=5
                    for bullet in bullets:
                        if bullet.y - bullet.radius < alien[j].hitbox[1] + alien[j].hitbox[3] and bullet.y - bullet.radius > alien[j].hitbox[1]:
                            if bullet.x + bullet.radius > alien[j].hitbox[0] and bullet.x - bullet.radius < alien[j].hitbox[0] + alien[j].hitbox[2]:
                                alien[j].hit() 
                                hitsound.play()
                                score+=1
                                bullets.pop(bullets.index(bullet))
                                
                if alien[y].visible:
                    pass
                else:
                    for k in range(0,13):
                        if cyn.hitbox[1] < alien[k].hitbox[1] + alien[k].hitbox[3] and cyn.hitbox[1] + cyn.hitbox[3] > alien[k].hitbox[1]:
                            if cyn.hitbox[0] + cyn.hitbox[2] > alien[k].hitbox[0] and cyn.hitbox[0] < alien[k].hitbox[0] + alien[k].hitbox[2]:
                                cyn.hit() 
                                score-=5
                        for bullet in bullets:
                            if bullet.y - bullet.radius < alien[k].hitbox[1] + alien[k].hitbox[3] and bullet.y - bullet.radius > alien[k].hitbox[1]:
                                if bullet.x + bullet.radius > alien[k].hitbox[0] and bullet.x - bullet.radius < alien[k].hitbox[0] + alien[k].hitbox[2]:
                                    alien[k].hit() 
                                    hitsound.play()
                                    score+=1
                                    bullets.pop(bullets.index(bullet))
                                    
                    if alien[q].visible:
                        pass
                    else:
                        for l in range(13,26):
                            if cyn.hitbox[1] < alien[l].hitbox[1] + alien[l].hitbox[3] and cyn.hitbox[1] + cyn.hitbox[3] > alien[l].hitbox[1]:
                                if cyn.hitbox[0] + cyn.hitbox[2] > alien[l].hitbox[0] and cyn.hitbox[0] < alien[l].hitbox[0] + alien[l].hitbox[2]:
                                    cyn.hit() 
                                    score-=5
                            for bullet in bullets:
                                if bullet.y - bullet.radius < alien[l].hitbox[1] + alien[l].hitbox[3] and bullet.y - bullet.radius > alien[l].hitbox[1]:
                                    if bullet.x + bullet.radius > alien[l].hitbox[0] and bullet.x - bullet.radius < alien[l].hitbox[0] + alien[l].hitbox[2]:
                                        alien[l].hit() 
                                        hitsound.play()
                                        score+=1
                                        bullets.pop(bullets.index(bullet))
                                        
                        if alien[0].visible or alien[1].visible or alien[2].visible or alien[3].visible or alien[4].visible or alien[5].visible or alien[6].visible or alien[7].visible or alien[8].visible or alien[9].visible or alien[10].visible or alien[11].visible or alien[12].visible or alien[13].visible or alien[14].visible or alien[15].visible or alien[16].visible or alien[17].visible or alien[18].visible or alien[19].visible or alien[20].visible or alien[21].visible or alien[22].visible or alien[23].visible or alien[24].visible or alien[25].visible:
                            pass
                        else:
                            for m in range(26,30):
                                if cyn.hitbox[1] < alien[m].hitbox[1] + alien[m].hitbox[3] and cyn.hitbox[1] + cyn.hitbox[3] > alien[m].hitbox[1]:
                                    if cyn.hitbox[0] + cyn.hitbox[2] > alien[m].hitbox[0] and cyn.hitbox[0] < alien[m].hitbox[0] + alien[m].hitbox[2]:
                                        cyn.hit() 
                                        score-=5
                                for bullet in bullets:
                                    if bullet.y - bullet.radius < alien[m].hitbox[1] + alien[m].hitbox[3] and bullet.y - bullet.radius > alien[m].hitbox[1]:
                                        if bullet.x + bullet.radius > alien[m].hitbox[0] and bullet.x - bullet.radius < alien[m].hitbox[0] + alien[m].hitbox[2]:
                                            alien[m].hit() 
                                            hitsound.play()
                                            score+=1
                                            bullets.pop(bullets.index(bullet))
                        
                   
    
    if shootLoop>0:
        shootLoop+=1
    if shootLoop>3:
        shootLoop=0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_ESCAPE]:
        pygame.quit()
        
    elif keys[pygame.K_SPACE] and shootLoop==0:
        
        if cyn.left:
            facing=-1
        else:
            facing=1
        if len(bullets)<5:
            bullets.append(projectile(round(cyn.x+cyn.width//2), round(cyn.y + cyn.height//2),6,(0,0,0),facing))
            bulletsound.play()
        shootLoop=1
    
    elif keys[pygame.K_RSHIFT]:
        while(cyn.isJump):
            break
        else:
            cyn.vel=10
    
    elif keys[pygame.K_LSHIFT]:
        while(cyn.isJump):
            break
        else:
            cyn.vel=5
        
    elif keys[pygame.K_LEFT] and cyn.x > cyn.vel: 
        cyn.x -= cyn.vel
        cyn.left = True
        cyn.right = False
        cyn.standing = False

    elif keys[pygame.K_RIGHT] and cyn.x < 1280 - cyn.vel - cyn.width:  
        cyn.x += cyn.vel
        cyn.left = False
        cyn.right = True
        cyn.standing = False
        
    else: 
        cyn.standing = True
        cyn.walkCount = 0
        
    if not(cyn.isJump):
        if keys[pygame.K_UP]:
            cyn.isJump = True
            cyn.walkCount = 0
    else:
        if cyn.jumpCount >= -10:
            neg=1
            
            if cyn.jumpCount<0:
                neg=-1
            cyn.y-=(cyn.jumpCount**2)*0.5*neg
            cyn.jumpCount-=1
            
        else:
            cyn.isJump=False
            cyn.jumpCount=10
            
            
    redrawGameWindow(z,y,q) 
    
    
pygame.quit()
sys.exit()