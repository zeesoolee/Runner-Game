import pygame
from sys import exit
from random import randint

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surface = text_font.render(f'Score: {current_time}',False,(64,64,64))
    score_rect = score_surface.get_rect(center = (350, 75))
    screen.blit(score_surface,score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom == 300:
                screen.blit(fireball_surface, obstacle_rect)
            else:
                screen.blit(fly_surface, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x>-50]
        return obstacle_list
    else:
        return []

def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True

def player_animation():
    global player_surface, player_index

    player_index += 0.1
    if player_index >= len(player_walk):
        player_index = 0
    player_surface = player_walk[int(player_index)]

pygame.init()
screen = pygame.display.set_mode((700,400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
text_font = pygame.font.Font(None, 20)
game_active = False
start_time = 0
score = 0

ground_surface = pygame.image.load('ground.png').convert()
sky_surface = pygame.image.load('sky.png').convert()

#Obstacles
fireball_surface = pygame.image.load('fireball1.png').convert_alpha()
fly_surface = pygame.image.load('fireball1.png').convert_alpha()

obstacle_rect_list = []

#character
player_walk1 = pygame.image.load('player_walk1.png').convert_alpha()
player_walk2 = pygame.image.load('player_walk2.png').convert_alpha()
player_walk = [player_walk1, player_walk2]
player_index = 0

player_surface = player_walk[player_index]
player_rect = player_surface.get_rect(midbottom = (75,300))
player_gravity = 0

#Intro screen
player_stand = pygame.image.load('player_stand.png').convert_alpha()
player_stand = pygame.transform.scale2x(player_stand)
player_stand_rect = player_stand.get_rect(center = (350,200))

game_name = text_font.render('Run 2 Live', False, 'Black')
game_name_rect = game_name.get_rect(center = (350,55))

game_message = text_font.render('Press space to run', False, 'Black')
game_message_rect = game_message.get_rect(center = (350,345))

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN and player_rect.bottom >=300:
                player_gravity = -20
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >=300:
                    player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)
        if event.type == obstacle_timer and game_active:
            if randint(0,2):
                obstacle_rect_list.append(fireball_surface.get_rect(bottomleft = (randint(700,900),300)))
            else:
                obstacle_rect_list.append(fly_surface.get_rect(bottomleft = (randint(700,900),200)))

    if game_active:
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))

        score = display_score()
        
        #fireball_rect.x -= 4
        #if fireball_rect.right <= 0:
         #   fireball_rect.left = 700
        #screen.blit(fireball_surface,fireball_rect)

        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300:
            player_rect.bottom = 300
        player_animation()
        screen.blit(player_surface,player_rect)

        #obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        #collisions
        game_active = collisions(player_rect,obstacle_rect_list)

    else:
        screen.fill('Beige')
        screen.blit(player_stand,player_stand_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (75,300)
        player_gravity = 0

        score_message = text_font.render(f'Your score: {score}', False, 'Black')
        score_message_rect = score_message.get_rect(center = (150,200))
        screen.blit(game_name,game_name_rect)

        if score == 0:
            screen.blit(game_message,game_message_rect)
        else:
            screen.blit(score_message,score_message_rect)
            screen.blit(game_message,game_message_rect)


    pygame.display.update()
    clock.tick(60) 