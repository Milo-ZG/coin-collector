import pygame
import sprite_sheet
from random import randint
pygame.init()

# variable definitions
screen_width, screen_height = pygame.display.get_desktop_sizes()[0]
score = 0
dir = "left"
x = screen_width/2
y = screen_height/2
BLACK = (0, 0, 0)

coin_positions = []
coins = []
for i in range(0, 4):
    coin_pos = randint(0, screen_width - 100), randint(0, screen_height - 100)
    coin_positions.append(coin_pos)

def scale_by(sprite, scale):
    return pygame.transform.scale(sprite, ((sprite.get_size()[0] * scale), (sprite.get_size()[1] * scale)))

#text engine
my_font = pygame.font.SysFont("Arial", 50)
def draw_text(text, font, text_col, x, y, scale):
    img = font.render(text, True, text_col)
    img = scale_by(img, scale)
    screen.blit(img, (x, y))

# coin class
class dot:
    def __init__(self, pos):
        self.pos = pos
        self.image = coin_sheet.get_image(coin_sheet.animate('coin', 0, 6, 250), 133.5, 118, 0.35, BLACK)
        self.mask = pygame.mask.from_surface(coin_sheet.get_image(coin_sheet.animate('coin', 0, 6, 250), 133.5, 118, 0.35, BLACK))
        self.size = self.image.get_size()

#defining sprites and masks
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Coin Collector")

maze = pygame.image.load("images/pac_maze.png")
maze = scale_by(maze, 3)
maze_mask = pygame.mask.from_surface(maze)

coin_sheet_image = pygame.image.load("images/coin_sheet_no_bg.png").convert_alpha()
pac_sheet_image = pygame.image.load("images/pacman_sprite_sheet.png").convert_alpha()
coin_sheet = sprite_sheet.SpriteSheet(coin_sheet_image)
pac_sheet = sprite_sheet.SpriteSheet(pac_sheet_image)

for coin in coin_positions:
    coins.append(dot(coin))

player = pac_sheet.get_image(pac_sheet.animate('pacman', 0, 3, 100), 219.3333, 196, 0.7, BLACK)
pac_mask = pygame.mask.from_surface(player)
    


def handle_movement(x, y, dir, player, screen_width, screen_height):
    key = pygame.key.get_pressed()
    
    # Movement and direction
    if key[pygame.K_a] or key[pygame.K_LEFT]:
        dir = "left"
        x -= 5
    if key[pygame.K_d] or key[pygame.K_RIGHT]:
        dir = "right"
        x += 5
    if key[pygame.K_w] or key[pygame.K_UP]:
        dir = "up"
        y -= 5
    if key[pygame.K_s] or key[pygame.K_DOWN]:
        dir = "down"
        y += 5
    if (key[pygame.K_a] or key[pygame.K_LEFT]) and (key[pygame.K_w] or key[pygame.K_UP]):
        dir = "top_left"
    if (key[pygame.K_a] or key[pygame.K_LEFT]) and (key[pygame.K_s] or key[pygame.K_DOWN]):
        dir = "bottom_left"
    if (key[pygame.K_d] or key[pygame.K_RIGHT]) and (key[pygame.K_w] or key[pygame.K_UP]):
        dir = "top_right"
    if (key[pygame.K_d] or key[pygame.K_RIGHT]) and (key[pygame.K_s] or key[pygame.K_DOWN]):
        dir = "bottom_right"

    # Border fencing
    if x > screen_width - player.get_size()[0]:
        x -= 5
    if x < 0:
        x += 5
    if y > screen_height - player.get_size()[1]:
        y -= 5
    if y < 0:
        y += 5

    # Collision detection with maze
    if maze_mask.overlap(pac_mask, (x - ((screen_width / 2) - (maze.get_width() / 2)), y)):
        if dir == "left":
            x += 5
        if dir == "right":
            x -= 5
        if dir == "up":
            y += 5
        if dir == "down":
            y -= 5
        if dir == "top_left":
            x += 5
            y += 5
        if dir == "top_right":
            x -= 5
            y += 5
        if dir == "bottom_left":
            x += 5
            y -= 5
        if dir == "bottom_right":
            x -= 5
            y -= 5

    return x, y, dir



#game loop
run = True
while run:
    screen.fill(BLACK)

    coins = []
    for coin in coin_positions:
        coins.append(dot(coin))

    # Re-defining sprites and masks for movement and animation
    player = pac_sheet.get_image(0, 219.3333, 196, 0.2, BLACK)
    pac_mask = pygame.mask.from_surface(player)
    player = pac_sheet.get_image(pac_sheet.animate('pacman', 0, 3, 250), 219.3333, 196, 0.2, BLACK)

    # Handle movement
    x, y, dir = handle_movement(x, y, dir, player, screen_width, screen_height)

    # Orientation
    if dir == "left":
        player = pygame.transform.flip(player, True, False)
    elif dir == "right":
        player = pygame.transform.rotate(player, 0)
    elif dir == "up":
        player = pygame.transform.rotate(player, 90)
    elif dir == "down":
        player = pygame.transform.rotate(player, -90)
    elif dir == "top_left":
        player = pygame.transform.rotate(player, 135)
    elif dir == "top_right":
        player = pygame.transform.rotate(player, 45)
    elif dir == "bottom_left":
        player = pygame.transform.rotate(player, 225)
    elif dir == "bottom_right":
        player = pygame.transform.rotate(player, 315)

    pac_mask = pygame.mask.from_surface(player)

    #bliting everything onto the screen
    screen.blit(player, (x, y))
    for coin in coins:
        screen.blit(coin.image, coin.pos)
    
    screen.blit(maze, (((screen_width / 2) - (maze.get_width() / 2)), 0))

    # Collision detection with coin
    for coin in coins:
        if pac_mask.overlap(coin.mask, (coin.pos[0] - x, coin.pos[1] - y)):
            coin_pos = randint(0, screen_width - coin.size[0]), randint(0, screen_height - coin.size[1])
            coin_positions[coins.index(coin)] = coin_pos
            score += 1

    # Score display
    draw_text(str(score), my_font, (255, 255, 255), 10, 10, 2)

    # Event handler
    key = pygame.key.get_pressed()
    if key[pygame.K_ESCAPE]:
        run = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()
pygame.quit()