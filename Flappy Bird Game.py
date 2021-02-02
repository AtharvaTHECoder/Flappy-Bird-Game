import pygame,sys,random

def draw_floor():
    screen.blit(floorSur,(floorXPos,450))
    screen.blit(floorSur,(floorXPos + 288,450))

def create_pipe():
    randomPipePos = random.choice(pipeHieght)
    bottomPipe = pipeSur.get_rect(midtop = (350,randomPipePos))
    topPipe = pipeSur.get_rect(midbottom = (350,randomPipePos - 150))
    return bottomPipe,topPipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 512:
            screen.blit(pipeSur,pipe)
        else:
            flipPipe = pygame.transform.flip(pipeSur,False,True)
            screen.blit(flipPipe,pipe)

def check_collision(pipes):
    for pipe in pipes:
       if birdRect.colliderect(pipe):
           hitSound.play()
           return False
        

    if birdRect.top <= -50 or birdRect.bottom >= 450:
        return False

    return True
               
def rotate_Bird(bird):
    newBird = pygame.transform.rotozoom(bird,-birdMove * 2,1)  
    return newBird 

def bird_animation():
    newBird = birdFrames[birdIndex]
    newBirdRect = newBird.get_rect(center = (50,birdRect.centery))
    return newBird,newBirdRect

def score_display(game_state):
    if game_state == 'main_game':
        scoreSur = gameFont.render(str(int(score)),True,(255,255,255)) 
        scoreRect = scoreSur.get_rect(center = (144,30))
        screen.blit(scoreSur,scoreRect)

    if game_state == 'game_over':
        scoreSur = gameFont.render(f'Score: {int(score)}',True,(255,255,255)) 
        scoreRect = scoreSur.get_rect(center = (144,30))
        screen.blit(scoreSur,scoreRect)


        highScoreSur = gameFont.render(f'High Score: {int(highscore)}',True,(255,255,255)) 
        highScoreRect = scoreSur.get_rect(center = (105,470))
        screen.blit(highScoreSur,highScoreRect)

def update_score(score,highscore):
    if score > highscore:
        highscore = score
    return highscore


pygame.mixer.pre_init()
pygame.init()
screen = pygame.display.set_mode((288,512))
clock = pygame.time.Clock()
gameFont = pygame.font.SysFont('jokerman',35)

gravity = 0.25
birdMove = 0
gameActive = True
score = 0
highscore = 0

floorSur = pygame.image.load('assets/base.png')
floorXPos = 0

bgsur = pygame.image.load('assets/background-day.png').convert()
gameOverSur = pygame.image.load('assets/message.png').convert_alpha()
gameOverRect = gameOverSur.get_rect(center = (144,256))


birdDown = pygame.image.load('assets/bluebird-downflap.png').convert_alpha()
birdMid = pygame.image.load('assets/bluebird-midflap.png').convert_alpha() 
birdUp = pygame.image.load('assets/bluebird-upflap.png').convert_alpha()
birdFrames = [birdDown,birdMid,birdUp]
birdIndex = 2
birdSur = birdFrames[birdIndex]
birdRect = birdSur.get_rect(center = (50,256))
BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP,200)



pipeSur = pygame.image.load('assets/pipe-green.png')
pipeList = []
SPAWNPIPE = pygame.USEREVENT
pipeHieght = [200,300,400]
pygame.time.set_timer(SPAWNPIPE,1000)


flapSound = pygame.mixer.Sound('sound/sfx_wing.wav')
pointSound = pygame.mixer.Sound('sound/sfx_point.wav')
pointSoundCountd = 65

hitSound = pygame.mixer.Sound('sound/sfx_hit.wav')


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and gameActive:
                birdMove = 0
                birdMove -= 7
                flapSound.play()
            if event.key == pygame.K_SPACE and gameActive == False:
                gameActive = True
                pipeList.clear()
                birdRect.center = 50,256
                birdMove = 0
                score = 0

        if event.type == SPAWNPIPE:
            pipeList.extend(create_pipe())

        if event.type == BIRDFLAP:
            if birdIndex < 2:
                birdIndex += 1
            else:
                birdIndex = 0

            birdSur,birdRect = bird_animation()

    screen.blit(bgsur,(0,0))    

    if gameActive:
        
       
        birdMove += gravity
        rotatedBird = rotate_Bird(birdSur)
        birdRect.centery += birdMove
        screen.blit(rotatedBird,birdRect)
        gameActive = check_collision(pipeList)

        

        pipeList = move_pipes(pipeList)
        draw_pipes(pipeList)
        score += 0.017
        score_display('main_game')
        pointSoundCountd -= 1
        if pointSoundCountd <= 0:
            pointSound.play()
            pointSoundCountd = 65


        draw_floor()
        floorXPos -= 1
        if floorXPos <= -288:
            floorXPos = 0

    else:
        screen.blit(gameOverSur,gameOverRect)
        highscore = update_score(score,highscore)
        score_display('game_over')
        score = 0
        
    

    pygame.display.update()
    clock.tick(60)  