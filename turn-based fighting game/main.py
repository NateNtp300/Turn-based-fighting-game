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
masterRun = True

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
attack_menu = pygame.image.load('Assets/attack_menu.png').convert_alpha()
flameImg = pygame.image.load('Assets/buttons/flame.png').convert_alpha()
darkVeilImg = pygame.image.load('Assets/buttons/dark_veil.png').convert_alpha()
purple_flames_img = pygame.image.load('Assets/spells/purple_flames_btn.png').convert_alpha()
buyImg = pygame.image.load('Assets/buttons/buy.png').convert_alpha()
bomb_img = pygame.image.load('Assets/items/bomb_btn.png').convert_alpha()
broccoli_img = pygame.image.load('Assets/items/broccoli_btn.png').convert_alpha()
purple_banana_img = pygame.image.load('Assets/items/purple_banana_btn.png').convert_alpha()
sus_liquid_img = pygame.image.load('Assets/items/sus_liquid_btn.png').convert_alpha()
browse_spells_img = pygame.image.load('Assets/buttons/browse_spells.png').convert_alpha()
browse_items_img = pygame.image.load('Assets/buttons/browse_items.png').convert_alpha()
punch_img = pygame.image.load('Assets/attacks/punch_btn.png').convert_alpha()
pierce_img = pygame.image.load('Assets/attacks/pierce_btn.png').convert_alpha()

shopMenu_purpleFlames = pygame.image.load('Assets/spells/shopMenu_purpleFlames.png').convert_alpha()

FPS = 60
clock = pygame.time.Clock()

class GameplayHandle():
    def __init__(self, turn):
        self.turn = turn

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
        damage = 100 + player.magicStrength - target.magicDefence
        if damage > 0:
            target.hp -= damage
        if damage <= 0:
            target.hp = target.hp
            print('Enemy magic defence is too high. no damage done')


    def usePurpleFlame(self,player,target, handle):
        damage = 50 + player.magicStrength - target.magicDefence
        if damage > 0:
            if player.mana >= 20:
                player.mana -=20
                target.hp -= damage
                handle.turn+=1
            else:
                print('not enough mana')
        if damage <= 0:
            handle.turn+=1
            print('Enemy magic defence is too high. no damage done')
    
    def useDarkVeil(self, target):
        reduction = 1
        if target.strength > 5:
            target.strength -= reduction
        else:
            print('enemy strength cannot go lower')
    
    def holyShield(self):
        pass

class Attacks():
    
    def __init__(self, name, energy_cost, coin_cost, description, isBought, column):
        self.name = name
        self.energy_cost = energy_cost
        self.coin_cost = coin_cost
        self.description = description
        self.isBought = isBought
        self.column = column
    
    def usePunch(self, player, target, handle):
        damage = 5 + player.strength - target.physicalDefence
        if damage > 0:
            target.hp -=damage
            handle.turn += 1
            
        if damage <= 0:
            print('Enemy defence too high. no damage done')
        
    
    def usePierce(self,player, target, handle):
        attack_sound_1 = mixer.Sound('Assets/sounds/attack_sound_1.wav')
        damage = 10 + player.strength - target.physicalDefence
        if damage > 0:
            if player.energy >=5:
                attack_sound_1.play()
                target.hp -=damage
                handle.turn+=1
                player.energy -=5
            else:
                print('not enough energy')
            
        if damage <= 0:
            print('Enemy defence too high. no damage done')


class Items():
    def __init__(self, name, description, coin_cost, quantity, isBought, column):
        self.name = name
        self.description = description
        self.coin_cost = coin_cost
        self.quantity = quantity
        self.isBought = isBought
        self.column = column

    def useBomb(self,target):
        damage = 30
        target.hp -= damage
    
    def usePurpleBanana(player):
        player.hp += 30
    
    def useBroccoli(player):
        player.strength +=5
    
    def useSusLiquid(player):
        rand = random.randint(0,4)
        if rand == 0:
            player.hp += 30
        if rand == 1:
            player.strength += 10
        if rand == 2:
            player.physicalDefence += 10
        if rand == 3:
            player.mana += 20
        if rand == 4:
            player.hp -= 30


class Player(Spells, Items, Attacks):
    def __init__(self, name, hp, strength, magicStrength, physicalDefence, magicDefence, mana, energy, image):
        self.name = name
        self.hp = hp
        self.strength = strength
        self.magicStrength = magicStrength
        self.physicalDefence = physicalDefence
        self.magicDefence = magicDefence
        self.mana = mana
        self.energy = energy
        self.image = pygame.image.load(image).convert_alpha()
        self.coins = 0

    
#heal method that will heal the player unless their hp is already full and if their hp is not full it still can not exceed 100
    def heal(self):
        # if self.hp < 100:
        #     self.hp +=10
        #     if self.hp > 100:
        #         self.hp = 100
        # else:
        #     print('hp already full')
        self.hp +=5

class EnemyMoves():
    def testMove():
        print('attacked')

    def noMove():
        pass 
    
    def basicHeal(self, target):
        self.hp +=10
        print('Enemy healed')
    
    def basicAttack(self, target):
        damage = self.strength - target.physicalDefence
        if damage > 0:
            target.hp -= damage
            ('Enemy attacked')
        if damage <=0:
            print('No damage done. Your physical defence blocked the attack')
    
    def strengthBoost(self,target):
        self.strength+=5
        print('Enemy boosted strength')
    
class Enemy(Spells, EnemyMoves):
    def __init__(self, name, category, hp, strength, physicalDefence, magicDefence, move1, move2, image):
        self.name = name
        self.category = category
        self.hp = hp
        self.strength = strength
        self.physicalDefence = physicalDefence
        self.magicDefence = magicDefence
        self.image = pygame.image.load(image).convert_alpha()
        self.move1 = move1
        self.move2 = move2
        

    
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
            #print('hover')
            
            #[0] means left click
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
                #print('clicked')
        
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        win.blit(self.image, (self.rect.x, self.rect.y))

        return action
    def drawBtn(self):
        win.blit(self.image, (self.rect.x, self.rect.y))
    
    def hover(self, target):
        #font = pygame.font.Font('Assets/fonts/Minecraft.ttf', 25)
        font = pygame.font.SysFont('verdana', 20)
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            #print(self.rect.x)
            if target.column == 1:
                surface = font.render(target.description, True, (250,250,250))
                pygame.draw.rect(win,(0,0,0), pygame.Rect(self.rect.x -20, self.rect.y -20, surface.get_width(),20))
                win.blit(surface,(self.rect.x -20, self.rect.y -25))
                #print(target.description)
            elif target.column == 2:
                surface = font.render(target.description, True, (250,250,250))
                pygame.draw.rect(win,(0,0,0), pygame.Rect(self.rect.x -100, self.rect.y -20, surface.get_width(),20))
                win.blit(surface,(self.rect.x -100, self.rect.y -25))
            elif target.column == 3:
                pass
            else:
                pass
    




#testEnemy = Enemy('testEnemy',100,10, EnemyMoves.basicHeal, 'Assets/player.png')        
# testPlayer = Fighter('you',100,10,'Assets/player.png')
# testPlayer.useMinorHeal()
# testPlayer.useFlame(testPlayer,testEnemy)
# print(testPlayer.hp)
# print(testEnemy.hp)
#print(pygame.font.get_fonts())

#testEnemy.move1(testEnemy)

    
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
    continue_g = Button((screenWidth/2) - (continueImg.get_width()/2), (screenHeight//2) - 330, continueImg, 1)
    startBtn = Button((screenWidth/2) - (startImg.get_width()/2), (screenHeight//2) - 150, startImg, 1)
    creditsBtn = Button((screenWidth//2) - (creditsImg.get_width()/2), (screenHeight//2) +30, creditsImg, 1)
    quitBtn = Button((screenWidth//2) - (quitImg.get_width()/2), (screenHeight//2) +210, quitImg, 1)
    #win.fill((250,0,0))
    def drawMenuBtns():
        win.blit(bg, (0, 0))
        continue_g.drawBtn()
        startBtn.drawBtn()
        creditsBtn.drawBtn()
        quitBtn.drawBtn()
        
        
    drawMenuBtns()
    
    while run:
        global masterRun

        if masterRun == False:
            run = False
            break
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        
        if startBtn.draw():
            button_sound_1.play()
            #run = False
            gameplay()
            drawMenuBtns()


        if creditsBtn.draw():
            button_sound_1.play()
            #run = False
            creditsMenu()
            drawMenuBtns()
            #break

        if quitBtn.draw():
            #button_sound_1.play()
            run = False
            break

        if continue_g.draw():
            button_sound_1.play()
            #run = False
            gameplay(currentEnemyNumber,enemyHealth,playerHealth,currentTurn,enemyStrength,playerStrength,currentRound,currentCoins, darkVeilbought)
            drawMenuBtns()

        pygame.display.update()
# currentEnemyNumber,enemyHealth,playerHealth,currentTurn
def gameplay(currentEnemyNumber=None,enemyHealth=None,playerHealth=None,currentTurn=None, enemyStrength=None, playerStrength=None, currentRound=None, currentCoins=None, darkVeilbought=None):
    
    global spellsMenuOpen, inventoryMenuOpen, shopOpen,turn, i, round, run, action_wait_time, action_cooldown, browseSpells, browseItems, roundOver, round_wait_time, round_cooldown, attackMenuOpen, intro
    
    
    run = True
    intro = True
    attackMenuOpen = False
    spellsMenuOpen = False
    inventoryMenuOpen = False
    shopOpen = False
    browseSpells = True
    browseItems = False
    roundOver = False

    #turn keeps track of current turns during gameplay
    turn = 1 if currentTurn is None else currentTurn 
    
    # i increments the enemy number
    i = 0 if currentEnemyNumber is None else currentEnemyNumber 
    
    action_cooldown = 0
    action_wait_time = 90
    round_cooldown = 0
    round_wait_time = 110
    
    #import sounds
    
    
    round = 0 if currentRound is None else currentRound
    playerHealth = 100 if playerHealth is None else playerHealth
    playerMana = 10 
    playerEnergy = 10 
    playerStrength = 0 if playerStrength is None else playerStrength
    playerMagicStrength = 0
    playerPhysicalDefence = 0
    playerMagicDefence = 0

    enemyStrength = 10 if enemyStrength is None else enemyStrength
    enemyPhysicalDefence = 0
    enemyMagicDefence = 0

    flame = Spells('Flame',10,30,'Deals minor fire damage to enemy', True)
    darkVeil = Spells('Dark Veil',10,30,'Lowers enemy strength by one', False)
    purpleFlames = Spells('Purple Flames', 20, 20, 'Searing purple flames that deal 50 dark damage', False)

    bomb = Items('Bomb','Deals 30 damage to enemies and ignores their defence',10,2,True,1)
    purple_banana = Items('Purple Banana','Heals 30 HP',10,2,True,1)
    broccoli = Items('Broccoli','Raises physical strength by 5 for one round',10,2,True,1)
    sus_liquid = Items('Sus Liquid','Has a random beneficial effect, Or possibly a negative',10,2,True,2)

    punch = Attacks('Punch',0,0,'[Punch] Deals 5 base damage. Energy cost: 0', True, 1)
    pierce = Attacks('Pierce',5,20,'[Pierce] Deals 10 base damage. Energy cost: 5', True, 1)

    gameplayHandle = GameplayHandle(1)

    player = Player('Player',playerHealth, playerStrength, playerMagicStrength, playerPhysicalDefence, playerMagicDefence, playerMana,playerEnergy,'Assets/player.png') # 200

    player.coins = 0 if currentCoins is None else currentCoins
    darkVeil.isBought = False if darkVeilbought is None else darkVeilbought

    enemy1 = Enemy('Blood gargoyle', 'Normal', 10, enemyStrength, enemyPhysicalDefence, enemyMagicDefence, EnemyMoves.basicAttack, EnemyMoves.basicHeal, 'Assets/enemies/blood_gargoyle.png')
    enemy2 = Enemy('Leg day knight', 'Normal',10,enemyStrength-5, enemyPhysicalDefence, enemyMagicDefence, EnemyMoves.basicAttack, EnemyMoves.basicHeal,'Assets/enemies/leg_day_knight.png')
    enemy3 = Enemy('Pissed Alien', 'Normal',30,enemyStrength, enemyPhysicalDefence, enemyMagicDefence+5, EnemyMoves.basicAttack, EnemyMoves.basicHeal,'Assets/enemies/pissed_alien.png')
    enemy4 = Enemy('Gargoyle', 'Normal',5,enemyStrength, enemyPhysicalDefence, enemyMagicDefence, EnemyMoves.basicAttack, EnemyMoves.basicHeal,'Assets/enemies/gargoyle.png')
    enemy5 = Enemy('Insane Knight', 'Normal',20,enemyStrength-5, enemyPhysicalDefence, enemyMagicDefence, EnemyMoves.basicAttack, EnemyMoves.basicHeal,'Assets/enemies/insane_knight.png')
    enemy6 = Enemy('Veno the Traitor', 'Normal',20,enemyStrength-5, enemyPhysicalDefence, enemyMagicDefence, EnemyMoves.basicAttack, EnemyMoves.basicHeal,'Assets/enemies/veno_the_traitor.png')
    enemy7 = Enemy('Pissed Gnome', 'Normal',5,enemyStrength, enemyPhysicalDefence, enemyMagicDefence, EnemyMoves.basicAttack, EnemyMoves.basicHeal,'Assets/enemies/pissed_gnome.png')
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
    purple_banana_btn = Button(screenWidth - purple_banana_img.get_width() - 550, screenHeight - inventory_menu.get_height() + 150, purple_banana_img, 1)
    bomb_btn = Button(screenWidth - purple_banana_img.get_width() - 550, screenHeight - inventory_menu.get_height() + 20, bomb_img, 1)
    broccoli_btn = Button(screenWidth - broccoli_img.get_width() - 550, screenHeight - inventory_menu.get_height() + 280, broccoli_img, 1)
    sus_liquid_btn = Button(screenWidth - sus_liquid_img.get_width() - 390, screenHeight - inventory_menu.get_height() + 20, sus_liquid_img, 1)
    buyDarkVeilBtn = Button((screenWidth//2), (screenHeight//2), buyImg, 0.3)
    buyPurpleFlamesBtn = Button(770,0, buyImg, 0.3)
    browse_spells_btn = Button(0 + browse_spells_img.get_width() - 320, screenHeight - browse_spells_img.get_height() -10, browse_spells_img, 1)
    browse_items_btn = Button(0 + browse_items_img.get_width() + 30, screenHeight - browse_items_img.get_height() -10, browse_items_img, 1)
    punch_btn = Button(screenWidth - punch_img.get_width() - 550, screenHeight - attack_menu.get_height() + 20, punch_img, 1)
    pierce_btn = Button(screenWidth - pierce_img.get_width() - 550, screenHeight - attack_menu.get_height() + 150, pierce_img, 1) 
    

    #continues to draw the players buttons to the screen during enemies turn but makes them non functional
    def drawNonFunctionalButtons():
        if attackBtn.draw():
            pass
        if healBtn.draw():
            pass
        if spellsBtn.draw():
            pass
        if InventoryBtn.draw():
            pass
    
    #opens the spell menu
    def spellsMenu():
        global spellsMenuOpen, inventoryMenuOpen, attackMenuOpen
        attackMenuOpen = False
        inventoryMenuOpen = False
        win.blit(spells_menu, (screenWidth - spells_menu.get_width(),screenHeight - spells_menu.get_height()))
        if flame.isBought == True:
            if flamesBtn.draw():
                player.useFlame(player,enemyList[i])
                print(enemyList[i].name + ' HP: '+ str(enemyList[i].hp))
                gameplayHandle.turn +=1
                spellsMenuOpen = False
        if darkVeil.isBought == True:
            if darkVeilBtn.draw():
                if enemyList[i].strength > 5:
                    player.useDarkVeil(enemyList[i])
                    print(enemyList[i].name + ' strength has been lowered to:  '+ str(enemyList[i].strength))
                    gameplayHandle.turn +=1
                    spellsMenuOpen = False
                else:
                    print('Enemy strength cannot go any lower')
                    
        if purpleFlames.isBought == True:
            if purple_flames_btn.draw():
                player.usePurpleFlame(player, enemyList[i], gameplayHandle)
                spellsMenuOpen = False

        if backBtn.draw():
            spellsMenuOpen = False
    
    def inventoryMenu():
        global spellsMenuOpen, inventoryMenuOpen, attackMenuOpen
        
        spellsMenuOpen = False
        attackMenuOpen = False
        win.blit(inventory_menu, (screenWidth - inventory_menu.get_width(),screenHeight - inventory_menu.get_height()))

        if purple_banana.isBought == True:
            if purple_banana.quantity > 0:
                purpleBananaQuantityDisplay = font.render('x'+ str(purple_banana.quantity), True, (250, 250, 250))
                win.blit(purpleBananaQuantityDisplay, (screenWidth - purple_banana_img.get_width() - 440, screenHeight - inventory_menu.get_height() + 150))
                purple_banana_btn.hover(purple_banana)
                if purple_banana_btn.draw():
                    player.usePurpleBanana()
                    gameplayHandle.turn +=1
                    purple_banana.quantity -= 1
                    inventoryMenuOpen = False
        
        if bomb.isBought == True:
            if bomb.quantity > 0:
                bombQuantityDisplay = font.render('x'+ str(bomb.quantity), True, (250, 250, 250))
                win.blit(bombQuantityDisplay, (screenWidth - purple_banana_img.get_width() - 440, screenHeight - inventory_menu.get_height() + 20))
                bomb_btn.hover(bomb)
                if bomb_btn.draw():
                    player.useBomb(enemyList[i])
                    gameplayHandle.turn +=1
                    bomb.quantity -= 1
                    inventoryMenuOpen = False
                
                

        if broccoli.isBought == True:
            if broccoli.quantity > 0:
                broccoliQuantityDisplay = font.render('x'+ str(broccoli.quantity), True, (250, 250, 250))
                win.blit(broccoliQuantityDisplay, (screenWidth - purple_banana_img.get_width() - 440, screenHeight - inventory_menu.get_height() +280 ))
                broccoli_btn.hover(broccoli)
                if broccoli_btn.draw():
                    player.useBroccoli()
                    gameplayHandle.turn +=1
                    broccoli.quantity -=1
                    inventoryMenuOpen = False

        if sus_liquid.isBought == True:
            if sus_liquid.quantity > 0:
                susLiquidQuantityDisplay = font.render('x'+ str(sus_liquid.quantity), True, (250, 250, 250))
                win.blit(susLiquidQuantityDisplay, (screenWidth - sus_liquid_img.get_width() - 280, screenHeight - inventory_menu.get_height() +20 ))
                sus_liquid_btn.hover(sus_liquid)
                if sus_liquid_btn.draw():
                    player.useSusLiquid()
                    gameplayHandle.turn +=1
                    sus_liquid.quantity -=1
                    inventoryMenuOpen = False

        if backBtn.draw():
            inventoryMenuOpen = False

    def enemyDeath():
            global i, round, run, roundOver
            i+=1
            #print(i)
            #if the last enemy in the lists hp hits 0 then the game ends and all increments are reset to 0
            if i >= len(enemyList):
                run = False
                #menu()
                gameplayHandle.turn = 1
                i=0
                round = 0
                
            #if it is not the last enemy in the list the game continues and turn counter is set back to 1
            else:
                #floorTransition()
                roundOver = True
                player.coins +=10
                player.strength = 0
                player.magicStrength = 0
                print("Your coins are " + str(player.coins))
                gameplayHandle.turn = 1
                round +=1
                print('floor: '+ str(i+1))
    
    def shopMenu():
            global round, shopOpen, browseSpells, browseItems, roundOver
            
            win.fill((30,20,0))
            coinDisplay = font.render('Your coins: '+ str(player.coins), True, (250, 250, 250))
            win.blit(coinDisplay, (1050,10))
            shopOpen = True

            if browse_spells_btn.draw():
                browseSpells = True
                browseItems = False
            if browse_items_btn.draw():
                browseSpells = False
                browseItems = True
            
            if browseSpells == True:
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
            
            if browseItems == True:
                pass


            if backBtn.draw():
                shopOpen = False
                roundOver = True
                round+=1
    
    def attackMenu():
        global attackMenuOpen, spellsMenuOpen, inventoryMenuOpen
        spellsMenuOpen = False
        inventoryMenuOpen = False
        win.blit(attack_menu, (screenWidth - attack_menu.get_width(),screenHeight - attack_menu.get_height()))
        if punch.isBought == True:
            punch_btn.hover(punch)   
            if punch_btn.draw():
                player.usePunch(player,enemyList[i], gameplayHandle)
        
        if pierce.isBought == True:
            pierce_btn.hover(pierce)
            if pierce_btn.draw():
                player.usePierce(player,enemyList[i], gameplayHandle)
        
        if backBtn.draw():
            attackMenuOpen = False

    #handles the players turn
    def playerMove():
            global spellsMenuOpen, inventoryMenuOpen, attackMenuOpen, i
            if attackBtn.draw():
                attackMenuOpen = True

            if attackMenuOpen == True:
                attackMenu()

            if healBtn.draw():
                spellsMenuOpen = False
                inventoryMenuOpen = False
                player.heal()
                print( player.name + ' HP: ' +  str(player.hp))
                gameplayHandle.turn+=1
                
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

            action_cooldown += 1
            rand = random.randint(0,1)
            #print(action_cooldown)
            if action_cooldown >= action_wait_time:
                if rand == 0:
                    enemyList[i].move1(enemyList[i], player)
                    print(enemyList[i].name + ' attacked. Your HP is: ' + str(player.hp))
                    gameplayHandle.turn+=1
                    action_cooldown = 0 
                if rand == 1:
                    enemyList[i].move2(enemyList[i], player)
                    print(enemyList[i].name + ' healed. Enemy HP is: ' + str(enemyList[i].hp))
                    gameplayHandle.turn+=1
                    action_cooldown = 0

            #this code draws the button too the screen while its the enemies turn but makes the buttons not functional
            drawNonFunctionalButtons()
    
    def floorTransition():
        global round_wait_time, round_cooldown, roundOver
        round_cooldown += 1
        if round_cooldown < round_wait_time:
            win.fill((0,0,0))
            surface = font.render('Floor ' + str(round+1), True, (250, 250, 250))
            win.blit(surface, ((screenWidth/2 - surface.get_width()/2), (screenHeight/2 - surface.get_height()/2)))
        if round_cooldown >= round_wait_time:
            roundOver = False
            round_cooldown = 0
    
    def introScene():
        global round_wait_time, round_cooldown, intro
        round_cooldown += 1
        
        if round_cooldown < round_wait_time:
            win.fill((0,0,0))
            surface = font.render('Floor ' + str(round+1), True, (250, 250, 250))
            win.blit(surface, ((screenWidth/2 - surface.get_width()/2), (screenHeight/2 - surface.get_height()/2)))
        if round_cooldown >= round_wait_time:
            round_cooldown = 0
            intro = False

    while run:
        win.fill((20,20,0))
        font = pygame.font.Font('Assets/fonts/Minecraft.ttf', 25)
        playerSurface1 = font.render(player.name , True, (250, 250, 250))
        playerSurface2 = font.render('HP: ' + str(player.hp), True, (250,250,250))
        playerSurface3 = font.render('Mana: ' + str(player.mana), True, (250,250,250))
        playerSurface4 = font.render('Energy: ' + str(player.energy), True, (250,250,250))
        playerSurface5 = font.render('Strength Bonus: ' + str(player.strength), True, (250,250,250))
        playerSurface6 = font.render('Magic Bonus: ' + str(player.magicStrength), True, (250,250,250))
        playerSurface7 = font.render('Physical Defence: ' + str(player.physicalDefence), True, (250,250,250))
        playerSurface8 = font.render('Magic Defence: ' + str(player.magicDefence), True, (250,250,250))
        win.blit(playerSurface1, (screenWidth * 0.8,10))
        win.blit(playerSurface2, (screenWidth * 0.7,40))
        win.blit(playerSurface3, (screenWidth * 0.8,40))
        win.blit(playerSurface4, (screenWidth * 0.9,40))
        win.blit(playerSurface5, (screenWidth * 0.7,70))
        win.blit(playerSurface6, (screenWidth * 0.7,100))
        win.blit(playerSurface7, (screenWidth * 0.7,130))
        win.blit(playerSurface8, (screenWidth * 0.7,160))
        enemySurface1 = font.render(enemyList[i].name, True, (250,250,250))
        enemySurface2 = font.render('HP: ' + str(enemyList[i].hp), True, (250, 250, 250))
        enemySurface3 = font.render('Physical Defence: ' + str(enemyList[i].physicalDefence), True, (250,250,250))
        enemySurface4 = font.render('Magic Defence: ' + str(enemyList[i].magicDefence), True, (250,250,250))
        win.blit(enemySurface1, (0 + 10, 10))
        win.blit(enemySurface2, (0 + 10 ,40))
        win.blit(enemySurface3, (0 + 10 ,70))
        win.blit(enemySurface4, (0 + 10 ,100))
        win.blit(enemyList[i].image,(100,200))
        #print(newImage)
        clock.tick(FPS)
        for event in pygame.event.get():
        
            if event.type == pygame.QUIT:
                global masterRun
                masterRun = False
                run = False
                break
        

        #checks if the enemies hp goes below 0
        if enemyList[i].hp <= 0:
            enemyDeath()

        if intro == True:
            introScene()

        if roundOver == True:
            floorTransition()
                       

        #this will open the shop menu every 5 rounds except for the first round
        if round % 5 == 0 and round != 0:
            shopMenu()
        

        #if players hp goes to 0 or below the game ends
        if player.hp <= 0:
            run = False
            gameOver()
            break
        
        #if the turn modulus 2 returns a value of 1 then it is the players turn to pick a move
        if gameplayHandle.turn % 2 == 1 and shopOpen == False and roundOver == False and intro == False:
            playerMove()
            
                

        #if the turn modulus 2 returns a value of 0 then it is the enemies turn to pick a move
        if gameplayHandle.turn % 2 == 0 and shopOpen == False:
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
    #win.fill((0,0,0))
    backBtn = Button((screenWidth - screenWidth * 0.98), (screenHeight - screenHeight * 0.12), backImg, 1)
    
    def drawMenuBtns():
        win.blit(bg, (0, 0))
        backBtn.drawBtn()
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
        if backBtn.draw():
            run = False  
            #menu()

        pygame.display.update()

def gameOver():
    run = True
    win.fill((0,0,0))
    win.blit(game_over, ((screenWidth//2) -350 , 0))
    backBtn = Button(screenWidth - backImg.get_width() * 2.2, screenHeight - backImg.get_height(), backImg, 1)
    
    
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        if backBtn.draw():
            run = False
            #menu()
            

        pygame.display.update()
 
menu()
pygame.quit()
