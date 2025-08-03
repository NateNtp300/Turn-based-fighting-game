import pygame
from pygame import mixer

class Assets:
    def __init__(self):
        self.bg = pygame.image.load('Assets/background.png').convert_alpha()
        self.game_over = pygame.image.load('Assets/game_over.png').convert_alpha()
        self.continueImg = pygame.image.load('Assets/buttons/continue.png').convert_alpha()
        self.startImg = pygame.image.load('Assets/buttons/start_game.png').convert_alpha()
        self.startHighlightImg = pygame.image.load('Assets/buttons/start_game_highlight.png').convert_alpha()
        self.quitImg = pygame.image.load('Assets/buttons/quit.png').convert_alpha()
        self.creditsImg = pygame.image.load('Assets/buttons/credits.png').convert_alpha()
        self.optionsImg = pygame.image.load('Assets/buttons/options.png').convert_alpha()
        self.volume_left_img = pygame.image.load('Assets/buttons/volume_left.png').convert_alpha()
        self.volume_right_img = pygame.image.load('Assets/buttons/volume_right.png').convert_alpha()
        self.volume_pointer_img = pygame.image.load('Assets/options/volume_pointer.png').convert_alpha()
        self.volume_slider_img = pygame.image.load('Assets/options/volume_slider.png').convert_alpha()
        self.backImg = pygame.image.load('Assets/buttons/back.png').convert_alpha()
        self.attackImg = pygame.image.load('Assets/buttons/attack.png').convert_alpha()
        self.healImg = pygame.image.load('Assets/buttons/heal.png').convert_alpha()
        self.inventoryImg = pygame.image.load('Assets/buttons/inventory.png').convert_alpha()
        self.spellsImg = pygame.image.load('Assets/buttons/spells.png').convert_alpha()
        self.spells_menu = pygame.image.load('Assets/spells_menu.png').convert_alpha()
        self.inventory_menu = pygame.image.load('Assets/inventory_menu.png').convert_alpha()
        self.attack_menu = pygame.image.load('Assets/attack_menu.png').convert_alpha()
        self.flameImg = pygame.image.load('Assets/buttons/flame.png').convert_alpha()
        self.darkVeilImg = pygame.image.load('Assets/buttons/dark_veil.png').convert_alpha()
        self.purple_flames_img = pygame.image.load('Assets/spells/purple_flames_btn.png').convert_alpha()
        self.buyImg = pygame.image.load('Assets/buttons/buy.png').convert_alpha()
        self.bomb_img = pygame.image.load('Assets/items/bomb_btn.png').convert_alpha()
        self.broccoli_img = pygame.image.load('Assets/items/broccoli_btn.png').convert_alpha()
        self.purple_banana_img = pygame.image.load('Assets/items/purple_banana_btn.png').convert_alpha()
        self.sus_liquid_img = pygame.image.load('Assets/items/sus_liquid_btn.png').convert_alpha()
        self.browse_spells_img = pygame.image.load('Assets/buttons/browse_spells.png').convert_alpha()
        self.browse_items_img = pygame.image.load('Assets/buttons/browse_items.png').convert_alpha()
        self.punch_img = pygame.image.load('Assets/attacks/punch_btn.png').convert_alpha()
        self.pierce_img = pygame.image.load('Assets/attacks/pierce_btn.png').convert_alpha()

        self.shopMenu_purpleFlames = pygame.image.load('Assets/spells/shopMenu_purpleFlames.png').convert_alpha()

class Button:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False
        self.over = False
    
    def draw(self, win):
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
    def drawBtn(self, win):
        win.blit(self.image, (self.rect.x, self.rect.y))
    def highLightBtn(self, win):
        hover_sound = mixer.Sound('Assets/sounds/hover_sound.mp3')
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            win.blit(self.image, (self.rect.x, self.rect.y))
            #hover_sound.play()

    def hover(self, target, win):
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