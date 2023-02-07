import pygame
import os
import random
import sys
import time
from pygame import mixer
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')

pygame.font.init()
pygame.init()

pygame.display.set_caption("Window") #window name
keys = pygame.key.get_pressed()

screenWidth = 1280
screenHeight = 720
black = (0,0,0)
red = (255,0,0)
white = (255,255,255)

win = pygame.display.set_mode((screenWidth,screenHeight))


#import images and store in a variable
bg = pygame.image.load('Assets/background.png').convert_alpha()
game_over = pygame.image.load('Assets/game_over.png').convert_alpha()
continueImg = pygame.image.load('Assets/buttons/continue.png').convert_alpha()
startImg = pygame.image.load('Assets/buttons/start_game.png').convert_alpha()
quitImg = pygame.image.load('Assets/buttons/quit.png').convert_alpha()
creditsImg = pygame.image.load('Assets/buttons/credits.png').convert_alpha()
backImg = pygame.image.load('Assets/buttons/back.png').convert_alpha()
attackImg = pygame.image.load('Assets/buttons/attack.png').convert_alpha()
healImg = pygame.image.load('Assets/buttons/heal.png').convert_alpha()
inventoryImg = pygame.image.load('Assets/buttons/inventory.png').convert_alpha()
spellsImg = pygame.image.load('Assets/buttons/spells.png').convert_alpha()
spells_menu = pygame.image.load('Assets/spells_menu.png').convert_alpha()
flameImg = pygame.image.load('Assets/buttons/flame.png').convert_alpha()
darkVeilImg = pygame.image.load('Assets/buttons/dark_veil.png').convert_alpha()


FPS = 60
clock = pygame.time.Clock()

class Spells():
    def __init__(self, name, mana_cost, coin_cost, description):
        self.name = name
        self.mana_cost = mana_cost
        self.coin_cost = coin_cost
        self.description = description

    
    def useMinorHeal(self):
        self.hp+=20
    
    def useFlame(self,player,target):
        damage = player.strength
        target.hp -= damage
    
    def useDarkVeil(self, target):
        reduction = 1
        if target.strength > 5:
            target.strength -= reduction
        else:
            print('enemy strength cannot go lower')
    
    def holyShield(self):
        pass
        
        


class Fighter(Spells):
    def __init__(self, name, hp, strength, image):
        self.name = name
        self.hp = hp
        self.strength = strength
        self.image = pygame.image.load(image).convert_alpha()
        self.coins = 0
    #attack method that can be called to deal damage to enemy or player
    def attack(self, target):
        damage = self.strength
        target.hp -= damage

    
#heal method that will heal the player unless their hp is already full and if their hp is not full it still can not exceed 100
    def heal(self):
        # if self.hp < 100:
        #     self.hp +=10
        #     if self.hp > 100:
        #         self.hp = 100
        # else:
        #     print('hp already full')
        self.hp +=5

    
    def enemyHeal():
        pass

class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False
        self.over = False
    
    def draw(self):
        action = False
        #get mouse position
        pos = pygame.mouse.get_pos()

        #check if mouse is over button and check click conditions
        if self.rect.collidepoint(pos):
            
            #[0] means left click
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
                #print('clicked')
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        win.blit(self.image, (self.rect.x, self.rect.y))

        return action


        

# testEnemy = Fighter('testEnemy',100,10,'Assets/player.png')        
# testPlayer = Fighter('you',100,10,'Assets/player.png')
# testPlayer.useMinorHeal()
# testPlayer.useFlame(testPlayer,testEnemy)
# print(testPlayer.hp)
# print(testEnemy.hp)






def menu():

    savegameExist = config.getboolean('section_a', 'savegameExist')
    currentEnemyNumber = config.getint('section_a', 'currentEnemyNumber')
    enemyHealth = config.getint('section_a', 'enemyHealth')
    playerHealth = config.getint('section_a', 'playerHealth')
    currentTurn = config.getint('section_a', 'currentTurn')
    playerStrength = config.getint('section_a', 'playerStrength')
    enemyStrength = config.getint('section_a', 'EnemyStrength')

    #import sounds
    button_sound_1 = mixer.Sound('Assets/sounds/button_sound_1.wav')
    

    run = True
    
    #win.fill((250,0,0))
    win.blit(bg, (0, 0))
    continue_g = Button((screenWidth//2) - 360, (screenHeight//2) - 300, continueImg, 0.9)
    startBtn = Button((screenWidth//2) - 330, (screenHeight//2) - 120, startImg, 0.9)
    creditsBtn = Button((screenWidth//2) - 260, (screenHeight//2) +50, creditsImg, 0.8)
    quitBtn = Button((screenWidth//2) - 180, (screenHeight//2) +220, quitImg, 0.8)
    while run:
    
        clock.tick(FPS)
        for event in pygame.event.get():
        
            if event.type == pygame.QUIT:
                run = False
        
        if startBtn.draw():
            button_sound_1.play()
            run = False
            gameplay()

        if creditsBtn.draw():
            button_sound_1.play()
            run = False
            creditsMenu()

        if quitBtn.draw():
            #button_sound_1.play()
            run = False

        if continue_g.draw():
            button_sound_1.play()
            run = False
            gameplay(currentEnemyNumber,enemyHealth,playerHealth,currentTurn,enemyStrength,playerStrength)

        pygame.display.update()
# currentEnemyNumber,enemyHealth,playerHealth,currentTurn
def gameplay(currentEnemyNumber=None,enemyHealth=None,playerHealth=None,currentTurn=None, enemyStrength=None, playerStrength=None):
    run = True
    menuOpen = False
    disable = False

    #import sounds
    attack_sound_1 = mixer.Sound('Assets/sounds/attack_sound_1.wav')

    playerHealth = 100 if playerHealth is None else playerHealth 
    playerStrength = 10 if playerStrength is None else playerStrength
    enemyStrength = 10 if enemyStrength is None else enemyStrength

    player = Fighter('you',playerHealth,playerStrength,'Assets/player.png') # 200
    enemy1 = Fighter('blood gargoyle',30,enemyStrength,'Assets/enemies/blood_gargoyle.png')
    enemy2 = Fighter('leg day knight',22,enemyStrength-5,'Assets/enemies/leg_day_knight.png')
    enemyList = []
    enemyList.append(enemy1)
    enemyList.append(enemy2)

    if currentEnemyNumber != None:
        enemyList[currentEnemyNumber].hp = enemyHealth 

    attackBtn = Button((screenWidth//2) - 600, (screenHeight//2) +120, attackImg, 0.7)
    healBtn = Button((screenWidth//2) - 600, (screenHeight//2) +230, healImg, 0.7)
    spellsBtn = Button((screenWidth//2) - 250, (screenHeight//2) +120, spellsImg, 0.7)
    backBtn = Button((screenWidth//2) +300, (screenHeight//2) +300, backImg, 0.7)
    flamesBtn = Button((screenWidth//2) +320, (screenHeight//2) -100, flameImg, 0.6)
    darkVeilBtn = Button((screenWidth//2) +320, (screenHeight//2) - 40, darkVeilImg, 0.6)

    def drawNonFunctionalButtons():
        if attackBtn.draw():
            pass
        if healBtn.draw():
            pass
        if spellsBtn.draw():
            pass
    # turn = 1
    turn = 1 if currentTurn is None else currentTurn 
    
    # i increments the enemy number
    i = 0 if currentEnemyNumber is None else currentEnemyNumber 
    action_cooldown = 0
    action_wait_time = 90
    
    #win.blit(player.image,(100,100))
    while run:
        win.fill((20,20,0))
        font = pygame.font.SysFont('freesansbold.ttf', 30)
        surface = font.render(player.name + ' HP: ' + str(player.hp), False, (250, 250, 250))
        win.blit(surface, (1000,20))
        surface2 = font.render(enemyList[i].name + ' HP: ' + str(enemyList[i].hp), False, (250, 250, 250))
        win.blit(surface2, (1000,50))
        win.blit(enemyList[i].image,(100,100))
        #print(newImage)
        clock.tick(FPS)
        for event in pygame.event.get():
        
            if event.type == pygame.QUIT:
                run = False
            
        #checks if the enemies hp goes below 0 and increments to the next enemy
        if enemyList[i].hp <= 0:
            i+=1
            #if the last enemy in the lists hp hits 0 then the game ends and all increments are reset to 0
            if i >= len(enemyList):
                run = False
                menu()
                turn = 1
                i=0
            #if it is not the last enemy in the list the game continues and turn counter is set back to 1
            else:
                print('next floor')
                turn = 1

        #this will open the shop menu every 5 rounds
        if i % 5 == 0 and i != 0:
            pass
        

        #if players hp goes to 0 or below the game ends
        if player.hp <= 0:
            run = False
            gameOver()
        
        #if the turn modulus x returns a value of 1 then it is the players turn to pick a move
        if turn % 2 == 1:
            if attackBtn.draw():
                attack_sound_1.play()
                timer = 200
                sceneExit = False
                player.attack(enemyList[i])
                print('Enemy HP: ' + str(enemyList[i].hp))
                #displays attack notification for set amount of time in timer variable
                while not sceneExit:
                    #win.fill((20,20,0))
                    drawNonFunctionalButtons()
                    text_surface = font.render(player.name + ' attacked', False, (250, 250, 250))
                    win.blit(text_surface, (500,160))
                    pygame.display.update()
                    passed_time = clock.tick(60)
                    timer -= passed_time
                    if timer <= 0:
                        sceneExit = True
                turn+=1

            if healBtn.draw():
                player.heal()
                print( player.name + ' HP: ' +  str(player.hp))
                turn+=1
                

            if spellsBtn.draw():
                menuOpen = True
            
            #opens spell menu
            if menuOpen == True:
                win.blit(spells_menu, (943,230))
                if flamesBtn.draw():
                    player.useFlame(player,enemyList[i])
                    print(enemyList[i].name + ' HP: '+ str(enemyList[i].hp))
                    turn+=1
                    menuOpen = False
                if darkVeilBtn.draw():
                    if enemyList[i].strength > 5:
                        player.useDarkVeil(enemyList[i])
                        print(enemyList[i].name + ' strength has been lowered to:  '+ str(enemyList[i].strength))
                        turn+=1
                        menuOpen = False
                    else:
                        print('Enemy strength cannot go any lower')
                        turn+=0
                if backBtn.draw():
                    menuOpen = False
                    
                    
                    


        #if the turn modulus x returns a value of 0 then it is the enemies turn to pick a move
        if turn % 2 == 0:
            action_cooldown +=1
            rand = random.randint(0,1)
            #print(action_cooldown)
            if action_cooldown >= action_wait_time:
                if rand == 0:
                    enemyList[i].attack(player)
                    print(enemyList[i].name + ' attacked. Your HP is: ' + str(player.hp))
                    turn+=1
                    action_cooldown = 0 
                if rand == 1:
                    enemyList[i].heal()
                    print(enemyList[i].name + ' healed. Enemy HP is: ' + str(enemyList[i].hp))
                    turn+=1
                    action_cooldown = 0

            #this code draws the button too the screen while its the enemies turn but makes the buttons not functional
            drawNonFunctionalButtons()
        
        config.set('section_a', 'currentEnemyNumber', 'True')
        config.set('section_a', 'currentEnemyNumber', str(i))
        config.set('section_a', 'enemyHealth', str(enemyList[i].hp))
        config.set('section_a', 'playerHealth', str(player.hp))
        config.set('section_a', 'currentTurn', str(turn))
        config.set('section_a', 'playerStrength', str(player.strength))
        config.set('section_a', 'enemyStrength', str(enemyList[i].strength))
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        pygame.display.update()
    
def creditsMenu():
    run = True
    win.blit(bg, (0, 0))
    backBtn = Button((screenWidth//2) -580, (screenHeight//2) +250, backImg, 0.8)
    
    while run:
    
        clock.tick(FPS)
        for event in pygame.event.get():
        
            if event.type == pygame.QUIT:
                run = False
        
        if backBtn.draw():
            run = False
            menu()

        pygame.display.update()

def gameOver():
    run = True
    win.fill((0,0,0))
    win.blit(game_over, ((screenWidth//2) -350 , 0))
    
    while run:
    
        clock.tick(FPS)
        for event in pygame.event.get():
        
            if event.type == pygame.QUIT:
                run = False
        
        

        pygame.display.update()
 
menu()
pygame.quit()
