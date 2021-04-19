import pygame
from pygame.locals import *

#Initialize pygame
pygame.init()

#-----------------------------Set Other Variables-------------------------------
tile_size = 50
clock = pygame.time.Clock()
frame_rate = 60
#-----------------------------Set Game Window-----------------------------------
#Set game window size (pixel)
screen_width = 1000
screen_height = 1000

#Set game window with the size of screen_width and screen_height
game_window = pygame.display.set_mode((screen_width, screen_height))
#Set caption of the window
pygame.display.set_caption("CNIT481Project")

#-----------------------------Load Images---------------------------------------
background = pygame.image.load('imgs/Background.png')


#-----------------------------Set World-----------------------------------------
world_grid = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 2, 1, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 2, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 2, 0, 0, 1],
[1, 2, 2, 2, 2, 1, 1, 1, 2, 2, 2, 2, 2, 2, 1, 1, 1, 2, 2, 1]
]

#-----------------------------Player Class--------------------------------------
class Player():
	def __init__(self, x, y):

		#For animation
		self.right_animation = []
		self.left_animation = []
		self.counter = 0
		self.idx = 0	#For cycling through right_animation list
 		
		for num in range(1, 5):		#Only have 4 images for SmolCh
			going_right = pygame.image.load(f'imgs/SmolCh{num}.png') 	#Loads the image
			going_right = pygame.transform.scale(going_right, (50, 100))	#Scales the image
			going_left = pygame.transform.flip(going_right, True, False)		#Flips all of the going_right images	
			self.right_animation.append(going_right)
			self.left_animation.append(going_left)

		#Starting image
		self.image = self.right_animation[self.idx]
		#Transform image to rectangle
		self.rect = self.image.get_rect()#creating collision rectangle
		#x and y coordinate variables for player
		self.rect.x = x
		self.rect.y = y
		#Defining variables for jumping
		self.velocity_y = 0
		self.jumped = False

		self.direction = 0

	#Draws player 
	def update(self):

		#Assign temporary x and y variables to check for collision before moving player
		temp_x = 0
		temp_y = 0

		#Keyprecesses for player
		key = pygame.key.get_pressed()
		if key[pygame.K_SPACE] and self.jumped == False:	#Sets jumped to True so player can't press and hold space button
			self.velocity_y = -15
			self.jumped = True		
		if key[pygame.K_SPACE] == False:	#Reset jumped to false for continuous spacebar pressing
			self.jumped = False
		if key[pygame.K_LEFT]:
			temp_x -= 5
			self.counter += 1	#For handling speed of animation
			self.direction = -1	
		if key[pygame.K_RIGHT]:
			temp_x += 5
			self.counter += 1	#For handling speed of animation
			self.direction = 1

		#Update animation
		max_walking_speed = 10
		
		if self.counter > max_walking_speed:		#If counter reaches maximum speed
			self.counter = 0
			self.idx += 1		#For cyclying through images in the right_animation list 
			if self.idx >= len(self.right_animation):
				self.idx = 0

			#For handling direction
			if self.direction == 1:
				self.image = self.right_animation[self.idx]
			if self.direction == -1:
				self.image = self.left_animation[self.idx]

		#Add gravity
		self.velocity_y += 1	#The line for adjusting gravity

		if self.velocity_y > 10:	#Set a cap on acceleration
			self.velocity_y = 10
		temp_y += self.velocity_y

		#Checking for collision

		#Update player coordinates
		self.rect.x += temp_x
		self.rect.y += temp_y

		if self.rect.bottom > screen_height - 50:
			self.rect.bottom = screen_height - 50
			temp_y = 0

		#Set player image using blit function, draws player onto screen
		game_window.blit(self.image, self.rect)
		pygame.draw.rect(game_window, (255, 255, 255), self.rect, 2)

#-----------------------------World Class--------------------------------------
class World():
	def __init__(self, grid):
		
		self.tile_list = []
		#load all images
		dirt = pygame.image.load('imgs/dirt.png')
		grass = pygame.image.load('imgs/grass.png')

		#-----------Navigate throw world_grid list-----------
		#Set a counter to iterate through rows
		row_ctr = 0
		for row in grid: 	#For every list within world_grid list
			column_ctr = 0	#Set a counter to iterate through columns
			for tile in row:	#For every value within each list
				#For dirt blocks (tile = 1)
				if tile == 1:
					#Set tile to be dirt if tile equals 1
					img = pygame.transform.scale(dirt, (tile_size, tile_size))
					#Set img to also be a rectangle variable for collisions, etc
					img_rectangle = img.get_rect()
					#Set x and y coordinates of rectangle object
					img_rectangle.x = column_ctr * tile_size
					img_rectangle.y = row_ctr * tile_size
					#Store tile information in tile_list
					tile = (img, img_rectangle)
					self.tile_list.append(tile)
				#For grass blocks (tile = 2)
				if tile == 2:
					#Set tile to be dirt if tile equals 1
					img = pygame.transform.scale(grass, (tile_size, tile_size))
					#Set img to also be a rectangle variable for collisions, etc
					img_rectangle = img.get_rect()
					#Set x and y coordinates of rectangle object
					img_rectangle.x = column_ctr * tile_size
					img_rectangle.y = row_ctr * tile_size
					#Store tile information in tile_list
					tile = (img, img_rectangle)
					self.tile_list.append(tile)
				column_ctr += 1
			row_ctr += 1

	#Create a method in World class to draw each tiles store in tile_list on screen
	def draw(self):
		for tile in self.tile_list:
			game_window.blit(tile[0], tile[1])

#Create instances of classes
player_instance = Player(100, screen_height - 150)
world_instance = World(world_grid)

#Set run to True to keep the game running
run = True
while run:

	clock.tick(frame_rate)		#For fixing framerate
	#Set images using blit function
	game_window.blit(background, (0, 0))

	world_instance.draw()
	player_instance.update()

	#If user clicks 'X', or close window in any way, the program would exit
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	#Updates the display window		
	pygame.display.update()

pygame.quit()