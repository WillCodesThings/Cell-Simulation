import pygame
import random
import brain as br
import nodes
import base64
import math

# Define the Cell class


class Cell(pygame.sprite.Sprite):
    def __init__(self, x, y, size, color, width, height, cellNumber):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.canvas_width = width
        self.canvas_height = height
        self.cellNum = cellNumber
        self.cellX = self.rect.center[0]
        self.cellY = self.rect.center[1]
        self.energy = 1
        self.speed = random.randint(1, 5)
        self.NN = None
        self.selected = False

    def returnGenes(self):
        return self.NN.returnGenome()

    def update(self, cells):
        # Move the cell randomly
        TouchingCellss = []
        if self.NN == None:
            self.NN = br.NNet([nodes.eyesight, nodes.Touch], [nodes.HiddenNode], [nodes.Consume, nodes.MoveF, nodes.MoveL, nodes.MoveR, nodes.MoveB, nodes.RotationL, nodes.RotationR], 2,
                              self.cellX, self.cellY, [(h.rect.x, h.rect.y)for h in cells])
        print(self.NN.feedForeward())
        if isinstance(self.NN.feedForeward()[0], nodes.Consume):
            for i in cells:
                if ((i[0] >= (self.cellX-1)) and (i[0] <= (self.cellX+1))) and ((i[1] >= (self.cellY-1)) and ((i[1] <= self.cellY + self.NN.randomizedEyesightStrength))):
                    TouchingCellss.append((self.cellX, self.cellY, i.cellNum))
                    distanceofcells = [
                        ((i[0] >= ((self.cellX-1)) and (i[0] <= (self.cellX+1))) and (i[1] >= (self.cellY-1)))]

            for h in all_sprites:
                if (h.cellNum == TouchingCellss.index(distanceofcells.index(max(distanceofcells)))[2]):
                    all_sprites.remove(h)
                    break
        elif isinstance(self.NN.feedForeward()[0], nodes.MoveF):
            print("hello")
            self.rect.y += self.speed
            self.cellY += self.speed
            self.energy -= (self.speed/10)
        elif isinstance(self.NN.feedForeward()[0], nodes.MoveB):
            print("hello")
            self.rect.y -= self.speed
            self.cellY -= self.speed
            self.energy -= (self.speed/10)
        elif isinstance(self.NN.feedForeward()[0], nodes.MoveL):
            print("hello")
            self.rect.x -= self.speed
            self.cellX -= self.speed
            self.energy -= (self.speed/10)
        elif isinstance(self.NN.feedForeward()[0], nodes.MoveR):
            print("hello")
            self.rect.x += self.speed
            self.cellX += self.speed
            self.energy -= (self.speed/10)
        elif isinstance(self.NN.feedForeward()[0], nodes.RotationL):
            print("hello")
            self.NN.InputWeight.rotateL()
            self.energy -= 0.1
        elif isinstance(self.NN.feedForeward()[0], nodes.RotationR):
            print("hello")
            self.NN.InputWeight.rotateR()
            self.energy -= 0.1

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
pygame.display.set_caption("Zoomable Cellular Automation")

# Create a group for all sprites
all_sprites = pygame.sprite.Group()

# Create the cells
num_cells = 100
cell_size = 10
cell_color = (255, 0, 0)  # Red

cells = []
for _ in range(num_cells):
    x = random.randint(0, width - cell_size)
    y = random.randint(0, height - cell_size)
    cell = Cell(x, y, cell_size, cell_color, width, height, _ + 1)
    cells.append(cell)
    all_sprites.add(cell)

# Zoom variables
zoom_center = pygame.Vector2(width // 2, height // 2)
zoom_factor = 1.0


def GETRAYCAST(x, y, pointa, pointb, eyesightStrength):
    eyesight_strength = eyesightStrength  # Define the eyesight strength for FOV
    radius = eyesightStrength  # Define the radius of the FOV circle
    segment_color = (255, 0, 0)  # Red

    # Calculate the start and stop points for the FOV segment
    start_point = math.radians(pointa)
    stop_point = math.radians(pointb)

    # Draw the FOV segment on the canvas
    pygame.draw.arc(canvas, segment_color, self.rect,
                    start_point, stop_point, radius)


# Selected cell for zooming
selected_cell = None

# Set up the clock
clock = pygame.time.Clock()

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left button: Select a cell for zooming
                for cell in cells:
                    if cell.rect.collidepoint(event.pos):
                        selected_cell = cell
                        cell.selected = True
            elif event.button == 3:  # Right button: Unzoom
                selected_cell = None
                zoom_factor = 1.0

        elif event.type == pygame.MOUSEWHEEL:
            if selected_cell:
                if event.y > 0:  # Scroll up: Zoom in
                    zoom_factor += 0.1
                else:  # Scroll down: Zoom out
                    zoom_factor = max(0.1, zoom_factor - 0.1)
    # Update all sprites
    all_sprites.update(cells)

    # Clear the canvas
    canvas.fill((255, 255, 255))  # White

    # Check if there is a selected cell
    if selected_cell:
        # Update zoom center to selected cell's position
        zoom_center = selected_cell.rect.center

        # Update selected cell's position based on zoom
        selected_cell.rect.center = zoom_center

        # Scale the canvas based on zoom factor
        scaled_width = int(width * zoom_factor)
        scaled_height = int(height * zoom_factor)
        scaled_canvas = pygame.Surface((scaled_width, scaled_height))
        scaled_rect = scaled_canvas.get_rect(center=zoom_center)

        # Clear the scaled canvas with white color
        scaled_canvas.fill((255, 255, 255))

        # Draw all sprites on the scaled canvas
        all_sprites.draw(scaled_canvas)

        # Draw the FOV of the selected cell
        try:
            GETRAYCAST(selected_cell.cellX, selected_cell.cellY,
                       selected_cell.NN.degrees[0], selected_cell.NN.degrees[1], selected_cell.NN.randomizedEyesightStrength)
        except:
            pass

        # Draw the scaled canvas on the main canvas
        canvas.fill((255, 255, 255))  # Clear the canvas with white color
        canvas.blit(scaled_canvas, (0, 0), scaled_rect)

        # Reset selected cell's position after drawing
        selected_cell.rect.center = (selected_cell.cellX, selected_cell.cellY)
        selected_cell.selected = False

    else:
        # Draw all sprites on the main canvas
        canvas.fill((255, 255, 255))  # Clear the canvas with white color
        all_sprites.draw(canvas)

    # Update the display
    pygame.display.flip()
    # Limit the frame rate
    clock.tick(30)

# Quit the game
pygame.quit()
