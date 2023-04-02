import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
        player_walk_2 = pygame.image.load("graphics/player/player_walk_2.png").convert_alpha()
        self.player_walk = [player_walk_1,player_walk_2]
        self.player_index = 0
        self.player_jump =  pygame.image.load("graphics/player/jump.png").convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80,300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.5)
    
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.jump_sound.play()
            self.gravity = -20

    def apply_gravity(self):
        self.gravity +=1
        self.rect.y += self.gravity
        if self.rect.bottom >=300:
            self.rect.bottom = 300

    def animation_stat(self):
        if self.rect.bottom <300:
            self.image = self.player_jump
        else:
            self.player_index+=0.1
            if self.player_index>= len(self.player_walk):self.player_index=0
            self.image = self.player_walk[int(self.player_index)]
    
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_stat()
    

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()

        if type == 'fly':
            fly_1 = pygame.image.load("graphics/Fly/Fly1.png").convert_alpha()
            fly_2 = pygame.image.load("graphics/Fly/Fly2.png").convert_alpha()
            self.frames = [fly_1,fly_2]
            y_pos = 210
        else:
            snail_1 = pygame.image.load("graphics/snail1.png").convert_alpha()
            snail_2 = pygame.image.load("graphics/snail2.png").convert_alpha()
            self.frames = [snail_1,snail_2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))

    def animation_state(self):
        self.animation_index +=0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()
    
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


def display_score():
    current_time = int(pygame.time.get_ticks()/1000) - start_time
    score_surf = test_font.render(f'Score: {current_time}', False,(64,64,64))
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf,score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom==300:
                screen.blit(snail_surface,obstacle_rect)  
            else:
                screen.blit(fly_surface,obstacle_rect)

        obstacle_list =[obstacle for obstacle in obstacle_list if obstacle.x >-100]

        return obstacle_list
    else:return[]

def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True

def collison_sprite():
    if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
        obstacle_group.empty()
        return False
    else: return True

def player_animation():
    global player_surf, player_index

    if player_rect.bottom < 300:
        #jump
        player_surf = player_jump
    else:
        #walk
        player_index+=0.1
        if player_index >= len(player_walk): player_index=0
        player_surf = player_walk[int(player_index)]
    #play walking animation if the player is on floor
    #dispal the jump surface when player in not on the floor


pygame.init()#inicjalizacja

size = HEIGHT, WEIGHT = 800, 400 #rozmiar okna

screen = pygame.display.set_mode(size)#ustawienie okna
pygame.display.set_caption("Just Learning") #ustawienie tytułu aplikacji
clock = pygame.time.Clock()
test_font = pygame.font.Font("font/Pixeltype.ttf",50)
game_active = False
start_time = 0
score =0
bg_Music = pygame.mixer.Sound('audio/music.wav')
bg_Music.play(loops = -1)
bg_Music.set_volume(0.2)

#Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

#test_surface = pygame.Surface((50,50))
#test_surface.fill("Blue")
sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

#score_surface = test_font.render("My first game", False, (64,64,64))
#score_rect = score_surface.get_rect(center=(400,50))

#Obstacles
snail_frame_1 = pygame.image.load("graphics/snail1.png").convert_alpha()
snail_frame_2 = pygame.image.load("graphics/snail2.png").convert_alpha()
snail_frames = [snail_frame_1,snail_frame_2]
snail_frame_index = 0
snail_surface = snail_frames[snail_frame_index]

#snail_rect = snail_surface.get_rect(bottomright = (300,300))
fly_frame_1 = pygame.image.load("graphics/Fly/Fly1.png").convert_alpha()
fly_frame_2 = pygame.image.load("graphics/Fly/Fly2.png").convert_alpha()
fly_frames = [fly_frame_1,fly_frame_2]
fly_frame_index = 0
fly_surface = fly_frames[fly_frame_index]

obstacle_rect_list = []

player_walk_1 = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
player_walk_2 = pygame.image.load("graphics/player/player_walk_2.png").convert_alpha()
player_walk = [player_walk_1,player_walk_2]
player_index = 0
player_jump =  pygame.image.load("graphics/player/jump.png").convert_alpha()

player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom = (80, 300))
player_gravity = 0

#intro screen
player_stand = pygame.image.load("graphics/player/player_stand.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center =(400,200))

game_name = test_font.render("Pixel Runner", False,(111,196,169))
name_rect = game_name.get_rect(center = (400,80))

instruction = test_font.render("Press SPACE to start", False, (111,196,169))
instruction_rect = instruction.get_rect(center =(400, 330))


#Timer
obstacle_timer = pygame.USEREVENT +1
pygame.time.set_timer(obstacle_timer,1400)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer,500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer,200)

while True:
    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
            pygame.quit()
            exit()
    
        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom == 300:
                        player_gravity = -20 

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom == 300:
                    player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_active = True
                    #snail_rect.left = 800
                    start_time = int(pygame.time.get_ticks()/1000)
        if game_active:
            if event.type==obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly','snail','snail','snail'])))
                #if randint(0,2):
                #    obstacle_rect_list.append(snail_surface.get_rect(bottomright = (randint(900,1100),300)))
                #else:
                #    obstacle_rect_list.append(fly_surface.get_rect(bottomright = (randint(900,1100),210)))
            
            if event.type == snail_animation_timer:
                if snail_frame_index== 0: snail_frame_index =1
                else: snail_frame_index=0
                snail_surface = snail_frames[snail_frame_index]
            if event.type == fly_animation_timer:
                if fly_frame_index== 0: fly_frame_index =1
                else: fly_frame_index=0
                fly_surface = fly_frames[fly_frame_index]



    if game_active:
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))

        #pygame.draw.rect(screen, '#c0e8ec', score_rect)
        #pygame.draw.rect(screen, '#c0e8ec', score_rect, 10)
        #screen.blit(score_surface, score_rect)

        score = display_score()

        #pygame.draw.ellipse(screen, 'brown', pygame.Rect(50,200,100,100))
        #pygame.draw.line(screen, 'black',(0,0),pygame.mouse.get_pos(),3)

        #Basic snail movement
        #snail_rect.x -= 5
        #if snail_rect.right <= 0:
        #    snail_rect.left = 800
        #screen.blit(snail_surface,snail_rect)

        #Player
        #player_gravity += 1
        #player_rect.y += player_gravity
        #if player_rect.bottom>=300:
        #    player_rect.bottom =300
        #player_animation()
        #screen.blit(player_surf,player_rect)
        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        #obstacle movement
        #obstacle_rect_list = obstacle_movement(obstacle_rect_list)
        #collision
        #game_active = collisions(player_rect,obstacle_rect_list)
        game_active = collison_sprite()

    else:
        
        screen.fill((94,129,162))
        screen.blit(player_stand,player_stand_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (80,300)
        player_gravity = 0

        score_message = test_font.render(f'Your score: {score}' ,False, (111,196,169))
        score_message_rect = score_message.get_rect(center = (400,330))
        screen.blit(game_name,name_rect)

        if score==0:
            screen.blit(instruction,instruction_rect)
        else:
            screen.blit(score_message,score_message_rect)



    pygame.display.update()
    clock.tick(60)
