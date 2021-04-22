import pygame
from pygame.locals import *

#Initialize pygame
pygame.init()

#-----------------------------Set Other Variables-------------------------------
tile_size = 50
clock = pygame.time.Clock()		#Create clock variable for framerate usage
frame_rate = 60		#Setting framerate makes the game run at same speed
game_over = 0		#Setting game over variable to signify end of game
menu = True		#Set variable for determining whether the game is in main menu or not
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
restart_img = pygame.image.load('imgs/restartBtn.png')
restart_img = pygame.transform.scale(restart_img, (tile_size * 3, tile_size))
start_img = pygame.image.load('imgs/startBtn.png')
start_img = pygame.transform.scale(start_img, (tile_size * 3, tile_size))
exit_img = pygame.image.load('imgs/exitBtn.png')
exit_img = pygame.transform.scale(exit_img, (tile_size * 3, tile_size))

#-----------------------------Set The World-----------------------------------------
world_grid = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 3, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 1],
[1, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 2, 1, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 2, 1, 1, 4, 4, 4, 4, 4, 4, 1, 1, 2, 0, 0, 1],
[1, 2, 2, 2, 2, 1, 1, 1, 2, 2, 2, 2, 2, 2, 1, 1, 1, 2, 2, 1]
]

#-----------------------------Button Class--------------------------------------
class Button():
	def __init__(self, x, y, image):
		self.image = image		#Loads image
		self.rect = self.image.get_rect()		#Makes image into a rectangle
		self.rect.x = x		#Set x coordinate
		self.rect.y = y		#Set y coordinate
		self.clicked = False		#This variable is for preventing the user from spamming the restart button

	def draw(self):
		mouse_position = pygame.mouse.get_pos()		#Get the mouse position
		has_clicked = False		#This variable is for returning. So that the global scope would know a button has been clicked

		if self.rect.collidepoint(mouse_position):		#Check if mouse is hovering over button
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:		#Check if left mouse button is clicked
				self.clicked = True
				has_clicked = True
		if pygame.mouse.get_pressed()[0] == 0:		#Check if left mouse button is released
			self.clicked = False		#Set to False to reset 

		game_window.blit(self.image, self.rect)		#Draws image to screen 
		return has_clicked

	

#-----------------------------Player Class--------------------------------------
class Player():
	def __init__(self, x, y):
		self.reset(x, y)	#Calls reset function which basically sets character to starting position

	#Draws player 
	def update(self, game_over):
		#Assign temporary x and y variables to check for collision before moving player
		temp_x = 0
		temp_y = 0

		if game_over == 0:	#Player will keep updating while game_over is 0
			#Keyprecesses for player
			key = pygame.key.get_pressed()
			if key[pygame.K_SPACE] and self.jumped == False and self.inair == False:	#Sets jumped to True so player can't press and hold space button. Also sets inair to False so player can't jump multiple times in air
				self.velocity_y = -15
				self.jumped = True		
			if key[pygame.K_SPACE] == False:	#Reset jumped to false for continuous spacebar pressing
				self.jumped = False
			if key[pygame.K_LEFT]:
				temp_x -= 5
				self.counter += 1	#For handling speed of animation
				self.direction = -1		#For setting direction of the character
			if key[pygame.K_RIGHT]:
				temp_x += 5
				self.counter += 1	#For handling speed of animation
				self.direction = 1		#For setting direction of the character

			#Update animation
			max_walking_speed = 10
			if self.counter > max_walking_speed:		#If counter reaches maximum speed
				self.counter = 0
				self.idx += 1		#For cyclying through images in the animation list 
				if self.idx >= len(self.right_animation):	#If self.idx reaches/goes over the last image, resets self.idx
					self.idx = 0

				#For handling direction and animation
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
			self.inair = True
			for tile in world_instance.tile_list:		#Access the whole tile_list inside the world_instance
				#X-axis collision detection
				if tile[1].colliderect(self.rect.x + temp_x, self.rect.y, self.width, self.height):
					temp_x = 0		#Sets temporary x to 0 so player would stop moving

				#Y-axis collision detection
				if tile[1].colliderect(self.rect.x, self.rect.y + temp_y, self.width, self.height):
					#Check if player box hits the bottom of a tile when jumping
					if self.velocity_y < 0:
						temp_y = tile[1].bottom - self.rect.top		#Setting temporary y coordinate to be the difference between the bottom of a tile and top of the player box
						self.velocity_y = 0		#For fluid falling animation after hitting head
					#Check if player box hits the top of a tile when standing on platform (whether or not character is in air basically)
					elif self.velocity_y > 0:
						temp_y = tile[1].top - self.rect.bottom
						self.velocity_y = 0
						self.inair = False	#Sets inair to false so that program knows player is on land

			#Checking for enemy collision
			if pygame.sprite.spritecollide(self, enemy_group, False):
				game_over = 1	#Sets game_over to 1 if player collides with enemy

			#Checking for lava collision
			if pygame.sprite.spritecollide(self, lava_group, False):
				game_over = 1	#Same as enemy collision
					

			#Update player coordinates
			self.rect.x += temp_x
			self.rect.y += temp_y

		elif game_over == 1:
			#Create character animation when player dies
			self.image = self.dead_charc
			#Animates the character ascending when dead 
			if self.rect.y > 50:
				self.rect.y -= 5
			
		#Set player image using blit function, draws player onto screen
		game_window.blit(self.image, self.rect)		#Uses blit function to draw character onto the screen
		pygame.draw.rect(game_window, (255, 255, 255), self.rect, 2)	#Draws collision box around character for visualizing collision

		return game_over

	def reset(self, x, y):		#This function is used for resetting player to original position after clicking on restart button
		#For animation
		self.right_animation = []
		self.left_animation = []
		self.counter = 0	#For setting character animation speed
		self.idx = 0	#For cycling through animation lists (both right and left)
 		
		#Loading and scaling dead character image
		self.dead_charc = pygame.image.load('imgs/deadCharc.png')
		self.dead_charc = pygame.transform.scale(self.dead_charc, (50, 100))

		for num in range(1, 5):		#Only have 4 images for SmolCh
			going_right = pygame.image.load(f'imgs/SmolCh{num}.png') 	#Loads the image
			going_right = pygame.transform.scale(going_right, (50, 100))	#Scales the image
			going_left = pygame.transform.flip(going_right, True, False)		#Flips all of the going_right images	
			self.right_animation.append(going_right)	#Adds all going_right images to the right_animation list
			self.left_animation.append(going_left)		#Adds all going_left images to the left_animation list

		self.image = self.right_animation[self.idx]		#Starting image for animation
		self.rect = self.image.get_rect()	#Transform image to rectangle
		#x and y coordinate variables for player
		self.rect.x = x
		self.rect.y = y
		#Grab width and height of character box for collision detection
		self.width = self.image.get_width()
		self.height = self.image.get_height()
		#Defining variables for jumping
		self.velocity_y = 0
		self.jumped = False
		self.inair = True

		self.direction = 0


#-----------------------------World Class--------------------------------------
class World():
	def __init__(self, grid):
		
		self.tile_list = []
		#load all images
		dirt = pygame.image.load('imgs/dirt.png')
		grass = pygame.image.load('imgs/grass.png')

		#-----------Navigate throw world_grid list-----------
		row_ctr = 0		#Set a counter to iterate through rows
		for row in grid: 	#For every list within world_grid list
			column_ctr = 0	#Set a counter to iterate through columns
			for tile in row:	#For every value within each list
				#For dirt blocks (tile = 1)
				if tile == 1:
					img = pygame.transform.scale(dirt, (tile_size, tile_size))		#Set tile to be dirt if tile equals 1
					img_rectangle = img.get_rect()		#Set img to also be a rectangle variable for collisions, etc
					#Set x and y coordinates of rectangle object
					img_rectangle.x = column_ctr * tile_size
					img_rectangle.y = row_ctr * tile_size
					#Store tile information in tile_list
					tile = (img, img_rectangle)
					self.tile_list.append(tile)
				#For grass blocks (tile = 2)
				if tile == 2:
					img = pygame.transform.scale(grass, (tile_size, tile_size))		#Set tile to be grass if tile equals 2
					img_rectangle = img.get_rect()		#Set img to also be a rectangle variable for collisions, etc
					#Set x and y coordinates of rectangle object
					img_rectangle.x = column_ctr * tile_size
					img_rectangle.y = row_ctr * tile_size
					#Store tile information in tile_list
					tile = (img, img_rectangle)
					self.tile_list.append(tile)
				#For enemies (tile = 3)
				if tile == 3:
					slime = Enemy(column_ctr * tile_size, row_ctr * tile_size + 10)		#Set x and y coordinates of slime object
					enemy_group.add(slime)
				#For lava (tile = 4)
				if tile == 4:
					lava = Lava(column_ctr * tile_size, row_ctr * tile_size + int(tile_size//2))	#Set x and y coordinates of lava object
					lava_group.add(lava)
				column_ctr += 1
			row_ctr += 1

	#Create a method in World class to draw each tiles store in tile_list on screen
	def draw(self):
		for tile in self.tile_list:
			game_window.blit(tile[0], tile[1])	#Uses blit function to draw tiles onto the screen
			pygame.draw.rect(game_window, (255, 255, 255), tile[1], 2)	#Draws collision box around tiles for visualizing collision

#-----------------------------Enemy Class--------------------------------------
class Enemy(pygame.sprite.Sprite):		#Access the sprite class from pygame's library (Enemy class will be a child of pygame's Sprite class)
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		
		slime_image = pygame.image.load('imgs/slime.png')
		self.image = pygame.transform.scale(slime_image, (tile_size, 40))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.direction = 1		#For updating coordinate in order to move
		self.direction_ctr = 0		#For setting the maximum number of spaces to move

	
	def update(self):
		self.rect.x += self.direction	#Continuously move enemy everytime program calls update function in the while loop
		#If direction_ctr reaches maximum of 40 pixels, the enemy flips direction
		self.direction_ctr += 1
		if abs(self.direction_ctr) > 50:
			self.direction *= -1
			self.direction_ctr *= -1

#-----------------------------Lava Class--------------------------------------
#Almost same as enemy class
class Lava(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)

		lava_image = pygame.image.load('imgs/lava.png')
		self.image = pygame.transform.scale(lava_image, (tile_size, tile_size // 2))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y


#Create instances and groups of classes
player_instance = Player(100, screen_height - 150)
enemy_group = pygame.sprite.Group()		#Group function creates a list for adding enemies into
lava_group = pygame.sprite.Group()		#Same as enemy group
world_instance = World(world_grid)
#-----Button instances
restart_button = Button(screen_width - 600, screen_height // 2 + 50, restart_img)
start_button = Button(screen_width - 900, screen_height // 2 + 50, start_img)
exit_button = Button(screen_width - 300, screen_height // 2 + 50, exit_img)

#-----------------------------Game Loop Area--------------------------------------
#Set run to True to keep the game running
run = True
while run:

	clock.tick(frame_rate)		#For setting a limit on FPS (also sets consistency of game)

	game_window.blit(background, (0, 0))	#Set background image using blit function

	if menu == True:
		if start_button.draw():		#Draws start button to screen. The draw function also checks whether the button has been clicked or not due to the Button class returning the has_clicked variable
			menu = False	
		if exit_button.draw():		#Same as start button
			run = False
	else: 
		world_instance.draw()		#Calls the draw function in the World class
		
		if game_over == 0:		#If player is still alive
			enemy_group.update()		#Updates enemy's position while player is still alive

		enemy_group.draw(game_window)		#Draws enemies to the screen
		lava_group.draw(game_window)		#Same as enemies
		
		game_over = player_instance.update(game_over)	#Updates the player movements in the Player class and game_over status

		if game_over == 1:		#If player has died
			if restart_button.draw():		#Calls draw function if player dies
				player_instance.reset(100, screen_height - 150)		#Resets instance if restart button is hit
				game_over = 0

	#If user clicks 'X', or close window in any way, the program would exit
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	pygame.display.update()		#Updates the display window	so images are updated repeatedly

pygame.quit()