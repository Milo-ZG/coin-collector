import pygame

def handle_movement(x, y, xv, yv, desired_xv, desired_yv, player, cells, wall, screen_width, screen_height, key):

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
