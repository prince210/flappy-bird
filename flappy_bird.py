import pygame,sys,random

isOpen = True
pygame.init()
screen = pygame.display.set_mode((576,600))
clock = pygame.time.Clock()   ## it is done to maintain the speed of frames per second
game_active = True
score = 0
score_font = pygame.font.Font('04B_19.TTF',25)
high_score_font = pygame.font.Font('04B_19.TTF',30)
high_score = 0
bird_wing_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
bird_die_sound = pygame.mixer.Sound('sound/sfx_die.wav')
score_update_sound = pygame.mixer.Sound('sound/sfx_point.wav')

## background and floor variables
bg_surface = pygame.image.load('assets/background-day.png').convert()   ## converts it into a type of surface that is easy to handle by pygame
                                                                        ## visualize it as a scenario when we have multiple objects in our screen
                                                                        ## then bliting anything on screen becomes slow so as to maintain its speed it is used
floor_surface = pygame.image.load('assets/base.png')
floorX = 0  ## since we want our floor to move to left so we kept descrement our floorX by 1 in our game loop


## bird variables

            ## performing animations for bird
blueBirdDown_surface = pygame.transform.scale(pygame.image.load('assets/bluebird-downflap.png'),(45,45))
blueBirdMid_surface = pygame.transform.scale(pygame.image.load('assets/bluebird-midflap.png'),(45,45))
blueBirdUp_surface = pygame.transform.scale(pygame.image.load('assets/bluebird-upflap.png'),(45,45))
bird_motions_list = [blueBirdDown_surface,blueBirdMid_surface,blueBirdUp_surface]
bird_index = 0 ## animation is just iteration through 'bird_motions_list' multiple times and 'bird_index' provides this functionality
bird_surface = bird_motions_list[bird_index]
bird_rect = bird_surface.get_rect(center = (100,150))
gravity = 0.15
bird_movement = 0
BIRDFLAP = pygame.USEREVENT + 1  ## we are creating another event so as to increase bird_index by 1 everytime
pygame.time.set_timer(BIRDFLAP,200)  ## event will occur in every 0.2 sec



## pipe variables
pipe_surface = pygame.image.load('assets/pipe-green.png').convert()
pipe_list = []
SPAWNPIPE = pygame.USEREVENT   ## it will create out user event with name SPAWNPIPE (generally event is name in uppercase letter),
                                # here we have the purpose to draw pipe based on some time

pygame.time.set_timer(SPAWNPIPE,1200)    ## now we have an event that triggred every 1.2 sec

pipe_height = [300,400,450]  ## we need our pipe of different heights


## game over display
game_over_surface = pygame.image.load('assets/message.png')


def drawFloor():
    screen.blit(floor_surface,(floorX,520))
    screen.blit(floor_surface, (floorX+576, 520))

def create_pipe():
    random_pipeY = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (700,random_pipeY))  ## get_rect is used because normal surface can be placed by only one point (i.e. top left)
                                                             ## but get_rect creates rectangle on surface and gives functionality to move pipe by multiple points
                                                             ## that is, by top-left, bottom-right,mid-top,mid-bottom or other points
    top_pipe = pipe_surface.get_rect(midbottom = (700,random_pipeY-200))
    return bottom_pipe,top_pipe

def move_pipe(pipes,score):
    for pipe in pipes:
        pipe.centerx -= 5
        if pipe.centerx == bird_rect.centerx:
            score += 1
            score_update_sound.play()
    return pipes,score

def drawPipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 600:
            screen.blit(pipe_surface,pipe)
        else:
            screen.blit(pygame.transform.flip(pipe_surface,False,True),pipe)  ## flip --> it flips the object in x or y axis or both, arg2 is flix on x, arg3 is flip on y

def check_collision(pipes):
    for pipe in pipes:
        if pipe.colliderect(bird_rect):  ## colliderect gives true if pipe collide with bird else false
            bird_die_sound.play()
            return False

        #
        if bird_rect.bottom <= 0 or bird_rect.bottom >= 520:
            bird_die_sound.play()
            return False

    return True

def rotate_bird(bird):
    return pygame.transform.rotozoom(bird,-bird_movement * 3,1)  ## provide functionality for rotation and scale arg1 is rotation angle, arg2 is scale [1 means no scale]

def animate_bird():
    new_bird = bird_motions_list[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100,bird_rect.centery))  ## 'center = (100,bird_rect.centery)' bird_rect.centery because we want rectangle on current bird that is bird_rect
    return new_bird,new_bird_rect

def display_score(score,state,high_score):
    if state == 'INGAME':
        score_surface = score_font.render('Score : '+str(score),True,(255,255,255))  ## arg2 show how sharp the image should look like
        screen.blit(score_surface,(200,80))
    if state == 'GAMEOVER':
        score_surface = score_font.render('Score : ' + str(score), True,(255, 255, 255))  ## arg2 show how sharp the image should look like
        screen.blit(score_surface, (200, 80))

        high_score_surface = high_score_font.render('High Score : ' + str(high_score), True,(255, 255, 255))  ## arg2 show how sharp the image should look like
        screen.blit(high_score_surface, (180, 470))


def update_high_score(score,high_score):
    if score > high_score:
        high_score = score
    return high_score


while isOpen:
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isOpen = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = 0
                bird_movement -= 6
                bird_wing_sound.play()
            if event.key == pygame.K_RETURN and game_active == False:
                game_active = True
                pipe_list.clear()  ## since a lot of pipe was already there when we restart the game so we need to clear that
                bird_movement = 0  ## since bird movement is already there so we need to fix that
                bird_rect.center = (100,150)
                score = 0

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0

            bird_surface,bird_rect = animate_bird()


    screen.blit(bg_surface,(0,0))

    if game_active:
        # bird
        bird_movement += gravity
        bird_rect.centery += bird_movement
        rotated_bird = rotate_bird(bird_surface)
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)

        ## pipe
        pipe_list,score = move_pipe(pipe_list,score)
        drawPipes(pipe_list)
        display_score(score//2,'INGAME',high_score)
    else:
        screen.blit(game_over_surface,(170,170))
        high_score = update_high_score(score//2,high_score)
        display_score(score//2,'GAMEOVER',high_score)

    ## floor
    floorX -= 2
    drawFloor()
    if floorX <= -576:
        floorX = 0



    clock.tick(120)   ## we are allowing a maximum of 120fps [frame per second is how fast frames are moving on the screen we need to limit that for better experience]
    pygame.display.update()

pygame.quit()