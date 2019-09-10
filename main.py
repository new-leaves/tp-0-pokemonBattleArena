import pygame
from pygame.locals import *
import time
from tkinter import *
from tkinter import messagebox

#Import here.
#FIX ME.

winSize = (600, 400)

def initMain():
    #Pokemons
    
    #Trainers
    
    #Afficher pokemons du trainer1;
    
    #Choisir pok1 et pok2.
     
    return trainer1, trainer2, pok1, pok2

class SpellMenu(pygame.sprite.DirtySprite):

    def __init__(self):
        pygame.sprite.DirtySprite.__init__(self)

        tmp = pygame.image.load("img/spellMenu.png").convert()   
        self.image = pygame.transform.scale(tmp, (winSize[0], 115))
        self.rect = self.image.get_rect(x=0, y=285)
        self.isActivated = True

    def update(self):
        self.dirty = 1
        if not self.isActivated: #Remove sprite.
            self.image.set_alpha(0)
        else:
            self.image.set_alpha(255)

class PokemonMenu(pygame.sprite.DirtySprite):

    def __init__(self):
        pygame.sprite.DirtySprite.__init__(self)

        tmp = pygame.image.load("img/pokemonMsg.png").convert()   
        self.image = pygame.transform.scale(tmp, (winSize[0], 115))
        self.rect = self.image.get_rect(x=0, y=285)
        self.isActivated = True

    def update(self):
        self.dirty = 1
        if not self.isActivated: #Remove sprite.
            self.image.set_alpha(0)
        else:
            self.image.set_alpha(255)

class PokemonSprite(pygame.sprite.DirtySprite):

    def __init__(self, name, pos):
        pygame.sprite.DirtySprite.__init__(self)

        self.name = name
        self.pos = pos

        tmp = pygame.image.load("img/pokemon/{}.png".format(name)).convert()
        self.image = pygame.transform.scale(tmp, (150, 150))
        self.rect = self.image.get_rect(x=self.pos[0], y=self.pos[1])   
        self.isActivated = True

    def update(self):
        self.dirty = 1

        if not self.isActivated: #Remove sprite.
            self.image.set_alpha(0)
        else:
            self.image.set_alpha(255)

def drawRect(screen, left, top, width, height):
    """  
        Returns a pygame rectangle.
        :param 'screen': pygame surface.
        :param 'left': integer, x coordinate.
        :param 'top': integer, y coordinate.
        :param 'width': integer, screen width.
        :param 'height': integer, screen height.
    """
    return pygame.draw.rect(screen, (255, 255, 255), 
                            pygame.Rect(left, top, width, height), 1)

def displaySpellText(screen, pok, myFont, mouse_pos, selection):
    """
        Displays on the screen pokemon spells.
    """
    #Pokemon spells.
    rectSpell1 = drawRect(screen, 30, 300, 140, 35)
    rectSpell2 = drawRect(screen, 30, 360, 140, 30)
    rectSpell3 = drawRect(screen, 190, 300, 140, 35)
    rectSpell4 = drawRect(screen, 190, 360, 140, 30)

    n = len(pok.listSpell)

    for i in range(n):
    
        text = myFont.render(pok.listSpell[i][0], False, (0, 0, 0))

        if i == 0:
            screen.blit(text, (30, 310))
        elif i == 1:
            screen.blit(text, (30, 360))
        elif i == 2: 
            screen.blit(text, (205, 310))
        else:
            screen.blit(text, (205, 360))

    tmp = None

    if rectSpell1.collidepoint(mouse_pos):
        tmp = 0
    elif rectSpell2.collidepoint(mouse_pos):
        tmp = 1
    elif rectSpell3.collidepoint(mouse_pos):
        tmp = 2
    elif rectSpell4.collidepoint(mouse_pos):
        tmp = 3
    
    if tmp is not None:
        #Sound Effect.
        selection.play()

        spell1 = pok.listSpell[tmp][0]
        
        spellIsChoosen = True

        return spellIsChoosen, spell1

    return False, None

def healthBar(screen, hpMax, newHp, isPok1):
    
    if newHp > hpMax * 0.5:
        colorBar = (0, 128, 0)
    elif newHp > hpMax * 0.25:
        colorBar = (255, 165, 0)
    else: 
        colorBar = (255, 0, 0)
    
    tmp = (newHp * 120) // hpMax
    
    if newHp > 0:
        if isPok1:
            pygame.draw.rect(screen, colorBar, pygame.Rect(435, 230, tmp, 7))
        else: 
            pygame.draw.rect(screen, colorBar, pygame.Rect(130, 82, tmp, 7))
    else:
        if isPok1:
            pygame.draw.rect(screen, colorBar, pygame.Rect(435, 230, 0, 7))
        else:
            pygame.draw.rect(screen, colorBar, pygame.Rect(130, 82, 0, 7))

def main():
    #Avoid crashing the game while picking the character.
    begin = False
    #Initializing everything.
    screen = pygame.display.set_mode(winSize)
    pygame.display.set_caption("Pokemon Battle Arena")
    clock = pygame.time.Clock()
    
    #Music.
    pygame.mixer.pre_init(buffer=2048)
    pygame.mixer.init()
    pygame.init()
    pygame.mixer.music.load('music/battleTheme.ogg')
    pygame.mixer.music.play(-1, 0.0)

    selection = pygame.mixer.Sound('music/selection.wav')
    hitDamage = pygame.mixer.Sound('music/hitDamage.wav')
    faintNoHp = pygame.mixer.Sound('music/faintNoHp.wav')
             
    #Police Font.
    pygame.font.init()
    myFont12 = pygame.font.SysFont('PKMN RBYGSC', 12)
    myFont15 = pygame.font.SysFont('PKMN RBYGSC', 15)

    #Create the background used to restore sprite previous location.
    background = pygame.Surface(screen.get_size())
    background = background.convert()

    s = "img/background.png"
    tmp = pygame.transform.scale(pygame.image.load(s), winSize)
    background.blit(tmp, (0, 0))
    screen.blit(background, (0, 0))

    trainer1, trainer2, pok1, pok2 = initMain()

    #Create the sprites.
    spellMenuImg =  SpellMenu()
    pokemonMsgImg = PokemonMenu()
    pok1Sprite = PokemonSprite(pok1.name, (90, 145))
    pok2Sprite = PokemonSprite(pok2.name, (370, 25)) 

    #Grouping the sprites. 
    mySprites =  pygame.sprite.LayeredDirty()
    mySprites.add(pok1Sprite, pok2Sprite, spellMenuImg, pokemonMsgImg)

    #Draw Everything.
    #Select only areas of the screen that need re-rendering.
    dirtyRects = mySprites.draw(screen)
    pygame.display.update(dirtyRects)     

    #Tells where to clean.
    mySprites.clear(screen, background)
    
    pokemonMsgImg.isActivated = False
    spellMenuImg.isActivated = False
    menuBack = True
    alreadyClicked = False
    rectFightClicked = False
    spellIsChoosen = False
    
    while trainer1.nbPokemon > 0 and trainer2.nbPokemon > 0:
              
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            #Go back in menu.
            if event.type == KEYDOWN and event.key == K_b:
                #Sound Effect.
                selection.play() 

                pokemonMsgImg.isActivated = False
                spellMenuImg.isActivated = False
                menuBack, alreadyClicked, rectFightClicked =  True, False, False
            
            if begin and event.type == MOUSEBUTTONDOWN:

                mouse_pos = event.pos 
                                   
                if rectPokemon.collidepoint(mouse_pos) and not alreadyClicked:

                    #Sound Effect.
                    selection.play()

                    #Switch pokemon.
                    trainer1.displayTeamPokemon()
                    pok1 = trainer1.choosePokemon()
                    
                    mySprites.remove(pok1Sprite)
                    pok1Sprite = PokemonSprite(pok1.name, (90, 145))
                    mySprites.add(pok1Sprite)

                    #Display Pokemon name.
                    text = myFont15.render(pok1.name, False, (0, 0, 0))
                    screen.blit(text, (360, 200))

                    #If switch, bot should attack.
                    spell2 = trainer2.chooseSpell(pok2)
                    type2, burst2 = pok2.attackPokemon(spell2)
                    pok1.takeDamage(type2, burst2, pok2)
                    
                    #Sound Effect.
                    hitDamage.play()
                    
                    #Display health bar
                    healthBar(screen, pok1.maxHp, pok1.hp, isPok1 = True) 
                    healthBar(screen, pok2.maxHp, pok2.hp, isPok1 = False) 
                    
                    #Display Pokemon hp.
                    text = myFont15.render(str(pok1.hp), False, (0, 0, 0))
                    screen.blit(text, (455, 242))    
                
                    text = myFont15.render(str(pok1.maxHp), False, (0, 0, 0))
                    screen.blit(text, (520, 242))
        
                    if pok1.isKo():
                        #Sound Effect.
                        faintNoHp.play()

                        #Switch pokemon.
                        trainer1.deletePokemon(pok1)

                        if trainer1.nbPokemon > 0:
                            trainer1.displayTeamPokemon()
                            pok1 = trainer1.choosePokemon()  
                            
                            mySprites.remove(pok1Sprite)
                            pok1Sprite = PokemonSprite(pok1.name, (90, 145))
                            mySprites.add(pok1Sprite)
            
                if rectFight.collidepoint(mouse_pos) and not alreadyClicked:
                    menuBack, alreadyClicked = False, True

                    #Sound Effect.
                    selection.play()
                    
                    #Show spell menu.
                    spellMenuImg.isActivated = True
                    pokemonMsgImg.isActivated = False
                    
                    #Display spell text.
                    rectFightClicked = True
        
        mySprites.update()
        dirtyRects= mySprites.draw(screen)
     
        #Draw all rectangles here.

        #Display Pokemon name.
        text = myFont15.render(pok1.name, False, (0, 0, 0))
        screen.blit(text, (360, 200))

        text = myFont15.render(pok2.name, False, (0, 0, 0))
        screen.blit(text, (50, 50))
        
        #Display health bar
        healthBar(screen, pok1.maxHp, pok1.hp, isPok1 = True) 
        healthBar(screen, pok2.maxHp, pok2.hp, isPok1 = False) 

        #Display Pokemon hp.
        text = myFont15.render(str(pok1.hp), False, (0, 0, 0))
        screen.blit(text, (455, 242))    
    
        text = myFont15.render(str(pok1.maxHp), False, (0, 0, 0))
        screen.blit(text, (520, 242))

        if menuBack:
            #Fight button
            rectFight = drawRect(screen, 335, 300, 110, 40)

            #Pokemon button
            rectPokemon = drawRect(screen, 335, 345, 120, 35)
            
            #Message
            screen.blit(myFont15.render("Que doit faire", False,
                                (255, 255, 255)), (40, 315))
        
            screen.blit(myFont15.render(pok1.name + " ?", False, 
                                (255, 255, 255)), (40, 345))
        
        if rectFightClicked:
            spellIsChoosen, spell1 = displaySpellText(screen, 
                                        pok1, myFont15, mouse_pos, selection)
            if spellIsChoosen:
                spell2 = trainer2.chooseSpell(pok2)
                
                if pok1.speed > pok2.speed:
                    fastestPok, slowestPok = pok1, pok2
                    fastestSpell, slowestSpell = spell1, spell2
                    firstTrainer, secondTrainer = trainer1, trainer2
                else:
                    fastestPok, slowestPok = pok2, pok1
                    fastestSpell, slowestSpell = spell2, spell1
                    firstTrainer, secondTrainer = trainer2, trainer1
                
                #Fastest pokemon attack.
                typeTmp, burstTmp = fastestPok.attackPokemon(fastestSpell)
                slowestPok.takeDamage(typeTmp, burstTmp, fastestPok)
                
                #Sound Effect.
                hitDamage.play()

                spellMenuImg.isActivated = False
                pokemonMsgImg.isActivated = True
            
                mySprites.update()
                dirtyRects = mySprites.draw(screen)
                
                #Display pokemons name.
                text = myFont15.render(pok1.name, False, (0, 0, 0))
                screen.blit(text, (360, 200))

                text = myFont15.render(pok2.name, False, (0, 0, 0))
                screen.blit(text, (50, 50))
                
                #Display fastest pokemon attack message.
                msg = "{}   utilise   {} ! ".format(fastestPok.name, fastestSpell)
            
                screen.blit(myFont15.render(msg, False,(255, 255, 255)),
                            (40, 330))
                #Update slowest pokemon hp bar.

                if slowestPok is pok1:
                    isPok1 = True
                    pok1.hp = slowestPok.hp
                    pok2.hp = fastestPok.hp

                else:
                    isPok1 = False
                    pok1.hp = fastestPok.hp
                    pok2.hp = slowestPok.hp

                healthBar(screen, slowestPok.maxHp, slowestPok.hp, isPok1) 
                healthBar(screen, fastestPok.maxHp, fastestPok.hp, not isPok1) 

                if pok1.hp < 0:
                    tmp = 0
                else:
                    tmp = pok1.hp

                text = myFont15.render(str(tmp), False, (0, 0, 0))
                screen.blit(text, (455, 242)) 
                
                text = myFont15.render(str(pok1.maxHp), False, (0, 0, 0))
                screen.blit(text, (520, 242))

                pygame.display.update(dirtyRects)
                time.sleep(1)
            
                if slowestPok.isKo():
                    #Sound Effect.
                    faintNoHp.play()

                    #Switch pokemon.
                    secondTrainer.deletePokemon(slowestPok)

                    if secondTrainer is trainer1:
                        secondTrainer.displayTeamPokemon()

                    if secondTrainer.nbPokemon > 0:
                        slowestPok = secondTrainer.choosePokemon()

                        if secondTrainer is trainer1:
                            pok1 = slowestPok
                            
                            #Display Pokemon sprite.
                            mySprites.remove(pok1Sprite)
                            pok1Sprite = PokemonSprite(pok1.name, (90, 145))
                            mySprites.add(pok1Sprite)
                          
                            #Display Pokemon name.
                            text = myFont15.render(pok1.name, False, (0, 0, 0))
                            screen.blit(text, (360, 200))

                        else:
                            pok2 = slowestPok

                            #Display Pokemon sprite.
                            mySprites.remove(pok2Sprite)
                            pok2Sprite = PokemonSprite(pok2.name, (370, 25))
                            mySprites.add(pok2Sprite)

                            #Display Pokemon name.
                            text = myFont15.render(pok2.name, False, (0, 0, 0))
                            screen.blit(text, (50, 50))
                else:
                    #Slowest pokemon attack.
                    typeTmp, burstTmp = slowestPok.attackPokemon(slowestSpell)
                    fastestPok.takeDamage(typeTmp, burstTmp, slowestPok)
                    
                    #Sound Effect.
                    hitDamage.play()
                    
                    mySprites.update()
                    dirtyRects = mySprites.draw(screen)
                    
                    #Display pokemons name.
                    text = myFont15.render(pok1.name, False, (0, 0, 0))
                    screen.blit(text, (360, 200))

                    text = myFont15.render(pok2.name, False, (0, 0, 0))
                    screen.blit(text, (50, 50))

                    #Display slowest pokemon message.
                    msg = "{}   utilise   {} ! ".format(slowestPok.name, slowestSpell)
     
                    screen.blit(myFont15.render(msg, False, (255, 255, 255)), 
                                (40, 330))
                    
                    #Update fastest pokemon hp bar.
                    if fastestPok is pok1:
                        isPok1 = True
                        pok1.hp = fastestPok.hp
                        pok2.hp = slowestPok.hp
                    else:
                        isPok1 = False
                        pok1.hp = slowestPok.hp
                        pok2.hp = fastestPok.hp
                    
                    healthBar(screen, fastestPok.maxHp, fastestPok.hp, isPok1)
                    healthBar(screen, slowestPok.maxHp, slowestPok.hp, not isPok1) 

                    if pok1.hp < 0:
                        tmp = 0 
                    else:
                        tmp = pok1.hp
                        
                    text = myFont15.render(str(tmp), False, (0, 0, 0))
                    screen.blit(text, (455, 242))

                    text = myFont15.render(str(pok1.maxHp), False, (0, 0, 0))
                    screen.blit(text, (520, 242))

                    pygame.display.update(dirtyRects)
                    time.sleep(1)                 
                    
                    if fastestPok.isKo():
                        #Sound Effect.
                        faintNoHp.play()

                        #Switch pokemon.
                        firstTrainer.deletePokemon(fastestPok)

                        if firstTrainer is trainer1:
                            firstTrainer.displayTeamPokemon()

                        if firstTrainer.nbPokemon > 0:
                            fastestPok = firstTrainer.choosePokemon()

                            if firstTrainer is trainer1:
                                pok1 = fastestPok 
                                
                                #Display Pokemon sprite.
                                mySprites.remove(pok1Sprite)
                                pok1Sprite = PokemonSprite(pok1.name, (90, 145))
                                mySprites.add(pok1Sprite)
                              
                                #Display Pokemon name.
                                text = myFont15.render(pok1.name, False, (0, 0, 0))
                                screen.blit(text, (360, 200))

                            else:
                                pok2 = fastestPok 

                                #Display Pokemon sprite.
                                mySprites.remove(pok2Sprite)
                                pok2Sprite = PokemonSprite(pok2.name, (370, 25))
                                mySprites.add(pok2Sprite)

                                #Display Pokemon name.
                                text = myFont15.render(pok2.name, False, (0, 0, 0))
                                screen.blit(text, (50, 50))

                
                rectFightClicked, menuBack, alreadyClicked = False, True, False
                pokemonMsgImg.isActivated = False
                spellMenuImg.isActivated = False
        
        begin = True
        clock.tick(18)
        pygame.display.update(dirtyRects)
       
    if trainer1.nbPokemon == 0:
        Tk().withdraw() #to hide the main window
        messagebox.showinfo('Continue','YOU LOSE!')
    else:
        pygame.mixer.music.load('music/victory.ogg')
        pygame.mixer.music.play(-1, 0.0)

        Tk().withdraw() #to hide the main window
        messagebox.showinfo('Continue','YOU WIN !')

main()
