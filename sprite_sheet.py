import pygame
animation_users = {}
current_time = pygame.time.get_ticks()
previous_time = current_time
class SpriteSheet():
    def __init__(self, image):
        self.sheet = image

    def get_image(self, frame, width, height, scale, color):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(color)
        return image
    
    def animate(self, id, start_frame, end_frame, wait):
        current_time = pygame.time.get_ticks()
    
        # Initialize animation state for the given id if not already present
        if id not in animation_users:
            animation_users[id] = [start_frame, current_time]
    
        frame_number, previous_time = animation_users[id]
    
        # Update frame if enough time has passed
        if current_time - previous_time >= wait:
            frame_number += 1
            previous_time = current_time
    
        # Loop back to start_frame if frame_number exceeds end_frame
        if frame_number >= end_frame:
            frame_number = start_frame
    
        # Update the animation state
        animation_users[id] = [frame_number, previous_time]
    
        return frame_number