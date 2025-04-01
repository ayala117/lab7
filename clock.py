import pygame
import time
import math
import os


pygame.init()

# Экран параметрлері
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lab 7 - Clock, Music Player, Ball Movement")


WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)


clock_image = pygame.image.load("Clock.png").convert_alpha()
right_hand = pygame.image.load("right_hand.png").convert()  # Минут стрелкасы
left_hand = pygame.image.load("left_hand.png").convert()  # Секунд стрелкасы

# Ақ түсті мөлдір ету
right_hand.set_colorkey((255, 255, 255))
left_hand.set_colorkey((255, 255, 255))

# Қолдарды масштабтау (кішірейту)
right_hand = pygame.transform.scale(right_hand, (120, 50))  
left_hand = pygame.transform.scale(left_hand, (150, 30))  

# Сағаттың ортасы
center_x, center_y = WIDTH // 2, HEIGHT // 2

# Шар параметрлері
ball_radius = 10
ball_x, ball_y = center_x, center_y
ball_speed = 20

# Музыка ойнатқыш
music_files = ["song1.mp3", "song2.mp3", "song3.mp3"]
current_song = 0

pygame.mixer.init()

def play_music():
    if os.path.exists(music_files[current_song]):
        pygame.mixer.music.load(music_files[current_song])
        pygame.mixer.music.play()

running = True
while running:
    screen.fill(WHITE)

    # Сағатты салу
    screen.blit(clock_image, (center_x - clock_image.get_width() // 2, center_y - clock_image.get_height() // 2))

    # Уақытты алу
    current_time = time.localtime()
    minute_angle = (current_time.tm_min % 60) * 6
    second_angle = (current_time.tm_sec % 60) * 6

    # Қолдарды бұру
    rotated_minute_hand = pygame.transform.rotate(right_hand, -minute_angle)
    rotated_second_hand = pygame.transform.rotate(left_hand, -second_angle)

    # Минут стрелкасы
    minute_rect = rotated_minute_hand.get_rect(center=(center_x, center_y))
    screen.blit(rotated_minute_hand, minute_rect.topleft)

    # Секунд стрелкасы
    second_rect = rotated_second_hand.get_rect(center=(center_x, center_y))
    screen.blit(rotated_second_hand, second_rect.topleft)

    # Шарды салу
    pygame.draw.circle(screen, RED, (ball_x, ball_y), ball_radius)

    pygame.display.flip()

    # Оқиғаларды өңдеу (Event Handling)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and ball_y - ball_speed >= ball_radius:
                ball_y -= ball_speed
            elif event.key == pygame.K_DOWN and ball_y + ball_speed <= HEIGHT - ball_radius:
                ball_y += ball_speed
            elif event.key == pygame.K_LEFT and ball_x - ball_speed >= ball_radius:
                ball_x -= ball_speed
            elif event.key == pygame.K_RIGHT and ball_x + ball_speed <= WIDTH - ball_radius:
                ball_x += ball_speed

            # Музыка басқару
            elif event.key == pygame.K_p:  # Ойнату (Play)
                play_music()
            elif event.key == pygame.K_s:  # Тоқтату (Stop)
                pygame.mixer.music.stop()
            elif event.key == pygame.K_RIGHTBRACKET:  # Келесі ән
                current_song = (current_song + 1) % len(music_files)
                play_music()
            elif event.key == pygame.K_LEFTBRACKET:  # Алдыңғы ән
                current_song = (current_song - 1) % len(music_files)
                play_music()

    pygame.time.delay(50)

pygame.quit()