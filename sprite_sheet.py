import pygame
current_time = pygame.time.get_ticks()
class SpriteSheet():
    def __init__(self, image):
        self.sheet = image

    def get_image(self, frame, width, height, scale, color):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(color)
        return image
    
    def animate(self, start_frame, end_frame, wait):
        current_time = pygame.time.get_ticks()
    
        # Initialize animation state for the given id if not already present
        if not hasattr(self, 'frame_number'):
            self.frame_number = start_frame
            self.previous_time = current_time
    
        # Update frame if enough time has passed
        if current_time - self.previous_time >= wait:
            self.frame_number += 1
            self.previous_time = current_time

        # Loop back to start_frame if frame_number exceeds end_frame
        if self.frame_number >= end_frame:
            self.frame_number = start_frame
    
        return self.frame_number