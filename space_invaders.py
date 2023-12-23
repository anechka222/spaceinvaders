import pygame
import sys
import random

# Импорт необходимых модулей.
# Инициализация Pygame.
# Определение основных параметров игры, таких как размеры экрана, размеры игрока и врагов, количество врагов и другие.
pygame.init()

WIDTH, HEIGHT = 600, 400
PLAYER_SIZE = 50
ENEMY_SIZE = 15
BLUE_ENEMY_SIZE = 30
ENEMY_ROWS = 3
ENEMY_BLOCKS = 3
ENEMY_SPACING = 10
ENEMY_COUNT_IN_ROW = 4
FPS = 60

# Определение цветов, используемых в игре
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Создание окна Pygame с указанными размерами и названием
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# Создание поверхностей с различными изображениями для игрока, врагов, пуль и сердец
player_image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
player_image.fill(GREEN)

enemy_image = pygame.Surface((ENEMY_SIZE, ENEMY_SIZE))
enemy_image.fill(WHITE)

blue_enemy_image = pygame.Surface((BLUE_ENEMY_SIZE, BLUE_ENEMY_SIZE))
blue_enemy_image.fill(BLUE)

bullet_image = pygame.Surface((5, 15))
bullet_image.fill((255, 255, 255))

heart_image = pygame.Surface((20, 20))
heart_image.fill(RED)

# Создание объекта Clock для управления частотой кадров
clock = pygame.time.Clock()

# Начальные позиции игрока, врагов и пуль
player_pos = [WIDTH // 2 - PLAYER_SIZE // 2, HEIGHT - PLAYER_SIZE - 10]
enemy_list = []
blue_enemy_list = []
player_bullets = []
enemy_bullets = []

# Настройка скоростей для игрока, врагов, синего корабля и пуль
player_speed = 5
enemy_speed = 1
blue_enemy_speed = 5
bullet_speed = 5

# Инициализация направления движения врагов (1 - вправо, -1 - влево)
enemy_direction = 1

# Инициализация количества жизней игрока, счета и шрифта
player_lives = 3
score = 0
font = pygame.font.SysFont(None, 30)

# Инициализация переменной для отслеживания состояния стрельбы игрока
is_shooting = False

# Функция отображения сообщения "Game Over" и завершения игры при достижении условий поражения
def game_over():
    """
    Отображает сообщение "Game Over" и завершает игру при наступлении условий поражения.

    Данная функция использует библиотеку Pygame для отображения текста "Game Over" на экране,
    ждет 2 секунды, а затем завершает выполнение программы.
    """
    font = pygame.font.SysFont(None, 55)
    text = font.render("Game Over", True, RED)
    screen.blit(text, (WIDTH // 2 - 150, HEIGHT // 2 - 30))
    pygame.display.flip()
    pygame.time.delay(2000)
    pygame.quit()
    sys.exit()

def create_enemies():
    """
    Создает список врагов и располагает их на экране в виде матрицы.

    Функция использует вложенные циклы для генерации координат врагов на игровом экране.
    Каждый враг представлен координатами в виде списка [x, y], где x - горизонтальная позиция,
    y - вертикальная позиция.

    """
    for row in range(ENEMY_ROWS):
        for block in range(ENEMY_BLOCKS):
            for col in range(ENEMY_COUNT_IN_ROW):
                enemy_list.append([(col * (ENEMY_SIZE + ENEMY_SPACING)) + block * (WIDTH // ENEMY_BLOCKS),
                                   row * (ENEMY_SIZE + ENEMY_SPACING) + 50])


def create_blue_enemy():
    """
    Создает синего врага и добавляет его в список синих врагов.

    Функция генерирует случайные координаты для синего врага в пределах ширины игрового экрана
    и добавляет его в список blue_enemy_list. Каждый синий враг представлен списком координат [x, y],
    где x - горизонтальная позиция, y - вертикальная позиция.

    """
    blue_enemy_list.append([random.randint(0, WIDTH - BLUE_ENEMY_SIZE), 0])

def draw_lives():
    """
    Отображает сердца, представляющие количество жизней игрока.

    Функция рисует на экране изображения сердец для каждой жизни игрока.
    Координаты каждого сердца рассчитываются с учетом ширины экрана, количества жизней и размера сердец.
    """
    for i in range(player_lives):
        screen.blit(heart_image, (WIDTH - 30 - i * 25, 10))
def draw_objects():
    """
    Отображает игровые объекты на игровом экране.

    Функция заполняет экран черным цветом и отображает следующие игровые объекты:
    - Игрока
    - Врагов
    - Синих врагов
    - Пули игрока
    - Пули врагов
    - Количество жизней игрока

    """
    screen.fill((0, 0, 0))
    screen.blit(player_image, player_pos)
    for enemy in enemy_list:
        screen.blit(enemy_image, enemy)
    for blue_enemy in blue_enemy_list:
        screen.blit(blue_enemy_image, blue_enemy)
    for bullet in player_bullets:
        screen.blit(bullet_image, bullet)
    for bullet in enemy_bullets:
        screen.blit(bullet_image, bullet)
    draw_lives()

def update_enemy_bullets(enemy_bullets, bullet_speed, screen_height):
    """
    Обновляет позиции пуль врагов и удаляет те, которые вышли за пределы экрана.

    Функция изменяет вертикальные позиции пуль врагов в соответствии со скоростью движения,
    а затем удаляет пули, вышедшие за верхний предел экрана.


        enemy_bullets (list): Список координат пуль врагов.
        bullet_speed (int): Скорость движения пуль врагов.
        screen_height (int): Высота игрового экрана.

    return:
        list: Обновленный список координат пуль врагов.

        Эта функция предполагает, что координаты пуль врагов представлены списком,
        где каждый элемент - это координаты пули в формате [x, y].
    """
    updated_bullets = [[bullet[0], bullet[1] + bullet_speed] for bullet in enemy_bullets]
    # Удаление пуль врагов, вышедших за пределы экрана
    updated_bullets = [bullet for bullet in updated_bullets if 0 <= bullet[1] <= screen_height]
    return updated_bullets

def update_player_bullets(player_bullets, bullet_speed, screen_height):
    """
    Обновляет позиции пуль игрока и удаляет те, которые вышли за пределы экрана.

    Функция изменяет вертикальные позиции пуль игрока в соответствии со скоростью движения,
    а затем удаляет пули, вышедшие за нижний предел экрана.

    Параметры:
        player_bullets (list): Список координат пуль игрока.
        bullet_speed (int): Скорость движения пуль игрока.
        screen_height (int): Высота игрового экрана.

    Возвращает:
        list: Обновленный список координат пуль игрока.

        Эта функция предполагает, что координаты пуль игрока представлены списком,
        где каждый элемент - это координаты пули в формате [x, y].
    """
    updated_bullets = [[bullet[0], bullet[1] - bullet_speed] for bullet in player_bullets]
    # Удаление пуль игрока, вышедших за пределы экрана
    updated_bullets = [bullet for bullet in updated_bullets if 0 <= bullet[1] <= screen_height]
    return updated_bullets

def update_enemy_shooting(enemy_list, enemy_bullets, max_enemy_bullets):
    """
    Обновляет стрельбу врагов с некоторой вероятностью.

    Функция, основываясь на случайном выборе, решает, стреляет ли случайный враг,
    и если да, добавляет координаты новой пули врага в список пуль врагов.

    Параметры:
        enemy_list (list): Список координат врагов.
        enemy_bullets (list): Список координат пуль врагов.
        max_enemy_bullets (int): Максимальное количество пуль врагов на экране.

    Возвращает:
        list: Обновленный список координат пуль врагов.


        Эта функция предполагает, что координаты врагов и пуль врагов представлены списками,
        где каждый элемент - это координаты врага или пули в формате [x, y].
    """
    if random.randint(0, 100) < 1 and len(enemy_bullets) < max_enemy_bullets:
        enemy = random.choice(enemy_list)
        enemy_bullet = [enemy[0] + ENEMY_SIZE // 2 - 2, enemy[1] + ENEMY_SIZE]
        enemy_bullets.append(enemy_bullet)
    return enemy_bullets

def update_game_state(player_lives, score, enemy_bullets, player_bullets, enemy_list, blue_enemy_list):
    """
    Обновляет состояние игры, обрабатывает столкновения пуль и обновляет количество жизней и счет.

    Функция проверяет столкновения пуль врагов с игроком, пуль игрока с врагами и пуль игрока
    с синим врагом, обновляя при этом количество жизней, счет и списки пуль и врагов.

    Параметры:
        player_lives (int): Текущее количество жизней игрока.
        score (int): Текущий счет игрока.
        enemy_bullets (list): Список координат пуль врагов.
        player_bullets (list): Список координат пуль игрока.
        enemy_list (list): Список координат врагов.
        blue_enemy_list (list): Список координат синего врага.

    Возвращает:
        int: Обновленное количество жизней игрока.
        int: Обновленный счет игрока.
        list: Обновленный список координат пуль врагов.
        list: Обновленный список координат пуль игрока.
        list: Обновленный список координат врагов.
        list: Обновленный список координат синего врага.

    """
    updated_enemy_bullets = update_enemy_bullets(enemy_bullets, bullet_speed, HEIGHT)
    updated_player_bullets = update_player_bullets(player_bullets, bullet_speed, HEIGHT)
    updated_enemy_bullets = update_enemy_shooting(enemy_list, updated_enemy_bullets, 3)  # Указываем макс. количество пуль врагов

    # Проверка столкновения пуль врагов с игроком
    for bullet in updated_enemy_bullets:
        if (
                player_pos[0] < bullet[0] < player_pos[0] + PLAYER_SIZE
                and player_pos[1] < bullet[1] < player_pos[1] + PLAYER_SIZE
        ):
            updated_enemy_bullets.remove(bullet)
            player_lives -= 1
            if player_lives == 0:
                game_over()

    # Проверка столкновения пуль игрока с врагами
    for bullet in updated_player_bullets:
        for enemy in enemy_list:
            if (
                    enemy[0] < bullet[0] < enemy[0] + ENEMY_SIZE
                    and enemy[1] < bullet[1] < enemy[1] + ENEMY_SIZE
            ):
                updated_player_bullets.remove(bullet)
                enemy_list.remove(enemy)
                score += 10

    # Проверка столкновения пуль синего корабля с игроком
    for bullet in updated_player_bullets:
        bullet_x, bullet_y = bullet
        blue_enemy_x, blue_enemy_y = blue_enemy_list[0]
        if (
                blue_enemy_x < bullet_x < blue_enemy_x + BLUE_ENEMY_SIZE
                and blue_enemy_y < bullet_y < blue_enemy_y + BLUE_ENEMY_SIZE
        ):
            updated_player_bullets.remove(bullet)
            score += 50

    return player_lives, score, updated_enemy_bullets, updated_player_bullets, enemy_list, blue_enemy_list

def main():
    """
    Основной игровой цикл, отвечающий за обработку событий, управление объектами, обновление состояния игры
    и отрисовку игровых элементов.

    В данной функции определены переменные и параметры игры, а также осуществляется основная логика игрового цикла.

    """
    global player_lives, score, is_shooting, enemy_direction

    # Инициализация начальных объектов
    create_enemies()
    create_blue_enemy()

    # Инициализация переменных
    player_pos = [WIDTH // 2 - PLAYER_SIZE // 2, HEIGHT - PLAYER_SIZE - 10]
    enemy_list = []
    blue_enemy_list = []
    player_bullets = []  # Пули игрока
    enemy_bullets = []  # Пули врагов

    # Настройка скоростей
    player_speed = 5
    enemy_speed = 1
    blue_enemy_speed = 5
    bullet_speed = 5

    # Направление движения врагов
    enemy_direction = 1  # 1 - вправо, -1 - влево

    # Жизни игрока
    player_lives = 3
    score = 0

    # Переменная для отслеживания состояния стрельбы игрока
    is_shooting = False

    # Основной игровой цикл
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        # Обработка стрельбы игрока
        if keys[pygame.K_SPACE] and not is_shooting:
            player_bullet = [player_pos[0] + PLAYER_SIZE // 2 - 2, player_pos[1]]
            player_bullets.append(player_bullet)
            is_shooting = True

        # Управление движением игрока
        if keys[pygame.K_LEFT] and player_pos[0] > 0:
            player_pos[0] -= player_speed
        if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - PLAYER_SIZE:
            player_pos[0] += player_speed

        # Движение врагов
        for enemy in enemy_list:
            enemy[0] += enemy_direction * enemy_speed

        # Изменение направления движения врагов
        if any(enemy[0] <= 0 or enemy[0] >= WIDTH - ENEMY_SIZE for enemy in enemy_list):
            enemy_direction *= -1

        # Движение синего врага
        if blue_enemy_list:
            if blue_enemy_list[0][0] >= WIDTH:
                blue_enemy_list[0][0] = 0
            blue_enemy_list[0][0] += blue_enemy_speed

        # Движение пуль игрока и удаление вышедших за пределы экрана
        player_bullets = [[bullet[0], bullet[1] - bullet_speed] for bullet in player_bullets]
        player_bullets = [bullet for bullet in player_bullets if 0 <= bullet[1] <= HEIGHT]

        # Стрельба врагов и проверка столкновений с игроком
        if keys[pygame.K_SPACE] and len(player_bullets) < 3:
            player_bullet = [player_pos[0] + PLAYER_SIZE // 2 - 2, player_pos[1]]
            player_bullets.append(player_bullet)

            # Движение пуль врагов
            enemy_bullets = [[bullet[0], bullet[1] + bullet_speed] for bullet in enemy_bullets]
            enemy_bullets = [bullet for bullet in enemy_bullets if 0 <= bullet[1] <= HEIGHT]

            # Проверка столкновения пуль врагов с игроком
            for bullet in enemy_bullets:
                if (
                        player_pos[0] < bullet[0] < player_pos[0] + PLAYER_SIZE
                        and player_pos[1] < bullet[1] < player_pos[1] + PLAYER_SIZE
                ):
                    enemy_bullets.remove(bullet)
                    player_lives -= 1
                    if player_lives == 0:
                        game_over()

            # Проверка столкновения пуль синего корабля с игроком
            for bullet in player_bullets:
                bullet_x, bullet_y = bullet
                blue_enemy_x, blue_enemy_y = blue_enemy_list[0]
                if (
                        blue_enemy_x < bullet_x < blue_enemy_x + BLUE_ENEMY_SIZE
                        and blue_enemy_y < bullet_y < blue_enemy_y + BLUE_ENEMY_SIZE
                ):
                    player_bullets.remove(bullet)
                    score += 50

        update_game_state()
        draw_objects()

        # Обновление флага is_shooting
        is_shooting = any(0 <= bullet[1] for bullet in player_bullets)

        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

def main():
    """
    Главная функция программы, реализующая основной игровой цикл.

    В этой функции происходит обработка событий, управление объектами, обновление состояния игры и отрисовка игровых элементов.

    """
    global player_lives, score, is_shooting, enemy_direction, player_pos, enemy_list, blue_enemy_list, player_bullets, enemy_bullets

    # Инициализация начальных параметров игры
    create_enemies()  # Создание врагов
    create_blue_enemy()  # Создание синего врага

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        # Обработка нажатия клавиши "Пробел" для выстрела
        if keys[pygame.K_SPACE] and not is_shooting:
            player_bullet = [player_pos[0] + PLAYER_SIZE // 2 - 2, player_pos[1]]
            player_bullets.append(player_bullet)
            is_shooting = True

        # Обработка движения игрока влево
        if keys[pygame.K_LEFT] and player_pos[0] > 0:
            player_pos[0] -= player_speed

        # Обработка движения игрока вправо
        if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - PLAYER_SIZE:
            player_pos[0] += player_speed

        # Движение врагов вправо и влево
        for enemy in enemy_list:
            enemy[0] += enemy_direction * enemy_speed

        # Изменение направления движения врагов при достижении границы экрана
        if any(enemy[0] <= 0 or enemy[0] >= WIDTH - ENEMY_SIZE for enemy in enemy_list):
            enemy_direction *= -1

        # Движение синего врага
        if blue_enemy_list:
            if blue_enemy_list[0][0] >= WIDTH:
                blue_enemy_list[0][0] = 0

            blue_enemy_list[0][0] += blue_enemy_speed

        # Обновление позиций пуль игрока и врагов
        player_bullets = update_player_bullets(player_bullets, bullet_speed, HEIGHT)
        enemy_bullets = update_enemy_bullets(enemy_bullets, bullet_speed, HEIGHT)
        enemy_bullets = update_enemy_shooting(enemy_list, enemy_bullets, 3)

        # Проверка столкновения пуль врагов с игроком и обновление состояния игры
        for bullet in enemy_bullets:
            if (
                    player_pos[0] < bullet[0] < player_pos[0] + PLAYER_SIZE
                    and player_pos[1] < bullet[1] < player_pos[1] + PLAYER_SIZE
            ):
                enemy_bullets.remove(bullet)
                player_lives -= 1
                if player_lives == 0:
                    game_over()

        # Проверка столкновения пуль игрока с врагами и обновление состояния игры
        for bullet in player_bullets:
            for enemy in enemy_list:
                if (
                        enemy[0] < bullet[0] < enemy[0] + ENEMY_SIZE
                        and enemy[1] < bullet[1] < enemy[1] + ENEMY_SIZE
                ):
                    player_bullets.remove(bullet)
                    enemy_list.remove(enemy)
                    score += 10

        # Проверка столкновения пуль синего врага с игроком и обновление состояния игры
        for bullet in player_bullets:
            bullet_x, bullet_y = bullet
            blue_enemy_x, blue_enemy_y = blue_enemy_list[0]
            if (
                    blue_enemy_x < bullet_x < blue_enemy_x + BLUE_ENEMY_SIZE
                    and blue_enemy_y < bullet_y < blue_enemy_y + BLUE_ENEMY_SIZE
            ):
                player_bullets.remove(bullet)
                score += 50

        # Отрисовка объектов на экране
        draw_objects()

        # Обновление флага is_shooting
        is_shooting = any(0 <= bullet[1] for bullet in player_bullets)

        # Отображение текущего счета на экране
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
