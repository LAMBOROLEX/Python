import pygame 

pygame.init()

screen_width = 480
screen_height = 640
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Kevin_Shooting_Game")

# Background
background = pygame.image.load("Game\\Images\\background.png")

# Character
character = pygame.image.load("Game\\Images\\character.png")  # 1. Image
character_size = character.get_rect().size                    # 2. Collision
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width/2) - (character_width/2)      # 3. Position
character_y_pos = (screen_height/2) - (character_height/2)

# Move Character
character_to_x = 0
character_to_y = 0

running = True
while running: 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                character_to_y -= 5
            elif event.key == pygame.K_DOWN:
                character_to_y += 5
            elif event.key == pygame.K_LEFT:
                character_to_x -= 5
            elif event.key == pygame.K_RIGHT:
                character_to_x += 5

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                character_to_y = 0
            elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                character_to_x = 0

    character_x_pos += character_to_x
    character_y_pos += character_to_y

    # Control Escaped from Window
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width :
        character_x_pos = screen_width - character_width
    if character_y_pos < 0:
        character_y_pos = 0
    elif character_y_pos > screen_height - character_height :
        character_y_pos = screen_height - character_height
    
    
    
    
    screen.blit(background, (0, 0))
    screen.blit(character, (character_x_pos, character_y_pos))
    pygame.display.update()

pygame.quit()