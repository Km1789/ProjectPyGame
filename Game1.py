import pygame
import random   # импорт
from states import *
from save import *

pygame.init()

display_width = 800
display_height = 600  # дисплей



display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Dinosaur')
icon = pygame.image.load('Background/icon.png')   # загрузка спрайтов и музыки

pygame.mixer.music.load('background.mp3')
pygame.mixer.music.set_volume(0.3)

jump_sound = pygame.mixer.Sound('Sounds/Rrr.wav')
fall_sound = pygame.mixer.Sound('Sounds/Bdish.wav')
loss_sound = pygame.mixer.Sound('Sounds/loss.wav')
button_sound = pygame.mixer.Sound('Sounds/button.wav')

cactus_img = [pygame.image.load('Objects/Cactus0.png'), pygame.image.load('Objects/Cactus1.png'),
              pygame.image.load('Objects/Cactus2.png')]
cactus_options = [69, 449, 37, 410, 40, 420]
stone_img = [pygame.image.load('Objects/Stone0.png'), pygame.image.load('Objects/Stone1.png')]
cloud_img = [pygame.image.load('Objects/Cloud0.png'), pygame.image.load('Objects/Cloud1.png')]
dino_img = [pygame.image.load('Dino0.png')]


heart_img = pygame.image.load('Effects/heart.png')
need_input = True
input_text = '|'
input_tick = 30
img_counter = 0  # переменные
health = 3
game_state = GameState()
save_data = Save()


def start():  # функция отвечающая за состояния
    global max_scores
    while True:
        if game_state.check(State.MENU):
            show_menu()
        elif game_state.check(State.START):

            start_game()
        elif game_state.check(State.CONTINUE):
            max_scores = save_data.get('max')
            start_game()
        elif game_state.check(State.QUIT):
            save_data.save()
            save_data.add('max', max_scores)
            break


class Object:  # сщздание объектов
    def __init__(self, x, y, width, image, speed):
        self.x = x
        self.y = y
        self.width = width
        self.image = image
        self.speed = speed

    def move(self):
        if self.x >= -self.width:
            display.blit(self.image, (self.x, self.y))
            self.x -= self.speed
            return True
        else:
            return False

    def return_self(self, radius, y, width, image):
        self.x = radius
        self.y = y
        self.width = width
        self.image = image
        display.blit(self.image, (self.x, self.y))


class Button: # создание кнопок
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.inactive_clr = (13, 162, 58)
        self.active_clr = (0, 255, 0)
        self.draw_effects = False
        self.rect_h = 10
        self.rect_w = width
        self.clear_effects = False

    def draw(self, x, y, message, action=None, font_size=30): # курсор и кнопки
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            if click[0] == 1:
                pygame.mixer.Sound.play(button_sound)
                pygame.time.delay(300)
                if action is not None:
                    if action == quit:
                        pygame.quit()
                        quit()
                    else:
                        action()
                else:
                    return True
        self.draw_beautiful_rect(mouse[0], mouse[1], x, y)
        print_text(message=message, x=x + 10, y=y + 10, font_size=font_size)

    def draw_beautiful_rect(self, ms_x, ms_y, x, y): # оформление кнопок
        if x <= ms_x <= x + self.width and y <= ms_y <= y + self.height:
            self.draw_effects = True
        if self.draw_effects:
            if ms_x < x or ms_x > x + self.width or ms_y < y or ms_y > y + self.height:
                self.clear_effects = True
                self.draw_effects = False
            if self.rect_h < self.height:
                self.rect_h += (self.height - 10) / 40
        if self.clear_effects and not self.draw_effects:
            if self.rect_h > 10:
                self.rect_h -= (self.height - 10) / 40
            else:
                self.clear_effects = False
        draw_y = y + self.height - self.rect_h
        pygame.draw.rect(display, self.active_clr, (x, draw_y, self.rect_w, self.rect_h))



pygame.display.set_icon(icon)
usr_width = 60
usr_height = 92
usr_x = display_width // 3
usr_y = display_height - usr_height - 102
clock = pygame.time.Clock()
make_jump = False
jump_counter = 30
cactus_width = 20  # перменные
cactus_height = 70
cactus_x = display_width - 50
cactus_y = display_height - cactus_height - 100
scores = 0
max_above = 0

max_scores = 0


def show_menu(): # меню
    menu_bckgr = pygame.image.load('Background/menu.png')
    start_btn = Button(270, 70)
    quit_btn = Button(160, 70)
    continue_button = Button(300, 70)
    show = True
    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        display.blit(menu_bckgr, (0, 0))
        if start_btn.draw(270, 200, 'Начать игру', None, font_size=50):
            game_state.change(State.START)
            return
        if continue_button.draw(250, 300, 'Продолжить', font_size=50):
            game_state.change(State.CONTINUE)
            return
        if quit_btn.draw(330, 400, 'Выход', None, font_size=50):
            game_state.change(State.QUIT)
            return

        # get_input()
        pygame.display.update()
        clock.tick(60)


def start_game(): # начало игры
    global scores, make_jump, jump_counter, usr_y, health
    while game_cycle():
        scores = 0
        make_jump = False
        jump_counter = 30
        usr_y = display_height - usr_height - 100
        health = 3


def game_cycle(): # основной игровой цикл
    global make_jump
    game = True
    cactus_arr = []
    create_cactus_arr(cactus_arr)
    land = pygame.image.load('Background/Land.png')
    pygame.mixer.music.play(-1)

    stone, cloud = open_random_objects()
    button = Button(80, 50)

    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            make_jump = True

        if keys[pygame.K_ESCAPE]:
            pause()


        if make_jump:
            jump()

        count_scores(cactus_arr)
        display.blit(land, (0, 0))
        print_text('Счет: ' + str(scores), 630, 40)

        draw_array(cactus_arr)
        move_objects(stone, cloud)
        draw_dino()

        if check_collisison(cactus_arr):
            pygame.mixer.music.stop()
            game = False
        show_health()

        pygame.display.update()
        clock.tick(80)
    return game_over()


def jump(): # работа прыжка
    global usr_y, jump_counter, make_jump
    if jump_counter >= -30:
        if jump_counter == 30:
            pygame.mixer.Sound.play(jump_sound)
        if jump_counter == -20:
            pygame.mixer.Sound.play(fall_sound)

        usr_y -= jump_counter / 2.5
        jump_counter -= 1
    else:
        jump_counter = 30
        make_jump = False


def create_cactus_arr(array): # появление кактусов
    choice = random.randrange(0, 3)
    img = cactus_img[choice]
    width = cactus_options[choice * 2]
    height = cactus_options[choice * 2 + 1]
    array.append(Object(display_width + 20, height, width, img, 4))

    choice = random.randrange(0, 3)
    img = cactus_img[choice]
    width = cactus_options[choice * 2]
    height = cactus_options[choice * 2 + 1]
    array.append(Object(display_width + 250, height, width, img, 4))

    choice = random.randrange(0, 3)
    img = cactus_img[choice]
    width = cactus_options[choice * 2]
    height = cactus_options[choice * 2 + 1]
    array.append(Object(display_width + 550, height, width, img, 4))


def find_radius(array): # вероятность появления двух кактусов рядом
    maximum = max(array[0].x, array[1].x, array[2].x)
    if maximum < display_width:
        radius = display_width
        if radius - maximum < 50:
            radius += 280
    else:
        radius = maximum

    choice = random.randrange(0, 5)
    if choice == 0:
        radius += random.randrange(20, 65)
    else:
        radius += random.randrange(250, 400)
    return radius


def draw_array(array): # проверка кактусов
    for cactus in array:
        check = cactus.move()
        if not check:
            object_return(array, cactus)


def object_return(objects, obj):  # рандомизация изображения кактусов
    radius = find_radius(objects)

    choice = random.randrange(0, 3)
    img = cactus_img[choice]
    width = cactus_options[choice * 2]
    height = cactus_options[choice * 2 + 1]

    obj.return_self(radius, height, width, img)


def open_random_objects():  # камни
    choice = random.randrange(0, 2)
    img_of_stone = stone_img[choice]

    choice = random.randrange(0, 2)
    img_of_cloud = cloud_img[choice]

    stone = Object(display_width, display_height - 80, 10, img_of_stone, 4)
    cloud = Object(display_width, 80, 70, img_of_cloud, 2)

    return stone, cloud


def move_objects(stone, cloud):  # движение объектов
    check = stone.move()
    if not check:
        choice = random.randrange(0, 2)
        img_of_stone = stone_img[choice]
        stone.return_self(display_width, 500 + random.randrange(10, 80), stone.width, img_of_stone)

    check = cloud.move()
    if not check:
        choice = random.randrange(0, 2)
        img_of_cloud = cloud_img[choice]
        cloud.return_self(display_width, random.randrange(10, 200), stone.width, img_of_cloud)


def draw_dino(): # сам динозавр
    global img_counter
    display.blit(dino_img[img_counter], (usr_x, usr_y))


def print_text(message, x, y, font_color=(0, 0, 0), font_type='Background/Calibri.ttf', font_size=30):  # шрифт
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    display.blit(text, (x, y))


def pause(): # пауза
    paused = True

    pygame.mixer.music.pause()

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        print_text('Пауза. Нажмите enter чтобы продолжить...', 160, 300)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            paused = False

        pygame.display.update()
        clock.tick(15)

    pygame.mixer.music.unpause()


def check_collisison(barriers): # условие прыжка
    for barrier in barriers:
        if barrier.y == 449:
            if not make_jump:
                if barrier.x <= usr_x + usr_width - 15 <= barrier.x + barrier.width:
                    if check_health():
                        object_return(barriers, barrier)
                        return False
                    else:
                        return True
            elif jump_counter >= 0:
                if usr_y + usr_height - 5 >= barrier.y:
                    if barrier.x <= usr_x + usr_width - 35 <= barrier.x + barrier.width:
                        if check_health():
                            object_return(barriers, barrier)
                            return False
                        else:
                            return True
            else:
                if usr_y + usr_height - 10 >= barrier.y:
                    if barrier.x <= usr_x + usr_width - 35 <= barrier.x + barrier.width:
                        if check_health():
                            object_return(barriers, barrier)
                            return False
                        else:
                            return True
        else:
            if not make_jump:
                if barrier.x <= usr_x + usr_width + 5 <= barrier.x + barrier.width:
                    if check_health():
                        object_return(barriers, barrier)
                        return False
                    else:
                        return True
            elif jump_counter == 10:
                if usr_y + usr_height - 5 >= barrier.y:
                    if barrier.x <= usr_x + usr_width - 5 <= barrier.x + barrier.width:
                        if check_health():
                            object_return(barriers, barrier)
                            return False
                        else:
                            return True
            elif jump_counter >= -1:
                if usr_y + usr_height - 15 >= barrier.y:
                    if barrier.x <= usr_x + usr_width - 35 <= barrier.x + barrier.width:
                        if check_health():
                            object_return(barriers, barrier)
                            return False
                        else:
                            return True
            else:
                if usr_y + usr_height - 25 >= barrier.y:
                    if barrier.x <= usr_x + 5 <= barrier.x + barrier.width:
                        if check_health():
                            object_return(barriers, barrier)
                            return False
                        else:
                            return True
    return False


def count_scores(barriers):  # счетчик
    global scores, max_above
    above_cactus = 0
    if -20 <= jump_counter < 25:
        for barrier in barriers:
            if usr_y + usr_height - 5 <= barrier.y:
                if barrier.x <= usr_x <= barrier.x + barrier.width:
                    above_cactus += 1
                elif barrier.x <= usr_x + usr_width <= barrier.x + barrier.width:
                    above_cactus += 1
        max_above = max(max_above, above_cactus)
    else:
        if jump_counter == -30:
            scores += max_above
            max_above = 0


def game_over(): # окончание игры
    global scores, max_scores
    if scores > max_scores:
        max_scores = scores

    stopped = True
    while stopped:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        print_text('Нажмите Enter чтобы сыграть еще и Esc чтобы выйти.', 60, 270)
        print_text('Максимум очков: ' + str(max_scores), 280, 350)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            return True
        if keys[pygame.K_ESCAPE]:
            game_state.change(State.MENU)
            return False

        pygame.display.update()
        clock.tick(15)


def show_health(): # здоровье
    global health
    show = 0
    x = 20
    while show != health:
        display.blit(heart_img, (x, 20))
        x += 70
        show += 1


def check_health(): # проверка здоровья
    global health
    health -= 1
    if health == 0:
        pygame.mixer.Sound.play(loss_sound)
        game_over()
        return False
    else:
        pygame.mixer.Sound.play(loss_sound)
        return True


'''def get_input():
    global need_input, input_text, input_tick
    input_rect = pygame.Rect(20, 400, 250, 70)

    pygame.draw.rect(display, (255, 255, 255), input_rect)
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if input_rect.collidepoint(mouse[0], mouse[1] and click[0]):
        need_input = True
    if need_input:
        for event in pygame.event.get():
            if need_input and event.type == pygame.KEYDOWN:
                input_text = input_text.replace('|', '')
                input_tick = 30
                if event.key == pygame.K_RETURN:
                    need_input = False
                    input_text = ''
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    if len(input_text) < 10:
                        input_text += event.unicode
                input_text += '|'
    if len(input_text) > 0:
        print_text(message=input_text, x=input_rect.x + 10, y=input_rect.y + 10, font_size=50)
    input_tick -= 1
    if input_tick == 0:
        input_text = input_text[:-1]
    if input_tick == -30:
        input_text += '|'
        input_tick = 30'''


start()
pygame.quit()
quit()
