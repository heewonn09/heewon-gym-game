import pygame
import random
import sys
import os

pygame.init()

# 화면 설정
screen_width = 480
screen_height = 640
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Heewon Gym Game - Final Syringe Edition")
clock = pygame.time.Clock()

font = pygame.font.Font(None, 40)
title_font = pygame.font.Font(None, 70)

selected_character_path = ""
character_scale = 1.0
junk_hit_count = 0

pygame.mixer.init()
pygame.mixer.music.load("C:\\Users\\heewon\\Desktop\\Python Workspace\\pygame_basic\\Buddy.mp3")
pygame.mixer.music.play(-1)

sound_protein = pygame.mixer.Sound("C:\\Users\\heewon\\Desktop\\Python Workspace\\pygame_basic\\protein.mp3")
sound_dumbbell = pygame.mixer.Sound("C:\\Users\\heewon\\Desktop\\Python Workspace\\pygame_basic\\dumbbell.mp3")
sound_junkfood = pygame.mixer.Sound("C:\\Users\\heewon\\Desktop\\Python Workspace\\pygame_basic\\junkfood.mp3")

# 이미지 로드
junk_food_images = [
    pygame.transform.scale(pygame.image.load(f"C:\\Users\\heewon\\Desktop\\Python Workspace\\pygame_basic\\junk{i}.png"), (60, 60))
    for i in range(1, 6)
]
protein_img = pygame.transform.scale(pygame.image.load("C:\\Users\\heewon\\Desktop\\Python Workspace\\pygame_basic\\protein.png"), (40, 40))
dumbbell_img = pygame.transform.scale(pygame.image.load("C:\\Users\\heewon\\Desktop\\Python Workspace\\pygame_basic\\dumbbell.png"), (60, 60))
syringe_img = pygame.transform.scale(pygame.image.load("C:\\Users\\heewon\\Desktop\\Python Workspace\\pygame_basic\\syringe.png"), (50, 50))

class Star(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((2, 2))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width)
        self.rect.y = random.randint(-20, screen_height)
        self.speed = random.uniform(0.5, 1.5)
    def update(self):
        self.rect.y += self.speed
        if self.rect.top > screen_height:
            self.rect.y = random.randint(-10, -1)
            self.rect.x = random.randint(0, screen_width)

stars = pygame.sprite.Group()
for _ in range(80):
    stars.add(Star())

class Protein(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = protein_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = -50
        self.speed = 4
    def update(self):
        self.rect.y += self.speed
        if self.rect.top > screen_height:
            self.kill()

class Dumbbell(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = dumbbell_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = -50
        self.speed = 5
    def update(self):
        self.rect.y += self.speed
        if self.rect.top > screen_height:
            self.kill()

class Syringe(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = syringe_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = -50
        self.speed = 3.5
    def update(self):
        self.rect.y += self.speed
        if self.rect.top > screen_height:
            self.kill()

def get_stage_background(stage):
    index = (stage - 1) % 3 + 1
    return pygame.image.load(f"C:\\Users\\heewon\\Desktop\\Python Workspace\\pygame_basic\\gym_stage{index}.jpg")

def draw_text_center(text, font, color, y):
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=(screen_width // 2, y))
    screen.blit(surface, rect)

def draw_button(text, x, y, w, h, color, font):
    pygame.draw.rect(screen, color, (x, y, w, h))
    label = font.render(text, True, (255, 255, 255))
    label_rect = label.get_rect(center=(x + w // 2, y + h // 2))
    screen.blit(label, label_rect)
    return pygame.Rect(x, y, w, h)

def start_screen():
    global selected_character_path
    bg = pygame.transform.scale(
        pygame.image.load("C:\\Users\\heewon\\Desktop\\Python Workspace\\pygame_basic\\character_intro.png"),
        (screen_width, screen_height)
    )
    while True:
        screen.blit(bg, (0, 0))
        draw_text_center("Raising Ronikolman", title_font, (255, 255, 255), 100)

        char1 = draw_button("Character 1", 70, 250, 150, 60, (100, 100, 255), font)
        char2 = draw_button("Character 2", 260, 250, 150, 60, (255, 100, 100), font)
        exit_btn = draw_button("Exit", 140, 400, 200, 60, (200, 50, 50), font)

        pygame.display.update()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                if char1.collidepoint(e.pos):
                    selected_character_path = "C:\\Users\\heewon\\Desktop\\Python Workspace\\pygame_basic\\Ronny1.PNG"
                    return
                elif char2.collidepoint(e.pos):
                    selected_character_path = "C:\\Users\\heewon\\Desktop\\Python Workspace\\pygame_basic\\character2.png"
                    return
                elif exit_btn.collidepoint(e.pos):
                    pygame.quit()
                    sys.exit()

def game():
    global character_scale, junk_hit_count
    character_scale = 1.0
    junk_hit_count = 0
    stage = 1
    score = 0

    original_image = pygame.image.load(selected_character_path)
    character = pygame.transform.scale(original_image, (100, 80))

    x = (screen_width - character.get_width()) // 2
    y = screen_height - character.get_height()
    speed = 10
    to_x = 0

    junk_y = 0
    junk_speed = 5
    junk_img = random.choice(junk_food_images)
    junk_x = random.randint(0, screen_width - junk_img.get_width())

    protein_items = pygame.sprite.Group()
    dumbbell_items = pygame.sprite.Group()
    syringe_items = pygame.sprite.Group()
    item_timer = pygame.time.get_ticks()
    dumbbell_timer = pygame.time.get_ticks()
    syringe_timer = pygame.time.get_ticks()

    running = True
    while running:
        dt = clock.tick(30)
        if score >= 10000 and stage == 1:
            stage = 2
            junk_speed += 2
            character_scale += 0.2
        elif score >= 20000 and stage == 2:
            stage = 3
            junk_speed += 2
            character_scale += 0.2
        elif score >= 30000:
            return "clear"

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_LEFT:
                    to_x = -speed
                elif e.key == pygame.K_RIGHT:
                    to_x = speed
            if e.type == pygame.KEYUP:
                if e.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    to_x = 0

        x += to_x
        x = max(0, min(screen_width - character.get_width(), x))

        junk_y += junk_speed
        if junk_y > screen_height:
            junk_y = 0
            junk_x = random.randint(0, screen_width - junk_img.get_width())
            junk_img = random.choice(junk_food_images)

        now = pygame.time.get_ticks()
        if now - item_timer > 5000:
            protein_items.add(Protein())
            item_timer = now
        if now - dumbbell_timer > 4000:
            dumbbell_items.add(Dumbbell())
            dumbbell_timer = now
        if now - syringe_timer > 7000:
            syringe_items.add(Syringe())
            syringe_timer = now

        character = pygame.transform.scale(original_image, (int(70 * character_scale), int(70 * character_scale)))
        rect_char = pygame.Rect(x, y, character.get_width(), character.get_height())
        rect_junk = pygame.Rect(junk_x, junk_y, junk_img.get_width(), junk_img.get_height())

        if rect_char.colliderect(rect_junk):
            junk_hit_count += 1
            sound_junkfood.play()
            if junk_hit_count >= 5:
                return score
            junk_y = 0
            junk_x = random.randint(0, screen_width - junk_img.get_width())
            junk_img = random.choice(junk_food_images)

        for item in protein_items:
            if rect_char.colliderect(item.rect):
                score += 500
                sound_protein.play()
                item.kill()

        for db in dumbbell_items:
            if rect_char.colliderect(db.rect):
                score += 1000
                sound_dumbbell.play()
                db.kill()

        for s in syringe_items:
            if rect_char.colliderect(s.rect):
                score += 2000
                character_scale += 0.2
                s.kill()

        bg = get_stage_background(stage)
        screen.blit(bg, (0, 0))
        stars.update()
        stars.draw(screen)
        protein_items.update()
        protein_items.draw(screen)
        dumbbell_items.update()
        dumbbell_items.draw(screen)
        syringe_items.update()
        syringe_items.draw(screen)
        screen.blit(character, (x, y))
        screen.blit(junk_img, (junk_x, junk_y))

        screen.blit(font.render(f"Score: {score}", True, (255, 255, 255)), (10, 10))
        screen.blit(font.render(f"Junk Hits: {junk_hit_count}/5", True, (255, 100, 100)), (10, 50))
        screen.blit(font.render(f"Stage: {stage}", True, (0, 255, 0)), (10, 90))
        pygame.display.update()

def game_over(score):
    save_high_score(score)
    high = load_high_score()
    while True:
        screen.fill((0, 0, 0))
        draw_text_center("Game Over", title_font, (255, 0, 0), 120)
        draw_text_center(f"Score: {score}", font, (255, 255, 255), 200)
        draw_text_center(f"High Score: {high}", font, (255, 215, 0), 260)

        restart = draw_button("Restart", 140, 360, 200, 60, (50, 150, 250), font)
        exit_btn = draw_button("Exit", 140, 440, 200, 60, (200, 50, 50), font)
        pygame.display.update()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                if restart.collidepoint(e.pos):
                    return
                elif exit_btn.collidepoint(e.pos):
                    pygame.quit()
                    sys.exit()

def game_clear():
    while True:
        screen.fill((0, 0, 0))
        draw_text_center("Game Clear!", title_font, (0, 255, 0), 200)
        btn = draw_button("Play Again", 140, 360, 200, 60, (50, 150, 250), font)
        pygame.display.update()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                if btn.collidepoint(e.pos):
                    return

while True:
    start_screen()
    result = game()
    if result == "clear":
        game_clear()
    else:
        game_over(result)
