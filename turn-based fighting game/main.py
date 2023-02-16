import pygame, os, random, sys, time
from pygame import mixer
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')

pygame.font.init()
pygame.init()

pygame.display.set_caption("Window") #window name
keys = pygame.key.get_pressed()

# screenWidth = pygame.display.get_desktop_sizes()[0][0]
# screenHeight = pygame.display.get_desktop_sizes()[0][1]
## fullscreen window (for 1080p)
screenWidth = pygame.display.get_desktop_sizes()[0][0] * 1
screenHeight = pygame.display.get_desktop_sizes()[0][1] * 0.93
## window
# screenWidth = 1280
# screenHeight = 720

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
inventory_menu = pygame.image.load('Assets/inventory_menu.png').convert_alpha()
flameImg = pygame.image.load('Assets/buttons/flame.png').convert_alpha()
darkVeilImg = pygame.image.load('Assets/buttons/dark_veil.png').convert_alpha()
purple_flames_img = pygame.image.load('Assets/spells/purple_flames_btn.png').convert_alpha()
buyImg = pygame.image.load('Assets/buttons/buy.png').convert_alpha()
bomb_img = pygame.image.load('Assets/items/bomb_btn.png').convert_alpha()
purple_banana_img = pygame.image.load('Assets/items/purple_banana_btn.png').convert_alpha()

shopMenu_purpleFlames = pygame.image.load('Assets/spells/shopMenu_purpleFlames.png').convert_alpha()

FPS = 60
clock = pygame.time.Clock()

class Spells():
    def __init__(self, name, mana_cost, coin_cost, description, isBought):
        self.name = name
        self.mana_cost = mana_cost
        self.coin_cost = coin_cost
        self.description = description
        self.isBought = isBought

    
    def useMinorHeal(self):
        self.hp+=20
    
    def useFlame(self,player,target):
        damage = player.strength
        target.hp -= damage

    def usePurpleFlame(self,target):
        damage = 50
        target.hp -= damage
    
    def useDarkVeil(self, target):
        reduction = 1
        if target.strength > 5:
            target.strength -= reduction
        else:
            print('enemy strength cannot go lower')
    
    def holyShield(self):
        pass

class Items():
    def __init__(self, name, description, coin_cost, quantity, isBought):
        self.name = name
        self.description = description
        self.coin_cost = coin_cost
        self.quantity = quantity
        self.isBought = isBought

    def useBomb(self,target):
        damage = 30
        target.hp -= damage
    
    def usePurpleBanana(player):
        player.hp += 30


class Player(Spells, Items):
    def __init__(self, name, hp, strength, mana, energy, image):
        self.name = name
        self.hp = hp
        self.strength = strength
        self.mana = mana
        self.energy = energy
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

class Enemy(Spells):
    def __init__(self, name, hp, strength, image):
        self.name = name
        self.hp = hp
        self.strength = strength
        self.image = pygame.image.load(image).convert_alpha()
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
#print(pygame.font.get_fonts())


def menu():

    savegameExist = config.getboolean('section_a', 'savegameExist')
    currentEnemyNumber = config.getint('section_a', 'currentEnemyNumber')
    enemyHealth = config.getint('section_a', 'enemyHealth')
    playerHealth = config.getint('section_a', 'playerHealth')
    currentTurn = config.getint('section_a', 'currentTurn')
    playerStrength = config.getint('section_a', 'playerStrength')
    enemyStrength = config.getint('section_a', 'EnemyStrength')
    currentRound = config.getint('section_a', 'currentRound')
    currentCoins = config.getint('section_a', 'currentcoins')
    darkVeilbought = config.getboolean('section_a', 'darkVeilbought')

    #import sounds
    button_sound_1 = mixer.Sound('Assets/sounds/button_sound_1.wav')
    

    run = True
    
    #win.fill((250,0,0))
    win.blit(bg, (0, 0))
    continue_g = Button((screenWidth/2) - (continueImg.get_width()/2), (screenHeight//2) - 330, continueImg, 1)
    startBtn = Button((screenWidth/2) - (startImg.get_width()/2), (screenHeight//2) - 150, startImg, 1)
    creditsBtn = Button((screenWidth//2) - (creditsImg.get_width()/2), (screenHeight//2) +30, creditsImg, 1)
    quitBtn = Button((screenWidth//2) - (quitImg.get_width()/2), (screenHeight//2) +210, quitImg, 1)
    
    
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
            gameplay(currentEnemyNumber,enemyHealth,playerHealth,currentTurn,enemyStrength,playerStrength,currentRound,currentCoins, darkVeilbought)

        pygame.display.update()
# currentEnemyNumber,enemyHealth,playerHealth,currentTurn
def gameplay(currentEnemyNumber=None,enemyHealth=None,playerHealth=None,currentTurn=None, enemyStrength=None, playerStrength=None, currentRound=None, currentCoins=None, darkVeilbought=None):
    
    global spellsMenuOpen, inventoryMenuOpen, turn, shopOpen, i, round, run, action_wait_time, action_cooldown
    run = True
    spellsMenuOpen = False
    inventoryMenuOpen = False
    shopOpen = False
    
    #turn keeps track of current turns during gameplay
    turn = 1 if currentTurn is None else currentTurn 
    
    # i increments the enemy number
    i = 0 if currentEnemyNumber is None else currentEnemyNumber 
    
    action_cooldown = 0
    action_wait_time = 90
    
    #import sounds
    attack_sound_1 = mixer.Sound('Assets/sounds/attack_sound_1.wav')
    
    round = 0 if currentRound is None else currentRound
    playerHealth = 100 if playerHealth is None else playerHealth
    playerMana = 100 
    playerEnergy = 100 
    playerStrength = 50 if playerStrength is None else playerStrength
    enemyStrength = 10 if enemyStrength is None else enemyStrength

    flame = Spells('Flame',10,30,'Deals minor fire damage to enemy', True)
    darkVeil = Spells('Dark Veil',10,30,'Lowers enemy strength by one', False)
    purpleFlames = Spells('Purple Flames', 20, 20, 'Searing purple flames that deal 50 dark damage', False)

    bomb = Items('Bomb','Deals 30 damage to enemies and ignores their defence',10,2,True)
    purple_banana = Items('Purple Banana','Heals 30 HP',10,2,True)

    player = Player('you',playerHealth,playerStrength,playerMana,playerEnergy,'Assets/player.png') # 200

    player.coins = 0 if currentCoins is None else currentCoins
    darkVeil.isBought = False if darkVeilbought is None else darkVeilbought

    enemy1 = Enemy('Blood gargoyle',30,enemyStrength,'Assets/enemies/blood_gargoyle.png')
    enemy2 = Enemy('Leg day knight',22,enemyStrength-5,'Assets/enemies/leg_day_knight.png')
    enemy3 = Enemy('Pissed Alien',5,enemyStrength,'Assets/enemies/pissed_alien.png')
    enemy4 = Enemy('Gargoyle',5,enemyStrength,'Assets/enemies/gargoyle.png')
    enemy5 = Enemy('Insane Knight',22,enemyStrength-5,'Assets/enemies/insane_knight.png')
    enemy6 = Enemy('Veno the Traitor',22,enemyStrength-5,'Assets/enemies/veno_the_traitor.png')
    enemy7 = Enemy('Pissed Gnome',5,enemyStrength,'Assets/enemies/pissed_gnome.png')
    enemyList = []
    for x in enemy1, enemy2, enemy3, enemy4, enemy5, enemy6, enemy7:
        enemyList.append(x)
    

    if currentEnemyNumber != None:
        enemyList[currentEnemyNumber].hp = enemyHealth 

    attackBtn = Button(0 + 20, screenHeight - (attackImg.get_height() *2.4), attackImg, 1)
    healBtn = Button(0 + 20, screenHeight - (healImg.get_height()*1.2), healImg, 1)
    spellsBtn = Button(0 + spellsImg.get_width()* 0.95, screenHeight - (spellsImg.get_height()*2.4), spellsImg, 1)
    InventoryBtn = Button(0 + spellsImg.get_width()* 0.95, screenHeight - (healImg.get_height()*1.2), inventoryImg, 1)
    backBtn = Button(screenWidth - backImg.get_width() * 2.2, screenHeight - backImg.get_height(), backImg, 1)
    flamesBtn = Button(screenWidth - flameImg.get_width() - 65, screenHeight - spells_menu.get_height() + 10, flameImg, 1)
    darkVeilBtn = Button(screenWidth - flameImg.get_width() - 65, screenHeight - spells_menu.get_height() + 80, darkVeilImg, 1)
    purple_flames_btn = Button(screenWidth - flameImg.get_width() - 65, screenHeight - spells_menu.get_height() + 150, purple_flames_img, 1)
    purple_banana_btn = Button(screenWidth - purple_banana_img.get_width() - 210, screenHeight - inventory_menu.get_height() + 150, purple_banana_img, 1)
    bomb_btn = Button(screenWidth - purple_banana_img.get_width() - 210, screenHeight - inventory_menu.get_height() + 15, bomb_img, 1)
    buyDarkVeilBtn = Button((screenWidth//2), (screenHeight//2), buyImg, 0.3)
    buyPurpleFlamesBtn = Button(770,0, buyImg, 0.3)

    #continues to draw the players buttons to the screen during enemies turn but makes them non functional
    def drawNonFunctionalButtons():
        if attackBtn.draw():
            pass
        if healBtn.draw():
            pass
        if spellsBtn.draw():
            pass
    
    #opens the spell menu
    def spellsMenu():
        global turn
        global spellsMenuOpen
        global inventoryMenuOpen
        inventoryMenuOpen = False
        win.blit(spells_menu, (screenWidth - spells_menu.get_width(),screenHeight - spells_menu.get_height()))
        if flame.isBought == True:
            if flamesBtn.draw():
                player.useFlame(player,enemyList[i])
                print(enemyList[i].name + ' HP: '+ str(enemyList[i].hp))
                turn+=1
                spellsMenuOpen = False
        if darkVeil.isBought == True:
            if darkVeilBtn.draw():
                if enemyList[i].strength > 5:
                    player.useDarkVeil(enemyList[i])
                    print(enemyList[i].name + ' strength has been lowered to:  '+ str(enemyList[i].strength))
                    turn+=1
                    spellsMenuOpen = False
                else:
                    print('Enemy strength cannot go any lower')
                    turn+=0
        if purpleFlames.isBought == True:
            if purple_flames_btn.draw():
                player.usePurpleFlame(enemyList[i])
                print(enemyList[i].name + ' HP: '+ str(enemyList[i].hp))
                turn+=1
                spellsMenuOpen = False

        if backBtn.draw():
            spellsMenuOpen = False
    
    def inventoryMenu():
        global spellsMenuOpen
        global inventoryMenuOpen
        global turn
        
        spellsMenuOpen = False
        win.blit(inventory_menu, (screenWidth - spells_menu.get_width(),screenHeight - spells_menu.get_height()))

        if purple_banana.isBought == True:
            if purple_banana.quantity > 0:
                purpleBananaQuantityDisplay = font.render('x'+ str(purple_banana.quantity), True, (250, 250, 250))
                win.blit(purpleBananaQuantityDisplay, (screenWidth - purple_banana_img.get_width() - 100, screenHeight - inventory_menu.get_height() + 150))
                if purple_banana_btn.draw():
                    player.usePurpleBanana()
                    turn +=1
                    purple_banana.quantity -= 1
                    inventoryMenuOpen = False
        
        if bomb.isBought == True:
            if bomb.quantity > 0:
                bombQuantityDisplay = font.render('x'+ str(bomb.quantity), True, (250, 250, 250))
                win.blit(bombQuantityDisplay, (screenWidth - purple_banana_img.get_width() - 100, screenHeight - inventory_menu.get_height() + 20))
                if bomb_btn.draw():
                    player.useBomb(enemyList[i])
                    turn+=1
                    bomb.quantity -= 1
                    inventoryMenuOpen = False

        if backBtn.draw():
            inventoryMenuOpen = False

    def enemyDeath():
            global i, turn, round, run
            i+=1
            #print(i)
            #if the last enemy in the lists hp hits 0 then the game ends and all increments are reset to 0
            if i >= len(enemyList):
                run = False
                menu()
                turn = 1
                i=0
                round = 0
            #if it is not the last enemy in the list the game continues and turn counter is set back to 1
            else:
                player.coins +=10
                print("Your coins are " + str(player.coins))
                turn = 1
                round +=1
                print('floor: '+ str(i+1))
    
    def shopMenu():
            global round, shopOpen
            win.fill((30,20,0))
            coinDisplay = font.render('Your coins: '+ str(player.coins), True, (250, 250, 250))
            win.blit(coinDisplay, (1050,10))
            shopOpen = True
            
            if darkVeil.isBought == False:
                if buyDarkVeilBtn.draw():
                    if player.coins>= darkVeil.coin_cost:
                        player.coins -= darkVeil.coin_cost
                        darkVeil.isBought = True
                        print('dark veil bought for ' + str(darkVeil.coin_cost) + ' coins')
                    else:
                        print('not enough coins')
            
            if purpleFlames.isBought == False:
                win.blit(shopMenu_purpleFlames, (0, 0))
                spellName = font.render(purpleFlames.name, True, (250, 250, 250))
                win.blit(spellName, (180,5))
                spellDescription = font.render(purpleFlames.description, True, (250, 250, 250))
                win.blit(spellDescription, (180,40))
                spellCost = font.render('Cost: ' + str(purpleFlames.coin_cost), True, (250, 250, 250))
                win.blit(spellCost, (180,85))
                if buyPurpleFlamesBtn.draw():
                    if player.coins>= purpleFlames.coin_cost:
                        player.coins -= purpleFlames.coin_cost
                        purpleFlames.isBought = True
                        print('Purple Flames bought for ' + str(purpleFlames.coin_cost) + ' coins')
                    else:
                        print('not enough coins')

            if backBtn.draw():
                shopOpen = False
                round+=1
    
    #handles the players turn
    def playerMove():
            if attackBtn.draw():
                global spellsMenuOpen, inventoryMenuOpen, turn, i
                spellsMenuOpen = False
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
                spellsMenuOpen = False
                player.heal()
                print( player.name + ' HP: ' +  str(player.hp))
                turn+=1
                
            #If player clicks on the spells button then it sets spellsMenuOpen to true which then will open the spell menu
            if spellsBtn.draw():
                spellsMenuOpen = True
            
            #opens spell menu
            if spellsMenuOpen == True:
                spellsMenu()
            
            if InventoryBtn.draw():
                inventoryMenuOpen = True
            
            if inventoryMenuOpen == True:
                inventoryMenu()
    
    #handles the enemys turn
    def enemyMove():
            global turn, i, action_cooldown, action_wait_time

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

    while run:
        win.fill((20,20,0))
        font = pygame.font.Font('Assets/fonts/Minecraft.ttf', 25)
        surface = font.render(player.name + ' HP: ' + str(player.hp), True, (250, 250, 250))
        win.blit(surface, (screenWidth - 300,10))
        surface2 = font.render(enemyList[i].name + ' HP: ' + str(enemyList[i].hp), True, (250, 250, 250))
        win.blit(surface2, (screenWidth - 300,50))
        win.blit(enemyList[i].image,(100,100))
        #print(newImage)
        clock.tick(FPS)
        for event in pygame.event.get():
        
            if event.type == pygame.QUIT:
                run = False
            
        #checks if the enemies hp goes below 0
        if enemyList[i].hp <= 0:
            enemyDeath()            

        #this will open the shop menu every 5 rounds except for the first round
        if round % 5 == 0 and round != 0:
            shopMenu()
        

        #if players hp goes to 0 or below the game ends
        if player.hp <= 0:
            run = False
            gameOver()
        
        #if the turn modulus 2 returns a value of 1 then it is the players turn to pick a move
        if turn % 2 == 1 and shopOpen == False:
            playerMove()
            
                

        #if the turn modulus 2 returns a value of 0 then it is the enemies turn to pick a move
        if turn % 2 == 0 and shopOpen == False:
            enemyMove()
            
        
        config.set('section_a', 'currentEnemyNumber', 'True')
        config.set('section_a', 'currentEnemyNumber', str(i))
        config.set('section_a', 'enemyHealth', str(enemyList[i].hp))
        config.set('section_a', 'playerHealth', str(player.hp))
        config.set('section_a', 'currentTurn', str(turn))
        config.set('section_a', 'playerStrength', str(player.strength))
        config.set('section_a', 'enemyStrength', str(enemyList[i].strength))
        config.set('section_a', 'currentRound', str(round))
        config.set('section_a', 'currentcoins', str(player.coins))
        config.set('section_a', 'darkVeilbought', str(darkVeil.isBought))
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        pygame.display.update()



def creditsMenu():
    run = True
    win.blit(bg, (0, 0))
    backBtn = Button((screenWidth - screenWidth * 0.98), (screenHeight - screenHeight * 0.12), backImg, 1)
    
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
