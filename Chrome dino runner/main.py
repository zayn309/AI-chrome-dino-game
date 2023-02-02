from contextlib import nullcontext
import os
import random
import math
import neat
import pygame


pygame.init()
pygame.font.init()

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100

TRACK_POS = 381
FPS = 60


POINTS_FONT = pygame.font.SysFont('calibri', 30)


Ico = pygame.image.load("assets/DinoWallpaper.png")
pygame.display.set_icon(Ico)

RUNNING = [
    pygame.image.load(os.path.join("assets/Dino", "DinoRun1.png")),
    pygame.image.load(os.path.join("assets/Dino", "DinoRun2.png")),
]

JUMPING = pygame.image.load(os.path.join("assets/Dino", "DinoJump.png"))

DUCKING = [
    pygame.image.load(os.path.join("assets/Dino", "DinoDuck1.png")),
    pygame.image.load(os.path.join("assets/Dino", "DinoDuck2.png")),
]

CACTUS = [
    pygame.image.load(os.path.join("assets/Cactus", "LargeCactus1.png")),
    pygame.image.load(os.path.join("assets/Cactus", "LargeCactus2.png")),
    pygame.image.load(os.path.join("assets/Cactus", "LargeCactus3.png")),
    pygame.image.load(os.path.join("assets/Cactus", "SmallCactus1.png")),
    pygame.image.load(os.path.join("assets/Cactus", "SmallCactus2.png")),
    pygame.image.load(os.path.join("assets/Cactus", "SmallCactus3.png")),
]

BIRD = [
    pygame.image.load(os.path.join("assets/Bird", "Bird1.png")),
    pygame.image.load(os.path.join("assets/Bird", "Bird2.png")),
]

CLOUD = pygame.image.load(os.path.join("assets/Other", "Cloud.png"))

TRACK = pygame.image.load(os.path.join("assets/Other", "Track.png"))


WHITE = (255,255,255)

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class Dinosaur:

    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8
    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False
        self.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
    def action(self):
        if self.step_index >= 20:
            self.step_index = 0
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump :
            self.jump()
    def make_jump(self):
        if not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
    def make_duck(self):
        if not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
    def update(self):
        if not (self.dino_jump or self.dino_duck):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False
        
        
    def run(self):
        self.image = self.run_img[self.step_index // 10]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1
        if self.step_index >=20:
            self.step_index = 0

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel *2.5
            self.jump_vel -= 0.5
        if self.jump_vel < -self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL
            
    def duck(self):
        self.image = self.duck_img[self.step_index // 10]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1
        self.dino_duck = False
        if self.step_index >=20:
            self.step_index = 0


    def get_image(self):
        return self.image

    def draw(self, SCREEN,bird,cactus):
        global CACTUS_ON,BIRD_ON
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))
        pygame.draw.rect(SCREEN,self.color,(self.dino_rect.x, self.dino_rect.y,self.dino_rect.width,self.dino_rect.height+2),2)
        if CACTUS_ON:
            pygame.draw.line(SCREEN, self.color, (self.dino_rect.x + 50, self.dino_rect.y + 8), cactus.rect.center, 2)
        else:
            pygame.draw.line(SCREEN, self.color, (self.dino_rect.x + 50, self.dino_rect.y + 8), bird.rect.center, 2)



class Track:
    width = TRACK.get_width()
    def __init__(self,y):
        self.image = TRACK
        self.x1 = 0
        self.y = y
        self.x2 = self.width

    def move_track(self):
        self.x1 -= GAME_SPEED
        self.x2 -= GAME_SPEED
        if self.x1 + self.width <0:
            self.x1 = self.x2 + self.width 
        
        if self.x2 + self.width < 0:
            self.x2 = self.x1 + self.width 

    def draw(self,SCREEN):
        SCREEN.blit(self.image, (self.x1,self.y))
        SCREEN.blit(self.image, (self.x2,self.y))
        
class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= GAME_SPEED
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        self.update()
        SCREEN.blit(self.image, (self.x, self.y))


class Obstacle:
    def __init__(self, image, type):
        self.image = image
        global CACTUS_ON
        CACTUS_ON = True
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH


    def update(self):
        global CACTUS_ON
        global BIRD_ON
        if CACTUS_ON:
            self.rect.x -= GAME_SPEED
            if self.rect.x <= -self.rect.width :
                for genome in ge:
                    genome.fitness += 5

                CACTUS_ON = False | bool(random.randint(0,2))
                if not CACTUS_ON:
                    BIRD_ON = True
                self.type = random.randint(0,5)
                self.rect = self.image[self.type].get_rect()
                self.rect.x = SCREEN_WIDTH
                self.rect.y = TRACK_POS - self.rect.height +12

    def draw(self, SCREEN):
        self.update()
        SCREEN.blit(self.image[self.type], self.rect)


class Cactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 5)
        super().__init__(image, self.type)
        self.rect.y = TRACK_POS - self.rect.height + 12 




class Bird():
    BIRD_HEIGHTS = [245]
    def __init__(self, image):
        self.image = image
        self.rect = image[0].get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = random.choice(self.BIRD_HEIGHTS)
        self.index = 0
    def update(self):
        global CACTUS_ON
        global BIRD_ON
        if BIRD_ON:
            self.rect.x -= GAME_SPEED + 4
            if self.index == 19:
                self.index = 0
            self.index += 1
            if self.rect.x <= -self.rect.width :
                for genome in ge:
                    genome.fitness += 5
                BIRD_ON = False | bool(random.randint(0,1))
                if not BIRD_ON:
                    CACTUS_ON = True
                
                self.rect.x = SCREEN_WIDTH
                self.rect.y = random.choice(self.BIRD_HEIGHTS)

        
    def draw(self, SCREEN):
        self.update()
        SCREEN.blit(self.image[self.index // 10], self.rect)

def get_prev_maxScore():
    temp = 0
    with open('score.txt','r+') as f:
        temp = int(f.readline())
    return temp
def score():
        global POINTS,max_score
        POINTS += 1

        max_score = get_prev_maxScore()
        if int(POINTS/3) > max_score:
            max_score = int(POINTS/3)
        
        points_text = POINTS_FONT.render("score: " + str(int(POINTS/3)), 1, (0,0,0))
        max_score_text = POINTS_FONT.render("max score: " + str(int(max_score)), 1, (0,0,0))
        textRect = points_text.get_rect()
        maxrect = max_score_text.get_rect()
        SCREEN.blit(points_text, (SCREEN_WIDTH - textRect.width- 20,10))
        SCREEN.blit(max_score_text, (SCREEN_WIDTH - maxrect.width -20,50))

def remove(index):
    dinos.pop(index)
    ge.pop(index)
    nets.pop(index)

def distance(pos_a, pos_b):
    dx = pos_a[0]-pos_b[0]
    dy = pos_a[1]-pos_b[1]
    return math.sqrt(dx**2+dy**2)

def eval_genomes(genomes, config):
    global POINTS,BIRD_ON,CACTUS_ON,GAME_SPEED,max_score,ge, nets,dinos
    clock = pygame.time.Clock()

    run = True
    POINTS = 0
    BIRD_ON = False
    CACTUS_ON = False
    GAME_SPEED = 9.0

    ge = []
    nets = []
    dinos = []

    cloud = Cloud()
    track = Track(TRACK_POS)
    bird = Bird(BIRD)
    cactus = Cactus(CACTUS)

    for _, genome in genomes:
        dinos.append(Dinosaur())
        ge.append(genome)
        nets.append(neat.nn.FeedForwardNetwork.create(genome, config))
        genome.fitness = 0

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                run = False
        
        SCREEN.fill(WHITE)
        for dinosaur in dinos:
            dinosaur.update()
            dinosaur.action()
            dinosaur.draw(SCREEN,bird,cactus)
        
        if len(dinos) == 0:
            with open('score.txt','r+') as f:
                f.write(str(max_score))
            break

        for i, dino in enumerate(dinos):
                if dino.dino_rect.colliderect(cactus.rect) or dino.dino_rect.colliderect(bird.rect):
                    ge[i].fitness -= 5
                    remove(i)


        track.draw(SCREEN)
        track.move_track()
        cloud.draw(SCREEN)
        bird.draw(SCREEN)
        cactus.draw(SCREEN)
        score()
        clock.tick(FPS)
        if POINTS/3 >=800:
            break
        for i, dinosaur in enumerate(dinos):
            
            ob_x = cactus.rect.x if CACTUS_ON else bird.rect.x
            ob_y = cactus.rect.y if CACTUS_ON else bird.rect.y
            dis = distance((dinosaur.dino_rect.x, dinosaur.dino_rect.y),cactus.rect.midtop if CACTUS_ON else bird.rect.midtop)
            output = nets[i].activate((ob_x,ob_y,dis))
            decision = output.index(max(output))
            
            if decision == 0 :
                ge[i].fitness += 0.01
                pass

            elif decision == 1 and dinosaur.dino_rect.y == dinosaur.Y_POS :
                ge[i].fitness -= 0.02
                dinosaur.make_jump()

            elif decision == 2:
                ge[i].fitness -= 0.01
                dinosaur.make_duck()

            
        pygame.display.update()

def run(config_path):
    global pop
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )
    #pop = neat.Checkpointer.restore_checkpoint('neat-cheakpoint-20')
    pop = neat.Population(config)
    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)
    winner = pop.run(eval_genomes, 50)
    
if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    run(config_path)