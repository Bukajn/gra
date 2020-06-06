import pygame,math
from pygame import mixer
import  asset



class Player(object):
    def __init__(self,main):
        self.main = main

        self.RightReka = pygame.image.load(asset.imgRekaRight)
        self.LeftReka = pygame.image.load(asset.imgRekaLeft)
        self.imgRight=pygame.image.load(asset.imgPlayerRight)
        self.imgLeft=pygame.image.load(asset.imgPlayerLeft)


        self.img = pygame.image.load(asset.imgPlayerRight)
        self.imgReka = self.RightReka
        self.jumpSound = mixer.Sound(asset.soundJump)
        self.szerokosc=64


        #self.img = pygame.transform.rotate(self.img,45)
        self.pos = pygame.Vector2(336,0)#336
        self.posReka = self.pos
        self.state = 1 # 0=na ziemie 1=podczas spadania 2=podczas skoku
        self.speed = pygame.Vector2(0,0)
        self.speedGravitation=0.1
        self.speedJump=-8
        self.wysSkoku=100
        self.old_pos_y=0
        self.ruch = "prawo"

        self.clock=pygame.time.Clock()
        self.delta=0.0
        self.max_tps=self.main.max_tps

        self.OdlegloscRekiOdRoguPrawo = pygame.Vector2(37,31)

        self.OdlegloscRekiOdRoguLewo = pygame.Vector2(-27, -30)

        self.Rotate=0
        self.ZmianaWielkosci(1.5)

        self.wczesniejszyKlik = pygame.mouse.get_pressed()
    def wys(self):
        #print(pygame.mouse.get_pos())
        for i in range(self.Zegar()):

            self.Physik()
            self.Ruch()



        self.Ruch()
    def Ruch(self):
        if self.ruch=="prawo":
            self.RuchwPrawo()
        elif self.ruch =="lewo":
            self.RuchWlewo()
    def RuchwPrawo(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.pos.x, mouse_y - self.pos.y
        self.Rotate = ((180 / math.pi) * math.atan2(rel_y, rel_x))-40
        self.PunktZaczepieniaRekiPrawo = pygame.Vector2(self.pos.x + (self.OdlegloscRekiOdRoguPrawo.x),self.pos.y + (self.OdlegloscRekiOdRoguPrawo.y))
        self.main.screen.blit(self.img, self.pos)
        rotate_reka, rect = self.ObrotPunktu(self.imgReka,self.Rotate,self.PunktZaczepieniaRekiPrawo,pygame.math.Vector2(-6,4))
        self.main.screen.blit(rotate_reka,rect)
        if pygame.mouse.get_pressed()[0]:
            self.Strzał()

    def RuchWlewo(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.pos.x, mouse_y - self.pos.y
        self.Rotate = ((180 / math.pi) * math.atan2(rel_y, rel_x))+220
        self.PunktZaczepieniaRekiLewo = pygame.Vector2(self.pos.x + (-self.OdlegloscRekiOdRoguLewo.x),self.pos.y + (-self.OdlegloscRekiOdRoguLewo.y))
        self.main.screen.blit(self.img, self.pos)
        rotate_reka, rect = self.ObrotPunktu(self.imgReka, self.Rotate, self.PunktZaczepieniaRekiLewo,pygame.math.Vector2(6, 4))
        self.main.screen.blit(rotate_reka, rect)
    def Strzał(self):
        pass
    def ObrotPunktu(self,image, promien, pivot, przesuniecie):

        rotate_img = pygame.transform.rotozoom(image, -promien, 1)  # Rotate the image.
        rotated_offset = przesuniecie.rotate(promien)  # Rotate the offset vector.

        rect = rotate_img.get_rect(center=pivot+rotated_offset)
        return rotate_img,rect
    def Physik(self):

        height=self.main.Teren.ColisionWithFloar() #przyjęcie wysokości podłożą
        heightSufit=self.main.Teren.CollisionWithUnderFloar()#przyjęcie wysokości sufitu

        self.grawitacja(height,heightSufit)

        self.keys = pygame.key.get_pressed()

        self.jump(heightSufit)

        self.pos.y+=self.speed.y
        self.grawitacja(height,heightSufit)
        self.jump(heightSufit)
        self.wczesniejszekeys=self.keys
    def grawitacja(self,height,heightSufit):
        if self.pos.y < heightSufit:
            self.speed.y = 1
            self.state = 1
        if self.pos.y < height and self.state!=2:
            self.state=1
            self.speed.y += self.speedGravitation
        elif self.pos.y != self.old_pos_y and self.state == 1: # jest na ziemi
            self.speed.y=0
            self.state=0

            #self.ZmianaTex("assets/playerRight.png")
        if self.pos.y > height:
            self.pos.y = height
    def jump(self,heightSufit):
        if self.keys[pygame.K_SPACE] and self.state == 0 and self.keys[pygame.K_SPACE]!= self.wczesniejszekeys[pygame.K_SPACE]:
            #self.ZmianaTex(self.imgSkok)
            self.jumpSound.play()
            self.state = 2
            self.speed.y = self.speedJump
            self.posStart = self.pos.y
        if self.state == 2:
            if self.pos.y+self.szerokosc > self.old_pos_y - self.wysSkoku:
                if self.speed.y < -5:

                    self.speed.y += -(self.speed.y / (self.wysSkoku - (self.posStart - self.pos.y)))
            else:
                self.state = 1
            if self.pos.y<heightSufit:
                self.speed.y=0
                self.state=1
        elif self.state == 0:
            self.old_pos_y = self.pos.y+self.szerokosc
    def ZmianaWielkosci(self, mnoznik):
        self.imgRight = pygame.transform.rotozoom(self.imgRight, 0, mnoznik)
        self.imgLeft = pygame.transform.rotozoom(self.imgLeft, 0, mnoznik)
        self.RightReka= pygame.transform.rotozoom(self.RightReka, 0, mnoznik)
        self.LeftReka=pygame.transform.rotozoom(self.LeftReka, 0, mnoznik)

        self.img =pygame.transform.rotozoom(self.img,0,mnoznik)
        self.imgReka = pygame.transform.rotozoom(self.imgReka, 0, mnoznik)

        self.OdlegloscRekiOdRoguPrawo.x*=mnoznik
        self.OdlegloscRekiOdRoguPrawo.y *= mnoznik
        self.OdlegloscRekiOdRoguLewo.x *= mnoznik
        self.OdlegloscRekiOdRoguLewo.y *= mnoznik
        self.szerokosc*=mnoznik
    def ZmianaWprawo(self):
        self.ruch = "prawo"
        self.img = self.imgRight
        self.imgReka = self.RightReka
    def ZmianaWLewo(self):
        self.ruch = "lewo"
        self.img = self.imgLeft
        self.imgReka=self.LeftReka
    def Zegar(self):
        self.delta+=self.clock.tick()/1000.0
        i=0
        while self.delta>1/self.max_tps:
            i+=1
            self.delta-=1/self.max_tps
        return i