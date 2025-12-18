import tkinter as tk
from funk import ship_place
import random

# переменные состояния игры
game_on = False  # состояние игры
my_ships = []  # Список кораблей игрока
bot_ships = []  # Список кораблей бота
my_turn = True  # Чей сейчас ход
my_all_ships = []  # Полный список кораблей игрока
bot_all_ships = []  # Полный список кораблей бота


def count_ships(ships): # Подсчитывает количество элементов в матрице
    total = 0
    for ship in ships:
        if ship:
            total += 1
    return total


def show_around(ship_cells, buttons_grid): # открывает все клетки вокруг корабля при его уничтожении
    ship_set = set(ship_cells)

    cells_to_show = set()
    for x, y in ship_cells:
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < 10 and 0 <= ny < 10:
                    if (nx, ny) not in ship_set:
                        cells_to_show.add((nx, ny))

    # Отмечаем все собранные клетки
    for nx, ny in cells_to_show:
        btn = buttons_grid[nx][ny]
        btn.config(bg="gray", state="disabled", text="•")


def on_bot_click(row, col): # обрабатывает клик по полю бота
    global game_on, my_turn, bot_ships, bot_all_ships

    # условия для хода
    if not game_on:
        return
    if not my_turn:
        return

    btn = bot_grid[row][col]

    # Если клетка отмечена
    if btn.cget("state") == "disabled":
        return

    hit = False
    ship_dead = False
    ship_gone = None
    ship_id = -1

    # Проверяем попадание по кораблям бота
    for i, ship in enumerate(bot_ships):
        if (row, col) in ship:
            hit = True
            ship_id = i
            ship.remove((row, col))  # Удаляем попадание из корабля

            # Проверяем, уничтожен ли корабль
            if len(ship) == 0:
                ship_dead = True
                ship_gone = ship
            break

    # Если корабль уничтожен, отмечаем клетки вокруг полного корабля
    if ship_dead and ship_id != -1:
        show_around(bot_all_ships[ship_id], bot_grid)

    # Удаляем уничтоженный корабль из списков
    if ship_gone:
        bot_ships.remove(ship_gone)
        if ship_id != -1:
            del bot_all_ships[ship_id]

    # Обработка попадания
    if hit:
        btn.config(bg="red", state="disabled", text="X", fg="white")

        # Проверяем, не закончилась ли игра
        if count_ships(bot_ships) == 0:
            end_game("player")
            return

        # Обновляем статус игры
        if ship_dead:
            status_text.config(text="Корабль противника уничтожен!")
        else:
            status_text.config(text="Попадание! Ваш ход продолжается")
    else:
        # передаем ход боту если промах
        btn.config(bg="gray", state="disabled", text="•")
        my_turn = False
        status_text.config(text="Ход бота...")
        root.after(1000, bot_move)


def bot_move(): # ход бота
    global game_on, my_turn, my_ships, my_all_ships

    if not game_on:
        return

    # Собираем все доступные для выстрела клетки
    free_cells = []
    for r in range(10):
        for c in range(10):
            btn = my_grid[r][c]
            if btn.cget("state") != "disabled":
                free_cells.append((r, c))

    if not free_cells:
        end_game("bot")
        return

    # Случайный выстрел бота
    row, col = random.choice(free_cells)
    btn = my_grid[row][col]

    hit = False
    ship_gone = None
    ship_dead = False
    ship_id = -1

    # Проверяем попадание по кораблям игрока
    for i, ship in enumerate(my_ships):
        if (row, col) in ship:
            hit = True
            ship_id = i
            ship.remove((row, col))

            if len(ship) == 0:
                ship_dead = True
                ship_gone = ship
            break

    # Если корабль уничтожен, отмечаем клетки вокруг полного корабля
    if ship_dead and ship_id != -1:
        show_around(my_all_ships[ship_id], my_grid)

    if ship_gone:
        my_ships.remove(ship_gone)
        if ship_id != -1:
            del my_all_ships[ship_id]

    # проверяем попадание
    if hit:
        btn.config(bg="red", state="disabled", text="X", fg="white")

        # Проверяем конец игры
        if count_ships(my_ships) == 0:
            end_game("bot")
            return

        # если попадание бот продолжает ход
        if ship_dead:
            status_text.config(text="Бот уничтожил ваш корабль!")
        else:
            status_text.config(text="Бот попал! Он ходит снова")
        root.after(1000, bot_move)
    else:
        # передаем ход игроку если промах
        btn.config(bg="gray", state="disabled", text="•")
        my_turn = True
        status_text.config(text="Ваш ход!")


def clear_my_field(): # очищает поле игрока
    for row in range(10):
        for col in range(10):
            my_grid[row][col].config(bg="light blue", state="normal", text="", fg="black")


def clear_bot_field(): # очищает поле бота
    for row in range(10):
        for col in range(10):
            bot_grid[row][col].config(bg="light gray", state="normal", text="", fg="black")


def place_ships(): # расставляет корабли игрока
    global my_ships, game_on, my_all_ships

    if game_on:
        status_text.config(text="Нельзя менять корабли во время игры!")
        return

    clear_my_field()

    my_ships = ship_place()
    my_all_ships = [list(ship) for ship in my_ships]

    # отмечаем корабли на поле
    for ship in my_ships:
        ship_size = len(ship)
        # Выбираем цвет в зависимости от размера корабля
        if ship_size == 4:
            color = "dark blue"
        elif ship_size == 3:
            color = "blue"
        elif ship_size == 2:
            color = "green"
        else:
            color = "orange"

        for x, y in ship:
            if 0 <= x < 10 and 0 <= y < 10:
                my_grid[x][y].config(bg=color)

    status_text.config(text="Корабли расставлены. Нажмите 'Начать игру'", fg="blue")


def start_game(): # старт игры
    global game_on, my_turn, bot_ships, bot_all_ships

    if game_on:
        status_text.config(text="Игра уже идет!")
        return

    if not my_ships or count_ships(my_ships) != 10:
        status_text.config(text="Сначала правильно расставьте корабли!")
        return

    # Генерируем корабли для бота
    bot_ships = ship_place()
    bot_all_ships = [list(ship) for ship in bot_ships]

    clear_bot_field()

    game_on = True
    my_turn = True

    # Блокируем кнопки расстановки и начала
    place_btn.config(state="disabled")
    start_btn.config(state="disabled")
    restart_btn.config(state="normal")

    status_text.config(text="Игра началась! Ваш ход", fg="black")


def end_game(winner): # конец игры
    global game_on

    game_on = False

    # отображаем результат
    if winner == "player":
        message = "🎉 Вы победили! 🎉"
        color = "green"
        # Показываем все оставшиеся корабли бота
        for ship in bot_all_ships:
            for x, y in ship:
                btn = bot_grid[x][y]
                if btn.cget("bg") != "red":
                    btn.config(bg="dark red", text="X", fg="white")
            # Отмечаем клетки вокруг них
            show_around(ship, bot_grid)
    else:
        message = "💀 Бот победил! 💀"
        color = "red"
        for ship in bot_all_ships:
            for x, y in ship:
                my_grid[x][y].config(bg="dark red", text="X", fg="white")

    status_text.config(text=message, fg=color, font=("Arial", 12, "bold"))

    # Блокируем все клетки
    for row in range(10):
        for col in range(10):
            bot_grid[row][col].config(state="disabled")
            my_grid[row][col].config(state="disabled")

    # Настраиваем состояние кнопок
    restart_btn.config(state="normal")
    start_btn.config(state="disabled")
    place_btn.config(state="disabled")


def restart_game(): # перезапуск игры
    global game_on, my_ships, bot_ships, my_turn, my_all_ships, bot_all_ships

    # Сбрасываем все параметры игры
    game_on = False
    my_ships = []
    bot_ships = []
    my_all_ships = []
    bot_all_ships = []
    my_turn = True

    # Очищаем поля
    clear_my_field()
    clear_bot_field()

    # Настраиваем состояние кнопок
    place_btn.config(state="normal")
    start_btn.config(state="normal")
    restart_btn.config(state="disabled")

    status_text.config(text="Расставьте корабли и начните игру", fg="black", font=("Arial", 10))


# Создание графического интерфейса
root = tk.Tk()
root.title("Морской бой")

# Фреймы для полей игрока и бота
my_frame = tk.Frame(root)
my_frame.grid(row=0, column=0, padx=20, pady=10)

bot_frame = tk.Frame(root)
bot_frame.grid(row=0, column=1, padx=20, pady=10)

# Метки полей
my_label = tk.Label(my_frame, text="Мое поле", font=("Arial", 14))
my_label.grid(row=0, column=0, columnspan=10)

bot_label = tk.Label(bot_frame, text="Поле бота", font=("Arial", 14))
bot_label.grid(row=0, column=0, columnspan=10)

my_grid = []
bot_grid = []

# Создание поля игрока (10x10)
for row in range(10):
    row_buttons = []
    for col in range(10):
        btn = tk.Button(my_frame, width=3, height=1, bg="light blue")
        btn.grid(row=row + 1, column=col, padx=1, pady=1)
        row_buttons.append(btn)
    my_grid.append(row_buttons)

# Создание поля бота (10x10)
for row in range(10):
    row_buttons = []
    for col in range(10):
        btn = tk.Button(bot_frame, width=3, height=1, bg="light gray",
                        command=lambda r=row, c=col: on_bot_click(r, c))
        btn.grid(row=row + 1, column=col, padx=1, pady=1)
        row_buttons.append(btn)
    bot_grid.append(row_buttons)

# Панель управления
control_frame = tk.Frame(root)
control_frame.grid(row=1, column=0, columnspan=2, pady=20)

# Кнопки управления
place_btn = tk.Button(control_frame, text="Расставить корабли", width=20, command=place_ships)
place_btn.pack(side=tk.LEFT, padx=5)

start_btn = tk.Button(control_frame, text="Начать игру", width=15, command=start_game)
start_btn.pack(side=tk.LEFT, padx=5)

restart_btn = tk.Button(control_frame, text="Перезапустить", width=20, command=restart_game, state="disabled")
restart_btn.pack(side=tk.LEFT, padx=5)

status_text = tk.Label(control_frame, text="Расставьте корабли", font=("Arial", 10))
status_text.pack(side=tk.LEFT, padx=20)

root.mainloop()