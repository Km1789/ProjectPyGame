import pygame



# отдельно переменные
display_width = 800
display_height = 600

display = pygame.display.set_mode((display_width, display_height))

mouse_counter = 0
need_draw_click = False

usr_width = 60
usr_height = 92
usr_x = display_width // 3
usr_y = display_height - 100 - usr_height

clock = pygame.time.Clock()

