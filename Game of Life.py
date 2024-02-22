import random
import pygame, sys
from button import Button

pygame.init()

BLACK = (0, 0, 0)
GREY = (128, 128, 128)
YELLOW = (255, 255, 0)

WIDTH, HEIGHT = 1280, 720
FPS = 200


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu")
clock = pygame.time.Clock()

BG = pygame.image.load("assets/Background.png")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

def gen(num):
    return set(((random.randrange(0, HEIGHT), random.randrange(0, WIDTH)) for _ in range(num)))


def draw_grid(positions, TILE_SIZE, GRID_HEIGHT, GRID_WIDTH):
    for position in positions:
        col, row = position
        top_left = (col * TILE_SIZE, row * TILE_SIZE)
        pygame.draw.rect(screen, YELLOW, (*top_left, TILE_SIZE, TILE_SIZE))
    for row in range(GRID_HEIGHT):
        pygame.draw.line(screen, BLACK, (0, row * TILE_SIZE), (WIDTH, row * TILE_SIZE))
    for col in range(GRID_WIDTH):
        pygame.draw.line(screen, BLACK, (col * TILE_SIZE, 0), (col * TILE_SIZE, HEIGHT))
def adjust_grid(positions, GRID_WIDTH, GRID_HEIGHT):
    all_neighbors = set()
    new_positions = set()

    for position in positions:
        neighbors = get_neighbors(position, GRID_HEIGHT, GRID_WIDTH)
        all_neighbors.update(neighbors)

        neighbor_count = sum((1 for neighbor in neighbors if neighbor in positions))

        if neighbor_count in [2, 3]:
            new_positions.add(position)

    for position in all_neighbors - positions:
        neighbors = get_neighbors(position, GRID_HEIGHT, GRID_WIDTH)
        neighbor_count = sum((1 for neighbor in neighbors if neighbor in positions))

        if neighbor_count == 3:
            new_positions.add(position)

    return new_positions
def get_neighbors(pos, GRID_HEIGHT, GRID_WIDTH):
    x, y = pos
    neighbors = []
    for dx in [-1, 0, 1]:
        if x + dx < 0 or x + dx >= GRID_HEIGHT:
            continue
        for dy in [-1, 0, 1]:
            if y + dy < 0 or y + dy >= GRID_WIDTH:
                continue
            if dx == 0 and dy == 0:
                continue
            neighbors.append((x + dx, y + dy))
    return neighbors

def play():
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        screen.fill("black")

        PLAY_TEXT = get_font(45).render("CHOOSE LEVEL:", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 100))
        screen.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_EASY = Button(image=None, pos=(200, 340),
                            text_input="EASY", font=get_font(80), base_color="Yellow", hovering_color="Yellow")

        PLAY_NORMAL = Button(image=None, pos=(650, 340),
                           text_input="NORMAL", font=get_font(80), base_color="Yellow", hovering_color="Yellow")

        PLAY_HARD = Button(image=None, pos=(1090, 340),
                             text_input="HARD", font=get_font(80), base_color="Yellow", hovering_color="Yellow")
        PLAY_BACK = Button(image=None, pos=(640, 600),
                            text_input="BACK", font=get_font(65), base_color="White", hovering_color="Green")

        PLAY_EASY.changeColor(PLAY_MOUSE_POS)
        PLAY_EASY.update(screen)
        PLAY_NORMAL.changeColor(PLAY_MOUSE_POS)
        PLAY_NORMAL.update(screen)
        PLAY_HARD.changeColor(PLAY_MOUSE_POS)
        PLAY_HARD.update(screen)
        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_EASY.checkForInput(PLAY_MOUSE_POS):
                    easy()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_NORMAL.checkForInput(PLAY_MOUSE_POS):
                    normal()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_HARD.checkForInput(PLAY_MOUSE_POS):
                    hard()

        pygame.display.update()

def easy():
    TILE_SIZE_EASY = 40
    GRID_WIDTH_EASY = WIDTH // TILE_SIZE_EASY
    GRID_HEIGHT_EASY = HEIGHT // TILE_SIZE_EASY
    running = True
    playing = False
    count = 0
    update_frequency = 120

    positions = set()

    while running:

        clock.tick(FPS)

        if playing and count >= update_frequency:
            positions = adjust_grid(positions, GRID_HEIGHT_EASY, GRID_WIDTH_EASY)
            count = 0

        pygame.display.set_caption("Playing" if playing else "Paused")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col = x // TILE_SIZE_EASY
                row = y // TILE_SIZE_EASY
                pos = (col, row)

                if pos in positions:
                    positions.remove(pos)
                else:
                    positions.add(pos)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    playing = not playing

                if event.key == pygame.K_c:
                    positions = set()
                    playing = False
                    count = 0
                if event.key == pygame.K_g:
                    positions = gen(random.randrange(30, 50) * WIDTH)
                if event.key == pygame.K_b:
                    play()

        screen.fill(GREY)
        draw_grid(positions, TILE_SIZE_EASY, GRID_HEIGHT_EASY, GRID_WIDTH_EASY)
        pygame.display.update()

        if playing:
            count += 1

    pygame.quit()

def normal():
    TILE_SIZE_NORMAL = 20
    GRID_WIDTH_NORMAL = WIDTH // TILE_SIZE_NORMAL
    GRID_HEIGHT_NORMAL = HEIGHT // TILE_SIZE_NORMAL

    running = True
    playing = False
    count = 0
    update_frequency = 120
    positions = set()

    while running:
        clock.tick(FPS)

        if playing and count >= update_frequency:
            positions = adjust_grid(positions, GRID_HEIGHT_NORMAL, GRID_WIDTH_NORMAL)
            count = 0

        pygame.display.set_caption("Playing" if playing else "Paused")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col = x // TILE_SIZE_NORMAL
                row = y // TILE_SIZE_NORMAL
                pos = (col, row)

                if pos in positions:
                    positions.remove(pos)
                else:
                    positions.add(pos)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    playing = not playing

                if event.key == pygame.K_c:
                    positions = set()
                    playing = False
                    count = 0
                if event.key == pygame.K_g:
                    positions = gen(random.randrange(80, 100) * WIDTH)
                if event.key == pygame.K_b:
                    play()

        screen.fill(GREY)
        draw_grid(positions, TILE_SIZE_NORMAL, GRID_WIDTH_NORMAL, GRID_WIDTH_NORMAL)
        pygame.display.update()

        if playing:
            count += 1

    pygame.quit()

def hard():
    TILE_SIZE_HARD = 10
    GRID_WIDTH_HARD = WIDTH // TILE_SIZE_HARD
    GRID_HEIGHT_HARD = HEIGHT // TILE_SIZE_HARD
    running = True
    playing = False
    count = 0
    update_frequency = 120

    positions = set()

    while running:
        clock.tick(FPS)

        if playing and count >= update_frequency:
            positions = adjust_grid(positions, GRID_HEIGHT_HARD, GRID_WIDTH_HARD)
            count = 0

        pygame.display.set_caption("Playing" if playing else "Paused")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col = x // TILE_SIZE_HARD
                row = y // TILE_SIZE_HARD
                pos = (col, row)

                if pos in positions:
                    positions.remove(pos)
                else:
                    positions.add(pos)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    playing = not playing

                if event.key == pygame.K_c:
                    positions = set()
                    playing = False
                    count = 0
                if event.key == pygame.K_g:
                    positions = gen(random.randrange(160, 200) * WIDTH)
                if event.key == pygame.K_b:
                    play()

        screen.fill(GREY)
        draw_grid(positions, TILE_SIZE_HARD, GRID_HEIGHT_HARD, GRID_WIDTH_HARD)
        pygame.display.update()

        if playing:
            count += 1

    pygame.quit()


pygame.mixer.init()

# Load and play background music
pygame.mixer.music.load('C:\\Users\\nazir\\Downloads\\stranger-things-124008.mp3')  # Corrected path
pygame.mixer.music.play(-1)
def draw_volume_bar(volume):
    # Define bar dimensions
    bar_height = int(volume * HEIGHT)
    bar_y = HEIGHT - bar_height

    # Draw background bar (full height, gray)
    screen.blit(BG, (0, 0))
    # Draw foreground bar (volume level, green)
    screen.fill("yellow", (WIDTH - 60, bar_y, 40, bar_height))
    VOLUME_CONTROL = get_font(75).render("VOLUME CONTROL", True, "WHITE")
    VOLUME_RECT = VOLUME_CONTROL.get_rect(center=(640, 100))
    VOLUME_CONTROL_RULE = get_font(45).render("use LMB to change volume", True, "WHITE")
    VOLUME_CONTROL_RECT = VOLUME_CONTROL.get_rect(center=(640, 400))
    screen.blit(VOLUME_CONTROL, VOLUME_RECT)
    screen.blit(VOLUME_CONTROL_RULE, VOLUME_CONTROL_RECT)
def volume():
    # Set initial volume
    volume = 0.5  # Volume ranges from 0.0 to 1.0
    pygame.mixer.music.set_volume(volume)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:  # If left mouse button is pressed
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if WIDTH - 60 <= mouse_x <= WIDTH - 20:  # Within the volume bar area
                        volume = 1 - mouse_y / HEIGHT
                        volume = max(0.0, min(1.0, volume))  # Clamp volume to 0.0 - 1.0
                        pygame.mixer.music.set_volume(volume)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    options()

        # Drawing
        screen.fill((0, 0, 0))
        draw_volume_bar(volume)
        pygame.display.flip()
def rules():
    screen.blit(BG, (0, 0))
    while True:
        RULES = get_font(75).render("RULES", True, "WHITE")
        RULES_RECT = RULES.get_rect(center=(640, 100))
        RULES_TEXT1 = get_font(25).render("1. Birth: A dead cell with exactly three", True, "WHITE")
        RULES_TEXT1_RECT = RULES_TEXT1.get_rect(center=(640, 200))
        RULES_TEXT2 = get_font(25).render("live neighbors becomes a live cell", True, "WHITE")
        RULES_TEXT2_RECT = RULES_TEXT2.get_rect(center=(700, 240))
        RULES_TEXT3 = get_font(25).render("(as if by reproduction)", True, "WHITE")
        RULES_TEXT3_RECT = RULES_TEXT3.get_rect(center=(850, 280))
        RULES_TEXT4 = get_font(25).render("2. Survival: A live cell with two or three", True, "WHITE")
        RULES_TEXT4_RECT = RULES_TEXT4.get_rect(center=(640, 320))
        RULES_TEXT5 = get_font(25).render("live neighbors stays alive for", True, "WHITE")
        RULES_TEXT5_RECT = RULES_TEXT5.get_rect(center=(740, 360))
        RULES_TEXT6 = get_font(25).render("the next generation", True, "WHITE")
        RULES_TEXT6_RECT = RULES_TEXT6.get_rect(center=(880, 400))
        RULES_TEXT7 = get_font(25).render("3. Death: ", True, "WHITE")
        RULES_TEXT7_RECT = RULES_TEXT7.get_rect(center=(220, 440))
        RULES_TEXT8 = get_font(25).render("Overpopulation: A live cell with more than", True, "WHITE")
        RULES_TEXT8_RECT = RULES_TEXT8.get_rect(center=(640, 480))
        RULES_TEXT9 = get_font(25).render("three live neighbors dies.", True, "WHITE")
        RULES_TEXT9_RECT = RULES_TEXT9.get_rect(center=(740, 520))
        RULES_TEXT10 = get_font(25).render("in the next generation", True, "WHITE")
        RULES_TEXT10_RECT = RULES_TEXT10.get_rect(center=(880, 560))
        RULES_TEXT11 = get_font(25).render("Underpopulation: A live cell with fewer than", True, "WHITE")
        RULES_TEXT11_RECT = RULES_TEXT11.get_rect(center=(640, 600))
        RULES_TEXT12 = get_font(25).render("two live neighbors dies", True, "WHITE")
        RULES_TEXT12_RECT = RULES_TEXT12.get_rect(center=(890, 640))
        RULES_TEXT13 = get_font(25).render("in the next generation.", True, "WHITE")
        RULES_TEXT13_RECT = RULES_TEXT13.get_rect(center=(900, 680))
        screen.blit(RULES, RULES_RECT)
        screen.blit(RULES_TEXT1, RULES_TEXT1_RECT)
        screen.blit(RULES_TEXT2, RULES_TEXT2_RECT)
        screen.blit(RULES_TEXT3, RULES_TEXT3_RECT)
        screen.blit(RULES_TEXT4, RULES_TEXT4_RECT)
        screen.blit(RULES_TEXT5, RULES_TEXT5_RECT)
        screen.blit(RULES_TEXT6, RULES_TEXT6_RECT)
        screen.blit(RULES_TEXT7, RULES_TEXT7_RECT)
        screen.blit(RULES_TEXT8, RULES_TEXT8_RECT)
        screen.blit(RULES_TEXT9, RULES_TEXT9_RECT)
        screen.blit(RULES_TEXT10, RULES_TEXT10_RECT)
        screen.blit(RULES_TEXT11, RULES_TEXT11_RECT)
        screen.blit(RULES_TEXT12, RULES_TEXT12_RECT)
        screen.blit(RULES_TEXT13, RULES_TEXT13_RECT)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    options()
        pygame.display.update()
def control():
    screen.blit(BG, (0, 0))
    while True:
        CONTROL = get_font(75).render("CONTROL", True, "WHITE")
        CONTROL_RECT = CONTROL.get_rect(center=(640, 100))
        CONTROL_TEXT1 = get_font(25).render("1. To create and remove a live cell,", True, "WHITE")
        CONTROL_TEXT1_RECT = CONTROL_TEXT1.get_rect(center=(640, 200))
        CONTROL_TEXT2 = get_font(25).render("use the left mouse button on the cell", True, "WHITE")
        CONTROL_TEXT2_RECT = CONTROL_TEXT2.get_rect(center=(700, 240))
        CONTROL_TEXT4 = get_font(25).render("2. You can randomly generate a cell", True, "WHITE")
        CONTROL_TEXT4_RECT = CONTROL_TEXT4.get_rect(center=(625 , 320))
        CONTROL_TEXT5 = get_font(25).render("in different places by pressing", True, "WHITE")
        CONTROL_TEXT5_RECT = CONTROL_TEXT5.get_rect(center=(720, 360))
        CONTROL_TEXT3 = get_font(25).render("the G button", True, "WHITE")
        CONTROL_TEXT3_RECT = CONTROL_TEXT3.get_rect(center=(1000, 400))
        CONTROL_TEXT7 = get_font(25).render("3. To remove all cells, click C ", True, "WHITE")
        CONTROL_TEXT7_RECT = CONTROL_TEXT7.get_rect(center=(590, 480))
        CONTROL_TEXT8 = get_font(25).render("4. To return, click B", True, "WHITE")
        CONTROL_TEXT8_RECT = CONTROL_TEXT8.get_rect(center=(450, 560))
        CONTROL_TEXT9 = get_font(25).render("5. to play, click Space.", True, "WHITE")
        CONTROL_TEXT9_RECT = CONTROL_TEXT9.get_rect(center=(490, 640))
        screen.blit(CONTROL, CONTROL_RECT)
        screen.blit(CONTROL_TEXT1, CONTROL_TEXT1_RECT)
        screen.blit(CONTROL_TEXT2, CONTROL_TEXT2_RECT)
        screen.blit(CONTROL_TEXT3, CONTROL_TEXT3_RECT)
        screen.blit(CONTROL_TEXT4, CONTROL_TEXT4_RECT)
        screen.blit(CONTROL_TEXT5, CONTROL_TEXT5_RECT)
        screen.blit(CONTROL_TEXT7, CONTROL_TEXT7_RECT)
        screen.blit(CONTROL_TEXT8, CONTROL_TEXT8_RECT)
        screen.blit(CONTROL_TEXT9, CONTROL_TEXT9_RECT)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    options()
        pygame.display.update()
def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        screen.fill("black")

        OPTIONS_VOLUME = Button(image=None, pos=(640, 200),
                            text_input="VOLUME", font=get_font(75), base_color="Yellow", hovering_color="GREEN")
        OPTIONS_VOLUME.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_VOLUME.update(screen)
        OPTIONS_RULES = Button(image=None, pos=(640, 330),
                            text_input="RULES", font=get_font(75), base_color="Yellow", hovering_color="GREEN")
        OPTIONS_RULES.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_RULES.update(screen)
        OPTIONS_CONTROL = Button(image=None, pos=(640, 460),
                            text_input="CONTROL", font=get_font(75), base_color="Yellow", hovering_color="GREEN")
        OPTIONS_CONTROL.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_CONTROL.update(screen)
        OPTIONS_BACK = Button(image=None, pos=(640, 600),
                            text_input="BACK", font=get_font(75), base_color="white", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_VOLUME.checkForInput(OPTIONS_MOUSE_POS):
                    volume()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_RULES.checkForInput(OPTIONS_MOUSE_POS):
                    rules()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_CONTROL.checkForInput(OPTIONS_MOUSE_POS):
                    control()

        pygame.display.update()

def main_menu():
    running = True
    playing = False
    count = 0
    update_frequency = 60

    positions = set()

    while running:

        screen.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250),
                             text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400),
                                text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550),
                             text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        clock.tick(FPS)

        pygame.display.update()

        if playing:
            count += 1

main_menu()