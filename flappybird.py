import pygame #importing all the necessary modules
import neat#i was able to import all these modules using the pip function via the command prompt
import time
import os
import random
pygame.font.init

Win_Width = 500
Win_Height = 800

Bird_Imgs = [pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird1.png')))], pygame.transform.scale2x(pygame.imageload(os.path.join('imgs', 'bird2.png'))), pygame.transform.scale2x(pygame.imageload(os.path.join('imgs', 'bird3.png')))
Pip_Img = pygame.transform.scale2x(pygame.imageload(os.path.join('imgs', 'bird.png')))
Base_Img = pygame.transform.scale2x(pygame.imageload(os.path.join('imgs', 'base.png')))
	Background_Img = pygame.transform.scale2x(pygame.imageload(os.path.join('imgs', 'bg.png')))

STAT_FONT = pygame.font.SysFont("comic sans", 50)#creating a font used in order to talk about the score

class Bird:
	Imgs = Bird_Imgs
	MAX_ROTATION = 25 #declaring the amount of rotation/velocity that will be present on the birds
	ROT_VEL = 20
	ANIMATION = 5

	def __init__(self,x,y):
		self.x = x #setting everything at 0 so that the bird doesn't start from nowhere
		self.y = y
		self.tilt = 0 
		self.tick_count = 0
		self.vel = 0
		self.height = self.y
		self.img_count = 0
		self.img = self.Imgs[0]

	def jump(self):
		self.vel = -10.5
		self.tick_count = 0
		self.height = self.y #keeps track of where the bird is jumping from

	def move(self):
		self.tick_count +=1

		d = self.vel*self.tick_count + 1.5*self.tick_count**2 #displacement how many pixels up and down

		if d>= 16: #making sure the velocity isn't moving way for up or down keeping it in right range, terminal velocity
			d = 16 

		if d < 0:
			d -=2

		self.y = self.y + d

		if d < 0 or self.y < self.height + 50:
			if self.tilt < self.MAX_ROTATION: #making sure the bird doesn't tilt in crazy rotation
				self.tilt = self.MAX_ROTATION
		else:
			if self.tilt > -90:
				self.tilt -= self.ROT_VEL #allowing us to rotate the flappy bird in a 90 degree direction, don't want to completely tilt


	def draw(self, win): #win represents the windows by which we'll be drawing in
		self.img_count += 1

		if self.img_count < self.ANIMATION_Time:
			self.img = self.IMGS[0]
		elif self.img_count < self.ANIMATION_Time*2: #changes the image
			self.img = self.IMGS[1]

		elif self.img_count < self.ANIMATION_Time*3: #will show the last image
			self.img = self.IMGS[1]

		elif self.img_count < self.ANIMATION_Time*4:
			self.img = self.IMGS[1]

		elif self.img_count < self.ANIMATION_Time*4 + 1:
			self.img = self.IMGS[1]

			self.img = self.IMGS[0] #resetting the imagine count 
			self.img_count = 0

		if self.tilt <= -80: #making sure the flappy bird doesn't constantly flap
			self.img = self.IMGS[1]
			self.img_count = self.ANIMATION_Time*2 #when the bird jumps back up it doesn't skip a frame


		rotated_image = pygame.transform.rotate(self.img, self.tilt)#github algorithim
		new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft = (self.x, self.y)).center)#rotates the image around the center
		win,blit(rotated_image, new_rect.topleft)#how we rotate images in pygame

		def get_mask(self):
			return pygame.mask.from_surface(self.img)

class Pipe:
	GAP = 200 #a general rule is always name ur constant variables with uppercase as it makes your life a lot easier
	VEL = 5

	def __init__(self, x):
		self.x = x
		self.height = 0

		self.top = 0#lines 98-100 are used in order to define where the top of the pipe, as well as where the bottom of the pipe is
		self.bottom = 0
		self.PIP_TOP = pygame.transform.flip(PIPE_IMG, False, True)
		self.PIPE_BOTTOM = PIPE_IMG

		self.passed = False #this block of code is for collision purposes and will be used in the for the AI part later
		self.set_height()

	def set_height(self):#we will get a random number here to see where the top of our pipe will be
				self.height = random.randrange(50, 450)
				self.top = self.height = self.PIPE_TOP.get_height()#we need to figure out the top left position of the image of our pipe
				self.bottom = self.height + self.GAP#I am using the variable declaration on line 90 and referring to that, which is why i got rid of it on line 92. 				

	def move(self):#probably the easiest method in your code, because all we need to do is change the x and y coordinates in our pipe
			self.x -= self.VEL#every time we call this move method we will be moving the pipe a little bit to the left

	def draw(self, win):
		win.blit(self.PIPE_TOP, (self.x, self.top))
		win.blit(self.PIPE_BOTTOM (self.x, self.bottom))

	def collide(self, bird):#this whole method is calculating the offset, how far these masks are from each other
		bird_mask = bird.get_mask(self.PIP_TOP)
				top_mask = pygame.mask.from_surface(self.PIP_TOP)
		bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

		top_offset = (self.x - bird.x, self.top - round(bird.y))
		bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

		b_point = bird.mask.overlap(bottom_mask, bottom_offset)#this line of code tells us the point of collision, and if these don't collide it returns none
		t_point = bird.mask.overlap(top_mask, bottom_offset)

		if t_point or b_point:# if there are not none, we will collide with the other objects
			return true

		return False
class Base:
	VEL = 5#needs to be the same as the pipe other wise it will look uneven and not in sync
	Width = Base_Img.get_width()
	IMG = Base_Img

	def __init__(self,y):
		self.y = y
		self.x1 = 0
		self.x2 = self.WIDTH

	def move(self):
		self.x1 -= self.VEL
		self.x2 -= self.VEL

		if self.x1 + self.WIDTH < 0:#the purpose of these if statements is in order to create a circular rotation of the images so that we never run out circular github algorithim
			self.x1 = self.x2 + self.WIDTH

		if self.x2 + self.WIDTH <0:
			self.x2 = self.x1 + self.WIDTH

	

def draw_window(win, bird, pipes, base, score):#this will draw the window where the game will be played
	win.blit(bg_IMG(0,0))#blit means draw in pygame also the top left position
	
	for pipes in pipes:#going to come in as a list, as we can have more than one pipe
		pipe.draw(win)

	text = STAT_FONT.render('Score:'+str(score), 1,(255,255,255))
	win.blit(text, (Win_Width - 10 - texxt.get_width(), 10))

		
	base.draw(win)
	
	for birds in birds:	
		bird.draw(win)
	pygame.display.update()#updates the display with the new classes



def main(genomes,config):#we need to modify this function to make it compatible with our fitness function
	nets = []
	ge = []
	birds = [] #via github found it this is the best location

	for _, g in genomes:
		net = neat.nn.FeedForwardNetwork.create(g,config)#give it the genome, config file
		nets.append (net)# append to the list
		birds.append(Bird(230, 350))#append the genome to the same position of the bird keeping track of fitness
		g.fitness = 0
		ge.append(g)

	

	base = Base(730)
	pipes = [Pipe(700)]
	win = pygame.display.set_mode((Win_Width, Win_Height))
	clock = pygame.time.Clock()# setting a frame rate by which the flappy bird will run in order to make the movement more synced
	clock = tick(30)#the bird is falling much slower and is even tilting down after this function. 
	pygame.quit()
	quit()

	score = 0
	
	run = True
	while run and clock = tick(30)
		for event in pygame.event.get():#when the user clicks the mouse or something we will run this while loop
				if event.type == pygame.QUIT:
					run = False

		pipe_ind = 0
		if len(birds) > 0:
			if len pipes > 1 and bird[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
				pipe_ind = 1

		for x, bird in enumerate(birds):
			bird.move()
			ge[x].fitness += 0.1

			output = nets[x].activate((bird.y, abs(bird.y - pipes[pipes_ind.height], abs(bird.y - pipes(pipe_ind.bottom)))

			if output[0] > 0.5:
				bird.jump()

				add_pipe = False 
				rem = []
				for pipe in pipes:
					for x bird in enumerate(birds):
						if pipe.collide(bird):
							ge[x].fitness -= 1
							birds.pop(x)
							nets.pop(x)
							ge.pop(x)
					
					
						if not pipe.passed and pipe.x < bird.x:
							pipe.passed = True
							add_pipe = True

					if pipe.x + pipe.PIPE_TOP.get_width() < 0:#checking if the pipe is completely off the screen and if it is it will automatically remove it
						rem.append(pipe)
					
					pipe.move()
				if add_pipe:
					score += 1
					for g in ge:
						g.fitness +=5#if it passes 5 it will gain 5 towards it's fitness course
					pipes.append(Pipe(600))#creating a new pipe


				for r in rem:
					pipes.remove(r)

				for x, bird in enumerate (birds):
				if bird.y + bird.img.get_height() >= 730 or bird.y < 0:#if birds reaches the top of the screen we mst make sure that it will terminate
					birds.pop(x)
					nets.pop(x)
					ge.pop(x)	xx	


				base.move()
				draw_window(win,birds, pipes, base, score)




main()	

def run(config_path): #taking the configuration path as a parameter thus making it easier to load it in as a file
	config = neat.config.Config(neat.defaultGenome, neat.DefaultReproduction, 
													neat.DefaultSpeciesSet, neat.DefaultStagnation,
													config_path)
	p = neat.Population(config)#generating a population to play our game based on the parameters given in the configuration file

	p.add_reporter(neat.StdOutReporter(True))# creating stats that will be shown when running the code in the command promot relating the fitness of each generation
	stats = neat.StatisticsReporter()
	p.add_reporter(stats)#setting an output

	winer = p.run(,50)#sitting the fitness function to run a certain amount of generations it will pass it 50 times to all the genos, as well as the config file



if __name__ = "__main"__:
	local_dir = os.path.dirname(__file__)#fancy stuff to load in our config file attained code from github
	config_path = os.path.join(local_dir, "config-feedforward.txt")
	run(config_path)






