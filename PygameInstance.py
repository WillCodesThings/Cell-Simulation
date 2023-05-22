import pygame
import random
from brain import NNet
# Define the Cell class


class Cell(pygame.sprite.Sprite):
    def __init__(self, x, y, size, color, width, height, speed):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = speed
        self.canvas_width = width
        self.canvas_height = height

    def update(self, cells):
        # Move the cell randomly

        # Ensure the cell stays within the canvas boundaries
        self.rect.x = max(
            0, min(self.rect.x, self.canvas_width - self.rect.width))
        self.rect.y = max(
            0, min(self.rect.y, self.canvas_height - self.rect.height))

        # Check for collisions with other cells
        for cell in cells:
            if cell != self and self.rect.colliderect(cell.rect):
                dx = self.rect.x - cell.rect.x
                dy = self.rect.y - cell.rect.y
                distance = (dx ** 2 + dy ** 2) ** 0.5
                min_distance = (self.rect.width + cell.rect.width) / 2

                if distance != 0 and distance < min_distance:
                    overlap = min_distance - distance
                    overlap_x = overlap * dx / distance
                    overlap_y = overlap * dy / distance

                    self.rect.x += int(overlap_x / 2)
                    self.rect.y += int(overlap_y / 2)
                    cell.rect.x -= int(overlap_x / 2)
                    cell.rect.y -= int(overlap_y / 2)


# Initialize Pygame
pygame.init()

# Set up the canvas
width, height = 800, 600
canvas = pygame.display.set_mode((width, height))
pygame.display.set_caption("Random Cell Movement")

# Create a group for all sprites
all_sprites = pygame.sprite.Group()

# Create the cells
num_cells = 10
cell_size = 20
cell_color = (255, 0, 0)  # Red

cells = []
for _ in range(num_cells):
    x = random.randint(0, width - cell_size)
    y = random.randint(0, height - cell_size)
    speed = random.randint(1, 5)
    cell = Cell(x, y, cell_size, cell_color, width, height, speed)
    cells.append(cell)
    all_sprites.add(cell)

# Set up the clock
clock = pygame.time.Clock()

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update all sprites
    all_sprites.update(cells)

    # Clear the canvas
    canvas.fill((255, 255, 255))  # White

    # Draw all sprites
    all_sprites.draw(canvas)

    # Update the display
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(30)

# Quit the game
pygame.quit()
