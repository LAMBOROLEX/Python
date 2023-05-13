import pygame 
import random

pygame.init()

screen_width = 480
screen_height = 640
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Kevin_Shooting_Game")

clock = pygame.time.Clock()
# Background
background = pygame.image.load("JJM-main\\Image-Fusion\\Game\\Images\\background.png")

# Character
character = pygame.image.load("JJM-main\\Image-Fusion\\Game\\Images\\P_character.png")  # 1. Image
character_size = character.get_rect().size                    # 2. Collision
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width/2) - (character_width/2)      # 3. Position
character_y_pos = (screen_height) - (character_height/2)

# Enemy 
Enemy = pygame.image.load("JJM-main\\Image-Fusion\\Game\\Images\\P_Enemy.png")  # 1. Image
Enemy_size = Enemy.get_rect().size                    # 2. Collision

enemy_images = [
    pygame.image.load("JJM-main\\Image-Fusion\\Game\\Images\\P_enemy.png"),
    pygame.image.load("JJM-main\\Image-Fusion\\Game\\Images\\P_enemy_2.png"),
    pygame.image.load("JJM-main\\Image-Fusion\\Game\\Images\\P_enemy_3.png")
]

enemies = []

enemy_speed_y = 2

enemies.append({
    "pos_x" : random.randint(0, screen_width - Enemy_size[1]),
    "pos_y" : 0,
    "img_idx" : 0,
    "to_x" : random.randint(-2, 2),
    "to_y" : random.randint(1, 3)
})

# Move Character
character_to_x = 0
character_to_y = 0
character_speed = 0.5


# Time configration

total_time = 10

start_ticks = pygame.time.get_ticks()

game_font = pygame.font.Font(None, 40)

# remove bullets and enemy
bullet_to_remove = -1
enemy_to_remove = -1

# Bullet 
bullet = pygame.image.load("JJM-main\\Image-Fusion\\Game\\Images\\P_bullet.png")  # 1. Image
bullet_size = bullet.get_rect().size                    # 2. Collision
bullet_width = bullet_size[0]
bullet_height = bullet_size[1]

bullets = []
bullet_speed = 10



running = True
while running: 
    frame = clock.tick(120)  # 60 - 100 Frame Per Second 
    
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                character_to_y -= character_speed
            elif event.key == pygame.K_DOWN:
                character_to_y += character_speed
            elif event.key == pygame.K_LEFT:
                character_to_x -= character_speed
            elif event.key == pygame.K_RIGHT:
                character_to_x += character_speed
            elif event.key == pygame.K_SPACE:
                bullet_x_pos = character_x_pos
                bullet_y_pos = character_y_pos
                bullets.append([bullet_x_pos, bullet_y_pos])

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                character_to_y = 0
            elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                character_to_x = 0
 
    # Move Charactor Position
    character_x_pos += character_to_x * frame
    character_y_pos += character_to_y * frame

    # Character hitbox
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    # Move Bullets Position
    bullets = [[bul[0], bul[1] - bullet_speed] for bul in bullets]
    bullets = [[bul[0], bul[1]] for bul in bullets if bul[1] < screen_height]

    # Enemies position 
    for enemy_idx, enemy_val in enumerate(enemies) :
        enemy_x_pos = enemy_val["pos_x"] 
        enemy_y_pos = enemy_val["pos_y"]
        enemy_img_idx = enemy_val["img_idx"]
        
        enemy_size = enemy_images[enemy_img_idx].get_rect().size
        enemy_width = enemy_size[0]
        enemy_height = enemy_size[1]

        if enemy_x_pos < 0 or enemy_x_pos > screen_width - enemy_width: 
            enemy_val["to_x"] = enemy_val["to_x"] * -1 

        if enemy_y_pos < 0 or enemy_y_pos > screen_width - enemy_width: 
            enemy_val["to_y"] = enemy_val["to_y"] * -1 

        enemy_val["pos_x"] += enemy_val["to_x"]
        enemy_val["pos_y"] += enemy_val["to_y"]

    # Enemies hit boxes
    for enemy_idx, enemy_val in enumerate(enemies):
        enemy_x_pos = enemy_val["pos_x"] 
        enemy_y_pos = enemy_val["pos_y"]
        enemy_img_idx = enemy_val["img_idx"]
        
        enemy_rect = enemy_images[enemy_img_idx].get_rect()
        enemy_rect.left = enemy_x_pos
        enemy_rect.top = enemy_y_pos

        # enemy vs character 
        if character_rect.colliderect(enemy_rect):
            running = False
            game_result = "Game Over"
            break

    # enemy vs bullets
    # bullets hit boxes
    for bullet_idx, bullet_val in enumerate(bullets):
        bullet_x_pos = bullet_val[0]
        bullet_y_pos = bullet_val[1]

        bullet_rect = bullet.get_rect()
        bullet_rect.left = bullet_x_pos
        bullet_rect.top = bullet_y_pos

        # Check Collision with enemy
        if bullet_rect.colliderect(enemy_rect):
            bullet_to_remove = bullet_idx
            enemy_to_remove = enemy_idx

            # Change enemy status
            if enemy_img_idx < 2 :
                enemy_width = enemy_rect.size[0]
                enemy_height = enemy_rect.size[1]

                next_enemy_rect = enemy_images[enemy_img_idx+1].get_rect()
                next_enemy_width = next_enemy_rect.size[0]
                next_enemy_width = next_enemy_rect.size[1]

                # Enemy Change 
                enemies.append({
                    "pos_x" : random.randint(0, screen_width - Enemy_size[1]),
                    "pos_y" : enemy_y_pos,
                    "img_idx" : enemy_img_idx + 1,
                    "to_x" : random.randint(-10, -5),
                    "to_y" : enemy_speed_y * 1.5
                })
                
                enemies.append({ 
                    "pos_x" : random.randint(0, screen_width - Enemy_size[1]),
                    "pos_y" : enemy_y_pos,
                    "img_idx" : enemy_img_idx + 1,
                    "to_x" : random.randint(5, 10),
                    "to_y" : enemy_speed_y * 1.5
                }) 
            break
        else: 
            continue 
        break 

    if enemy_to_remove > -1 : 
        del enemies[enemy_to_remove]
        enemy_to_remove = -1

    if bullet_to_remove > -1 :
        del bullets[bullet_to_remove]
        bullet_to_remove = -1
           
    # Control Escaped from Window
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width :
        character_x_pos = screen_width - character_width
    if character_y_pos < 0:
        character_y_pos = 0
    elif character_y_pos > screen_height - character_height :
        character_y_pos = screen_height - character_height
    
    # Character Hit Box
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    
    #Enemy Hit Box
    Enemy_rect = Enemy.get_rect()
    Enemy_rect.left = enemy_x_pos
    Enemy_rect.top = enemy_y_pos

    if character_rect.colliderect(Enemy_rect):
        print("Collider!")
        running = False
    
    # Rendering
    screen.blit(background, (0, 0))

    for idx, val in enumerate(enemies): 
        enemy_x_pos = val["pos_x"]
        enemy_y_pos = val["pos_y"]
        enemy_img_idx = val["img_idx"]
        screen.blit(enemy_images[enemy_img_idx], (enemy_x_pos, enemy_y_pos))

    screen.blit(character, (character_x_pos, character_y_pos))

    for bullet_x_pos, bullet_y_pos in bullets:
        screen.blit(bullet, (bullet_x_pos, bullet_y_pos))    
    
    # Timer Rendering
    past_time = (pygame.time.get_ticks() - start_ticks) / 1000 # sec
    timer = game_font.render(str(round((total_time - past_time), 2)), True, (255, 255, 255))
    screen.blit(timer, (10, 10))

    if total_time - past_time <= 0 :
        running = False
    pygame.display.update()


# Quit Game
pygame.time.delay(2000) # 2 sec delay
pygame.quit()