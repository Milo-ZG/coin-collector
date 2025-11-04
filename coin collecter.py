import pygame
import sprite_sheet
from math import floor
pygame.init()

# variable definitions
screen_width, screen_height = pygame.display.get_desktop_sizes()[0]
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Coin Collector")
score = 0
cell_size = int(screen_height // 19)
cell_size = 5 * floor(cell_size/5)
xv = 0
yv = 0
# desired (queued) velocity: record player's most recent requested direction
desired_xv = 0
desired_yv = 0
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
        self.rect = self.image.get_rect(topleft=pos)
        self.size = self.image.get_size()

class wall:
    def __init__(self, pos, size):
        self.pos = pos
        self.image = pygame.Surface(size)
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect(topleft=pos)
        self.size = self.image.get_size()

cells = []
cell_x = cell_size // 2
cell_y = cell_size // 2

map =  [
    ['W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W'],
    ['W','C','C','C','C','C','C','W','C','C','C','W','C','C','C','C','C','C','W'],
    ['W','C','W','W','W','C','W','W','W','C','W','W','W','C','W','W','W','C','W'],
    ['W','C','W',' ','W','C','C','C','C','C','C','C','C','C','W',' ','W','C','W'],
    ['W','C','W','W','W','C','W','W','W',' ','W','W','W','C','W','W','W','C','W'],
    ['W','C','C','C','C','C','W',' ','W',' ','W',' ','W','C','C','C','C','C','W'],
    ['W','C','W','W','W','C','W',' ','W','W','W',' ','W','C','W','W','W','C','W'],
    ['W','C','W',' ','W','C','C','C','C','C','C','C','C','C','W',' ','W','C','W'],
    ['W','C','W','W','W','W','W','W','W',' ','W','W','W','W','W','W','W','C','W'],
    ['W','C','C','C','C','C','C','W',' ',' ',' ','W','C','C','C','C','C','C','W'],
    ['W','W','W','W','W','W','C','W','W','W','W','W','C','W','W','W','W','W','W'],
    [' ',' ',' ',' ','W','C','C','C','C','P','C','C','C','C','W',' ',' ',' ',' '],
    ['W','W','W','W','W','C','W','W','W','W','W','W','W','C','W','W','W','W','W'],
    ['W','C','C','C','C','C','W',' ',' ',' ',' ',' ','W','C','C','C','C','C','W'],
    ['W','C','W','W','W','W','W','W','W',' ','W','W','W','W','W','W','W','C','W'],
    ['W','C','W',' ','W','C','C','C','C','C','C','C','C','C','W',' ','W','C','W'],
    ['W','C','W','W','W','C','W','W','W',' ','W','W','W','C','W','W','W','C','W'],
    ['W','C','C','C','C','C','W',' ','W',' ','W',' ','W','C','C','C','C','C','W'],
    ['W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W'],
]


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


player = pac_sheet.get_image(pac_sheet.animate(0, 3, 100), 219.3333, 196, (cell_size - 4), BLACK)
    
def handle_movement(x, y, xv, yv, desired_xv, desired_yv, player, screen_width, screen_height, key):

    speed = 5

    # update desired velocity when a direction key is pressed (queue input)
    if key[pygame.K_a] or key[pygame.K_LEFT]:
        desired_xv, desired_yv = -speed, 0
    elif key[pygame.K_d] or key[pygame.K_RIGHT]:
        desired_xv, desired_yv = speed, 0
    elif key[pygame.K_w] or key[pygame.K_UP]:
        desired_xv, desired_yv = 0, -speed
    elif key[pygame.K_s] or key[pygame.K_DOWN]:
        desired_xv, desired_yv = 0, speed

    # Try to apply the desired movement first (attempt the queued turn/move)
    if (desired_xv != 0 or desired_yv != 0) and (desired_xv != xv or desired_yv != yv):
        temp_x = x + desired_xv
        temp_y = y + desired_yv
        temp_rect = player.get_rect(topleft=(temp_x, temp_y))
        collision = False
        for cell in cells:
            if isinstance(cell, wall) and temp_rect.colliderect(cell.rect):
                collision = True
                break
        if not collision:
            # safe to switch to desired direction
            xv = desired_xv
            yv = desired_yv
            # once executed, keep desired the same (it matches current), or clear if you prefer
            desired_xv, desired_yv = xv, yv

    # horizontal movement + collision
    x += xv
    player_rect = player.get_rect(topleft=(x, y))
    for cell in cells:
        if isinstance(cell, wall):
            if player_rect.colliderect(cell.rect):
                x -= xv
                xv = 0
                break

    # vertical movement + collision
    y += yv
    player_rect = player.get_rect(topleft=(x, y))
    for cell in cells:
        if isinstance(cell, wall):
            if player_rect.colliderect(cell.rect):
                y -= yv
                yv = 0
                break

    # screen bounds
    if x > screen_width - player.get_size()[0]:
        x = screen_width - player.get_size()[0]
        xv = 0
    if x < 0:
        x = 0
        xv = 0
    if y > screen_height - player.get_size()[1]:
        y = screen_height - player.get_size()[1]
        yv = 0
    if y < 0:
        y = 0
        yv = 0

    return x, y, xv, yv, desired_xv, desired_yv



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
    # update coin images and rects
    for cell in cells:
        if isinstance(cell, dot):
            cell.image = coin_sheet.get_image(coin_sheet.animate(0, 6, 250), 133.5, 118, cell_size, BLACK)
            cell.rect = cell.image.get_rect(topleft=cell.pos)

    # Pass key to handle_movement (no mask). We also pass and receive the queued desired velocities
    x, y, xv, yv, desired_xv, desired_yv = handle_movement(
        x, y, xv, yv, desired_xv, desired_yv, player, screen_width, screen_height, key
    )

    # Orientation
    if xv < 0 and yv == 0:
        player = pygame.transform.flip(player, True, False)
    elif xv > 0 and yv == 0:
        player = pygame.transform.rotate(player, 0)
    elif yv < 0 and xv == 0:
        player = pygame.transform.rotate(player, 90)
    elif yv > 0 and xv == 0:
        player = pygame.transform.rotate(player, -90)

    # build player rect once for collision checks
    player_rect = player.get_rect(topleft=(x, y))

    screen.blit(player, (x, y))
    for cell in cells:
        screen.blit(cell.image, cell.pos)

    # Collision detection with coin (iterate over a copy to avoid issues)
    for cell in cells[:]:
        if isinstance(cell, dot):
            if player_rect.colliderect(cell.rect):
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

    if score >= 123:
        run = False
        screen.fill(BLACK)
        draw_text("You win!", my_font, (0, 255, 0), screen_width/2 - 150, screen_height/2 - 50, 2)
        draw_text("Your time was: " + str(pygame.time.get_ticks()//1000) + " seconds", my_font, (0, 255, 0), screen_width/2 - 250, screen_height/2 + 50, 2)
        pygame.display.update()
        pygame.time.delay(5000)

    pygame.display.update()
    
pygame.quit()