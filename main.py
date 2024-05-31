import pygame
import time
import string
import re

pygame.init()

screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h

screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)

font = pygame.font.Font(None, 36)

background_color = (51, 51, 51)
nothing_color = (255, 255, 255)
something_color = (0, 0, 0)
regular_text_color = (113, 112, 112)

def render_text(text, location, color):
    words = re.findall(r'\b\w+\b', text)
    punctuations = re.findall(r'\W+', text)
    total_width = sum(font.size(word)[0] for word in words) + sum(font.size(punc)[0] for punc in punctuations)
    x_offset = location[0] - total_width // 2

    for word, punc in zip(words, punctuations + ['']):
        word_color = color

        lower_word = word.lower()
        if lower_word == "nothing":
            word_color = nothing_color
        elif lower_word == "something":
            word_color = something_color


        word_surface = font.render(word, True, word_color)
        word_rect = word_surface.get_rect(topleft=(x_offset, location[1]))
        screen.blit(word_surface, word_rect)
        x_offset += word_surface.get_width()

        punc_surface = font.render(punc, True, color)
        punc_rect = punc_surface.get_rect(topleft=(x_offset, location[1]))
        screen.blit(punc_surface, punc_rect)
        x_offset += punc_surface.get_width()

        # print(f"Word: {word}, Color: {word_color}, Location: {x_offset, location[1]}")


def game_loop():
    start_time = None
    key_pressed = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if start_time is None and not key_pressed:
                    start_time = time.time()
                    key_pressed = True
                elif start_time is not None:
                    elapsed_time = int(time.time() - start_time)
                    screen.fill(background_color)
                    render_text(f"You did Something, you lost\n You did Nothing for {format_time(elapsed_time)}", (screen_width//2, screen_height//2), regular_text_color)
                    pygame.display.flip()
                    time.sleep(2)
                    start_time = None
                    key_pressed = False

        screen.fill(background_color)

        if start_time is None:
            if not key_pressed:
                render_text("Press any key to start doing Nothing", (screen_width//2, screen_height//2), regular_text_color)
            else:
                render_text("Press any key to continue doing Nothing", (screen_width//2, screen_height//2), regular_text_color)
        elif start_time is not None:
            elapsed_time = int(time.time() - start_time)
            render_text(f"You have been doing Nothing for {format_time(elapsed_time)}", (screen_width//2, screen_height//2), regular_text_color)

        pygame.display.flip()

def format_time(seconds):
    periods = [
        ('week', 60*60*24*7),
        ('day', 60*60*24),
        ('hour', 60*60),
        ('minute', 60),
        ('second', 1)
    ]

    strings=[]
    for period_name, period_seconds in periods:
        if seconds >= period_seconds:
            period_value , seconds = divmod(seconds,period_seconds)
            strings.append(f"{period_value} {period_name}{'s' if period_value > 1 else ''}")

    return ", ".join(strings)

game_loop()

pygame.quit()