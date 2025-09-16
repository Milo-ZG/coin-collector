import pygame
import sprite_sheet
from random import randint
pygame.init()

# variable definitions
screen_width, screen_height = pygame.display.get_desktop_sizes()[0]
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Coin Collector")
score = 0
cell_size = int(screen_width // 10)
cell_size = int((screen_width - (cell_size // 2)) // 10)
dir = "left"
x = screen_width/2
y = screen_height/2
BLACK = (0, 0, 0)
coin_sheet_image = pygame.image.load("images/coin_sheet_no_bg.png").convert_alpha()
pac_sheet_image = pygame.image.load("images/pacman_sprite_sheet.png").convert_alpha()
coin_sheet = sprite_sheet.SpriteSheet(coin_sheet_image)
pac_sheet = sprite_sheet.SpriteSheet(pac_sheet_image)

# coin class
class dot:
    def __init__(self, pos):
        self.pos = pos
        self.image = coin_sheet.get_image(coin_sheet.animate(0, 6, 250), 133.5, 118, cell_size, BLACK)
        self.mask = pygame.mask.from_surface(coin_sheet.get_image(coin_sheet.animate(0, 6, 250), 133.5, 118, cell_size, BLACK))
        self.size = self.image.get_size()

class wall:
    def __init__(self, pos, size):
        self.pos = pos
        self.image = pygame.Surface(size)
        self.image.fill((0, 0, 255))
        self.mask = pygame.mask.from_surface(self.image)
        self.size = self.image.get_size()

cells = []
cell_x = cell_size // 2
cell_y = cell_size // 2

map =  [['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'], \
        ['W', ' ', ' ', 'C', 'C', 'C', ' ', ' ', 'P', 'W'], \
        ['W', ' ', 'W', 'W', 'W', 'W', 'W', ' ', 'W', 'W'], \
        ['W', ' ', 'C', 'C', ' ', ' ', 'W', 'C', 'W', 'W'], \
        ['W', ' ', 'W', 'W', 'W', ' ', 'W', 'C', 'C', 'W'], \
        ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W']]

for row in map:
    for cell in row:
        if cell == 'W':
            cells.append(wall((cell_x, cell_y), (cell_size, cell_size)))
        if cell == 'C':
            cells.append(dot((cell_x, cell_y)))
        if cell == 'P':
            x = cell_x
            y = cell_y
        if cell == ' ':
            pass
        cell_x += cell_size
    cell_x = cell_size // 2
    cell_y += cell_size


def scale_by(sprite, scale):
    return pygame.transform.scale(sprite, ((sprite.get_size()[0] * scale), (sprite.get_size()[1] * scale)))

#text engine
my_font = pygame.font.SysFont("Arial", 50)
def draw_text(text, font, text_col, x, y, scale):
    img = font.render(text, True, text_col)
    img = scale_by(img, scale)
    screen.blit(img, (x, y))

#defining sprites and masks


player = pac_sheet.get_image(pac_sheet.animate(0, 3, 100), 219.3333, 196, (cell_size - 2), BLACK)
pac_mask = pygame.mask.from_surface(player)
    
def handle_movement(x, y, dir, player, screen_width, screen_height, key):
    # Movement and direction
    if key[pygame.K_a] or key[pygame.K_LEFT]:
        dir = "left"
        x -= 5
    elif key[pygame.K_d] or key[pygame.K_RIGHT]:
        dir = "right"
        x += 5
    elif key[pygame.K_w] or key[pygame.K_UP]:
        dir = "up"
        y -= 5
    elif key[pygame.K_s] or key[pygame.K_DOWN]:
        dir = "down"
        y += 5

    # Border fencing
    if x > screen_width - player.get_size()[0]:
        x = screen_width - player.get_size()[0]
    if x < 0:
        x = 0
    if y > screen_height - player.get_size()[1]:
        y = screen_height - player.get_size()[1]
    if y < 0:
        y = 0

    # Collision detection with maze
    for cell in cells:
        if isinstance(cell, wall):
            if pac_mask.overlap(cell.mask, (cell.pos[0] - x, cell.pos[1] - y)):
                if dir == "left":
                    while pac_mask.overlap(cell.mask, (cell.pos[0] - x, cell.pos[1] - y)):
                        x += 1
                elif dir == "right":
                    while pac_mask.overlap(cell.mask, (cell.pos[0] - x, cell.pos[1] - y)):
                        x -= 1
                elif dir == "up":
                    while pac_mask.overlap(cell.mask, (cell.pos[0] - x, cell.pos[1] - y)):
                        y += 1
                elif dir == "down":
                    while pac_mask.overlap(cell.mask, (cell.pos[0] - x, cell.pos[1] - y)):
                        y -= 1

    return x, y, dir



#game loop
clock = pygame.time.Clock()
run = True
while run:
    clock.tick(60)  # Limit to 60 FPS

    # Event handler (move this to the top of the loop)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    screen.fill(BLACK)
    key = pygame.key.get_pressed()

    # Only update player sprite once per frame
    player = pac_sheet.get_image(pac_sheet.animate(0, 3, 250), 219.3333, 196, (cell_size - 1), BLACK)
    pac_mask = pygame.mask.from_surface(player)
    for cell in cells:
        if isinstance(cell, dot):
            cell.image = coin_sheet.get_image(coin_sheet.animate(0, 6, 250), 133.5, 118, cell_size, BLACK)
            cell.mask = pygame.mask.from_surface(coin_sheet.get_image(coin_sheet.animate(0, 6, 250), 133.5, 118, cell_size, BLACK))

    # Pass key to handle_movement
    x, y, dir = handle_movement(x, y, dir, player, screen_width, screen_height, key)

    # Orientation
    if dir == "left":
        player = pygame.transform.flip(player, True, False)
    elif dir == "right":
        player = pygame.transform.rotate(player, 0)
    elif dir == "up":
        player = pygame.transform.rotate(player, 90)
    elif dir == "down":
        player = pygame.transform.rotate(player, -90)

    pac_mask = pygame.mask.from_surface(player)

    screen.blit(player, (x, y))
    for cell in cells:
        screen.blit(cell.image, cell.pos)

    # Collision detection with coin (iterate over a copy to avoid issues)
    for cell in cells[:]:
        if isinstance(cell, dot):
            if pac_mask.overlap(cell.mask, (cell.pos[0] - x, cell.pos[1] - y)):
                cells.remove(cell)
                score += 1

    # Score display
    draw_text(str(score), my_font, (255, 255, 255), 10, 10, 2)

    #time display
    draw_text(str(60 - pygame.time.get_ticks()//1000), my_font, (255, 255, 255), screen_width - 150, 10, 2)

    if key[pygame.K_ESCAPE]:
        run = False
    if pygame.time.get_ticks()//1000 >= 60:
        run = False
        screen.fill(BLACK)
        draw_text("Time's Up!", my_font, (255, 255, 255), screen_width/2 - 150, screen_height/2 - 50, 2)
        draw_text("Final Score: " + str(score), my_font, (255, 255, 255), screen_width/2 - 200, screen_height/2 + 50, 2)
        pygame.display.update()
        pygame.time.delay(5000)

    pygame.display.update()
    
pygame.quit()