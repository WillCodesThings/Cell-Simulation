import pygame
import random
import brain as br
import nodes
import base64
import math

# Define the Cell class
GENOMELENGTH = 3
width, height = 500, 500


class Cell(pygame.sprite.Sprite):
    def __init__(
        self,
        x,
        y,
        size,
        color,
        width,
        height,
        cellNumber,
        genomeLength,
        NN,
        energy=2,
        offspring=False,
    ):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.cellColor = color
        self.image.fill(self.cellColor)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.canvas_width = width
        self.canvas_height = height
        self.cellNum = cellNumber
        self.cellX = self.rect.center[0]
        self.cellY = self.rect.center[1]
        self.energy = energy
        self.cellSize = size
        self.speed = random.randint(1, 5)
        self.NN = NN
        self.selected = False
        self.genomeLength = genomeLength
        self.offspring = offspring
        self.reproduced = False

    def returnGenes(self):
        return self.NN.returnGenome()

    def reproduce(self, mutationRate, NN, cells):
        NN = self.NN.mutate(mutationRate)
        new_color = (
            min(self.cellColor[0] + 1, 255),
            min(self.cellColor[1] + 1, 255),
            min(self.cellColor[2] + 1, 255),
        )
        newCell = Cell(
            random.randint(0, width - cell_size),
            random.randint(0, width - cell_size),
            self.cellSize,
            new_color,
            width,
            height,
            len(cells) + 1,
            self.genomeLength,
            NN,
            self.energy - 0.6,
            True,
        )
        all_sprites.add(newCell)
        cells.append(newCell)
        self.energy -= 1

    def update(self, cells, biomassLoc):
        self.mutationRate = random.random()
        # Move the cell randomly
        if self.energy <= 0:
            all_sprites.remove(self)
        elif self.energy > 1 and not self.reproduced and not self.NN == None:
            self.reproduce(0.2, self.NN, cells)
            self.reproduced = True
        TouchingCellss = []
        if self.NN == None:
            self.NN = br.NNet(
                [nodes.eyesight, nodes.Touch],
                [nodes.HiddenNode],
                [
                    nodes.Consume,
                    nodes.MoveF,
                    nodes.MoveL,
                    nodes.MoveR,
                    nodes.MoveB,
                    nodes.RotationL,
                    nodes.RotationR,
                ],
                self.genomeLength,
                self.cellX,
                self.cellY,
                [(h.rect.x, h.rect.y) for h in cells],
            )
        if self.NN.carnivoreRate >= 0.6:
            self.NN.cellsLoc = cells
        else:
            self.NN.cellsLoc = biomassLoc
        currentChoiceOfNetwork = self.NN.feedForeward()
        distanceofcells = []
        if isinstance(currentChoiceOfNetwork[0], nodes.Consume):
            if self.NN.carnivoreRate >= 0.6:
                for i in cells:
                    if (
                        (i.rect.x >= (self.cellX - ((self.cellSize) ** 2)))
                        and (i.rect.x <= (self.cellX + ((self.cellSize) ** 2)))
                    ) and (
                        (i.rect.y >= (self.cellY - ((self.cellSize) ** 2)))
                        and ((i.rect.y <= self.cellY + ((self.cellSize) ** 2)))
                    ):
                        if self.cellNum != i.cellNum:
                            TouchingCellss.append((self.cellX, self.cellY, i.cellNum))
                            distanceofcells.append(
                                math.sqrt(
                                    ((i.cellX - self.cellX) ** 2)
                                    + ((i.cellY - self.cellY) ** 2)
                                )
                            )
                        else:
                            pass

                for h in all_sprites:
                    try:
                        if (
                            h.cellNum
                            != TouchingCellss.index(
                                distanceofcells.index(min(distanceofcells))
                            )[2]
                        ):
                            all_sprites.remove(h)
                            cells.remove(h)
                            self.energy += 0.4
                            break
                    except:
                        pass
            else:
                for i in biomassLoc:
                    distance = math.sqrt(
                        ((self.cellX - i.rect.x) ** 2) + ((self.cellY - i.rect.y) ** 2)
                    )
                    if distance <= 20:
                        distanceofcells.append((distance, i))
                for h in biomass_sprites:
                    try:
                        if (
                            h.cellNum
                            != TouchingCellss.index(
                                distanceofcells.index(min(distanceofcells))
                            )[2]
                        ):
                            biomass_sprites.remove(h)
                            biomass.remove(h)
                            self.energy += 0.2
                            break
                    except:
                        pass

        elif isinstance(currentChoiceOfNetwork[0], nodes.MoveF):
            self.rect.y += self.speed
            self.cellY += self.speed
            self.energy -= self.speed / 1000
        elif isinstance(currentChoiceOfNetwork[0], nodes.MoveB):
            self.rect.y -= self.speed
            self.cellY -= self.speed
            self.energy -= self.speed / 1000
        elif isinstance(currentChoiceOfNetwork[0], nodes.MoveL):
            self.rect.x -= self.speed
            self.cellX -= self.speed
            self.energy -= self.speed / 1000
        elif isinstance(currentChoiceOfNetwork[0], nodes.MoveR):
            self.rect.x += self.speed
            self.cellX += self.speed
            self.energy -= self.speed / 1000
        elif isinstance(currentChoiceOfNetwork[0], nodes.RotationL):
            try:
                self.NN.InputWeight.rotateL()
                self.energy -= 0.001
            except:
                pass
        elif isinstance(currentChoiceOfNetwork[0], nodes.RotationR):
            try:
                self.NN.InputWeight.rotateR()
                self.energy -= 0.001
            except:
                pass

        # Ensure the cell stays within the canvas boundaries
        self.rect.x = max(0, min(self.rect.x, self.canvas_width - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, self.canvas_height - self.rect.height))

        # Check for collisions with other cells
        for cell in cells:
            if cell != self and self.rect.colliderect(cell.rect):
                dx = self.rect.x - cell.rect.x
                dy = self.rect.y - cell.rect.y
                distance = (dx**2 + dy**2) ** 0.5
                min_distance = (self.rect.width + cell.rect.width) / 2

                if distance != 0 and distance < min_distance:
                    overlap = min_distance - distance
                    overlap_x = overlap * dx / distance
                    overlap_y = overlap * dy / distance

                    self.rect.x += int(overlap_x / 2)
                    self.rect.y += int(overlap_y / 2)
                    cell.rect.x -= int(overlap_x / 2)
                    cell.rect.y -= int(overlap_y / 2)
        for cell in biomassLoc:
            if cell != self and self.rect.colliderect(cell.rect):
                dx = self.rect.x - cell.rect.x
                dy = self.rect.y - cell.rect.y
                distance = (dx**2 + dy**2) ** 0.5
                min_distance = (self.rect.width + cell.rect.width) / 2

                if distance != 0 and distance < min_distance:
                    overlap = min_distance - distance
                    overlap_x = overlap * dx / distance
                    overlap_y = overlap * dy / distance

                    self.rect.x += int(overlap_x / 2)
                    self.rect.y += int(overlap_y / 2)
                    cell.rect.x -= int(overlap_x / 2)
                    cell.rect.y -= int(overlap_y / 2)


class Biomass(pygame.sprite.Sprite):
    def __init__(self, x, y, size, color, cellNum):
        super().__init__()
        # ease of use, dont have to change code in cell update function.
        self.cellNum = cellNum
        self.cellX = x
        self.cellY = y
        # other stuff #
        self.image = pygame.Surface((size, size))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


# Initialize Pygame
pygame.init()

# Set up the canvas

canvas = pygame.display.set_mode((width, height))
pygame.display.set_caption("Seeing Life -- WillCodesThings")

# Create a group for all sprites
all_sprites = pygame.sprite.Group()
biomass_sprites = pygame.sprite.Group()

# Create the cells
num_cells = 250
cell_size = 5
cell_color = (255, 0, 0)  # Red

cells = []
for _ in range(num_cells):
    x = random.randint(0, width - cell_size)
    y = random.randint(0, height - cell_size)
    cell = Cell(x, y, cell_size, cell_color, width, height, _ + 1, GENOMELENGTH, None)
    cells.append(cell)
    all_sprites.add(cell)

# Create the biomass sprites
num_biomass = 200
biomass_size = 3
biomass_color = (0, 255, 0)  # Green

currentBiomass = []
for _ in range(num_biomass):
    x = random.randint(0, width - biomass_size)
    y = random.randint(0, height - biomass_size)
    biomass = Biomass(x, y, biomass_size, biomass_color, _ + 1)
    currentBiomass.append(biomass)
    biomass_sprites.add(biomass)

# Zoom variables
zoom_center = pygame.Vector2(width // 2, height // 2)
zoom_factor = 1.0


def GETRAYCAST(x, y, pointa, pointb, eyesightStrength, zoom_factor):
    eyesight_strength = eyesightStrength  # Define the eyesight strength for FOV
    radius = eyesightStrength  # Define the radius of the FOV circle
    segment_color = (255, 0, 0)  # Red

    # Calculate the start and stop points for the FOV segment
    start_point = math.radians(pointa)
    stop_point = math.radians(pointb)

    # Calculate the scaled radius based on the zoom factor
    scaled_radius = int(radius * zoom_factor)

    # Calculate the scaled cell position based on the zoom factor
    scaled_x = int(x * zoom_factor)
    scaled_y = int(y * zoom_factor)

    # Create a scaled rectangle for the FOV segment
    fov_rect = pygame.Rect(
        scaled_x - scaled_radius,
        scaled_y - scaled_radius,
        scaled_radius * 2,
        scaled_radius * 2,
    )

    # Draw the FOV segment on the canvas
    pygame.draw.arc(
        canvas, segment_color, fov_rect, start_point, stop_point, scaled_radius
    )


def render_ui(selected_cell, canvas, zoom_factor):
    # Define the UI parameters
    ui_font_size = int(16 * zoom_factor)
    ui_width = 200
    ui_height = 100
    ui_padding = 10
    ui_font = pygame.font.Font(None, 24)
    ui_bg_color = (255, 255, 255)
    ui_text_color = (0, 0, 0)

    # Create the UI surface
    ui_surface = pygame.Surface((ui_width, ui_height))
    ui_surface.fill(ui_bg_color)

    # Render the selected cell's stats
    if selected_cell:
        energy_text = ui_font.render(
            f"Energy: {selected_cell.energy:.2f}", True, ui_text_color
        )
        speed_text = ui_font.render(
            f"Speed: {selected_cell.speed}", True, ui_text_color
        )

        # Adjust the position and size of UI elements based on the zoom factor
        scaled_ui_padding = int(ui_padding * zoom_factor)
        scaled_ui_font_size = int(ui_font_size * zoom_factor)

        # Update the font size for rendering text
        ui_font = pygame.font.Font(None, scaled_ui_font_size)

        # Blit the text onto the UI surface
        ui_surface.blit(energy_text, (scaled_ui_padding, scaled_ui_padding))
        ui_surface.blit(speed_text, (scaled_ui_padding, scaled_ui_padding + 30))

    # ...

    # Blit the UI surface onto the canvas
    canvas.blit(ui_surface, (ui_padding, ui_padding))


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
    all_sprites.update(cells, currentBiomass)

    # Clear the canvas
    canvas.fill((255, 255, 255))  # White

    # Check if there is a selected cell
    if selected_cell:
        # Update zoom center to selected cell's position
        # Update zoom center to selected cell's position
        zoom_center = (
            pygame.Vector2(selected_cell.cellX, selected_cell.cellY) * zoom_factor
        )

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
            GETRAYCAST(
                selected_cell.cellX,
                selected_cell.cellY,
                selected_cell.NN.degrees[0],
                selected_cell.NN.degrees[1],
                selected_cell.NN.randomizedEyesightStrength,
                zoom_factor,
            )
        except AttributeError:
            pass

        # Draw the scaled canvas on the main canvas
        canvas.fill((255, 255, 255))  # Clear the canvas with white color
        canvas.blit(scaled_canvas, (0, 0), scaled_rect)

        # Reset selected cell's position after drawing
        selected_cell.rect.center = (selected_cell.cellX, selected_cell.cellY)
        if scaled_rect.left < 0:
            scaled_rect.left = 0
        if scaled_rect.right > width:
            scaled_rect.right = width
        if scaled_rect.top < 0:
            scaled_rect.top = 0
        if scaled_rect.bottom > height:
            scaled_rect.bottom = height
        selected_cell.selected = False

    else:
        # Draw all sprites on the main canvas
        canvas.fill((255, 255, 255))  # Clear the canvas with white color
        all_sprites.draw(canvas)
    biomass_sprites.draw(canvas)
    # render_ui(selected_cell, canvas, zoom_factor)
    # Update the display
    pygame.display.flip()
    # Limit the frame rate
    clock.tick(30)

# Quit the game
pygame.quit()
