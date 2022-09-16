import pygame
import time
import random
from pygame.locals import *

size=30
bg_colour = (80,120,30)

class snake:
    def __init__(self, surface, length):
        self.p_screen=surface
        self.length=length
        self.block=pygame.image.load("resources/block.jpg").convert() #loading image
        self.block_x=[size]*length
        self.block_y=[size]*length
        self.direction='right'
        
    def increase_len(self):
        self.length += 1
        self.block_x.append(-1) 
        self.block_y.append(-1) 
        
    def draw(self):
        self.p_screen.fill(bg_colour)  # clears screen
        for i in range(self.length):
            self.p_screen.blit(self.block,(self.block_x[i],self.block_y[i]))  # draws the block on background
        pygame.display.flip()  # commits the final changes
        
    def move_up(self):
        self.direction='up'
        
    def move_down(self):
        self.direction='down'
        
    def move_left(self):
        self.direction='left'
        
    def move_right(self):
        self.direction='right'
        
    def run(self):
        
        for i in range(self.length-1,0,-1):    # placing last block at the place of 2nd last and so on
            self.block_x[i]=self.block_x[i-1]
            self.block_y[i]=self.block_y[i-1]
            
        if self.direction=='up':          # changing the position of head block
            self.block_y[0] -= size
        if self.direction=='down':
            self.block_y[0] += size
        if self.direction=='left':
            self.block_x[0] -= size
        if self.direction=='right':
            self.block_x[0] += size
            
        self.draw()

class apple:
    def __init__(self, p_screen):
        self.p_screen=p_screen
        self.img=pygame.image.load("resources/apple.png").convert()
        self.x=size*15
        self.y=size*15
        
    def draw(self):
        self.p_screen.blit(self.img,(self.x,self.y))  # draws the apple on background
        pygame.display.flip()  # commits the final changes
        
    def move(self):     # chossing random location for apple
        self.x=random.randint(0,32)*size     #  (990/30)-1
        self.y=random.randint(0,26)*size     #  (810/30)-1
        

class game:
    def __init__(self):
        pygame.init()   # initialize all imported pygame modules
        self.surface=pygame.display.set_mode((990,810))   # defining a screen   # making it as class member
        self.surface.fill((100,50,10))
        self.snake = snake(self.surface,2) # initialize the snake
        self.snake.draw()
        self.apple=apple(self.surface)
        self.apple.draw()
        
    def collide(self,x1,y1,x2,y2):          # x1 is dimension of snake , x2 of apple
        if x1 >= x2 and x1 < x2+size:
             if y1 >= y2 and y1 < y2+size:   # neurtrally y1=y2+size
                return True
        return False
        
    def play(self):
        self.snake.run()
        self.apple.draw()
        self.score()
        pygame.display.flip()  # refresh screen to update score
        
        # snake colliding with apple
        if self.collide(self.snake.block_x[0], self.snake.block_y[0], self.apple.x, self.apple.y):  # checks if snakes eat apple
            self.snake.increase_len()   # increase length of snake
            self.apple.move()   # randomly moves apple to new position
            
        # snake collinding with itself
        for i in range(3,self.snake.length):
            if self.collide(self.snake.block_x[0], self.snake.block_y[0], self.snake.block_x[i], self.snake.block_y[i]):
                raise "Game Over"
        
    def over(self):
        self.surface.fill(bg_colour)      # clears screen
        font=pygame.font.SysFont('arial',30)
        l1=font.render(f"Score: {self.snake.length-1}", True,(255,255,255))
        self.surface.blit(l1,(440,330))
        l2=font.render("Press SPACEBAR to play again", True,(255,255,255))
        self.surface.blit(l2,(300,380))
        pygame.display.flip()   # refresh the screen
        
    def reset(self):
        self.snake = snake(self.surface,2)    # re-initialize the snake
        self.apple=apple(self.surface)
    
    def score(self):
        font=pygame.font.SysFont('arial',30)
        scr=font.render(f"Score: {self.snake.length-1}", True,(200,200,200))
        self.surface.blit(scr,(800,10))  # displays on top-right corner
        
    def run(self):
        running=True      # creating an event loop
        p=False
        while running:
            for event in pygame.event.get():
                if event.type==KEYDOWN:
                    if event.key==K_ESCAPE:   # game window will close when we will press esc key
                        running=False
                    if event.key==K_SPACE:  # restarts the game after its over
                        p=False
                    if not p:
                        if event.key==K_UP:
                            self.snake.move_up()
                        if event.key==K_DOWN:
                            self.snake.move_down()
                        if event.key==K_LEFT:
                            self.snake.move_left()
                        if event.key==K_RIGHT:
                            self.snake.move_right()
                elif event.type==QUIT:    # game window will close when we will click cancel button
                    running=False
                 
            try:   
                if not p:  #till not paused
                    self.play()   # starts game
            except Exception as z:
                self.over()
                p=True
                self.reset()
            time.sleep(0.2)
        
if __name__ == "__main__":
    g=game()
    g.run()   # setups environment
